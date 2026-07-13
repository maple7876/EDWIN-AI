from memory_bridge import chat_with_memory, add_memory
from datetime import datetime

print("🧠 K.A.R.E.N. Activated")
print("Type 'exit' to stop\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "stop"]:
        print("K.A.R.E.N.: Shutting down live mode.")
        break

    print("\nKAREN: ", end="", flush=True)

    response = chat_with_memory(user_input)

    print("\n")

    # optional: log interaction separately
    add_memory(
        f"User: {user_input}\nAssistant: {response}",
        mtype="live_chat",
        importance=3
    )
