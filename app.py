import streamlit as st
import requests

# Define the Claude API endpoint 
API_ENDPOINT = "https://api-inference.huggingface.co/models/claude-cpc:latest"

# Define a function to get a response from Claude
def query(payload):
  response = requests.post(API_ENDPOINT, headers={"Content-Type": "application/json"}, data=payload)
  response = response.json()
  return response

# Create a title and intro on the page 
st.title("Chatbot")
st.write("This is a basic chatbot using the Claude API.")

# Prompt the user to enter a query 
query_input = st.text_input("You: ", "How can I help you today?")

# Call the Claude API with the user's query 
response = query({
  "inputs": query_input, 
})

# Display Claude's response
st.write("Claude: ",  response["responses"][0]["text"])

# Add interactivity by continuously prompting for new queries 
while True: 
  query_input = st.text_input("You: ", "")
  if query_input: 
    response = query({
      "inputs": query_input, 
    })
    st.write("Claude: ",  response["responses"][0]["text"])
