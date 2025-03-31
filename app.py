import streamlit as st
import pandas as pd
from ics import Calendar
from datetime import datetime

# Upload .ics calendar file
st.title("LiquidPlanner Notes Dashboard")
uploaded_file = st.file_uploader("Upload your .ics calendar file")

if uploaded_file:
    calendar = Calendar(uploaded_file.read().decode("utf-8"))
    events = []

    for event in calendar.events:
        events.append({
            "Date": event.begin.datetime.date(),
            "Time": event.begin.datetime.time().strftime("%I:%M %p"),
            "Client": event.name.split("–")[0].strip(),
            "Meeting Title": event.name,
            "Description": event.description or "",
            "Drafted Note": f"Met with {event.name.split('–')[0].strip()} on {event.begin.datetime.strftime('%B %d at %I:%M %p')}."
        })

    df = pd.DataFrame(events)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="lp_notes.csv", mime="text/csv")
