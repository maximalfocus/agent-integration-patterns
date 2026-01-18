from rich.console import Console
from rich.theme import Theme

# Define a custom theme for our Agent
custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "tool": "bold green",  # For tool calls
        "agent": "bold blue",  # For agent thoughts
        "result": "magenta",  # For tool outputs
    }
)

# Create a global console instance
console = Console(theme=custom_theme)


def log_agent(message: str):
    """Log an agent's thought or action."""
    console.print(f"[agent]🤖 Agent:[/agent] {message}")


def log_tool(tool_name: str, params: str):
    """Log a tool execution."""
    console.print(f"[tool]🛠️  Calling Tool:[/tool] {tool_name}({params})")


def log_result(result: str):
    """Log a tool result (truncated if too long)."""
    clean_result = str(result)
    if len(clean_result) > 200:
        clean_result = clean_result[:200] + "... (truncated)"
    console.print(f"[result]📄 Result:[/result] {clean_result}")
