import os
import time
import re
from pathlib import Path

from dotenv import load_dotenv

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

from langchain_google_genai import ChatGoogleGenerativeAI

from agents.application_agent import (
    open_app,
    close_app,
    list_running_apps
)

from agents.file_agent import (
    create_folder,
    create_file,
    list_files,
    search_files
)

from agents.terminal_agent import run_command

from agents.system_agent import (
    get_system_stats,
    set_volume,
    set_brightness
)

from agents.web_agent import web_research


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

current_dir = Path(__file__).resolve().parent
backend_root = current_dir.parent

env_path = backend_root / ".env"

load_dotenv(env_path)

api_key = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)

if not api_key:
    raise ValueError(
        "Gemini API key not found. "
        "Please add GEMINI_API_KEY to backend/.env"
    )


# =========================================================
# TOOL MAP
# =========================================================

TOOL_MAP = {

    "open_app": open_app,
    "close_app": close_app,
    "list_running_apps": list_running_apps,

    "create_folder": create_folder,
    "create_file": create_file,
    "list_files": list_files,
    "search_files": search_files,

    "web_research": web_research,

    "run_command": run_command,

    "get_system_stats": get_system_stats,
    "set_volume": set_volume,
    "set_brightness": set_brightness,
}


tools = list(TOOL_MAP.values())


# =========================================================
# GEMINI
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=api_key,
    temperature=0,
    max_retries=1
).bind_tools(tools)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are DeskPilot, an AI Operating System Assistant.

Your job is to understand natural-language commands and execute
real actions on the user's Windows computer.

IMPORTANT RULES:

1. ALWAYS use the appropriate tool when the user asks you to
   perform an action.

2. Do NOT simply describe what should be done.

3. For creating folders, use create_folder.

4. For creating files, use create_file.

5. For listing files/folders, use list_files.

6. For searching local files, use search_files.

7. For researching information from the internet, use web_research.

8. For opening applications, use open_app.

9. For closing applications, use close_app.

10. For system information, use get_system_stats.

11. For volume changes, use set_volume.

12. For brightness changes, use set_brightness.

13. Use run_command only when a dedicated tool cannot perform
    the requested task.

14. If the user's command contains multiple actions, perform
    ALL required actions.

15. Continue using tools until the complete request is finished.

16. IMPORTANT WINDOWS PATH RULE:
    Never invent paths such as C:\\Study or C:\\Desktop.

17. When the user says "my Desktop", "on Desktop", or
    "inside the Desktop", use the real Windows Desktop location.

18. When the user says "inside the Study folder" and Study is
    a folder on the Desktop, use:
    Desktop/Study

19. For files inside Study, use paths such as:
    Study/DBMS.txt

20. If the user asks to research information and save it to
    a file, research the information first and then create
    the file containing the researched content.

21. When creating study material, make the content clear,
    structured, concise and useful for exams and placements.

22. Do not stop after completing only one part of a
    multi-step request.

23. After all actions are complete, give a concise final response.

