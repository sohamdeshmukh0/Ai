from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


class Generator:
    def __init__(self, model_name="llama3-8b-8192"):
        self.llm = ChatGroq(model_name=model_name)

    def generate_questions(self, context):
        prompt = PromptTemplate(
            input_variables=["context"],
            template = (
            "Based on the context below:\n\n"
            "{context}\n\n"
            "Generate a JSON object grouped by relevant sections.\n"
            "Each section should contain key-value pairs where:\n"
            "- Keys are meaningful questions.\n"
            "- Values are empty strings (\"\").\n\n"
            "Format the response exactly like this:\n"
            "{{\n"
            "  \"Section\": {{\n"
            "    \"Question 1\": \"\",\n"
            "    \"Question 2\": \"\"\n"
            "  }}\n"
            "}}\n\n"
            "Only return valid JSON. No markdown, no explanation, no escape characters."
            )
    )

        chain = prompt | self.llm
        response = chain.invoke({"context": context})
        return response
    


if __name__ == "__main__":
    load_dotenv()
    generator = Generator()
    context = open("content.txt", "r", encoding="utf-8").read()
    questions = generator.generate_questions(context)
    print(questions)