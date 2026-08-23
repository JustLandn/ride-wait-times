import time
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import streamlit as st

PARKS = {
    "Universal Studios Hollywood": 66,
    "Six Flags Magic Mountain": 32,
    "Knott's Berry Farm": 61,
}

now = datetime.now(ZoneInfo("America/Los_Angeles"))  # Pacific Time

st.caption("Powered by [Queue-Times.com](https://queue-times.com/en-US)")

if "ntfy_topic" not in st.session_state:
    st.session_state["ntfy_topic"] = st.query_params.get("ntfy", "")

ntfy_topic = st.text_input(
    "Your ntfy topic (leave blank to skip push alerts)",
    key="ntfy_topic",
    placeholder="e.g. my-own-ride-alerts-1234",
    help="Bookmark this page after entering it and it'll be remembered via the URL.",
)

if ntfy_topic:
    st.query_params["ntfy"] = ntfy_topic
elif "ntfy" in st.query_params:
    del st.query_params["ntfy"]

selected_park = st.selectbox("Park", list(PARKS.keys()), key="selected_park")
park_id = PARKS[selected_park]

url = f"https://queue-times.com/parks/{park_id}/queue_times.json"
response = requests.get(url)
data = response.json()
st.caption(f"Last updated: {now.strftime('%I:%M %p')}")

show_kids_rides = st.checkbox("Show kids' rides", key="show_kids_rides")

lands = [
    land
    for land in data["lands"]
    if show_kids_rides or "kid" not in land["name"].lower()
]

ride_names = [ride["name"] for land in lands for ride in land["rides"]]

if (
    st.session_state.get("last_park") != selected_park
    or st.session_state.get("last_show_kids_rides") != show_kids_rides
):
    st.session_state["was_under_threshold"] = {}
    st.session_state["last_park"] = selected_park
    st.session_state["last_show_kids_rides"] = show_kids_rides
    st.session_state.pop("rides_i_care_about", None)

rides_i_care_about = st.multiselect(
    "Which rides do you want alerts for?",
    ride_names,
    default=ride_names,
    key="rides_i_care_about",
)

for land in lands:
    for ride in land["rides"]:
        if not ride["is_open"]:
            st.error(f"{ride['name']}: closed")
            continue

        wait_time = ride["wait_time"]
        is_low_now = wait_time < 20
        was_low_last = st.session_state["was_under_threshold"].get(ride["name"], True)
        if is_low_now and not was_low_last and ride["name"] in rides_i_care_about:
            st.toast(f"{ride['name']} just dropped under 20 min!")
            if ntfy_topic:
                requests.post(
                    f"https://ntfy.sh/{ntfy_topic}",
                    data=f"{ride['name']} just dropped under 20 min ({wait_time} min)".encode("utf-8"),
                    headers={"Title": "Ride wait alert", "Priority": "default", "Tags": "roller_coaster"},
                )
        st.session_state["was_under_threshold"][ride["name"]] = is_low_now

        if is_low_now:
            st.success(f"{ride['name']}: {wait_time} min")
        elif wait_time < 45:
            st.warning(f"{ride['name']}: {wait_time} min")
        else:
            st.error(f"{ride['name']}: {wait_time} min")

time.sleep(300)  # wait 5 minutes (matches the API's own refresh rate)
st.rerun()
