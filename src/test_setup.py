from src.config import Config
from src.logger import log_agent, log_tool


def test():
    print(
        f"Keys loaded! OpenAI: {Config.OPENAI_API_KEY[:5]}... GitHub: {Config.GITHUB_TOKEN[:5]}..."
    )
    log_agent("I am ready to work.")
    log_tool("test_tool", "arg=1")


if __name__ == "__main__":
    test()
