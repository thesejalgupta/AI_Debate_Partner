import streamlit as st
from chatbot import ChatBot
from debate_engine import DebateEngine
from fallacy_detector import FallacyDetector
from scoring import DebateScorer

# Page config
st.set_page_config(page_title="AI Debate Partner", layout="wide")

# Initialize session state
if 'chat_bot' not in st.session_state:
    st.session_state.chat_bot = ChatBot()

if 'debate_engine' not in st.session_state:
    st.session_state.debate_engine = None

if 'debate_active' not in st.session_state:
    st.session_state.debate_active = False

if 'debate_history' not in st.session_state:
    st.session_state.debate_history = []

# Title
st.title("🎤 AI Debate Partner")
st.markdown("---")

# Sidebar for mode selection
mode = st.sidebar.radio("Select Mode", ["Chat", "Debate"])

if mode == "Chat":
    st.header("💬 Chat Mode")
    st.write("Have a conversation with the AI chatbot.")
    
    user_input = st.text_input("You: ", key="chat_input", placeholder="Type your message...")
    
    if user_input:
        with st.spinner("AI is thinking..."):
            response = st.session_state.chat_bot.get_response(user_input)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("**You:**")
            st.info(user_input)
        with col2:
            st.write("**AI:**")
            st.success(response)

else:  # Debate mode
    st.header("⚔️ Debate Mode")
    
    # Debate setup
    if not st.session_state.debate_active:
        st.write("Set up your debate:")
        
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input("Debate Topic:", placeholder="e.g., AI should be regulated")
        with col2:
            user_side = st.selectbox("Your Side:", ["for", "against"])
        
        col3, col4 = st.columns(2)
        with col3:
            personality = st.selectbox("AI Personality:", ["calm", "aggressive", "witty"])
        with col4:
            difficulty = st.selectbox("Difficulty Level:", ["easy", "medium", "hard"])

        ai_role = st.selectbox("AI Role:", ["opponent", "support"], help="Opponent: AI counters your argument; Support: AI reinforces your argument")
        
        if st.button("Start Debate", key="start_debate"):
            if topic:
                st.session_state.debate_engine = DebateEngine(
                    topic=topic,
                    user_side=user_side,
                    personality=personality,
                    difficulty=difficulty,
                    ai_role=ai_role,
                    debug=False
                )
                st.session_state.debate_active = True
                st.session_state.debate_history = []
                st.rerun()
            else:
                st.error("Please enter a debate topic.")
    
    else:
        # Active debate
        engine = st.session_state.debate_engine
        
        st.write(f"**Topic:** {engine.topic}")
        ai_role_display = getattr(engine, 'ai_role', 'opponent')
        st.write(f"**Your Side:** {engine.user_side} | **AI Side:** {engine.ai_side} | **AI Role:** {ai_role_display} | **Personality:** {engine.personality} | **Difficulty:** {engine.difficulty}")
        st.markdown("---")
        
        # Debate history
        if st.session_state.debate_history:
            st.subheader("Debate History")
            for i, exchange in enumerate(st.session_state.debate_history, 1):
                with st.expander(f"Exchange {i}"):
                    st.write("**Your Argument:**")
                    st.info(exchange['user_arg'])
                    st.write("**AI Response:**")
                    st.success(exchange['ai_response'])
                    st.write("**Fallacy Detected:**")
                    st.warning(f"{exchange['fallacy']} - {exchange['fallacy_explanation']}")
        
        # New argument input
        st.subheader("Your Argument")
        user_argument = st.text_area("Enter your argument:", key="debate_input", placeholder="Make your argument...")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Submit Argument", key="submit_arg"):
                if user_argument:
                    with st.spinner("AI is preparing counter-argument..."):
                        # Generate AI response
                        ai_response = engine.generate_response(user_argument)
                        
                        # Extract fallacy info (from the output format)
                        lines = ai_response.split('\n')
                        fallacy_line = next((l for l in lines if l.startswith("Fallacy detected:")), "No major fallacy detected")
                        fallacy = fallacy_line.replace("Fallacy detected: ", "")
                        explanation_line = next((l for l in lines if l.startswith("Explanation:")), "No explanation")
                        explanation = explanation_line.replace("Explanation: ", "")
                        
                        # Store in history
                        st.session_state.debate_history.append({
                            'user_arg': user_argument,
                            'ai_response': ai_response,
                            'fallacy': fallacy,
                            'fallacy_explanation': explanation
                        })
                    
                    st.rerun()
                else:
                    st.error("Please enter an argument.")
        
        with col2:
            if st.button("View Memory", key="view_memory"):
                st.info(engine.memory.get_context())
        
        with col3:
            if st.button("End Debate", key="end_debate"):
                st.session_state.debate_active = False
                st.session_state.debate_engine = None
                st.rerun()

st.markdown("---")
st.caption("AI Debate Partner © 2026 | Powered by Hugging Face GPT-2")