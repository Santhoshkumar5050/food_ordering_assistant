import streamlit as st
from agents.orchestrator_agent import OrchestratorAgent

st.set_page_config(page_title="AI Food Ordering", page_icon="🤖")
st.title("🤖 Context-Engineered AI Food & Grocery Ordering Assistant")
st.markdown("Chat with me to order your favorite meals 🍕🥗")

if "agent" not in st.session_state:
    st.session_state.agent = OrchestratorAgent()
    st.session_state.chat_history = [("AI", st.session_state.agent.initial_message)]

user_input = st.chat_input("Say something...")

if user_input:
    response = st.session_state.agent.handle_message(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", response))

for sender, msg in st.session_state.chat_history:
    st.chat_message("assistant" if sender == "AI" else "user").write(msg)
