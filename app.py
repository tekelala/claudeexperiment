import streamlit as st
import requests
import time

# Define Claude API endpoint
API_ENDPOINT = "https://api-inference.huggingface.co/models/claude-cpc:latest" 

# Define function to query API 
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

# Create page content
st.title("Chatbot")
st.write("This is a basic chatbot using the Claude API.")

# Prompt user for query and call API
query_input = st.text_input("You: ", "How can I help you today?")  

# Add delay between requests to API 
time.sleep(2)  

# Call API and display response
response = query({ "inputs": query_input })
try: 
  st.write("Claude: ", response["responses"][0]["text"]) 
except:
  st.error("Unable to display response from API")
  st.stop()
  
# Continuously prompt for new queries  
while True:    
  query_input = st.text_input("You: ", "")
  if query_input:
    
    # Add delay between requests to API 
    time.sleep(2)  
    
    # Call API and display response
    response = query({ "inputs": query_input })
    try: 
      st.write("Claude: ", response["responses"][0]["text"])
    except:
      st.error("Unable to display response from API")
      st.stop() 
