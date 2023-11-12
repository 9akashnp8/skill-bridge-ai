from decouple import config
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser

llm = OpenAI(openai_api_key=config("OPENAI_API_KEY"))

prompt_template = """
You are an enthusiastic AI Agent who loves helping people. You
are tasked with generating (python) practice questions to help improve
ones knowledge.

Based on ONLY the "topic" and "info" provided below, generate good, real-world, scenario based
practice questions. The goal of these questions are to improve one knowledge
on the topic.

An example question:
"Imagine you are developing a script to analyze server logs for a
monitoring application. Each log entry includes a timestamp, log level, and a detailed message.
However, you are specifically interested in extracting the timestamp and log level while
excluding detailed module information to maintain brevity in your reports.

Sample log: "2023-11-12 15:30:45 | ERROR | Critical issue occurred in ModuleX: Connection timeout"

Create a function, extract_log_summary(log_entry, n), where log_entry is a string log entry,
and n is a positive integer representing the number of characters to exclude from the end of the log entry."

topic: {topic}
info: {info}
"""
prompt = PromptTemplate.from_template(prompt_template)


class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split(", ")


chain = prompt | llm
