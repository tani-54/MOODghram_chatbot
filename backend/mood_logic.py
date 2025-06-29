import os
import openai  # Make sure this is installed

# ----------------------------
# Keyword-based fallback detection
# ----------------------------
def map_mood_to_keywords(user_input):
    user_input = user_input.lower()
    mood_keywords = {
        "happy": ["happy", "joy", "excited", "funny", "laugh", "cheerful"],
        "sad": ["sad", "upset", "down", "emotional", "cry", "tears"],
        "motivated": ["motivate", "inspire", "goal", "hustle", "success", "dream"],
        "relaxed": ["calm", "relaxed", "chill", "peace", "slow", "breathe"],
        "angry": ["angry", "mad", "frustrated", "annoyed", "rage", "irritated"]
    }

    for mood, keywords in mood_keywords.items():
        for word in keywords:
            if word in user_input:
                return mood
    return None

# ----------------------------
# LLM-powered detection using OpenRouter API
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
            model="google/gemma-7b-it",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a mood detector. Based on the following input text, respond with ONLY ONE WORD from this list: "
                        "happy, sad, motivated, angry, relaxed. Do not say anything else."
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
# Final unified mood detector
# ----------------------------
def detect_mood(user_input, temperature=0.7, top_p=0.9, max_tokens=50):
    # First try LLM-based detection with passed parameters
    mood = detect_mood_with_llm(user_input, temperature, top_p, max_tokens)

    if mood in ["happy", "sad", "motivated", "angry", "relaxed"]:
        return mood

    # Fallback to keyword-based detection
    return map_mood_to_keywords(user_input)
