import React, { useState, useEffect, useRef } from "react";
import {
  BotMessageSquare,
  Send,
  Sparkles,
  User,
  Trash2,
  PlusCircle,
  HelpCircle,
  Layers,
  ShieldCheck,
  CheckCircle2,
  Terminal,
  Activity
} from "lucide-react";
import { sendChatMessage, getChatHistory, createChatSession, listChatSessions } from "../services/api";

export default function AICyberAssistant({ activeRun, initialQuery, recordIndex }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [groundedStats, setGroundedStats] = useState(null);
  const messagesEndRef = useRef(null);

  const suggestedQuestions = [
    "How many anomalous records were detected?",
    "What percentage of the uploaded traffic was flagged?",
    "Why did the model flag port 21 (FTP) and port 22 (SSH)?",
    "What are the most unusual traffic patterns in this dataset?",
    "Summarize this analysis run and provide defensive steps.",
    "Explain the model's precision and recall metrics."
  ];

  // Initialize or fetch sessions
  useEffect(() => {
    const initSession = async () => {
      try {
        const sessions = await listChatSessions();
        if (sessions && sessions.length > 0) {
          const latest = sessions[0];
          setSessionId(latest.id);
          const history = await getChatHistory(latest.id);
          if (history && history.length > 0) {
            setMessages(history);
          } else {
            setWelcomeMessage();
          }
        } else {
          const newSes = await createChatSession();
          setSessionId(newSes.id);
          setWelcomeMessage();
        }
      } catch (err) {
        console.error("Session init error", err);
        setWelcomeMessage();
      }
    };
    initSession();
  }, []);

  // Handle incoming initial query from other pages (Record Modal or Alerts)
  useEffect(() => {
    if (initialQuery && initialQuery.trim()) {
      handleSendMessage(initialQuery, recordIndex);
    }
  }, [initialQuery]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const setWelcomeMessage = () => {
    setMessages([
      {
        role: "assistant",
        content: `Greetings Analyst. I am **NetGuard AI Assistant**, powered by Groq high-speed LLM inference.\n\nI am grounded in your SQLite telemetry and model predictions. You can ask me to break down anomalies, explain specific port signatures, evaluate precision and recall, or outline SOC containment strategies.`
      }
    ]);
  };

  const handleSendMessage = async (textToSend, customRecordIdx = null) => {
    const query = textToSend || input;
    if (!query.trim() || isLoading) return;

    const userMsg = { role: "user", content: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const payload = {
        message: query,
        session_id: sessionId,
        run_id: activeRun?.id,
        record_index: customRecordIdx !== null ? customRecordIdx : undefined
      };

      const res = await sendChatMessage(payload);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.response }
      ]);
      if (res.grounded_stats) {
        setGroundedStats(res.grounded_stats);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Encountered an issue communicating with the AI service. Please verify your Groq connection in Settings."
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearHistory = async () => {
    try {
      const newSes = await createChatSession();
      setSessionId(newSes.id);
      setWelcomeMessage();
    } catch (err) {
      setWelcomeMessage();
    }
  };

  return (
    <div className="h-[calc(100vh-8.5rem)] flex flex-col bg-[#0f172a] rounded-xl border border-[#1e293b] shadow-2xl overflow-hidden animate-in fade-in duration-300">
      {/* Chat Header */}
      <div className="p-4 bg-[#0b1120] border-b border-[#1e293b] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
            <Sparkles className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              NetGuard AI Cybersecurity Assistant
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">
                GROQ LLM CORE
              </span>
            </h3>
            <p className="text-xs text-slate-400">
              Grounded exclusively in factual network analysis data from SQLite.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {activeRun && (
            <span className="hidden sm:inline-flex text-[11px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-2.5 py-1 rounded">
              Context: {activeRun.dataset_name} ({activeRun.total_records} rows)
            </span>
          )}
          <button
            onClick={handleClearHistory}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            title="Clear Chat / New Session"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Messages Thread */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        {messages.map((m, idx) => {
          const isUser = m.role === "user";
          return (
            <div
              key={idx}
              className={`flex items-start gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 text-xs font-bold border ${
                  isUser
                    ? "bg-cyan-600 text-white border-cyan-500"
                    : "bg-indigo-600/30 text-indigo-300 border-indigo-500/40"
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <BotMessageSquare className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-3xl rounded-xl p-4 text-xs leading-relaxed ${
                  isUser
                    ? "bg-cyan-600 text-white shadow-md shadow-cyan-900/30"
                    : "bg-[#080c17] text-slate-200 border border-[#1e293b] shadow-md shadow-black/40"
                }`}
              >
                <div className="whitespace-pre-wrap font-sans">{m.content}</div>
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600/30 text-indigo-300 border border-indigo-500/40 flex items-center justify-center flex-shrink-0">
              <Sparkles className="w-4 h-4 animate-spin" />
            </div>
            <div className="bg-[#080c17] p-3 rounded-xl border border-[#1e293b] text-xs text-slate-400 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
              NetGuard AI is synthesizing telemetry and generating SOC analysis...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions */}
      <div className="px-4 py-2 bg-[#0b1120] border-t border-[#1e293b] flex items-center gap-2 overflow-x-auto">
        <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider flex-shrink-0">
          Suggested:
        </span>
        {suggestedQuestions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(q)}
            className="whitespace-nowrap px-2.5 py-1 rounded bg-[#080c17] hover:bg-slate-800 text-[11px] text-slate-300 border border-[#1e293b] hover:border-cyan-500/50 transition-colors flex-shrink-0"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="p-4 bg-[#0b1120] border-t border-[#1e293b] flex items-center gap-3"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask NetGuard AI about anomaly rates, ports, metrics, or defense..."
          className="flex-1 bg-[#080c17] text-xs text-slate-200 px-4 py-2.5 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="px-4 py-2.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-cyan-900/40 transition"
        >
          <Send className="w-3.5 h-3.5" />
          <span>Send</span>
        </button>
      </form>
    </div>
  );
}