You are an action-oriented desktop assistant.
"""


# =========================================================
# TOOL EXECUTION
# =========================================================

def execute_tool(tool_call):

    tool_name = tool_call["name"]

    tool_args = tool_call.get(
        "args",
        {}
    )

    if tool_name not in TOOL_MAP:

        return {
            "status": "error",
            "message": f"Unknown tool: {tool_name}"
        }

    tool_function = TOOL_MAP[tool_name]

    try:

        result = tool_function(
            **tool_args
        )

        return result

    except Exception as e:

        return {
            "status": "error",
            "message": (
                f"Tool execution failed: {str(e)}"
            )
        }


# =========================================================
# FAST COMMAND DETECTION
# =========================================================

def get_fast_command(query: str):
    """
    Detect simple commands that do not need Gemini.

    This makes common desktop operations much faster.

    Examples:

        Open Calculator
        Open Chrome
        Open Notepad
        Close Calculator
        Close Chrome
    """

    if not query:
        return None

    text = query.lower().strip()

    # Remove common polite words
    text = re.sub(
        r"^(please\s+|can you\s+|could you\s+)",
        "",
        text
    ).strip()

    # -----------------------------------------------------
    # OPEN COMMAND
    # -----------------------------------------------------

    open_match = re.match(
        r"^(open|launch|start)\s+(.+?)\s*[.!?]*$",
        text
    )

    if open_match:

        app_name = open_match.group(2).strip()

        # Remove common endings
        app_name = re.sub(
            r"\s+(application|app)$",
            "",
            app_name
        ).strip()

        # Only use fast path for known applications
        known_apps = {
            "calculator",
            "calc",
            "notepad",
            "paint",
            "mspaint",
            "chrome",
            "google chrome",
            "edge",
            "microsoft edge",
            "msedge",
            "firefox",
            "brave",
            "brave browser",
            "vscode",
            "vs code",
            "visual studio code",
            "code",
            "spotify",
            "whatsapp",
            "discord",
            "cmd",
            "command prompt",
            "powershell",
            "file explorer",
            "explorer",
            "settings",
            "task manager",
            "taskmanager",
            "control panel",
            "controlpanel",
        }

        if app_name in known_apps:

            return {
                "action": "open",
                "name": app_name
            }

    # -----------------------------------------------------
    # CLOSE COMMAND
    # -----------------------------------------------------

    close_match = re.match(
        r"^(close|exit|quit|stop)\s+(.+?)\s*[.!?]*$",
        text
    )

    if close_match:

        app_name = close_match.group(2).strip()

        app_name = re.sub(
            r"\s+(application|app)$",
            "",
            app_name
        ).strip()

        known_apps = {
            "calculator",
            "calc",
            "notepad",
            "paint",
            "mspaint",
            "chrome",
            "google chrome",
            "edge",
            "microsoft edge",
            "msedge",
            "firefox",
            "brave",
            "brave browser",
            "vscode",
            "vs code",
            "visual studio code",
            "code",
            "spotify",
            "whatsapp",
            "discord",
            "cmd",
            "command prompt",
            "powershell",
        }

        if app_name in known_apps:

            return {
                "action": "close",
                "name": app_name
            }

    return None


# =========================================================
# FAST COMMAND EXECUTION
# =========================================================

def execute_fast_command(query: str):
    """
    Execute simple application commands directly.

    Gemini is completely skipped.
    """

    command = get_fast_command(query)

    if command is None:
        return None

    print()
    print("=" * 60)
    print("DESKPILOT FAST COMMAND")
    print("=" * 60)

    print("User command:")
    print(query)

    print("Action:")
    print(command)

    start_time = time.time()

    try:

        # -------------------------------------------------
        # OPEN
        # -------------------------------------------------

        if command["action"] == "open":

            result = open_app(
                command["name"]
            )

        # -------------------------------------------------
        # CLOSE
        # -------------------------------------------------

        elif command["action"] == "close":

            result = close_app(
                command["name"]
            )

        else:

            return None

        elapsed = time.time() - start_time

        print(
            f"Fast command completed in "
            f"{elapsed:.2f} seconds"
        )

        print("Result:")
        print(result)

        if result.get("status") == "success":

            return result.get(
                "message",
                "Task completed successfully."
            )

        elif result.get("status") == "warning":

            return result.get(
                "message",
                "No matching application was found."
            )

        else:

            return result.get(
                "message",
                "The requested action failed."
            )

    except Exception as e:

        print(
            "Fast command error:",
            str(e)
        )

        return (
            f"Could not complete the command: {str(e)}"
        )


# =========================================================
# MAIN ORCHESTRATOR
# =========================================================

def execute_user_query(query: str):

    print()
    print("=" * 60)
    print("DESKPILOT COMMAND")
    print("=" * 60)

    print("User:")
    print(query)

    # =====================================================
    # FAST PATH
    # =====================================================

    fast_result = execute_fast_command(
        query
    )

    if fast_result is not None:

        print()
        print("FAST PATH USED")
        print("=" * 60)

        return fast_result

    # =====================================================
    # GEMINI PATH
    # =====================================================

    print()
    print("Using Gemini orchestrator...")
    print("=" * 60)

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        ),
        HumanMessage(
            content=query
        )
    ]

    max_iterations = 8

    for iteration in range(
        max_iterations
    ):

        print()
        print("=" * 60)
        print(
            f"DESKPILOT ITERATION "
            f"{iteration + 1}"
        )
        print("=" * 60)

        try:

            response = llm.invoke(
                messages
            )

        except Exception as e:

            error_text = str(e)

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                print(
                    "Gemini temporarily unavailable."
                )

                print(
                    "Retrying..."
                )

                time.sleep(2)

                try:

                    response = llm.invoke(
                        messages
                    )

                except Exception as retry_error:

                    return (
                        "Gemini error: "
                        f"{str(retry_error)}"
                    )

            else:

                return (
                    "Gemini error: "
                    f"{error_text}"
                )

        print(
            "Gemini response:"
        )

        print(response)

        # -------------------------------------------------
        # ADD GEMINI RESPONSE
        # -------------------------------------------------

        messages.append(
            response
        )

        # -------------------------------------------------
        # NO MORE TOOLS
        # -------------------------------------------------

        if not response.tool_calls:

            print(
                "No more tools required."
            )

            content = response.content

            if isinstance(
                content,
                list
            ):

                text_parts = []

                for item in content:

                    if (
                        isinstance(item, dict)
                        and "text" in item
                    ):

                        text_parts.append(
                            item["text"]
                        )

                    elif isinstance(
                        item,
                        str
                    ):

                        text_parts.append(
                            item
                        )

                return "\n".join(
                    text_parts
                )

            return str(content)

        # -------------------------------------------------
        # EXECUTE ALL TOOLS
        # -------------------------------------------------

        print(
            f"Tool calls found: "
            f"{len(response.tool_calls)}"
        )

        for tool_call in response.tool_calls:

            print()
            print(
                "Executing tool:"
            )

            print(
                tool_call["name"]
            )

            print(
                "Arguments:"
            )

            print(
                tool_call.get(
                    "args",
                    {}
                )
            )

            result = execute_tool(
                tool_call
            )

            print(
                "Tool result:"
            )

            print(result)

            # -------------------------------------------------
            # SEND RESULT BACK TO GEMINI
            # -------------------------------------------------

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

    return (
        "I could not complete "
        "all requested actions."
    )