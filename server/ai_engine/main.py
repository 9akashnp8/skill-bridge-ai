import re
from decouple import config
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import BaseOutputParser

llm = OpenAI(openai_api_key=config("OPENAI_API_KEY"), model_name="gpt-4")


class QuestionOutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:  # "Q1: abc, Q2: def"
        questions = re.split(r"Q\d+:", text)  # ["abc", "def"]
        return [question.strip() for question in questions if question.strip()]


question_gen_template = """
You are an enthusiastic AI Agent who loves helping people. You
are tasked with generating (python) practice questions to help improve
ones knowledge.

Your Instructions:
1. Based on ONLY the "topic" and "info" provided below, generate good, real-world, scenario based
practice questions that test the users knowledge of respective "info"
2. Do not include answer in the prompt.
3. The Output/Questions must be in the numbered in the Q1:, Q2:, Q3: format.

An example question to be generated is provided below:
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
question_gen_prompt = PromptTemplate.from_template(question_gen_template)

question_gen_chain = question_gen_prompt | llm | QuestionOutputParser()

question_validate_template = """
You are an expert in analyzing similarity and making necessary changes.

Your Instructions:
1. Give a question or set of questions, you are tasked with enusuring that the given questions
are similar to the "Sample Question" provided
2. They must be similar in terms of being scenario based and being real-world problems.
3. If the questions are NOT similar, modify the question and return it. If
the questions are similar, simply return the original question.

Questions: {questions}

Sample Question Format: 
"Imagine you are developing a script to analyze server logs for a
monitoring application. Each log entry includes a timestamp, log level, and a detailed message.
Generate a function to extract the timestamp and log level while
excluding detailed module information to maintain brevity in your reports."
"""

question_validate_prompt = PromptTemplate.from_template(question_validate_template)

gen_validate_chain = {"questions": question_gen_chain} | question_validate_prompt | llm
