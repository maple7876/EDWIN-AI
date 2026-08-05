from system.model_selector import get_selected_model
from system.paths import memory_dir
from tool_registry import TOOLS
import requests
import chromadb
from datetime import datetime
import hashlib

# -----------------------------
# MEMORY SETUP (ChromaDB)
# -----------------------------
client = chromadb.PersistentClient(path=str(memory_dir()))

collection = client.get_or_create_collection("jarvis_memory")


def make_id(text):
    return hashlib.sha256(text.encode()).hexdigest()


def add_memory(text, mtype="fact", importance=3):
    collection.add(
        documents=[text],
        metadatas=[{
            "type": mtype,
            "importance": importance,
            "timestamp": str(datetime.now())
        }],
        ids=[make_id(text)]
    )


def get_memory(query, k=3):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )

    docs = results.get("documents", [[]])[0]
    return "\n".join(docs)


# -----------------------------
# MODEL ROUTER (FAST vs SMART)
# -----------------------------


# -----------------------------
# OLLAMA LLM CALL
# -----------------------------
def choose_num_predict(user_input):

    text = user_input.lower()

    # Simple requests
    if len(text.split()) < 10:
        return 60

    # Medium requests
    if len(text.split()) < 25:
        return 120

    # Complex requests
    return 250
def ollama_llm(prompt, model=None):
    if model is None:
        model = get_selected_model()

    print("MODEL BEING USED:", model)
    print("THINKING DISABLED: True")

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0.6,
                    "num_predict": choose_num_predict(prompt),
                },
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        print("OLLAMA RESPONSE KEYS:", data.keys())

        return data.get("response", "").strip()

    except Exception as e:
        return f"[OLLAMA ERROR]: {str(e)}"


# -----------------------------
# MEMORY AUTO STORAGE
# -----------------------------
def auto_add_memory(user_input, assistant_output):

    combined = user_input

    keywords = [
        "i am",
        "i'm",
        "my",
        "project",
        "friend",
        "building",
        "goal",
        "plan"
    ]

    if any(k in user_input.lower() for k in keywords):
        add_memory(combined, mtype="chat", importance=4)


# -----------------------------
# MAIN AGENT LOOP
# -----------------------------
def check_tools(user_input):

    text = user_input.lower()

    # direct keyword fallback
    for keyword, tool_data in TOOLS.items():

        if keyword in text:
            return tool_data["function"]()

    # lightweight intent understanding
    if "video" in text or "watch" in text:
        return TOOLS["youtube"]["function"]()

    if "search" in text or "browser" in text:
        return TOOLS["google"]["function"]()

    if "clock" in text or "current time" in text:
        return TOOLS["time"]["function"]()

    return None
def chat_with_memory(user_input):

    context = get_memory(user_input)

    tool_result = check_tools(user_input)

    if tool_result:
        return tool_result

    print("\n[DEBUG]")
    print("MEMORY:", context)
    print()

    prompt = f"""
You are EDWIN, an advanced personal AI assistant.

Your name is EDWIN.

You are not a fictional character and are not associated with Marvel, Stark Industries, or any existing AI assistant.

You assist with research, coding, planning, organization, and problem solving.

Address the user as Sir.

Keep responses concise and professional.

You are concise, intelligent, calm, and direct.

Rules:
- Keep answers short by default.
- Avoid customer-service style phrasing.
- Speak operationally and directly.
- Always respond in English.
- Stop speaking once the question is answered.
- Do not continue conversations unnecessarily.
- Never give long lists unless asked.
- Never act overly enthusiastic.
- Answer naturally like a real intelligent assistant.
- Use memory only if directly relevant.
- Do not over-explain.
- Keep responses efficient and sharp.
- Do not assume extra context unless explicitly stated.
- If memory is empty or uncertain, say you do not know instead of guessing.

MEMORY:
{context}

USER:
{user_input}

EDWIN:
"""

    response = ollama_llm(prompt)

    auto_add_memory(user_input, response)

    return response
