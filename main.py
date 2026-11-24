from agent import Agent
from tools import TOOL_SCHEMAS, TOOL_REGISTRY


def main():
    agent = Agent(
        model="qwen2.5:3b",
        system="You are a helpful assistant that can answer questions using the provided tools.",
        tools=TOOL_SCHEMAS,
        tool_registry=TOOL_REGISTRY,
    )

    print("Agent initialized with qwen2.5:7b. Type 'exit' or 'quit' to stop.\n")

    # Example single query test
    sample_query = "What is the weather in San Francisco today?"
    print(f"User: {sample_query}")
    response = agent(sample_query)
    print(f"Agent: {response}\n")

    # Interactive loop
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        reply = agent(user_input)
        print(f"Agent: {reply}\n")


if __name__ == "__main__":
    main()