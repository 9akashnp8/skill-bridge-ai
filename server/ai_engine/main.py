from decouple import config
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser

llm = OpenAI(openai_api_key=config("OPENAI_API_KEY"))

prompt_template = """
You are an enthusiastic AI Agent who loves helping people. You
are tasked with generating (python) practice questions to help improve
ones knowledge.

Based on solely the info provided below, generate good, real-world practice
questions. The goal of these questions are to improve one knowledge
on the topic.

{info}
"""
prompt = PromptTemplate.from_template(prompt_template)
prompt.format(info="THIS IS SOME INFO ABOUT SOMETHING")

class CommaSeparatedListOutputParser(BaseOutputParser):

    def parse(self, text: str):
        return text.strip().split(", ")

chain = prompt | llm | CommaSeparatedListOutputParser()
