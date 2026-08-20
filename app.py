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

NTFY_TOPIC_URL = st.secrets["NTFY_TOPIC_URL"]

selected_park = st.selectbox("Park", list(PARKS.keys()), key="selected_park")
park_id = PARKS[selected_park]

if st.session_state.get("last_park") != selected_park:
    st.session_state["was_under_threshold"] = {}
    st.session_state["last_park"] = selected_park

url = f"https://queue-times.com/parks/{park_id}/queue_times.json"
response = requests.get(url)
data = response.json()
st.caption(f"Last updated: {now.strftime('%I:%M %p')}")

for land in data["lands"]:
    for ride in land["rides"]:
        if not ride["is_open"]:
            st.error(f"{ride['name']}: closed")
            continue

        wait_time = ride["wait_time"]
        is_low_now = wait_time < 20
        was_low_last = st.session_state["was_under_threshold"].get(ride["name"], True)
        if is_low_now and not was_low_last:
            st.toast(f"{ride['name']} just dropped under 20 min!")
            requests.post(
                NTFY_TOPIC_URL,
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
