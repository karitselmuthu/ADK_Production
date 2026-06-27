import os
from google.genai import types

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# Default retry settings
DEFAULT_RETRY = types.HttpRetryOptions(attempts=3)

# Generation Configurations
ROOT_AGENT_CONFIG = {
    "model": MODEL_NAME,
    "temperature": 0.1,
    "max_output_tokens": 1024,
}

KNOWLEDGE_AGENT_CONFIG = {
    "model": MODEL_NAME,
    "temperature": 0.2,
    "max_output_tokens": 2048,
}

WORKFLOW_AGENT_CONFIG = {
    "model": MODEL_NAME,
    "temperature": 0.0,
    "max_output_tokens": 1024,
}

CALCULATION_AGENT_CONFIG = {
    "model": MODEL_NAME,
    "temperature": 0.0,
    "max_output_tokens": 512,
}

VALIDATION_AGENT_CONFIG = {
    "model": MODEL_NAME,
    "temperature": 0.1,
    "max_output_tokens": 1024,
}

ESCALATION_AGENT_CONFIG = {
    "model": MODEL_NAME,
    "temperature": 0.2,
    "max_output_tokens": 512,
}
