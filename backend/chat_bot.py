import os
import json
import streamlit as st
from dotenv import load_dotenv

from youtube_fetcher import fetch_youtube_shorts
from mood_logic import detect_mood, generate_reply_with_llm 
 # ✅ Uses LLM-based mood detection logic
st.set_page_config(page_title="MoodGram Reels Bot 🎬", layout="wide")

st.markdown("""
    <h1 style="
        background: linear-gradient(90deg, #ff6a00, #ee0979);
        color: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-align: center;
        font-size: 2.2rem;
        margin-top: 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    ">
        🎥 MoodGram - Reels Recommendation Bot
    </h1>
""", unsafe_allow_html=True)


# ----------------------------
# Load .env file for LLM key
# ----------------------------
load_dotenv()

# ----------------------------
# Load fallback JSON data
# ----------------------------
@st.cache_data
def load_reels_data():
    path = os.path.join(os.path.dirname(__file__), "..", "reels_data.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

# ----------------------------
# Greeting Detection
# ----------------------------
def is_greeting(text):
    if not isinstance(text, str):
        return False
    greetings = ['hi', 'hello', 'hey', 'hii', 'what’s up', 'whats up', 'yo', 'good morning', 'good evening']
    text = text.lower().strip()
    return any(greet in text for greet in greetings)

# ----------------------------
# Streamlit UI Setup
# ----------------------------
st.set_page_config(page_title="MoodGram Reels", page_icon="🎥", layout="wide")
#Has a chat history already been created for this session?"If not, it creates an empty list to start storing messages
if "chat_history" not in st.session_state:  ##temporary storage that holds data across user interactions.

    st.session_state.chat_history = []   #This line ensures your chatbot can remember and display full conversations — just like WhatsApp or ChatGPT!

# ----------------------------
# Sidebar for Controls
# ----------------------------
with st.sidebar:
    st.header("🛠 Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

    st.subheader("LLM Mood Detection Settings")
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.1)
    top_p = st.slider("Top P", 0.1, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max Tokens", 16, 128, 50, 8)

# ----------------------------
# Load Static JSON Fallback
# ----------------------------
mood_reels = load_reels_data()

# ----------------------------
# Chat Input Section
# ----------------------------
user_input = st.chat_input("How are you today? Type your mood or just say hi...")  ##chat box line

if user_input and isinstance(user_input, str):
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Show greeting message only on first user interaction
    if is_greeting(user_input) and len([msg for msg in st.session_state.chat_history if msg["role"] == "user"]) == 1:

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Hey there! 😊 How are you feeling today?"
        })
    else:
        # ✅ Use combined LLM + fallback keyword detection with parameters
        detected_mood = detect_mood(
            user_input,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        print("Detected mood:", detected_mood)
        
        # ✅ Generate smart dynamic reply based on user input
        llm_reply = generate_reply_with_llm(
        user_input,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": llm_reply
        })
        if detected_mood:
            try:
                reels_list = fetch_youtube_shorts(detected_mood)
            except Exception as e:
                print("API fetch error:", e)
                reels_list = []

            if reels_list:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Here are some {detected_mood} reels for you (real-time):"
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": reels_list
                })
            else:
                fallback = mood_reels.get(detected_mood, [])
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"(⚠ Couldn't fetch live data) Here are fallback {detected_mood} reels:"
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": fallback
                })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "😕 Sorry, I couldn't detect your mood. Try saying happy, sad, motivated, etc."
            })

# ----------------------------
# Display Chat Messages (Enhanced UI)
# ----------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], str):
            st.markdown(f"<div class='chat-message'>{msg['content']}</div>", unsafe_allow_html=True)

        elif isinstance(msg["content"], list):
            st.markdown("<div class='chat-message'>🎞️ <b>Here are some reels just for you:</b></div>", unsafe_allow_html=True)
            cols = st.columns(2)

            for i, reel in enumerate(msg["content"]):
                with cols[i % 2]:
                    st.markdown(f"<div class='reel-title'>🎬 {reel['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="video-box">
                            <iframe width="100%" height="240" src="{reel['video_url']}" frameborder="0" allowfullscreen></iframe>
                        </div>
                    """, unsafe_allow_html=True)
