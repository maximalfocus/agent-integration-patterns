from rich.console import Console
from rich.table import Table
from src.agent import Agent
from src.tools_rpc import GithubSDK, get_rpc_tool_schema
from src.tools_rest import make_http_request, get_rest_tool_schema

console = Console()


def run_showdown():
    # --- The Challenge ---
    TARGET_REPO = "pandas-dev/pandas"
    TARGET_USER = "mroeschke"
    LIMIT = 3

    prompt = (
        f"Find the titles of the last {LIMIT} issues created by user '{TARGET_USER}' "
        f"in repo '{TARGET_REPO}'. Return just the titles."
    )

    console.print("[bold yellow]🥊 THE API WRAPPER SHOWDOWN 🥊[/bold yellow]")
    console.print(f"Task: {prompt}\n")

    # --- CONTENDER 1: RPC AGENT ---
    console.print("[bold green]=== Round 1: The RPC Native Agent ===[/bold green]")
    sdk = GithubSDK()
    rpc_agent = Agent(
        name="RPC Agent",
        model="gpt-4o-mini",
        tools_map={"get_issues_rpc": sdk.get_issues},
        tool_schemas=[get_rpc_tool_schema()],
    )
    # Fix 1: We don't need to store the variable if we don't use it
    rpc_agent.run(prompt)

    # --- CONTENDER 2: REST AGENT ---
    console.print("\n[bold red]=== Round 2: The Raw REST Agent ===[/bold red]")
    rest_agent = Agent(
        name="REST Agent",
        model="gpt-4o-mini",
        tools_map={"make_http_request": make_http_request},
        tool_schemas=[get_rest_tool_schema()],
    )
    # Fix 2: Discard variable
    rest_agent.run(prompt, max_steps=8)

    # --- THE VERDICT ---
    print_scoreboard(rpc_agent, rest_agent)


def print_scoreboard(agent_a, agent_b):
    table = Table(title="Showdown Results (Lower Tokens = Better)")

    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column(f"{agent_a.name} (RPC)", style="green")
    table.add_column(f"{agent_b.name} (REST)", style="red")

    # Determine status
    a_success = "✅ Success" if agent_a.steps_taken < 8 else "❌ Failed"
    b_success = "✅ Success" if agent_b.steps_taken < 8 else "❌ Failed/Struggle"

    # Fix 3: Actually add the Status row to the table!
    table.add_row("Outcome", a_success, b_success)
    table.add_row("Steps Taken", str(agent_a.steps_taken), str(agent_b.steps_taken))
    table.add_row("Total Tokens", str(agent_a.total_tokens), str(agent_b.total_tokens))

    # Calculate Ratio
    if agent_a.total_tokens > 0:
        ratio = agent_b.total_tokens / agent_a.total_tokens
        cost_diff = f"{ratio:.1f}x More Expensive"
    else:
        cost_diff = "N/A"

    table.add_row("Cost Comparison", "1x (Baseline)", cost_diff)

    console.print("\n")
    console.print(table)


if __name__ == "__main__":
    run_showdown()
