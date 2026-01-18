import json
from openai import OpenAI
from src.config import Config
from src.logger import log_agent, log_tool, log_result, console


class Agent:
    def __init__(self, name: str, model: str, tools_map: dict, tool_schemas: list):
        self.name = name
        self.model = model
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.tools_map = tools_map  # Maps "name" -> python_function
        self.tool_schemas = tool_schemas  # JSON schemas for OpenAI

        # Metrics
        self.total_tokens = 0
        self.steps_taken = 0

    def run(self, prompt: str, max_steps: int = 10):
        """
        Executes the agent loop.
        """
        console.rule(f"[bold]{self.name} (Model: {self.model})[/bold]")

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the provided tools to answer the user's request efficiently.",
            },
            {"role": "user", "content": prompt},
        ]

        self.steps_taken = 0
        self.total_tokens = 0

        while self.steps_taken < max_steps:
            self.steps_taken += 1

            # 1. Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tool_schemas,
                tool_choice="auto",
            )

            # Track cost
            if response.usage:
                self.total_tokens += response.usage.total_tokens

            msg = response.choices[0].message
            messages.append(msg)  # Add assistant message to history

            # 2. Check if Tool Call needed
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    args_str = tool_call.function.arguments

                    log_tool(func_name, args_str)

                    # Execute
                    if func_name in self.tools_map:
                        try:
                            args = json.loads(args_str)
                            # Call the actual Python function
                            result_data = self.tools_map[func_name](**args)
                            result_str = json.dumps(result_data)
                        except Exception as e:
                            result_str = json.dumps({"error": str(e)})
                    else:
                        result_str = "Error: Tool not found"

                    log_result(result_str)

                    # Add result to history
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result_str,
                        }
                    )
            else:
                # 3. Final Answer (No more tools needed)
                log_agent(msg.content)
                return msg.content

        log_agent("[bold red]Max steps reached! I gave up.[/bold red]")
        return "Failed to complete task."
