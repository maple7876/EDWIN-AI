import SetupApp from "./setup/SetupApp";
import Header from "./components/Header";
import ChatInput from "./components/ChatInput";
import ChatMessage from "./components/ChatMessage";
import Sidebar from "./components/sidebar";

import type { AppView } from "./components/sidebar";

import {
  getHardware,
  getStatus,
  getOnboarding,
  sendChat,
} from "./services/api";
import { setupApi } from "./setup/api";

import { useState, useEffect } from "react";
import "./App.css";

import type { Message } from "./types/chat";
import type { Status } from "./types/status";
import type { HardwareData } from "./types/hardware";

type Chat = {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
};

const STORAGE_KEY = "edwin_chats";

function createNewChat(): Chat {
  const now = Date.now();

  return {
    id: crypto.randomUUID(),
    title: "New Conversation",
    messages: [
      {
        role: "edwin",
        content: "Good evening, Sir. EDWIN is online.",
      },
    ],
    createdAt: now,
    updatedAt: now,
  };
}

function App() {
  const [chats, setChats] = useState<Chat[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);

      if (saved) {
        const parsed = JSON.parse(saved);

        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (error) {
      console.error("Failed to load chats:", error);
    }

    return [createNewChat()];
  });

  const [activeChatId, setActiveChatId] = useState<string>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);

      if (saved) {
        const parsed = JSON.parse(saved);

        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed[0].id;
        }
      }
    } catch (error) {
      console.error("Failed to load active chat:", error);
    }

    return "";
  });

  const [activeView, setActiveView] =
    useState<AppView>("conversations");

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [status, setStatus] = useState<Status>({
    assistant: "",
    version: "",
    model: "Loading...",
    connected: false,
    memory: false,
    internet: false,
  });

  const [hardware, setHardware] =
    useState<HardwareData | null>(null);

  const [onboardingComplete, setOnboardingComplete] =
    useState<boolean | null>(null);

  const activeChat = chats.find(
    (chat) => chat.id === activeChatId
  );

  /*
   * INITIALIZE EDWIN
   */
  useEffect(() => {
    getHardware()
      .then((data) => setHardware(data))
      .catch((error) => {
        console.error("Hardware detection failed:", error);
      });

    getStatus()
      .then((data) => setStatus(data))
      .catch((error) => {
        console.error("Status unavailable:", error);
      });

    let attempts = 0;
    const waitForBackend = async () => {
      try {
        await setupApi.health();
        const data = await getOnboarding();
        setOnboardingComplete(data.complete);
      } catch (error) {
        attempts += 1;
        if (attempts < 25) window.setTimeout(waitForBackend, 400);
        else { console.error("EDWIN backend unavailable:", error); setOnboardingComplete(false); }
      }
    };
    void waitForBackend();
  }, []);

  /*
   * SAVE CHATS
   */
  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(chats)
    );
  }, [chats]);

  /*
   * CREATE NEW CHAT
   */
  function createChat() {
    const newChat = createNewChat();

    setChats((prev) => [newChat, ...prev]);
    setActiveChatId(newChat.id);
    setActiveView("conversations");
    setInput("");
  }

  /*
   * SELECT CHAT
   */
  function selectChat(chatId: string) {
    setActiveChatId(chatId);
    setActiveView("conversations");
    setInput("");
  }

  /*
   * SEND MESSAGE
   */
  async function sendMessage() {
    if (!input.trim() || loading || !activeChat) {
      return;
    }

    const userMessage = input.trim();
    const chatId = activeChatId;

    const userMessageObject: Message = {
      role: "user",
      content: userMessage,
    };

    setInput("");
    setLoading(true);

    setChats((prev) =>
      prev.map((chat) => {
        if (chat.id !== chatId) {
          return chat;
        }

        return {
          ...chat,
          title:
            chat.title === "New Conversation"
              ? userMessage.slice(0, 32)
              : chat.title,
          messages: [
            ...chat.messages,
            userMessageObject,
          ],
          updatedAt: Date.now(),
        };
      })
    );

    try {
      const data = await sendChat(userMessage);

      setChats((prev) =>
        prev.map((chat) => {
          if (chat.id !== chatId) {
            return chat;
          }

          return {
            ...chat,
            messages: [
              ...chat.messages,
              {
                role: "edwin",
                content: data.response,
              },
            ],
            updatedAt: Date.now(),
          };
        })
      );
    } catch (error) {
      console.error("Chat error:", error);

      setChats((prev) =>
        prev.map((chat) => {
          if (chat.id !== chatId) {
            return chat;
          }

          return {
            ...chat,
            messages: [
              ...chat.messages,
              {
                role: "edwin",
                content:
                  "Unable to establish connection to the EDWIN core, Sir.",
              },
            ],
            updatedAt: Date.now(),
          };
        })
      );
    } finally {
      setLoading(false);
    }
  }

  /*
   * STARTUP
   */
  if (onboardingComplete === null) {
    return (
      <div style={{ padding: 40 }}>
        <h1>Starting EDWIN...</h1>
        <p>Checking system configuration...</p>
      </div>
    );
  }

  /*
   * FIRST-TIME SETUP
   */
  if (!onboardingComplete) {
    return (
      <SetupApp
        onComplete={() => {
          setOnboardingComplete(true);
          getStatus().then(setStatus).catch(() => undefined);
        }}
      />
    );
  }

  /*
   * MAIN INTERFACE
   */
  return (
    <div className="window">
      <Sidebar
        chats={chats.map((chat) => ({
          id: chat.id,
          title: chat.title,
        }))}
        activeChatId={activeChatId}
        activeView={activeView}
        onNewChat={createChat}
        onSelectChat={selectChat}
        onNavigate={setActiveView}
      />

      <div className="main">
        {activeView === "conversations" && (
          <>
            <Header
              status={status}
              hardware={null}
            />

            <main className="chat">
              {activeChat?.messages.map(
                (message, index) => (
                  <ChatMessage
                    key={index}
                    message={message}
                  />
                )
              )}

              {loading && (
                <div className="message edwin">
                  <strong>EDWIN</strong>
                  <p>Processing...</p>
                </div>
              )}
            </main>

            <ChatInput
              input={input}
              loading={loading}
              setInput={setInput}
              sendMessage={sendMessage}
            />
          </>
        )}

        {activeView === "hardware" && (
          <main className="system-view">
            <div className="system-view-header">
              <h2>Hardware</h2>
              <p>
                System information and model recommendations.
              </p>
            </div>

            {hardware ? (
              <div className="hardware-dashboard">
                <div className="hardware-card">
                  <span>CPU</span>
                  <strong>
                    {hardware.system.cpu}
                  </strong>
                </div>

                <div className="hardware-card">
                  <span>CORES</span>
                  <strong>
                    {hardware.system.cores}
                  </strong>
                </div>

                <div className="hardware-card">
                  <span>RAM</span>
                  <strong>
                    {hardware.system.ram} GB
                  </strong>
                </div>

                <div className="hardware-card">
                  <span>GPU</span>
                  <strong>
                    {hardware.system.gpu
                      ? "Detected"
                      : "Not Detected"}
                  </strong>
                </div>
              </div>
            ) : (
              <p>Unable to retrieve hardware information.</p>
            )}
          </main>
        )}

        {activeView === "projects" && (
          <main className="system-view">
            <div className="system-view-header">
              <h2>Projects</h2>
              <p>
                Your projects and active workspaces.
              </p>
            </div>

            <div className="empty-view">
              No projects yet.
            </div>
          </main>
        )}

        {activeView === "memory" && (
          <main className="system-view">
            <div className="system-view-header">
              <h2>Memory</h2>
              <p>
                EDWIN's long-term memory system.
              </p>
            </div>

            <div className="empty-view">
              Memory controls will appear here.
            </div>
          </main>
        )}

        {activeView === "tools" && (
          <main className="system-view">
            <div className="system-view-header">
              <h2>Tools</h2>
              <p>
                Tools available to EDWIN.
              </p>
            </div>

            <div className="empty-view">
              No tools available yet.
            </div>
          </main>
        )}

        {activeView === "settings" && (
          <main className="system-view">
            <div className="system-view-header">
              <h2>Settings</h2>
              <p>
                Configure EDWIN.
              </p>
            </div>

            <div className="empty-view">
              Settings will appear here.
            </div>
          </main>
        )}
      </div>
    </div>
  );
}

export default App;
