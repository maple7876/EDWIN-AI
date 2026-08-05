interface ChatSummary {
  id: string;
  title: string;
}

export type AppView =
  | "conversations"
  | "projects"
  | "memory"
  | "tools"
  | "settings"
  | "hardware";

interface SidebarProps {
  chats: ChatSummary[];
  activeChatId: string;
  activeView: AppView;
  onNewChat: () => void;
  onSelectChat: (chatId: string) => void;
  onNavigate: (view: AppView) => void;
}

function Sidebar({
  chats,
  activeChatId,
  activeView,
  onNewChat,
  onSelectChat,
  onNavigate,
}: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>EDWIN</h1>
        <span className="sidebar-version">ALPHA</span>
      </div>

      <button className="new-chat" onClick={onNewChat}>
        <span>＋</span>
        <span>New Chat</span>
      </button>

      <section className="conversation-section">
        <h3>Conversations</h3>

        <button
          className={`sidebar-item ${
            activeView === "conversations" ? "active" : ""
          }`}
          onClick={() => onNavigate("conversations")}
        >
          <span>◌</span>
          <span>Conversations</span>
        </button>

        <div className="conversation-list">
          {chats.length === 0 ? (
            <p className="empty-chats">
              No conversations yet.
            </p>
          ) : (
            chats.map((chat) => (
              <button
                key={chat.id}
                className={`conversation-item ${
                  activeChatId === chat.id &&
                  activeView === "conversations"
                    ? "active"
                    : ""
                }`}
                onClick={() => {
                  onSelectChat(chat.id);
                  onNavigate("conversations");
                }}
              >
                <span className="conversation-icon">
                  ◌
                </span>

                <span className="conversation-title">
                  {chat.title}
                </span>
              </button>
            ))
          )}
        </div>
      </section>

      <section>
        <h3>Workspace</h3>

        <button
          className={`sidebar-item ${
            activeView === "projects" ? "active" : ""
          }`}
          onClick={() => onNavigate("projects")}
        >
          Projects
        </button>
      </section>

      <section>
        <h3>System</h3>

        <button
          className={`sidebar-item ${
            activeView === "memory" ? "active" : ""
          }`}
          onClick={() => onNavigate("memory")}
        >
          Memory
        </button>

        <button
          className={`sidebar-item ${
            activeView === "tools" ? "active" : ""
          }`}
          onClick={() => onNavigate("tools")}
        >
          Tools
        </button>

        <button
          className={`sidebar-item ${
            activeView === "hardware" ? "active" : ""
          }`}
          onClick={() => onNavigate("hardware")}
        >
          Hardware
        </button>

        <button
          className={`sidebar-item ${
            activeView === "settings" ? "active" : ""
          }`}
          onClick={() => onNavigate("settings")}
        >
          Settings
        </button>
      </section>
    </aside>
  );
}

export default Sidebar;