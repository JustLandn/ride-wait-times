import requests
import streamlit as st

url = "https://queue-times.com/parks/32/queue_times.json"
response = requests.get(url)
data = response.json()

for land in data["lands"]:
    for ride in land["rides"]:
        if not ride["is_open"]:
            st.error(f"{ride['name']}: closed")
        elif ride["wait_time"] < 20:
            st.success(f"{ride['name']}: {ride['wait_time']} min")
        elif ride["wait_time"] < 45:
            st.warning(f"{ride['name']}: {ride['wait_time']} min")
        else:
            st.error(f"{ride['name']}: {ride['wait_time']} min")
