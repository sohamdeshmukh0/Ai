from rag.splitter import Splitter
from rag.embedder import Embedder
from rag.generator import Generator
from rag.retriever import Retriever
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.documents import Document
from typing import List, Any
from dotenv import load_dotenv
import re
import time
import ast
import json
load_dotenv()


class Pipeline:
    def __init__(self):
        self.splitter = Splitter()
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.generator = Generator()
        self.memory = ConversationBufferMemory()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Here is the conversation so far:\n{chat_history}"),
            ("human", "{input}")
        ])

    def process_prompt(self, prompt_chunk: str):
        # Generate embeddings from the prompt text
        embeddings = self.embedder.generate_embeddings(prompt_chunk[0])
        context = self.retriever.retrieve(embeddings)
        response = self.generator.generate_questions(context)
        return response
        

    def process_documents(self, documents: str):
        chunks = self.splitter.chunks(documents)
        embeddings = self.embedder.generate_embeddings(chunks)
        self.retriever.insert_documents(chunks, embeddings)

    def chat(self, user_prompt: str):
        history = self.memory.load_memory_variables({}).get("history", "")
        formatted_prompt = self.prompt.format(history=history, input=user_prompt)
        response = self.generator.llm.invoke(formatted_prompt)
        self.memory.save_context({"input": user_prompt}, {"output": response.content})
        try:
        # Try converting string to dict assuming it's valid JSON
            return json.loads(response.content)
        except json.JSONDecodeError:
        # If not valid JSON, return raw text in a dict
            return {"response": "Kuch Nahi Mila"}

    def convert_response_to_dict(content: str) -> dict:
        try:
            # Try parsing as JSON first (if it's valid JSON with double quotes)
            return json.loads(content)
        except json.JSONDecodeError:
            try:
                # If JSON fails (usually due to single quotes), use ast.literal_eval
                return ast.literal_eval(content)
            except Exception as e:
                return {"error": "Failed to parse response content", "details": str(e)}

    def clean_double_encoded_json(response: dict) -> dict:
        raw_inner = response.get("questions", "")
        
        try:
            # First, clean up the inner string
            cleaned_str = raw_inner.replace("\\'", "'").replace("'", '"')  # fix quotes
            cleaned_str = cleaned_str.replace('\\"', '"')  # remove escaped quotes
            # Remove newline escape characters
            cleaned_str = cleaned_str.replace("\\n", "")
            # Parse it into JSON
            return json.loads(cleaned_str)
        except Exception as e:
            return {"error": "Failed to parse questions", "details": str(e)}


    def pretty_print_questions(self, raw_text: str):
        section_pattern = r"\*\*Section\s*\d+: ([^\*]+)\*\*\s*\n\n\{([^}]+)\}"
        question_pattern = r'"Q\d+":\s*"([^"]+)"'

        sections = re.findall(section_pattern, raw_text)
        if not sections:
            print(raw_text)
            return

        for section_title, questions_block in sections:
            print(f"\n=== {section_title.strip()} ===")
            questions = re.findall(question_pattern, questions_block)
            for i, q in enumerate(questions, 1):
                print(f"Q{i}: {q}")


if __name__ == "__main__":
    start_time = time.time()
    pipeline = Pipeline()
    print("Welcome to the LLM chat! Type 'exit' to quit.\n")
    
    # prompt = "Anything about PIM (Product Information Management) system, its features, benefits, and use cases."
    # print("Welcome to the LLM chat! Type 'exit' to quit.\n")
    # response = pipeline.process_prompt([prompt])
    # pipeline.pretty_print_questions(str(response.content))
    # while True:
    #     prompt = input("You: ")
    #     if prompt.strip().lower() in ["exit", "quit"]:
    #         print("Goodbye!")
    #         break
    #     response = pipeline.process_prompt([prompt])

    documents = open("oms.txt", "r", encoding="utf-8").read()
    pipeline.process_documents(documents)
    # pipeline.pretty_print_questions(str(response.content))
    # print({"response": response.content})
    end_time = time.time()
    print(f"Pipeline executed in {end_time - start_time:.2f} seconds.")
    print("Documents processed and inserted into the Collection.")
