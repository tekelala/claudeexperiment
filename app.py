import streamlit as st
import requests
import json

# Define the Claude API endpoint 
API_ENDPOINT = "https://api-inference.huggingface.co/models/claude-cpc:latest"

# Define a function to query Claude
def query(payload):
  response = requests.post(API_ENDPOINT, headers={"Content-Type": "application/json"}, data=payload)
  
  # Handle response and errors
  try: 
    response = response.json()
  except:
    st.error("Invalid JSON response from API")
    st.stop()
    
  # Check if "responses" key exists
  if "responses" not in response:
    st.error("Invalid JSON response from API")
    st.stop()
    
  return response

# Create page title and intro
st.title("Chatbot")
st.write("This is a basic chatbot using the Claude API.")

# Prompt user for query and call API  
query_input = st.text_input("You: ", "How can I help you today?") 
response = query({ "inputs": query_input })

# Display response from API 
try: 
  st.write("Claude: ", response["responses"][0]["text"]) 
except:
  st.error("Unable to display response from API")
  st.stop()
  
# Continuously prompt for queries 
while True:    
  query_input = st.text_input("You: ", "")
  if query_input:
    response = query({ "inputs": query_input })
    try: 
      st.write("Claude: ", response["responses"][0]["text"])
    except:
      st.error("Unable to display response from API")
      st.stop() 
