from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",   # ✅ CHANGE IS HERE
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)
print(llm.invoke("Say hello in one sentence.").content)