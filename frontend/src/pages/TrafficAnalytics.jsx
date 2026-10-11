import React, { useState } from "react";
import {
  BarChart3,
  PieChart as PieIcon,
  Activity,
  Filter,
  Layers,
  ShieldAlert,
  Clock,
  Radio
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from "recharts";

export default function TrafficAnalytics({ trends, summary }) {
  const [selectedPort, setSelectedPort] = useState("all");

  const portDistribution = trends?.port_distribution || [];
  const durationDistribution = trends?.duration_distribution || [];
  const scoreBins = trends?.anomaly_score_bins || [];
  const attackBreakdown = trends?.attack_breakdown || [];

  const filteredPorts =
    selectedPort === "all"
      ? portDistribution
      : portDistribution.filter((p) => String(p.port) === selectedPort);

  const COLORS = ["#06b6d4", "#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"];

  return (
    <div className="space-y-6 pb-12 animate-in fade-in duration-300">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-cyan-400" />
            Traffic Flow & Threat Vector Analytics
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Detailed statistical distributions of destination ports, flow duration latencies, and machine learning anomaly scores.
          </p>
        </div>

        {/* Port Filter */}
        <div className="flex items-center gap-2 bg-[#0f172a] p-1.5 rounded-lg border border-[#1e293b]">
          <Filter className="w-4 h-4 text-slate-400 ml-1" />
          <span className="text-xs text-slate-400 font-mono">Port Filter:</span>
          <select
            value={selectedPort}
            onChange={(e) => setSelectedPort(e.target.value)}
            className="bg-[#080c17] text-xs text-slate-200 rounded px-2 py-1 border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
          >
            <option value="all">All Destination Ports</option>
            {portDistribution.map((p) => (
              <option key={p.port} value={String(p.port)}>
                Port {p.port} ({p.total} flows)
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Grid 1: Port Distribution & Duration Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Destination Port Normal vs Anomaly */}
        <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
              Destination Port Breakdown (Normal vs Anomaly)
            </h3>
            <span className="text-xs text-slate-400 font-mono">Layer 4 Ingress</span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={filteredPorts} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
                <XAxis dataKey="port" stroke="#64748b" fontSize={11} tickFormatter={(val) => `Port ${val}`} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0f172a",
                    borderColor: "#334155",
                    borderRadius: "8px",
                    color: "#fff",
                    fontSize: "12px"
                  }}
                />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} />
                <Bar dataKey="normal" name="Normal (BENIGN)" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="anomaly" name="Anomalous Traffic" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Flow Duration Bins */}
        <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
              Flow Duration Latency Distribution
            </h3>
            <span className="text-xs text-slate-400 font-mono">Session Lifetime</span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={durationDistribution} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
                <XAxis dataKey="range" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0f172a",
                    borderColor: "#334155",
                    borderRadius: "8px",
                    color: "#fff",
                    fontSize: "12px"
                  }}
                />
                <Bar dataKey="count" name="Flow Count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Grid 2: Anomaly Score Distribution & Attack Categories */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Anomaly Score Distribution */}
        <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
              Model Confidence / Anomaly Score Spectrum
            </h3>
            <span className="text-xs text-slate-400 font-mono">Probability Bins</span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreBins} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
                <XAxis dataKey="bin" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0f172a",
                    borderColor: "#334155",
                    borderRadius: "8px",
                    color: "#fff",
                    fontSize: "12px"
                  }}
                />
                <Bar dataKey="count" name="Flow Count" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Attack Category Breakdown Pie */}
        <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 shadow-xl flex flex-col justify-between">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
              Attack Classification Breakdown
            </h3>
            <span className="text-xs text-slate-400 font-mono">Threat Profiles</span>
          </div>

          {attackBreakdown.length > 0 ? (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={attackBreakdown}
                    cx="50%"
                    cy="50%"
                    outerRadius={85}
                    dataKey="value"
                    nameKey="name"
                    label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                    labelLine={false}
                  >
                    {attackBreakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#0f172a",
                      borderColor: "#334155",
                      borderRadius: "8px",
                      color: "#fff",
                      fontSize: "12px"
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-72 flex items-center justify-center text-xs text-slate-500">
              No attacks classified.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
