from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools import search_tool,save_tool

load_dotenv()  # reads your .env file (needs GEMINI_API_KEY)


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash") 

agent = create_agent(
    model=llm,
    tools=[search_tool],
    system_prompt=(
         "You are a research assistant that helps generate a research paper. "
        "Answer the user's query and use the tools when needed. "
        "Write the summary in plain text only. Do not use markdown symbols "
        "such as #, **, *, or ---."
    ),
    response_format=ResearchResponse,
)

def research(query):
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["structured_response"]


if __name__ == "__main__":
    query = input("What can I help you research? ")
    print(research(query))