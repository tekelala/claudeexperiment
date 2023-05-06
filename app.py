import streamlit as st
import requests
import json

st.title("Chat with Claude")

# Define initial prompts
if "prompts" not in st.session_state:
    st.session_state.prompts = []

# Fetch user input
user_input = st.text_input("You: ")

# If there's user input, append it to the prompts
if user_input:
    st.session_state.prompts.append({
        "role": "Human",
        "content": user_input
    })

# When the user clicks "Send", make a request to Claude API
if st.button("Send"):
    if st.session_state.prompts:
        api_url = "https://api.anthropic.com/v1/complete"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": st.secrets["API_KEY"]  # Use the API key from Streamlit's secrets
        }

        # Prepare the prompts for Claude
        conversation = "\n\n".join([f'{item["role"]}: {item["content"]}' for item in st.session_state.prompts]) + "\n\nAssistant:"

        # Define the body of the request
        body = {
            "prompt": conversation,
            "model": "claude-v1",
            "max_tokens_to_sample": 100,
            "stop_sequences": ["\n\nHuman:"]
        }

        # Make a POST request to the Claude API
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(body))
            response.raise_for_status()

            result = response.json()
            st.text("Claude: " + result['completion'])

            # Append Claude's response to the prompts
            st.session_state.prompts.append({
                "role": "Assistant",
                "content": result['completion']
            })
        except requests.exceptions.HTTPError as errh:
            st.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            st.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            st.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            st.error(f"Something went wrong: {err}")
