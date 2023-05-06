import requests
import streamlit as st

# Define the API endpoint
API_ENDPOINT = "https://api.anthropic.com/v1/complete"

# Define the headers for the API request
headers = {
    "x-api-key": st.secrets["API_KEY"],
    "content-type": "application/json"
}

def get_response(prompt):
    # Define the data for the API request
    data = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant: ",
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
        return completion
    else:
        st.error("We encountered an error")
        return None

def app():
    st.title("Ask Claude")
    user_input = st.text_input("Enter your question:")
    if st.button("Ask"):
        with st.spinner("Please wait..."):
            response = get_response(user_input)
            if response:
                st.text(response)
            else:
                st.error("Failed to get a response.")

if __name__ == "__main__":
    app()
