"""
Pre-processing Module - Person A (Improved)
"""

import re
import spacy

nlp = spacy.load("en_core_web_sm")

def handle_leetspeak(text: str) -> str:
    """Convert common leetspeak."""
    leetspeak_map = {
        '4': 'a', '3': 'e', '1': 'i', '0': 'o', '@': 'a',
        '$': 's', '5': 's', '7': 't', '8': 'b', '9': 'g',
        '2': 'z', '!': 'i', '|': 'l'
    }
    text = text.lower()
    for old, new in leetspeak_map.items():
        text = text.replace(old, new)
    return text

def clean_text(text: str) -> str:
    """Clean text while preserving structure."""
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'@\w+', '[USER]', text)
    text = re.sub(r'[^a-z\s\']', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def lemmatize_text(text: str) -> str:
    """Light lemmatization - Avoid changing verbs like is/are/was too aggressively."""
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.is_punct:
            continue
        # Keep common auxiliary verbs as they are
        if token.lemma_ in ['be', 'have', 'do'] and token.text in ['is', 'are', 'was', 'were', 'am', 'has', 'had']:
            tokens.append(token.text)
        else:
            tokens.append(token.lemma_)
    return " ".join(tokens)

def preprocess_text(text: str) -> str:
    """Main preprocessing function"""
    text = handle_leetspeak(text)
    text = clean_text(text)
    text = lemmatize_text(text)
    return text

# Test
if __name__ == "__main__":
    test_cases = [
        "This is a Sh!t example post",
        "Th15 15 4 fuCk1ng b4d p0st!!!",
        "You are such an idiot @user123",
        "This is perfectly fine content",
        "KYS you stupid moron"
    ]
    
    print("=== Preprocessing Test ===\n")
    for text in test_cases:
        print(f"Original : {text}")
        print(f"Processed: {preprocess_text(text)}")
        print("-" * 70)