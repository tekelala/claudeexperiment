import streamlit as st
import requests
import json

st.title("Chat with Claude")

# Container for welcome message and banner
with st.container():
    st.write("Welcome to our chat app!")  # Welcome message
    # st.image("banner.jpg")  # Display a banner (uncomment this line and replace "banner.jpg" with the path to your banner image)

# Define initial prompts
if "prompts" not in st.session_state:
    st.session_state.prompts = []

# Placeholder for user input
user_input = st.empty()

# Container for conversation history
with st.container():
    # Display the entire conversation
    for prompt in st.session_state.prompts:
        if prompt['role'] == 'Human':
            st.write(f"You: {prompt['content']}")
        else:  # prompt['role'] == 'Assistant'
            st.write(f"Claude: {prompt['content']}")

# User input and Send button
user_message = user_input.text_input("You: ")

# When the user clicks "Send", append the input to the prompts and make a request to Claude API
if st.button("Send"):
    if user_message:
        st.session_state.prompts.append({
            "role": "Human",
            "content": user_message
        })

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
                "model": "claude-v1.3",
                "max_tokens_to_sample": 100,
                "stop_sequences": ["\n\nHuman:"]
            }

            # Make a POST request to the Claude API
            with st.spinner('Waiting for Claude...'):
                try:
                    response = requests.post(api_url, headers=headers, data=json.dumps(body))
                    response.raise_for_status()

                    result = response.json()

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

    # Clear the text input box
    user_input.text_input("You: ", value="", key="unique")
