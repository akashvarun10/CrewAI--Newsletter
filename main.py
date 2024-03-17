from crewai import Crew, Process

from agents import AINewsLetterAgents
from tasks import AINewsLetterTasks
from langchain_openai import ChatOpenAI
from file_io import save_markdown

import os 
from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI GPT-3 language model
OpenAIGPT = ChatOpenAI(
    model="gpt-3.5-turbo",
)

agents = AINewsLetterAgents()
tasks = AINewsLetterTasks()

# Setting up agents
editor = agents.editor_agent()
news_fetcher = agents.news_fetcher_agent()
news_analyzer = agents.news_analyzer_agent()
newsletter_compiler = agents.newsletter_compiler_agent()

#setting up tasks
fetch_news_task = tasks.fetch_news_task(news_fetcher)
analyzed_news_task = tasks.analyze_news_task(news_analyzer, [fetch_news_task])
compiled_newsletter_task = tasks.compile_newsletter_task(
    newsletter_compiler, [analyzed_news_task], save_markdown)

#setting up tools

crew = Crew(
    agents=[editor, news_fetcher, news_analyzer, newsletter_compiler],
    tasks=[fetch_news_task, analyzed_news_task, compiled_newsletter_task] ,
    process= Process.hierarchical,
    manager_llm=OpenAIGPT
)

results = crew.kickoff()

print("Crew has finished the task!")
print(results)
