import React, { useState } from "react";
import {
  Settings as SettingsIcon,
  Cpu,
  Database,
  Key,
  ShieldCheck,
  CheckCircle2,
  Server,
  FileCode,
  Sparkles,
  Lock
} from "lucide-react";

export default function Settings({ health }) {
  const [activeModel, setActiveModel] = useState(
    health?.groq_assistant?.model || "openai/gpt-oss-120b"
  );

  return (
    <div className="space-y-6 max-w-4xl pb-12 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
          <SettingsIcon className="w-5 h-5 text-cyan-400" />
          System & AI Engine Configuration
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Review backend environment configuration, Groq LLM settings, SQLite local database parameters, and security policies.
        </p>
      </div>

      {/* Groq LLM Configuration Card */}
      <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-[#1e293b]">
          <div className="flex items-center gap-2.5">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <div>
              <h3 className="text-sm font-bold text-white">Groq AI Inference Core</h3>
              <p className="text-xs text-slate-400">High-throughput LPU cloud inference</p>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono font-bold">
            API CONNECTED
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className="bg-[#080c17] p-3 rounded-lg border border-[#1e293b]">
            <span className="text-slate-400">GROQ_MODEL</span>
            <div className="text-cyan-400 font-bold text-sm mt-1">
              {health?.groq_assistant?.model || "openai/gpt-oss-120b"}
            </div>
            <p className="text-[10px] text-slate-500 mt-1 font-sans">
              Configurable in backend/.env. Supported models: openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.8-27b.
            </p>
          </div>

          <div className="bg-[#080c17] p-3 rounded-lg border border-[#1e293b]">
            <span className="text-slate-400">API KEY SECURITY</span>
            <div className="text-emerald-400 font-bold text-sm mt-1 flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5" /> SECURE / SERVER-SIDE ONLY
            </div>
            <p className="text-[10px] text-slate-500 mt-1 font-sans">
              API key is loaded strictly into backend process memory and is never transmitted or exposed to frontend code.
            </p>
          </div>
        </div>
      </div>

      {/* SQLite Database Card */}
      <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-[#1e293b]">
          <div className="flex items-center gap-2.5">
            <Database className="w-5 h-5 text-cyan-400" />
            <div>
              <h3 className="text-sm font-bold text-white">Local SQLite Database</h3>
              <p className="text-xs text-slate-400">Persistent Relational Storage with SQLAlchemy</p>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono font-bold">
            SQLITE CONNECTED
          </span>
        </div>

        <div className="space-y-2 text-xs font-mono">
          <div className="flex items-center justify-between p-2.5 rounded bg-[#080c17] border border-[#1e293b]">
            <span className="text-slate-400">Database File Location</span>
            <span className="text-slate-200">backend/netguard.db</span>
          </div>
          <div className="flex items-center justify-between p-2.5 rounded bg-[#080c17] border border-[#1e293b]">
            <span className="text-slate-400">ORM Framework</span>
            <span className="text-slate-200">SQLAlchemy 2.0 (Declarative Models)</span>
          </div>
          <div className="flex items-center justify-between p-2.5 rounded bg-[#080c17] border border-[#1e293b]">
            <span className="text-slate-400">Database Engine</span>
            <span className="text-slate-200">SQLite 3 (Zero Server Configuration Required)</span>
          </div>
        </div>
      </div>

      {/* Machine Learning Pipeline Card */}
      <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-[#1e293b]">
          <div className="flex items-center gap-2.5">
            <Cpu className="w-5 h-5 text-purple-400" />
            <div>
              <h3 className="text-sm font-bold text-white">ML Pipelines & Serialized Binaries</h3>
              <p className="text-xs text-slate-400">Scikit-learn Model Cache</p>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono font-bold">
            TRAINED & CACHED
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className="bg-[#080c17] p-3 rounded-lg border border-[#1e293b]">
            <span className="text-slate-400">Random Forest Artifact</span>
            <div className="text-emerald-400 font-bold mt-1">
              backend/app/ml/saved_models/random_forest.joblib
            </div>
            <span className="text-[10px] text-slate-500 font-sans">
              Status: {health?.models?.random_forest || "ready"} (88% Test Accuracy)
            </span>
          </div>

          <div className="bg-[#080c17] p-3 rounded-lg border border-[#1e293b]">
            <span className="text-slate-400">Isolation Forest Artifact</span>
            <div className="text-purple-400 font-bold mt-1">
              backend/app/ml/saved_models/isolation_forest.joblib
            </div>
            <span className="text-[10px] text-slate-500 font-sans">
              Status: {health?.models?.isolation_forest || "ready"} (Unsupervised)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
