from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.schema import HumanMessage

load_dotenv()
llm = OpenAI()

text = "집에 가고 싶다. 퇴근하고 싶다."
context = "라는 일기에 대해 감정분석을 해줘"
messages = [HumanMessage(content=text+context)]

result = llm.invoke(text)
print(result)

