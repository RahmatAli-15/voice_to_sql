import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class LLMAgent:
    def __init__(self, model="llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model=model, api_key=api_key)

    def ask(self, prompt):
        return self.llm.invoke(prompt).content.strip()
