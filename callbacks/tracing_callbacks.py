import logging
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

logger = logging.getLogger("enterprise_adk_agent.tracing")

try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    TRACING_AVAILABLE = True
    tracer = trace.get_tracer("enterprise-adk-agent")
except ImportError:
    TRACING_AVAILABLE = False
    tracer = None

async def before_model_trace(callback_context: CallbackContext, llm_request: LlmRequest) -> None:
    """Pre-model callback to start a tracing span."""
    if TRACING_AVAILABLE and tracer:
        # Create a span linked to the current execution
        span = tracer.start_span(f"llm_call_{llm_request.model}")
        span.set_attribute("model.name", llm_request.model)
        span.set_attribute("session.id", callback_context.session.id)
        # Store span reference in temp session state
        callback_context.state["temp:telemetry_span"] = span
    else:
        logger.debug("OpenTelemetry tracing is unavailable or tracer not initialized.")

async def after_model_trace(callback_context: CallbackContext, llm_response: LlmResponse) -> None:
    """Post-model callback to record outcomes and end the span."""
    span = callback_context.state.get("temp:telemetry_span")
    if TRACING_AVAILABLE and span:
        span.set_status(Status(StatusCode.OK))
        span.end()
        if "temp:telemetry_span" in callback_context.state:
            del callback_context.state["temp:telemetry_span"]
