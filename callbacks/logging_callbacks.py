import logging
import time
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools import BaseTool, ToolContext

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enterprise_adk_agent.telemetry")

async def before_agent_log(callback_context: CallbackContext) -> None:
    logger.info(f"Agent '{callback_context.agent_name}' execution started. Session ID: {callback_context.session.id}")

async def after_agent_log(callback_context: CallbackContext) -> None:
    logger.info(f"Agent '{callback_context.agent_name}' execution completed. Session ID: {callback_context.session.id}")

async def before_model_log(callback_context: CallbackContext, llm_request: LlmRequest) -> None:
    logger.info(f"Model call initiated. Model: {llm_request.model}. Prompt length: {len(str(llm_request.contents))}")
    callback_context.state["temp:model_start_time"] = str(time.time())

async def after_model_log(callback_context: CallbackContext, llm_response: LlmResponse) -> None:
    start_time_str = callback_context.state.get("temp:model_start_time")
    latency = time.time() - float(start_time_str) if start_time_str else 0.0
    
    # Safely get token counts
    prompt_tokens = "N/A"
    candidates_tokens = "N/A"
    if hasattr(llm_response, "usage_metadata") and llm_response.usage_metadata:
        prompt_tokens = getattr(llm_response.usage_metadata, "prompt_token_count", "N/A")
        candidates_tokens = getattr(llm_response.usage_metadata, "candidates_token_count", "N/A")
        
    logger.info(
        f"Model call completed. Latency: {latency:.2f}s. "
        f"Input tokens: {prompt_tokens}, Output tokens: {candidates_tokens}"
    )

async def before_tool_log(tool: BaseTool, args: dict, tool_context: ToolContext) -> None:
    logger.info(f"Tool '{tool.name}' started execution with args: {args}")
    tool_context.state["temp:tool_start_time"] = str(time.time())

async def after_tool_log(tool: BaseTool, args: dict, tool_context: ToolContext, tool_response: dict) -> None:
    start_time_str = tool_context.state.get("temp:tool_start_time")
    latency = time.time() - float(start_time_str) if start_time_str else 0.0
    logger.info(f"Tool '{tool.name}' completed in {latency:.2f}s. Result status: {tool_response.get('status', 'unknown')}")
