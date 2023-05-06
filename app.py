import requests
import streamlit as st
import SessionState

# Define the API endpoint
API_ENDPOINT = "https://api.anthropic.com/v1/complete"

# Define the headers for the API request
headers = {
    "x-api-key": st.secrets["API_KEY"],
    "content-type": "application/json"
}

def get_response(conversation, user_input):
    # Add the user input to the conversation
    conversation.append(f"\n\nHuman: {user_input}\n\nAssistant: ")

    # Define the data for the API request
    data = {
        "prompt": "".join(conversation), 
        "model": "claude-v1", 
        "max_tokens_to_sample": 300, 
        "stop_sequences": ["\n\nHuman:"]
    }

    # Send the API request
    response = requests.post(API_ENDPOINT, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the completion from the response
        completion = response.json()['completion']
        # Add the response to the conversation
        conversation.append(completion)
        return completion
    else:
        st.error("We encountered an error")
        return None

def app():
    st.title("Ask Claude")

    # Initialize session state for the conversation
    state = SessionState.get(conversation=[])

    user_input = st.text_input("Enter your question:")
    if st.button("Ask"):
        with st.spinner("Please wait..."):
            response = get_response(state.conversation, user_input)
            if response:
                st.text(response)
            else:
                st.error("Failed to get a response.")

if __name__ == "__main__":
    app()
