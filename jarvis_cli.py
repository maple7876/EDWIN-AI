from agent_controller import JarvisAgent

def boot_sequence():
    print("\n==============================")
    print("  J.A.R.V.I.S. SYSTEM ONLINE  ")
    print("==============================")
    print("Initializing core modules...")
    print("Memory systems: ACTIVE")
    print("Model router: ACTIVE")
    print("Interface: CLI MODE\n")


def main():
    jarvis = JarvisAgent()
    boot_sequence()

    while True:
        user_input = input("YOU > ")

        if user_input.lower() in ["exit", "quit"]:
            print("JARVIS > Shutting down.")
            break

        response = jarvis.process(user_input)
        print(f"JARVIS > {response}\n")


if __name__ == "__main__":
    main()
