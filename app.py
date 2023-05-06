import streamlit as st
import requests
import json

st.title("Chat with Claude")

# Define initial prompts
prompts = []

# Fetch user input
user_input = st.text_input("You: ")

# If there's user input, append it to the prompts
if user_input:
    prompts.append({
        "role": "Human",
        "content": user_input
    })

# When the user clicks "Send", make a request to Claude API
if st.button("Send"):
    if prompts:
        api_url = "https://api.anthropic.com/v1/complete"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": "API_KEY"
        }

        # Prepare the prompts for Claude
        conversation = "\n\n".join([f'{item["role"]}: {item["content"]}' for item in prompts]) + "\n\nAssistant:"

        # Define the body of the request
        body = {
            "prompt": conversation,
            "model": "claude-v1",
            "max_tokens_to_sample": 100,
            "stop_sequences": ["\n\nHuman:"]
        }

        # Make a POST request to the Claude API
        response = requests.post(api_url, headers=headers, data=json.dumps(body))

        # If the request is successful, display the response
        if response.status_code == 200:
            result = response.json()
            st.text("Claude: " + result['completion'])

            # Append Claude's response to the prompts
            prompts.append({
                "role": "Assistant",
                "content": result['completion']
            })
        else:
            st.error("There was an error making the request.")

st.session_state.prompts = prompts
