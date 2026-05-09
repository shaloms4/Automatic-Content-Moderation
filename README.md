# Automatic-Content-Moderation

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

This will install all necessary dependencies including:
- **spacy** - For text preprocessing and lemmatization
- **better-profanity** - For profanity detection
- **pandas** - For reading the custom profanity CSV
- And other supporting packages

## Running the Project

### Step 1: Run Preprocessing

To test the text preprocessing module:

```bash
python preprocess.py
```

This will:
- Convert leetspeak (e.g., `4` → `a`, `3` → `e`)
- Clean text (remove URLs, mentions, special characters)
- Lemmatize words while preserving auxiliary verbs

### Step 2: Run Rule-Based Moderation

To test the rule-based moderation module:

```bash
python rule_based.py
```

This will:
- Load custom profanity words from `data/custom_profanity.csv`
- Apply preprocessing to text
- Detect and flag profane content
- Generate masked text output
