# for RAG Chatbot - information all already processed at the back end

import streamlit as st
import requests
import logging

BASE_API_URL = "https://76d5-2001-e68-5431-ce6f-4862-a52a-6364-2e75.ngrok-free.app"
FLOW_ID = "33cda795-b6b7-4403-8428-4e6f11230814"
ENDPOINT = "Ai_Kids" # The endpoint name of the flow" # You can set a specific endpoint name in the flow settings

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat") -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    response = requests.post(api_url, json=payload, headers=headers)
    # Log the response for debugging purpose
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Text: {response.text}")
    return response.json()
# no need sidebar

# just continue with 

def extract_message(response: dict) -> str:
    try:
        #Extract response message
        return response['outputs'][0]['outputs'][0]['results']['message']['text']
    except (KeyError, IndexError):
        logging.error("No valid message found in the response")
        return "No valid message found in the response."
    
#%% 
def main():
    st.title("AI Kids School Employee Agent")
    
    # this is for streamlit chat history, not for langflow chat history, so that the chat does not disappear from the interface
    # Initilise session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display orevious messages with avatars
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    # Input box for user message
    if query := st.chat_input("Please provide your email criteria here"):
        # Add user message to chat history
        st.session_state.messages.append(
            {"role": "user", 
             "content": query,
             "avatar": "🗯️" #emoji for user
            } 
        )
        
        with st.chat_message("user", avatar="🗯️"): # Display user query
            st.write(query)
        
        # Call the Langflow API and get the assistant's response
        with st.chat_message("assistant", avatar="🤖"): #emoji for avatar
            message_placeholder = st.empty() # Placeholder for assistant response
            with st.spinner("Waiting for response..."):
                # Fetch response from Langflow with updated TWEAKS and using `query`
                assistant_response = extract_message(run_flow(query, endpoint=ENDPOINT))
                message_placeholder.write(assistant_response)
                
        # Add assistant response to session state
        st.session_state.messages.append(
            {"role": "assistant", 
             "content": assistant_response,
             "avatar": "🤖" #emoji for assistant
            }
        )

if __name__ == "__main__":
    main()