import os
import openai

# ----------------------------
# Keyword-based fallback detection
# ----------------------------
def map_mood_to_keywords(user_input):
    user_input = user_input.lower()
    mood_keywords = {
    "happy": [
        "happy", "joy", "glad", "excited", "cheerful", "funny", "delighted", "content", "blissful", "grateful",
        "positive", "ecstatic", "elated", "giggly", "laugh", "reels", "videos", "watch", "smiling"
    ],
    "sad": [
        "sad", "down", "upset", "depressed", "emotional", "cry", "lonely", "unhappy", "gloomy", "disappointed",
        "miserable", "heartbroken", "blue", "grief", "tearful"
    ],
    "motivated": [
        "motivated", "inspired", "driven", "focused", "ambitious", "energetic", "productive", "goal", "hustle",
        "success", "dream", "winning", "powerful", "determined"
    ],
    "relaxed": [
        "relaxed", "calm", "chill", "peaceful", "serene", "easygoing", "breathe", "slow", "unbothered", "gentle",
        "soothing", "lazy", "cozy", "quiet", "soft music"
    ],
    "angry": [
        "angry", "mad", "furious", "irritated", "frustrated", "annoyed", "raging", "pissed", "temper", "agitated",
        "grumpy", "snappy", "exploding", "shouting"
    ],
    "bored": [
        "bored", "nothing", "dull", "meh", "yawn", "lazy", "tired", "idle", "blank", "empty", "wasting time"
    ],
    "romantic": [
        "love", "romantic", "crush", "dating", "heart", "cute", "relationship", "valentine", "hug", "kiss",
        "affection", "feelings", "cuddle", "sweetheart"
    ],
    "anxious": [
        "nervous", "anxious", "worried", "stressed", "panic", "uneasy", "tense", "restless", "overthinking", "fear",
        "scared", "doubt", "uncertain", "freaked"
    ],
    "confident": [
        "confident", "bold", "fearless", "sure", "assertive", "powerful", "self-assured", "winner", "alpha", "strong"
    ]
}


    for mood, keywords in mood_keywords.items():
        for word in keywords:
            if word in user_input:
                return mood
    return None


# ----------------------------
# LLM-powered mood detection using OpenRouter API
# ----------------------------
def detect_mood_with_llm(user_input, temperature, top_p, max_tokens):
    api_key = os.getenv("OPENROUTER_API_KEY")
    print("🔑 Loaded OpenRouter API key:", api_key)
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment.")
        return None

    openai.api_key = api_key
    openai.api_base = "https://openrouter.ai/api/v1"

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a mood detector. Based on the user's input, reply with ONLY ONE word: "
                        "happy, sad, motivated, angry, or relaxed. If unsure, pick the closest. "
                        "Do NOT explain, just reply with the mood."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )

        mood = response.choices[0].message.content.strip().lower()
        return mood

    except Exception as e:
        print("LLM detection error:", e)
        return None


# ----------------------------
# LLM-powered chatbot reply generation using OpenRouter
# ----------------------------
def generate_reply_with_llm(user_input, temperature=0.7, top_p=0.9, max_tokens=100):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found.")
        return "I'm having trouble responding right now."

    openai.api_key = api_key
    openai.api_base = "https://openrouter.ai/api/v1"

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a cheerful and friendly chatbot that gives short, casual, fun replies. "
                        "If someone seems sad, cheer them up in a light and friendly way — no serious advice, no therapy talk. "
                        "Avoid suggesting professional help. Just be a comforting digital buddy."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )

        reply = response.choices[0].message.content.strip()
        return reply

    except Exception as e:
        print("LLM reply generation error:", e)
        return "Here are some reels which can match your mood"


# ----------------------------
# Final unified mood detector
# ----------------------------
def detect_mood(user_input, temperature=0.7, top_p=0.9, max_tokens=50):
    # First try LLM-based detection with passed parameters
    mood = detect_mood_with_llm(user_input, temperature, top_p, max_tokens)

    if mood in ["happy", "sad", "motivated", "angry", "relaxed"]:
        return mood

    # Fallback to keyword-based detection
    return map_mood_to_keywords(user_input)