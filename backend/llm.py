# # backend/llm.py

# import os
# import json
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# def generate_quiz(content: str) -> dict:
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY not found in environment")

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-flash-latest",
#         google_api_key=api_key,
#         temperature=0
#     )

#     prompt = f"""
# Return ONLY valid JSON.
# No markdown.
# No explanation.

# Format:
# {{
#   "quiz": [
#     {{
#       "question": "",
#       "options": ["", "", "", ""],
#       "answer": "",
#       "difficulty": "easy|medium|hard",
#       "explanation": ""
#     }}
#   ],
#   "related_topics": ["", "", ""]
# }}

# Content:
# {content[:4000]}
# """

#     response = llm.invoke(prompt)

#     # ✅ LANGCHAIN FIX (THIS IS THE KEY)
#     if isinstance(response.content, list):
#         text = response.content[0]["text"]
#     else:
#         text = response.content

#     try:
#         return json.loads(text)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Invalid JSON from LLM:\n{text}") from e




# import os
# import json
# import re
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# def generate_quiz(content: str) -> dict:
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY not found")

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-flash-latest",
#         google_api_key=api_key,
#         temperature=0
#     )

#     prompt = f"""
# Return ONLY valid JSON.
# No markdown.
# No explanation.
# No text outside JSON.

# Format:
# {{
#   "quiz": [
#     {{
#       "question": "",
#       "options": ["", "", "", ""],
#       "answer": "",
#       "difficulty": "easy|medium|hard",
#       "explanation": ""
#     }}
#   ],
#   "related_topics": ["", "", ""]
# }}

# Content:
# {content[:4000]}
# """

#     response = llm.invoke(prompt)

#     # Normalize LangChain output
#     text = response.content
#     if isinstance(text, list):
#         text = "".join(str(x) for x in text)

#     # 🔑 CRITICAL FIX: extract JSON block safely
#     match = re.search(r"\{[\s\S]*\}", text)
#     if not match:
#         raise ValueError("LLM response does not contain JSON")

#     json_text = match.group()

#     try:
#         return json.loads(json_text)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Invalid JSON returned from LLM: {e}")






# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# def generate_quiz(content: str) -> dict:
#     """
#     Use your existing LLM integration. This function MUST return a dict with keys:
#       - "quiz": list of question dicts
#       - "related_topics": list
#     Keep signature generate_quiz(content) to match your main.py.
#     """
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY not found in environment (.env)")

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-flash-latest",
#         google_api_key=api_key,
#         temperature=0,
#         response_mime_type="application/json"
#     )

#     prompt = f"""
# Return JSON only.

# Format:
# {{ "quiz": [{{ "question": "", "options": ["","","",""], "answer": "", "difficulty": "", "explanation": "" }}], "related_topics": ["", ""] }}

# Content:
# {content[:4000]}
# """

#     response = llm.invoke(prompt)
#     data = response.content

#     # normalize shapes LangChain/Gemini may return
#     if isinstance(data, dict):
#         return data

#     if isinstance(data, list):
#         # find a dict that holds json
#         for item in data:
#             if isinstance(item, dict) and "json" in item and isinstance(item["json"], dict):
#                 return item["json"]
#             if isinstance(item, dict) and "text" in item:
#                 # fallback: attempt to parse text block if present
#                 import json, re
#                 text = item["text"]
#                 m = re.search(r"\{[\s\S]*\}", text)
#                 if m:
#                     try:
#                         return json.loads(m.group())
#                     except Exception:
#                         pass
#     raise ValueError("Invalid JSON returned from LLM")





# # backend/llm.py
# import os
# import json
# import re
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# def _extract_json_from_text(text: str) -> dict:
#     """Try to safely extract JSON object from text."""
#     # find first {...} block
#     m = re.search(r"\{[\s\S]*\}", text)
#     if not m:
#         raise ValueError("LLM response does not contain a JSON object")

#     json_text = m.group()
#     # try normal json
#     try:
#         return json.loads(json_text)
#     except json.JSONDecodeError:
#         # try convert single quotes to double quotes as last resort
#         try:
#             return json.loads(json_text.replace("'", '"'))
#         except Exception as e:
#             raise ValueError(f"Invalid JSON returned from LLM: {e}")

