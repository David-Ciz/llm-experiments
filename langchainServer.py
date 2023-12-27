from dotenv import load_dotenv
# load from env file the api key
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from fastapi import FastAPI

load_dotenv()

chat_model = ChatOpenAI()

from langchain.prompts.chat import ChatPromptTemplate


class GptTranslator:
    def __init__(self):
        self.input_language = "english"
        self.output_language = "czech"

    def invoke_translation(self, text):
        template = f"You are a helpful assistant that translates {self.input_language} to {self.output_language}."
        human_template = "{text}"

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template),
        ])
        chain = chat_prompt | ChatOpenAI()
        response = chain.invoke({"text": f"{text}"})
        return response


gptTranslator = GptTranslator()
app = FastAPI()


@app.get("/get_input_language")
def get_input_language():
    return gptTranslator.input_language


@app.get("/get_output_language")
def get_input_language():
    return gptTranslator.output_language


@app.put("/change_input_language")
def translate(text: str):
    gptTranslator.input_language = text


@app.put("/change_output_language")
def translate(text: str):
    gptTranslator.output_language = text


@app.post("/translate")
def translate(text: str):
    response = gptTranslator.invoke_translation(text)
    return response
