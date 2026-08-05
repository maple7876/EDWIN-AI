import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import type { Message } from "../types/chat";


interface ChatMessageProps {
  message: Message;
}


function ChatMessage({ message }: ChatMessageProps) {

  return (
    <div className={`message ${message.role}`}>

      <strong>
        {message.role === "user" ? "You" : "EDWIN"}
      </strong>


      <ReactMarkdown
        components={{
          code({ className, children }) {

            const match = /language-(\w+)/.exec(
              className || ""
            );


            return match ? (
              <SyntaxHighlighter
                style={oneDark}
                language={match[1]}
                PreTag="div"
                customStyle={{
                  maxWidth: "100%",
                  overflowX: "auto",
                  margin: "12px 0",
                  borderRadius: "12px",
                }}
              >
                {String(children).replace(/\n$/, "")}
              </SyntaxHighlighter>

            ) : (

              <code>
                {children}
              </code>

            );
          },
        }}
      >

        {message.content}

      </ReactMarkdown>

    </div>
  );
}


export default ChatMessage;