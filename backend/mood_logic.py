def map_mood_to_keywords(user_input):
    user_input = user_input.lower()
    mood_keywords = {
        "happy": ["happy", "joy", "excited", "funny", "laugh"],
        "sad": ["sad", "upset", "down", "emotional"],
        "motivated": ["motivate", "inspire", "goal", "hustle"],
        "relaxed": ["calm", "relaxed", "chill", "peace"],
        "angry": ["angry", "mad", "frustrated", "annoyed"],
        "nature":["nature", "forest", "mountain", "river", "greenery", "sunset", "sunrise",
                    "rain", "beach", "waterfall", "trees", "flowers", "birds", "sky", "clouds",
                    "natural", "outdoor", "wildlife", "hiking", "camping", "woods", "jungle"]
    }

    for mood, keywords in mood_keywords.items():
        for word in keywords:
            if word in user_input:
                return mood
    return None
