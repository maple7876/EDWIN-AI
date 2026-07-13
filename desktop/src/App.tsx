import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useState, useEffect } from "react";
import "./App.css";


interface Message {
  role: "user" | "edwin";
  content: string;
}

interface Status {
  model: string;
  memory_entries: number;
}


function App() {

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "edwin",
      content: "Good evening, Sir. EDWIN is online.",
    },
  ]);


  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);


  const [status, setStatus] = useState<Status>({
    model: "Loading...",
    memory_entries: 0,
  });



  useEffect(() => {

    fetch("http://127.0.0.1:8000/status")

      .then((res) => res.json())

      .then((data) => setStatus(data))

      .catch(() => {

        setStatus({
          model: "Offline",
          memory_entries: 0,
        });

      });

  }, []);





  async function sendMessage() {

    if (!input.trim() || loading) return;


    const userMessage = input;


    setMessages((prev) => [
      ...prev,
      {
        role:"user",
        content:userMessage,
      }
    ]);


    setInput("");

    setLoading(true);



    try {


      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method:"POST",

          headers:{
            "Content-Type":"application/json",
          },

          body:JSON.stringify({
            message:userMessage,
          }),
        }
      );


      const data = await response.json();



      setMessages((prev)=>[
        ...prev,
        {
          role:"edwin",
          content:data.response,
        }
      ]);



    } catch {


      setMessages((prev)=>[
        ...prev,
        {
          role:"edwin",
          content:
          "Unable to establish connection to the EDWIN core, Sir.",
        }
      ]);

    }


    setLoading(false);

  }







  return (

    <div className="window">


      {/* SIDEBAR */}

      <aside className="sidebar">


        <h1>
          EDWIN
        </h1>


        <button className="new-chat">
          + New Chat
        </button>



        <section>

          <h3>
            Workspace
          </h3>


          <div className="sidebar-item">
            Conversations
          </div>


          <div className="sidebar-item">
            Projects
          </div>


        </section>





        <section>

          <h3>
            System
          </h3>


          <div className="sidebar-item">
            Memory
          </div>


          <div className="sidebar-item">
            Tools
          </div>


          <div className="sidebar-item">
            Settings
          </div>


        </section>



      </aside>







      {/* MAIN */}

      <div className="main">



        <header className="header">


          <div>

            <h2>
              EDWIN Alpha
            </h2>


            <p>
              Local Intelligence System
            </p>


          </div>




          <div className="status">


            <div className="status-card">

              <span>
                Model
              </span>

              <strong>
                {status.model}
              </strong>

            </div>



            <div className="status-card">

              <span>
                Memory
              </span>

              <strong>
                {status.memory_entries}
              </strong>


            </div>



          </div>


        </header>








        <main className="chat">


          {messages.map((message,index)=>(


            <div

              key={index}

              className={
                `message ${message.role}`
              }

            >


              <strong>

                {
                  message.role==="user"
                  ? "You"
                  : "EDWIN"
                }

              </strong>



              <ReactMarkdown
  components={{
    code({ className, children }) {
      const match = /language-(\w+)/.exec(className || "");

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
        <code>{children}</code>
      );
    },
  }}
>
  {message.content}
</ReactMarkdown>


            </div>


          ))}





          {loading && (

            <div className="message edwin">

              <strong>
                EDWIN
              </strong>


              <p>
                Processing...
              </p>

            </div>

          )}



        </main>







        <footer className="input-area">


          <input

            value={input}

            placeholder="Speak with EDWIN..."

            onChange={(event)=>
              setInput(event.target.value)
            }


            onKeyDown={(event)=>{

              if(event.key==="Enter")
                sendMessage();

            }}

          />



          <button onClick={sendMessage}>

            Send

          </button>



        </footer>





      </div>


    </div>


  );

}


export default App;