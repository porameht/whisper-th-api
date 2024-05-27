from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate

from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

class Command(BaseModel):
    command: str = Field(description="Action to perform, e.g., 'turn on', 'turn off'")
    room: str = Field(description="Room where the device is located")
    device: str = Field(description="Device to control, e.g., 'light'")
    time: str = Field(description="Time when action should be performed", default=None)

class FewShotLearning:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.llm_model = model_name
        self.chat = ChatOpenAI(temperature=0.0, model=self.llm_model)

    def few_shot_prompt(self, input):
        parser = JsonOutputParser(pydantic_object=Command)

        prompt = PromptTemplate(
            template="You are a smart home assistant and will answer to English user input. Follow examples if not understand Output None:\n\
                1. Input: เปิดไฟห้องนอนหน่อย\n\
                Output: 'command': 'turn on', 'room': 'bedroom', 'device': 'light'\n\
                2. Input: ปิดไฟโถงล่างตอนสามทุ่ม\n\
                Output: 'command': 'turn off', 'room': 'floor hall', 'device': 'light', 'time': '9:00 PM'\n\
                3. Input: เปิดไฟซีนเอ\n\
                Output: 'command': 'turn on', 'room': 'scene A', 'device': 'light'\n\
                4. Input: \n\
                Output: 'None'\n\
                {format_instructions}\n{input}\n",
            input_variables=["input"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.chat | parser

        try:
            res = chain.invoke({"input": input})
        except:
            res = None

        return res

