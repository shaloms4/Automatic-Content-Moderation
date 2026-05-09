"""
Rule-Based Moderation Module - Person A
"""

import pandas as pd
from better_profanity import profanity
from preprocess import preprocess_text   # <-- Important import
from typing import Dict

def load_custom_profanity_from_csv():
    try:
        df = pd.read_csv("data/custom_profanity.csv")
        extra_words = df['word'].dropna().str.lower().tolist()
        profanity.add_censor_words(extra_words)
        print(f"✅ Loaded {len(extra_words)} custom words from CSV.")
    except FileNotFoundError:
        print("⚠️ custom_profanity.csv not found!")
    except Exception as e:
        print(f"⚠️ Error loading CSV: {e}")

# Load custom words
load_custom_profanity_from_csv()

def rule_based_moderate(text: str) -> Dict:
    """
    Main rule-based function.
    It first preprocesses the text, then applies profanity detection.
    """
    # Step 1: Preprocess
    cleaned_text = preprocess_text(text)
    
    # Step 2: Apply moderation on cleaned text
    masked_text = profanity.censor(text)   # We censor original for better readability
    
    flagged = []
    lower_cleaned = cleaned_text.lower()
    
    for word in lower_cleaned.split():
        if profanity.contains_profanity(word):
            flagged.append(word)
    
    return {
        "original_text": text,
        "cleaned_text": cleaned_text,
        "is_profane": len(flagged) > 0,
        "flagged_words": flagged[:10],
        "masked_text": masked_text,
        "profane_count": len(flagged),
        "method": "rule_based"
    }

# Test
if __name__ == "__main__":
    tests = [
        "This is a Sh!t example post",
        "Th15 15 4 fuCk1ng b4d p0st!!!",
        "You are such an idiot",
        "This is perfectly fine content",
        "KYS you stupid moron"
    ]
    
    print("=== Rule-Based + Preprocess Test ===\n")
    for t in tests:
        result = rule_based_moderate(t)
        print(f"Original : {t}")
        print(f"Cleaned  : {result['cleaned_text']}")
        print(f"Profane  : {result['is_profane']}")
        print(f"Masked   : {result['masked_text']}")
        print("-" * 80)