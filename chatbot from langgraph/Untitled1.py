import streamlit as st
import uuid
from langchain_core.messages import HumanMessage

# This safely imports your compiled graph from chatbot.py
from chatbot import chatbot

st.set_page_config(page_title="My AI Chatbot", page_icon="🚀", layout="wide")
st.title("Vaibhav's AI Assistant 🚀")
st.markdown("Powered by LangGraph & Gemini")
st.divider()

# =====================================================================
# --- AMENDMENT 1 START: Upgrading the Data Structure ---
# Replaced the single 'thread_id' and 'messages' variables with 
# the 'all_chats' dictionary (bookshelf) and pointer (sticky note).
if "all_chats" not in st.session_state:
    first_thread_id = str(uuid.uuid4())
    st.session_state.all_chats = {first_thread_id: []}
    st.session_state.current_thread_id = first_thread_id
# --- AMENDMENT 1 END ---
# =====================================================================


# =====================================================================
# --- AMENDMENT 2 START: Building State Controllers ---
# Added these new helper functions so the app can easily swap notebooks.
def switch_chat(thread_id):
    st.session_state.current_thread_id = thread_id

def create_new_chat():
    new_id = str(uuid.uuid4())
    st.session_state.all_chats[new_id] = []
    st.session_state.current_thread_id = new_id
# --- AMENDMENT 2 END ---
# =====================================================================


# =====================================================================
# --- AMENDMENT 3 START: Constructing the Sidebar UI ---
# Inserted the entire sidebar block to act as the librarian. 
# It creates the "New Chat" button and lists all past sessions.
with st.sidebar:
    st.title("LangGraph Chatbot")
    
    if st.button("New Chat", use_container_width=True, type="primary"):
        create_new_chat()
        
    st.markdown("### My Conversations")
    
    for thread_id in st.session_state.all_chats.keys():
        button_label = f"{thread_id[:12]}..." 
        if st.button(button_label, key=thread_id, use_container_width=True):
            switch_chat(thread_id)
# --- AMENDMENT 3 END ---
# =====================================================================


# =====================================================================
# --- AMENDMENT 4 START: Dynamic Rendering in the Main UI ---
# Updated the main screen logic to ALWAYS look at the pointer first,
# so it only draws and saves messages for the currently open notebook.

# 1. Check the sticky note
active_thread = st.session_state.current_thread_id
st.caption(f"Active Session: {active_thread}")

# 2. Draw messages for this specific thread only
for msg in st.session_state.all_chats[active_thread]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. The Chat Input Bar
if user_input := st.chat_input("Type your message here..."):
    
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Save user message to THIS specific thread's history
    st.session_state.all_chats[active_thread].append({"role": "user", "content": user_input})

    # Pass the pointer's ID to the LangGraph backend
    config = {'configurable': {'thread_id': active_thread}}
    
    with st.spinner("Thinking..."):
        output_state = chatbot.invoke(
            {'messages': [HumanMessage(content=user_input)]}, 
            config=config
        )
    
    ans = output_state['messages'][-1].content

    with st.chat_message("assistant"):
        st.markdown(ans)
        
    # Save AI response to THIS specific thread's history
    st.session_state.all_chats[active_thread].append({"role": "assistant", "content": ans})
# --- AMENDMENT 4 END ---
# =====================================================================