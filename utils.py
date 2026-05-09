"""
Utility functions shared across the project - Person A
"""

def get_toxicity_label(score: float) -> str:
    """Convert toxicity score to readable label."""
    if score >= 0.85:
        return "Highly Toxic"
    elif score >= 0.65:
        return "Toxic"
    elif score >= 0.45:
        return "Mildly Toxic"
    else:
        return "Clean"

def get_color_for_score(score: float) -> str:
    """Return emoji color based on toxicity level."""
    if score >= 0.85:
        return "🔴"
    elif score >= 0.65:
        return "🟠"
    elif score >= 0.45:
        return "🟡"
    else:
        return "🟢"