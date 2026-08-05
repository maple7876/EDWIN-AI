interface ChatInputProps {
  input: string;
  loading: boolean;
  setInput: (value: string) => void;
  sendMessage: () => void;
}

function ChatInput({
  input,
  loading,
  setInput,
  sendMessage,
}: ChatInputProps) {
  return (
    <footer className="input-area">
      <input
        value={input}
        placeholder="Message EDWIN..."
        onChange={(event) => setInput(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
          }
        }}
        disabled={loading}
      />

      <button
        onClick={sendMessage}
        disabled={loading || !input.trim()}
      >
        {loading ? "..." : "Send"}
      </button>
    </footer>
  );
}

export default ChatInput;