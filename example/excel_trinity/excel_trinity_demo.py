import os, sys
curr_path = os.path.abspath(os.path.dirname(__file__))
parent_parent_path = os.path.dirname(os.path.dirname(curr_path))
sys.path.append(parent_parent_path)
from trinity.trinity import Trinity
from textwrap import dedent
from agno.tools.mcp import MCPTools
from agno.models.deepseek import DeepSeek
from agno.agent import Agent, RunResponse

mcp_tools = MCPTools(
        command=f"npx --yes @negokaz/excel-mcp-server",
        env={"EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"}
    )

excel_path = os.path.join(curr_path, "score.xlsx")
excel_trinity = Trinity(
    model=DeepSeek(id="deepseek-chat"),
    name="excel_trinity",
    description="A trinity for handling Excel files.",
    mcp_tools=mcp_tools,
    instructions=dedent("""\
        You are an Excel operation assistant:
        - If the user needs to read Excel information, extract relevant data from the Excel file and present organized results;
        - If the user requires modifications or additions, implement the requested changes to the Excel sheet;
        - If a value is modified, check and update any affected fields as it may impact other fields.
        - After making modifications or additions, provide a before-and-after comparison of the altered or newly added entries.\
    """) + f"\n\nCurrent Excel file path: {excel_path}"
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

                response:RunResponse = await excel_trinity.arun(message=message)
                if response.content:
                    console.print(Markdown(response.content.message))
            except Exception as e:
                print(f"An error occurred: {e}")
    
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")