import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# 1. Resolve project root and add to sys.path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent

if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# 2. Load .env file explicitly from backend/.env
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(f"GEMINI_API_KEY not found in .env file at {env_path}")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# 3. Import agent functions
from agents.application_agent import open_app, close_app, list_running_apps
from agents.file_agent import create_folder, create_file, list_files, search_files
from agents.terminal_agent import run_command
from agents.system_agent import get_system_stats, set_volume, set_brightness

# 4. Map tool names to execution functions
TOOL_MAP = {
    "open_app": open_app,
    "close_app": close_app,
    "list_running_apps": list_running_apps,
    "create_folder": create_folder,
    "create_file": create_file,
    "list_files": list_files,
    "search_files": search_files,
    "run_command": run_command,
    "get_system_stats": get_system_stats,
    "set_volume": set_volume,
    "set_brightness": set_brightness,
}

tools = [
    open_app, close_app, list_running_apps,
    create_folder, create_file, list_files, search_files,
    run_command, get_system_stats, set_volume, set_brightness
]

# 5. Initialize Gemini model (max_retries=1 avoids silent hanging)


# Initialize Gemini model with tools bound
# Initialize Gemini model with tools bound
# Initialize Gemini model with tools bound
# Initialize Gemini model with tools bound
# Initialize Gemini model with tools bound
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  # <--- Switch to the lite model to bypass 503 traffic spikes
    api_key=api_key,
    temperature=0,
    max_retries=1
).bind_tools(tools)
SYSTEM_PROMPT = """
You are DeskPilot, an AI Operating System Assistant capable of executing real tasks on the user's computer.
You have access to tools that can open/close applications, manipulate files and directories, run terminal commands, and control system volume, brightness, or stats.

Guidelines:
1. Always pick the appropriate tool based on user requests.
2. If multiple actions are requested in a single command, call the tools sequentially.
3. Be concise and helpful in your final response after tools have executed.
"""

def execute_user_query(query: str):
    """Processes a natural language query, calls tools, and returns final answer."""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query)
    ]

    print("⏳ Connecting to Gemini API...")
    
    # Retry loop for model invocation to handle 503 spikes gracefully
    max_retries = 3
    response = None
    
    for attempt in range(max_retries):
        try:
            response = llm.invoke(messages)
            break
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"⚠️ Google servers are busy (503). Retrying in 10 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(10)
            else:
                raise e

    if not response:
        raise Exception("Failed to connect to Gemini API after multiple 503 retries.")

    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            function_name = tool_call["name"]
            function_args = tool_call["args"]

            print(f"🤖 [Orchestrator] Calling Tool: {function_name} with args: {function_args}")

            if function_name in TOOL_MAP:
                result = TOOL_MAP[function_name](**function_args)
                messages.append(
                    ToolMessage(
                        content=json.dumps(result),
                        tool_call_id=tool_call["id"]
                    )
                )

        print("⏳ Synthesizing final response...")
        for attempt in range(max_retries):
            try:
                final_response = llm.invoke(messages)
                return final_response.content
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    print(f"⚠️ Server busy during synthesis. Retrying in 10s... ({attempt + 1}/{max_retries})")
                    time.sleep(10)
                else:
                    raise e
    
    return response.content
if __name__ == "__main__":
    test_query = "Set my volume to 80% and check my system stats."
    print(f"User: {test_query}\n")
    try:
        output = execute_user_query(test_query)
        print("\n----------------------------------------")
        print("🤖 DeskPilot Response:")
        print(output)
        print("----------------------------------------")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")