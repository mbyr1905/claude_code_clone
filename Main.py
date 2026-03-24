
import asyncio
import sys
from typing import Any
import click
from agents.agent import Agent
from agents.events import AgentEventType
from ui.tui import TUI, get_console

console = get_console()

class CLI:
    def __init__(self):
        self.agent: Agent | None=None
        self.tui = TUI(console)
    
    async def _process_message(self, messages:str)->str|None:
        if not self.agent:
            raise None
        
        assistant_streeming = False
        final_res: str|None = None
        
        async for event in self.agent.run(messages):
            if event.type == AgentEventType.TEXT_DELTA:
                content = event.data.get("content", "")
                if not assistant_streeming:
                    self.tui.begin_assistant()
                    assistant_streeming = True
                self.tui.stream_assistant_delta(content)
            elif event.type == AgentEventType.TEXT_COMPLETE:
                final_res = event.data.get("content", "")
                if assistant_streeming:
                    self.tui.end_assistant()
                    assistant_streeming = False
            elif event.type == AgentEventType.AGENT_ERROR:
                error = event.data.get("error", "Unknown error")
                console.print(f"\n[error] Error: {error}[/error]")
        return final_res 
    
    async def run_single(self, messages:str)->str|None:
        async with Agent() as agent:
            self.agent = agent
            await self._process_message(messages)

async def run(messages:dict[str, Any]):
    pass
        
@click.command()
@click.argument("prompt", required=False)
def main(prompt:str|None):
    cli = CLI()
    # messages = [
    #     {
    #         "role": "user",
    #         "content": prompt or "Hello, how are you?"
    #     }
    # ]
    if prompt:
        res = asyncio.run(cli.run_single(prompt))
        if res is None:
            sys.exit(1)
main()