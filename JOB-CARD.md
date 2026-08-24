# Job Card
What it does (one sentence): Classifies the sentiment of a piece of textual content.
Input: { "text": "string, 1-10,000 characters" }
Output: { 
            "sentiment": one of [positive|negative|neutral|unsure],
            "confidence": 0.0-1.0,
            "second_best" "The second best guess for the sentiment"
            "reason": "A small sentence."
        }
When unsure: It should return the unsure category.
