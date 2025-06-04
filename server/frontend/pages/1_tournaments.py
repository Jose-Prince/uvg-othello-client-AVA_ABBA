import streamlit as st 
import requests
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd

if not "tournaments_list" in st.session_state: 
    st.session_state.open_tournaments = []


load_dotenv(override=True) 
BASE_URL = os.getenv("BASE_URL")

print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print(os.getenv("BASE_URL"))
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')
print('---------------------------------------')

open_tournaments_req = requests.get(f"{BASE_URL}/tournament/list")
st.session_state.open_tournaments = open_tournaments_req.json().get("tournaments", [])

st.title("Tournaments")

if st.session_state.open_tournaments:
    # Convert the list of tournaments to a DataFrame
    tournaments_df = pd.DataFrame(st.session_state.open_tournaments)
    
    # Display the DataFrame
    st.dataframe(tournaments_df.sort_values(by = ['status'], ascending= True))

st.subheader("Create a New Tournament")

new_tournament_name = st.text_input("Tournament Name")

if st.button("Create Tournament"):
    if new_tournament_name:
        create_req = requests.post(f"{BASE_URL}/tournament/create", json={"name": new_tournament_name})
        if create_req.status_code == 200:
            st.success(f"Tournament '{new_tournament_name}' created successfully!")
            open_tournaments_req = requests.get(f"{BASE_URL}/tournament/list")
            st.session_state.open_tournaments = open_tournaments_req.json().get("tournaments", [])

        else:
            st.error("Failed to create tournament. Please try again.")
    else:
        st.error("Tournament name cannot be empty.")

st.subheader("Close Tournament")
# Add a multiselect to select tournaments to close
selected_tournaments = st.multiselect(
    "Select tournaments to close", 
    [tournament['name'] for tournament in st.session_state.open_tournaments if tournament.get('status') == 'available']
)

# Add a button to close selected tournaments
if st.button("Close Selected Tournaments"):
    if selected_tournaments:
        for tournament_name in selected_tournaments:
            close_req = requests.post(f"{BASE_URL}/tournament/close", json={"name": tournament_name})
            if close_req.status_code == 200:
                st.success(f"Tournament '{tournament_name}' closed successfully!")
                st.session_state.success_message = f"Tournament '{tournament_name}' closed successfully!"
            else:
                st.error(f"Failed to close tournament '{tournament_name}'.")
    else:
        st.error("No tournaments selected to close.")

deleted_tournaments = st.multiselect(
    "Select tournaments to delete", 
    [tournament['name'] for tournament in st.session_state.open_tournaments]
)
# Add a button to close selected tournaments
if st.button("Delete Selected Tournaments"):
    if deleted_tournaments:
        for tournament_name in deleted_tournaments:
            close_req = requests.post(f"{BASE_URL}/tournament/delete", json={"name": tournament_name})
            if close_req.status_code == 200:
                st.success(f"Tournament '{tournament_name}' deleted successfully!")
                st.session_state.success_message = f"Tournament '{tournament_name}' deleted successfully!"
            else:
                st.error(f"Failed to close tournament '{tournament_name}'.")
    else:
        st.error("No tournaments selected to close.")

        