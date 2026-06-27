# PII Patterns for Regex Scanning
PII_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "PHONE": r"\b(?:\+?\d{1,3}[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b",
}

# Injection Keywords
PROMPT_INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "system prompt",
    "you must now pretend to be",
    "override",
    "forget all instructions",
]

# Hallucination and validation thresholds
HALLUCINATION_THRESHOLD = 0.85
COMPLIANCE_REQUIRED_TERMS = [
    "confidentiality notice",
    "grounded based on",
]
