import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
import os
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv

from langchain_community.utilities import GoogleSerperAPIWrapper
from autogen_ext.tools.http import HttpTool

#load Environment Variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")
model_client = OpenAIChatCompletionClient(model='gpt-4o',api_key=api_key)

serper_key = os.getenv("SERPER_API_KEY")

# Validate
if not serper_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Use the keys
os.environ['SERPER_API_KEY'] = serper_key

search_tool_wrapper = GoogleSerperAPIWrapper(type='search')

def search_web(query:str) ->str:
    """Search the web for the given query and return the results."""
    try:
        results = search_tool_wrapper.run(query)
        return results
    except Exception as e:
        print(f"Error occured while searching the Web : {e}")
        return "No Result Found."

search_agent = AssistantAgent(
    name="SearchAgent",
    model_client=model_client,
    tools=[search_web],
    description="An agent that can search the web for information.",
    system_message="You are a helpful assistant that can search the web for information using the search_web tool." \
    "Please make sure that you use the search_web tool to find information before you return the answer.",
     reflect_on_tool_use=True
)

async def run_serper_search():
    """Run the search agent with a sample query."""
    query = "Who won the recently IPL in 2025 ?" 
    print(f"Querying: {query}")

    result = await search_agent.run(task=query)
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(run_serper_search())