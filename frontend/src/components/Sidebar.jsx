import React from "react";
import {
  LayoutDashboard,
  UploadCloud,
  BarChart3,
  ShieldAlert,
  BellRing,
  BotMessageSquare,
  Cpu,
  History,
  Settings,
  ChevronLeft,
  ChevronRight,
  ShieldCheck
} from "lucide-react";

export default function Sidebar({ currentTab, setCurrentTab, collapsed, setCollapsed, alertCount }) {
  const navItems = [
    { id: "overview", label: "Overview", icon: LayoutDashboard },
    { id: "upload", label: "Upload Dataset", icon: UploadCloud },
    { id: "analytics", label: "Traffic Analytics", icon: BarChart3 },
    { id: "detection", label: "Anomaly Detection", icon: ShieldAlert },
    { id: "alerts", label: "Security Alerts", icon: BellRing, badge: alertCount },
    { id: "assistant", label: "AI Cyber Assistant", icon: BotMessageSquare, highlight: true },
    { id: "performance", label: "Model Performance", icon: Cpu },
    { id: "history", label: "Analysis History", icon: History },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside
      className={`relative bg-[#0b1120] border-r border-[#1e293b] flex flex-col transition-all duration-300 z-30 select-none ${
        collapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Brand Header */}
      <div className="h-16 flex items-center px-4 border-b border-[#1e293b] gap-3">
        <div className="relative flex-shrink-0">
          <img
            src="/logo.png"
            alt="NetGuard AI"
            className="w-10 h-10 object-contain rounded-lg border border-cyan-500/30 shadow-lg shadow-cyan-500/10"
            onError={(e) => {
              e.target.style.display = "none";
            }}
          />
          <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full border-2 border-[#0b1120] animate-pulse" />
        </div>

        {!collapsed && (
          <div className="overflow-hidden">
            <h1 className="text-base font-bold tracking-wider text-white flex items-center gap-1.5">
              NETGUARD <span className="text-cyan-400 font-black">AI</span>
            </h1>
            <p className="text-[10px] text-slate-400 tracking-wider font-mono">
              SOC DEFENSE • ML CORE
            </p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-2 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all group relative ${
                isActive
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/10"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
              title={collapsed ? item.label : undefined}
            >
              <Icon
                className={`w-5 h-5 flex-shrink-0 transition-transform ${
                  isActive ? "text-cyan-400 scale-105" : "text-slate-400 group-hover:text-slate-200"
                }`}
              />

              {!collapsed && (
                <span className="truncate flex-1 text-left">{item.label}</span>
              )}

              {/* Alert Badge */}
              {item.badge > 0 && !collapsed && (
                <span className="px-1.5 py-0.5 text-[11px] font-bold rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30">
                  {item.badge}
                </span>
              )}

              {/* Highlight Pill for Groq Assistant */}
              {item.highlight && !collapsed && (
                <span className="px-1.5 py-0.2 text-[9px] font-semibold uppercase tracking-wider rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  GROQ
                </span>
              )}

              {isActive && (
                <div className="absolute left-0 top-1.5 bottom-1.5 w-1 bg-cyan-400 rounded-r" />
              )}
            </button>
          );
        })}
      </nav>

      {/* System Status / Collapse Button */}
      <div className="p-3 border-t border-[#1e293b] flex items-center justify-between">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-[11px] font-mono text-emerald-400">TELEMETRY LIVE</span>
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors ml-auto"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>
    </aside>
  );
}
