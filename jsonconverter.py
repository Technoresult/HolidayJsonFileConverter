import streamlit as st
import pandas as pd
from datetime import datetime
import json
import re

st.title("Holiday Data Converter")

st.write("""
This app converts raw holiday data into a structured JSON format.
Enter your raw holiday data in the format: 
`DD-MMM-YY Day Name Type`
""")

# Create a text area for input
raw_data = st.text_area("Enter raw holiday data:", 
                        height=300,
                        placeholder="Example:\n26-Jan-24 Friday Republic Day Mandatory\n09-Apr-24 Tuesday Ugadi / Gudi Padwa Mandatory")

if st.button("Convert to JSON"):
    if raw_data:
        # Parse the raw data
        holidays = []
        
        # Use regex to find date patterns and extract holiday entries
        date_pattern = r'(\d{2}-[A-Za-z]{3}-\d{2})\s+([A-Za-z]+)\s+([^M]+?)\s+(Mandatory|Optional)'
        matches = re.findall(date_pattern, raw_data)
        
        if not matches:
            st.error("Could not parse any holiday entries. Please check the format.")
        
        for match in matches:
            date_str, day, name, holiday_type = match
            name = name.strip()  # Remove leading/trailing whitespace
            
            # Parse the date
            try:
                date = datetime.strptime(date_str, "%d-%b-%y")
                
                # Format dates for JSON
                start_date = date.strftime("%Y-%m-%d")
                
                # Calculate end date (next day)
                end_date = (date.replace(day=date.day + 1)).strftime("%Y-%m-%d")
                
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
    st.subheader("Example Input")
    st.code("""26-Jan-24 Friday Republic Day Mandatory
09-Apr-24 Tuesday Ugadi / Gudi Padwa Mandatory
01-May-24 Wednesday May Day Mandatory""")
    
    st.subheader("Example Output")
    example_output = {
        "holidays": [
            {"subject": "Republic Day", "start": "2024-01-26", "end": "2024-01-27", "type": "Mandatory"},
            {"subject": "Ugadi / Gudi Padwa", "start": "2024-04-09", "end": "2024-04-10", "type": "Mandatory"},
            {"subject": "May Day", "start": "2024-05-01", "end": "2024-05-02", "type": "Mandatory"}
        ]
    }
    st.json(example_output)
