import os
import requests

def call_openrouter_chat(messages, temperature=0.7, top_p=0.9, max_tokens=100):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found.")
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("❌ OpenRouter call failed:", e)
        return None


# ----------------------------
# Global Mood Keyword Mapping
# ----------------------------
mood_keywords = {
    "happy": [
        "happy", "joy", "delighted", "cheerful", "smile", "grateful", "sunny", "ecstatic",
        "glad", "excited", "satisfied", "content", "positive", "optimistic", "playful", "good", "nice"
    ],
    "sad": [
        "sad", "depressed", "cry", "tearful", "gloomy", "lonely", "unhappy", "grief", "melancholy",
        "sorrow", "hurt", "pain", "miserable", "regret", "heartbroken"
    ],
    "angry": [
        "angry", "mad", "furious", "frustrated", "irritated", "annoyed", "rage", "resentful",
        "agitated", "jealous", "grumpy", "outraged", "pissed", "hostile"
    ],
    "motivated": [
        "motivated", "driven", "determined", "focused", "goal", "ambitious", "productive",
        "inspired", "empowered", "dedicated", "committed", "hustle", "strong", "rise"
    ],
    "relaxed": [
        "relaxed", "calm", "chill", "peaceful", "soothing", "serene", "unwind", "comfy",
        "lazy", "sleepy", "breathe", "slow", "tranquil", "zen"
    ],
    "romantic": [
        "romantic", "love", "in love", "affection", "sweet", "heart", "cute", "date",
        "crush", "darling", "flirt", "butterflies", "valentine", "passion"
    ],
    "bored": [
        "bored", "meh", "idle", "tired", "dull", "nothing to do", "blank", "waiting", "slow day",
        "yawn", "procrastinate", "wasting time"
    ],
    "anxious": [
        "anxious", "nervous", "scared", "tense", "shaky", "worried", "fear", "panic", "insecure",
        "afraid", "stress", "restless", "uneasy"
    ],
    "confident": [
        "confident", "strong", "bold", "sure", "courage", "ready", "assertive", "capable", "empowered",
        "fearless", "believe", "conquer", "stand tall", "unstoppable"
    ],
    "lonely": [
        "lonely", "alone", "isolated", "ignored", "abandoned", "unseen", "neglected", "quiet", "disconnected"
    ],
    "grateful": [
        "grateful", "thankful", "blessed", "appreciate", "gratitude", "thank you", "thankfulness"
    ],
    "anime": [
        "fight", "final battle", "cry", "tearful", "gloomy", "lonely"
    ]
}

# ----------------------------
# LLM-powered chatbot reply generation using OpenRouter
# ----------------------------
def generate_reply_with_llm(user_input, temperature=0.7, top_p=0.9, max_tokens=100):
    messages = [
    {
        "role": "system",
        "content": (
            "You are a cheerful and friendly chatbot that gives short, casual, fun replies.\n"
            "Only cheer someone up if their mood is detected as sad.\n"
            "If the mood is happy, motivated, or confident, reflect that in a fun or energetic way.\n"
            "Do not assume they are sad unless it's clearly stated.\n"
            "Avoid suggesting therapy or serious advice."
        )
    },
    {"role": "user", "content": user_input}
]


    reply = call_openrouter_chat(messages, temperature, top_p, max_tokens)
    print("🧠 LLM reply:", reply)
    return reply or "Here are some reels which can match your mood"

# ----------------------------
# LLM-powered mood detection using OpenRouter API
# ----------------------------
def detect_mood_with_llm(user_input, temperature, top_p, max_tokens):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a mood detector. Based on the user's input, reply with ONLY ONE word: "
                "happy, sad, motivated, angry, relaxed, romantic, bored, anxious, confident, lonely, grateful, or anime. "
                "Do NOT explain, just reply with the mood."
            )
        },
        {"role": "user", "content": user_input}
    ]

    mood = call_openrouter_chat(messages, temperature, top_p, max_tokens)
    print("🤖 LLM detected mood:", mood)
    return mood.lower() if mood else None


# ----------------------------
# Keyword-based fallback detection
# ----------------------------
def map_mood_to_keywords(user_input):
    user_input = user_input.lower()
    for mood, keywords in mood_keywords.items():
        for word in keywords:
            if word in user_input:
                return mood
    return None


# ----------------------------
# Final unified mood detector
# ----------------------------
def detect_mood(user_input, temperature=0.7, top_p=0.9, max_tokens=50):
    # First try LLM-based detection with passed parameters
    mood = detect_mood_with_llm(user_input, temperature, top_p, max_tokens)

    ALLOWED_MOODS = list(mood_keywords.keys())
    if mood in ALLOWED_MOODS:
        return mood

    # Fallback to keyword-based detection
    return map_mood_to_keywords(user_input)
