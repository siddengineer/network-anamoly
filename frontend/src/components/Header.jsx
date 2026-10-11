import React, { useState, useEffect } from "react";
import {
  ShieldAlert,
  Cpu,
  Sparkles,
  RefreshCw,
  UploadCloud,
  CheckCircle2,
  Clock
} from "lucide-react";

export default function Header({
  activeRun,
  historyRuns,
  onSelectRun,
  onOpenUpload,
  health,
  onRefresh
}) {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-16 bg-[#0b1120]/90 backdrop-blur-md border-b border-[#1e293b] px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Left: Active Run Information */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-slate-400">ACTIVE DATASET:</span>
          {historyRuns && historyRuns.length > 0 ? (
            <select
              value={activeRun?.id || ""}
              onChange={(e) => onSelectRun(e.target.value)}
              className="bg-[#0f172a] border border-[#334155] text-slate-200 text-xs rounded-md px-2.5 py-1.5 focus:outline-none focus:border-cyan-500 font-mono"
            >
              {historyRuns.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.dataset_name} ({r.model_name.includes("Forest Classifier") ? "Random Forest" : "Isolation Forest"}) - {new Date(r.created_at).toLocaleDateString()}
                </option>
              ))}
            </select>
          ) : (
            <span className="text-xs font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
              No Dataset Analyzed
            </span>
          )}
        </div>

        {activeRun && (
          <div className="hidden md:flex items-center gap-2">
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              {activeRun.model_name}
            </span>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              {activeRun.total_records.toLocaleString()} Flows
            </span>
          </div>
        )}
      </div>

      {/* Right: Telemetry, AI Engine Status, Quick Actions */}
      <div className="flex items-center gap-4">
        {/* Clock */}
        <div className="hidden lg:flex items-center gap-1.5 text-xs font-mono text-slate-400 bg-[#0f172a] px-2.5 py-1 rounded border border-[#1e293b]">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span>{time}</span>
        </div>

        {/* Groq AI Badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded bg-indigo-950/60 border border-indigo-800/40 text-indigo-300 text-xs font-mono">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400 animate-spin" style={{ animationDuration: "6s" }} />
          <span>GROQ: {health?.groq_assistant?.model ? health.groq_assistant.model.split("/").pop() : "ONLINE"}</span>
        </div>

        {/* System Health */}
        <div className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
          <span className="hidden md:inline font-mono">SOC SECURE</span>
        </div>

        {/* Refresh button */}
        <button
          onClick={onRefresh}
          className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors border border-transparent hover:border-[#334155]"
          title="Refresh telemetry"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        {/* Upload Button */}
        <button
          onClick={onOpenUpload}
          className="flex items-center gap-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium px-3 py-1.5 rounded-lg shadow-sm shadow-cyan-500/20 transition-all border border-cyan-400/30"
        >
          <UploadCloud className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Analyze Traffic</span>
        </button>
      </div>
    </header>
  );
}
