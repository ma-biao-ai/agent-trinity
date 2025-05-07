import os, sys
curr_path = os.path.abspath(os.path.dirname(__file__))
parent_parent_path = os.path.dirname(os.path.dirname(curr_path))
sys.path.append(parent_parent_path)
from trinity.trinity import Trinity
from textwrap import dedent
from agno.tools.mcp import MCPTools
from agno.models.deepseek import DeepSeek
from agno.agent import Agent, RunResponse

history_trinity = Trinity(
    model=DeepSeek(id="deepseek-chat"),
    name="history_trinity",
    description="A trinity for history introduction.",
    instructions=dedent("""\
        You are a historical Q&A assistant:
        -Answer users' history-related questions concisely and logically;
        -Only consider well-documented official historical records;
        -Clearly state "unknown" or "undetermined" for unverifiable historical queries with no reliable sources;
        -Organize historical information chronologically.\
    """)
)

if __name__ == "__main__":
    from rich.console import Console
    from rich.markdown import Markdown
    async def main():
        console = Console()
        while True:
            try:
                message = input("Enter your question: ")
                if message.lower() in ["exit", "quit"]:
                    break

                response:RunResponse = history_trinity.run(message=message)
                if response.content:
                    console.print(Markdown(response.content.message))
            except Exception as e:
                print(f"An error occurred: {e}")
    
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")