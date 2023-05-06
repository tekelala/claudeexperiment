import streamlit as st
import requests
import json

# Define Claude API endpoint
API_ENDPOINT = "https://api.anthropic.com/v1.3/complete" 

# Define function to query API 
def query(payload): 
  headers = {
    "Content-Type": "application/json",
    "X-API-Key": st.secrets["API_KEY"]
  }
  response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(payload))
  
  # Handle response and errors
  try: 
    response = response.json()
  except:
    st.error("Invalid JSON response from API")
    st.stop()
    
  # Check if "completion" key exists
  if "completion" not in response:
    st.error("Invalid JSON response from API")
    st.stop()
    
  return response

# Create page content
st.title("Chatbot")
st.write("This is a basic chatbot using the Claude API.")

# Prompt user for query and call API
query_input = st.text_input("You: ", "How can I help you today?", key = "query_input")  

if query_input:
  # Format the query for the Claude API
  prompt = f"\n\nHuman: {query_input}\n\nAssistant:"
  # Call API and display response
  response = query({
    "prompt": prompt,
    "model": "claude-v1",
    "max_tokens_to_sample": 100,
    "stop_sequences": ["\n\nHuman:"]
  })
  try: 
    st.write("Claude: ", response["completion"]) 
  except:
    st.error("Unable to display response from API")
    st.stop()

# Continuously prompt for new queries  
while True:    
  query_input = st.text_input("You: ", "", key = "query_input2") 
  if query_input:
    # Format the query for the Claude API
    prompt = f"\n\nHuman: {query_input}\n\nAssistant:"
    # Call API and display response
    response = query({
      "prompt": prompt,
      "model": "claude-v1",
      "max_tokens_to_sample": 100,
      "stop_sequences": ["\n\nHuman:"]
    })
    try: 
      st.write("Claude: ", response["completion"])
    except:
      st.error("Unable to display response from API")
      st.stop() 