# def generate_quiz(content: str) -> dict:
#     """
#     Return dict with keys:
#       - "quiz": list of question dicts
#       - "related_topics": list
#     """
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY not found in environment (.env)")

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-flash-latest",
#         google_api_key=api_key,
#         temperature=0
#         # you can add response_mime_type="application/json" if needed
#     )

#     prompt = f"""
# Return JSON only.

# Format:
# {{ "quiz": [{{ "question": "", "options": ["","","",""], "answer": "", "difficulty": "", "explanation": "" }}], "related_topics": ["", ""] }}

# Content:
# {content[:4000]}
# """

#     response = llm.invoke(prompt)
#     data = response.content

#     # 1) If already a dict, return it
#     if isinstance(data, dict):
#         return data

#     # 2) If list, try to find a text block or embedded json
#     if isinstance(data, list):
#         for item in data:
#             if isinstance(item, dict) and "json" in item and isinstance(item["json"], dict):
#                 return item["json"]
#             if isinstance(item, dict) and "text" in item and isinstance(item["text"], str):
#                 try:
#                     return _extract_json_from_text(item["text"])
#                 except ValueError:
#                     continue
#             if isinstance(item, str):
#                 # item might be string chunks
#                 try:
#                     return _extract_json_from_text(item)
#                 except ValueError:
#                     continue

#     # 3) If string (rare), try extract
#     if isinstance(data, str):
#         return _extract_json_from_text(data)

#     raise ValueError("Invalid JSON returned from LLM")


# backend/llm.py
import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def _extract_json_from_text(text: str):
    """Find first {...} JSON block and parse it."""
    if not isinstance(text, str):
        raise ValueError("Text to parse is not a string")
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        raise ValueError("LLM response does not contain a JSON object")
    json_text = m.group()
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # fallback: try replace single-quotes with double quotes
        try:
            return json.loads(json_text.replace("'", '"'))
        except Exception as e:
            raise ValueError(f"Invalid JSON returned from LLM: {e}")

def generate_quiz(content: str, min_questions: int = 8) -> dict:
    """
    Send prompt to Gemini (via langchain-google-genai).
    Returns dict with keys:
      - quiz: list of question dicts
      - related_topics: list of strings
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment (.env)")

    # Use a tested model available on your account. gemini-flash-latest is common.
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=api_key,
        temperature=0,
        # response_mime_type="application/json"  # optional
    )

    prompt = f"""
You are a strict JSON generator that creates quiz questions grounded only in the provided content.

Return ONLY valid JSON and NOTHING else.

Format required exactly:

{{
  "quiz": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer": "string",            # exact option text that is correct
      "difficulty": "easy|medium|hard",
      "explanation": "short explanation (1-2 sentences)"
    }}
  ],
  "related_topics": ["topic1", "topic2", "topic3"]
}}

Task:
- Generate at least {min_questions} questions strictly based on the CONTENT below.
- Each question must have 4 options.
- Do not invent facts outside the content.
- No numbering, no markdown, no commentary — JSON only.

CONTENT:
{content[:8000]}
"""

    response = llm.invoke(prompt)
    data = response.content

    # Normalize different shapes returned by the client
    # If it's dict already -> good
    if isinstance(data, dict):
        return data

    # If list, try to find json text or dict inside
    if isinstance(data, list):
        # maybe list of chunks or dicts
        for item in data:
            if isinstance(item, dict):
                # some clients embed a "json" key
                if "json" in item and isinstance(item["json"], dict):
                    return item["json"]
                # or item contains 'text'
                if "text" in item and isinstance(item["text"], str):
                    try:
                        return _extract_json_from_text(item["text"])
                    except Exception:
                        continue
            if isinstance(item, str):
                try:
                    return _extract_json_from_text(item)
                except Exception:
                    continue

    # If string, try to extract JSON block
    if isinstance(data, str):
        return _extract_json_from_text(data)

    # nothing worked
    raise ValueError("Invalid JSON returned from LLM")
