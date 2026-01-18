from src.tools_rpc import GithubSDK, get_rpc_tool_schema
from src.agent import Agent


def test_agent_loop():
    # 1. Setup Tools
    sdk = GithubSDK()

    # Map the string name "get_issues_rpc" to the actual method `sdk.get_issues`
    tools_map = {"get_issues_rpc": sdk.get_issues}
    schemas = [get_rpc_tool_schema()]

    # 2. Initialize Agent
    # We use gpt-4o-mini to prove the "Nano" concept
    agent = Agent(
        name="Test RPC Agent",
        model="gpt-4o-mini",
        tools_map=tools_map,
        tool_schemas=schemas,
    )

    # 3. Run
    print("Starting Agent Test...")
    agent.run("Get the last 5 open issues from repo 'pandas-dev/pandas'.")

    print("\n--- Metrics ---")
    print(f"Steps: {agent.steps_taken}")
    print(f"Tokens: {agent.total_tokens}")


if __name__ == "__main__":
    test_agent_loop()
