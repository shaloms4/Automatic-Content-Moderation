from transformers import pipeline
import torch
from preprocess import preprocess_text
from rule_based import rule_based_moderate
from typing import Dict

# ====================== LOAD TRANSFORMER (BERT) ======================
device = 0 if torch.cuda.is_available() else -1

toxicity_classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    return_all_scores=False,
    device=device
)

print("✅ Toxic-BERT model loaded successfully!\n")


def get_toxicity_score(text: str) -> Dict:
    """Get score from BERT Transformer"""
    cleaned = preprocess_text(text)
    result = toxicity_classifier(cleaned)[0]

    raw_score = result['score']
    normalized_score = min(max(raw_score, 0.0), 1.0)

    return {
        "raw_model_score": round(raw_score, 4),
        "toxicity_score": round(normalized_score, 4),
        "label": result['label'],
        "is_toxic": normalized_score > 0.75,
        "categories": {result['label']: round(normalized_score, 4)}
    }


def hybrid_moderate(text: str) -> Dict:
    """Improved Hybrid Logic - Respects Context Better"""
    rule_result = rule_based_moderate(text)
    bert_result = get_toxicity_score(text)
    
    final_score = bert_result["toxicity_score"]

    # === Smarter Hybrid Logic ===
    if rule_result.get("is_profane", False):
        # Only give a moderate boost instead of forcing high score
        final_score = (final_score * 0.65) + (0.88 * 0.35)   # Weighted average
        # This allows BERT's contextual understanding to still matter

    return {
        "original_text": text,
        "moderated_text": rule_result.get("masked_text", text),
        "raw_model_score": bert_result["raw_model_score"],
        "toxicity_score": round(final_score, 4),
        "is_toxic": final_score > 0.75,
        "rule_based": rule_result,
        "bert_categories": bert_result["categories"],
        "method": "hybrid"
    }


# ====================== TEST CASES ======================
if __name__ == "__main__":
    test_texts = [
        "You are a stupid fucking idiot!",                    # Clearly toxic
        "This is a great day for cognitive science",          # Clean
        "That girl is crazy talented",                        # Should be clean
        "This bastard is great!",                             # Contextual (your example)
        "I hate this stupid assignment",                      # Mild
        "Cognitive science is absolutely fascinating"         # Clean
    ]
    
    print("🚀 Testing Improved Hybrid System (Better Context Handling)\n")
    for text in test_texts:
        print("="*80)
        result = hybrid_moderate(text)
        print("Original       :", text)
        print("Moderated      :", result["moderated_text"])
        print("Raw BERT Score :", f"{result['raw_model_score']:.4f}")
        print("Final Score    :", f"{result['toxicity_score']:.1%}")
        print("Is Toxic       :", result["is_toxic"])
        print()