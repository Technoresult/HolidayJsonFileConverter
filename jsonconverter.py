import streamlit as st
import pandas as pd
from datetime import datetime
import json
import re

st.title("Holiday Data Converter")
st.write("""
This app converts raw holiday data into a structured JSON format.
Enter your raw holiday data in various formats:
- `DD-MMM-YY Day Name Type` (e.g., 26-Jan-24 Friday Republic Day Mandatory)
- `DD-MM-YYYY Day Name Type` (e.g., 15-08-2025 Friday Independence Day Mandatory)
""")

# Create a text area for input
raw_data = st.text_area("Enter raw holiday data:", 
                        height=300,
                        placeholder="Example:\n26-Jan-24 Friday Republic Day Mandatory\n15-08-2025 Friday Independence Day Mandatory")

if st.button("Convert to JSON"):
    if raw_data:
        # Parse the raw data
        holidays = []
        
        # Combined regex pattern to match different date formats
        # Format 1: DD-MMM-YY (26-Jan-24)
        # Format 2: DD-MM-YYYY (15-08-2025)
        date_pattern = r'(\d{2}-(?:\d{2}-\d{4}|[A-Za-z]{3}-\d{2}))\s+([A-Za-z]+)\s+([^M]+?)\s+(Mandatory|Optional)'
        matches = re.findall(date_pattern, raw_data)
        
        if not matches:
            st.error("Could not parse any holiday entries. Please check the format.")
        
        for match in matches:
            date_str, day, name, holiday_type = match
            name = name.strip()  # Remove leading/trailing whitespace
            
            # Parse the date based on its format
            try:
                # Try different date formats
                if re.match(r'\d{2}-\d{2}-\d{4}', date_str):  # DD-MM-YYYY
                    date = datetime.strptime(date_str, "%d-%m-%Y")
                elif re.match(r'\d{2}-[A-Za-z]{3}-\d{2}', date_str):  # DD-MMM-YY
                    date = datetime.strptime(date_str, "%d-%b-%y")
                else:
                    raise ValueError(f"Unrecognized date format: {date_str}")
                
                # Format dates for JSON
                start_date = date.strftime("%Y-%m-%d")
                
                # Calculate end date (next day)
                from datetime import timedelta
                next_day = date + timedelta(days=1)
                end_date = next_day.strftime("%Y-%m-%d")
                
                # Create holiday entry
                holiday = {
                    "subject": name,
                    "start": start_date,
                    "end": end_date,
                    "type": holiday_type
                }
                
                holidays.append(holiday)
            except ValueError as e:
                st.error(f"Error parsing date '{date_str}': {e}")
        
        # Create the JSON structure
        result = {"holidays": holidays}
        
        # Display the JSON output
        st.subheader("JSON Output")
        st.json(result)
        
        # Provide download button for the JSON file
        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="Download JSON",
            file_name="holidays.json",
            mime="application/json",
            data=json_str
        )
    else:
        st.warning("Please enter some raw holiday data.")

# Show example of input and output formats
with st.expander("Show Example"):
    st.subheader("Examples of Valid Input Formats")
    st.code("""# Format 1: DD-MMM-YY
26-Jan-24 Friday Republic Day Mandatory
09-Apr-24 Tuesday Ugadi / Gudi Padwa Mandatory

# Format 2: DD-MM-YYYY
15-08-2025 Friday Independence Day Mandatory
25-12-2025 Thursday Christmas Day Mandatory""")
    
    st.subheader("Example Output")
    example_output = {
        "holidays": [
            {"subject": "Republic Day", "start": "2024-01-26", "end": "2024-01-27", "type": "Mandatory"},
            {"subject": "Ugadi / Gudi Padwa", "start": "2024-04-09", "end": "2024-04-10", "type": "Mandatory"},
            {"subject": "Independence Day", "start": "2025-08-15", "end": "2025-08-16", "type": "Mandatory"},
            {"subject": "Christmas Day", "start": "2025-12-25", "end": "2025-12-26", "type": "Mandatory"}
        ]
    }
    st.json(example_output)
