import React, { useRef, useState } from "react";
import {
  ShieldAlert,
  ShieldCheck,
  Activity,
  AlertTriangle,
  Play,
  Pause,
  Volume2,
  VolumeX,
  Radio,
  ArrowUpRight,
  Cpu,
  Layers,
  ExternalLink,
  UploadCloud,
  BotMessageSquare
} from "lucide-react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis
} from "recharts";

export default function Overview({
  summary,
  trends,
  activeRun,
  onNavigate,
  onOpenUpload,
  onSelectRecord
}) {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isMuted, setIsMuted] = useState(true);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const total = summary?.total_analyzed || 0;
  const normal = summary?.normal_count || 0;
  const anomalies = summary?.anomaly_count || 0;
  const anomalyPct = summary?.anomaly_percentage || 0;
  const alertsCount = summary?.active_alerts_count || 0;
  const criticalCount = summary?.critical_alerts_count || 0;

  // Pie chart data for Normal vs Anomaly
  const pieData = [
    { name: "Normal (BENIGN)", value: normal, color: "#10b981" },
    { name: "Anomalous Traffic", value: anomalies, color: "#ef4444" },
  ];

  // Attack categories for bar chart
  const attackData = Object.entries(summary?.class_distribution || {})
    .filter(([k]) => k !== "BENIGN")
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count);

  return (
    <div className="space-y-6 pb-12 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-[#0d1627] via-[#0f172a] to-[#111e38] p-6 rounded-xl border border-[#1e293b] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl -z-0 pointer-events-none" />
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-2">
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-cyan-500"></span>
            </span>
            <span className="text-xs font-mono font-semibold tracking-wider text-cyan-400 uppercase">
              Security Operations Center • Active Defense
            </span>
          </div>
          <h2 className="text-2xl font-black tracking-tight text-white">
            Network Threat Detection Command
          </h2>
          <p className="text-sm text-slate-400 max-w-2xl mt-1">
            Analyzing real network flow vectors using Machine Learning. Real-time classification of DoS, PortScans, Patator brute-force, and unknown volumetric anomalies.
          </p>
        </div>

        <div className="flex items-center gap-3 relative z-10">
          <button
            onClick={() => onNavigate("assistant")}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600/40 text-indigo-200 border border-indigo-500/40 text-xs font-semibold transition-all shadow-lg shadow-indigo-950/50"
          >
            <BotMessageSquare className="w-4 h-4 text-indigo-400" />
            Consult Groq AI
          </button>
          <button
            onClick={onOpenUpload}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold transition-all shadow-lg shadow-cyan-900/40"
          >
            <UploadCloud className="w-4 h-4" />
            Upload New File
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Analyzed */}
        <div className="bg-[#0f172a] p-5 rounded-xl border border-[#1e293b] shadow-lg relative overflow-hidden group">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-medium uppercase tracking-wider">Total Scanned</span>
            <Activity className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-black font-mono text-white tracking-tight">
            {total.toLocaleString()}
          </div>
          <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
            <span>Verified Flow Packets</span>
            <span className="text-cyan-400 font-mono">100% Validated</span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500 to-blue-500" />
        </div>

        {/* Normal Traffic */}
        <div className="bg-[#0f172a] p-5 rounded-xl border border-[#1e293b] shadow-lg relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-medium uppercase tracking-wider">Normal (BENIGN)</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black font-mono text-emerald-400 tracking-tight">
            {normal.toLocaleString()}
          </div>
          <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
            <span>Clean Traffic Ratio</span>
            <span className="text-emerald-400 font-mono font-bold">
              {total > 0 ? (100 - anomalyPct).toFixed(1) : 0}%
            </span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-emerald-500" />
        </div>

        {/* Anomalies Detected */}
        <div className="bg-[#0f172a] p-5 rounded-xl border border-[#1e293b] shadow-lg relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-medium uppercase tracking-wider">Anomalies Flagged</span>
            <ShieldAlert className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-3xl font-black font-mono text-rose-400 tracking-tight">
            {anomalies.toLocaleString()}
          </div>
          <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
            <span>Anomaly Rate</span>
            <span className="text-rose-400 font-mono font-bold">{anomalyPct.toFixed(1)}%</span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-rose-500" />
        </div>

        {/* Active Alerts */}
        <div className="bg-[#0f172a] p-5 rounded-xl border border-[#1e293b] shadow-lg relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono font-medium uppercase tracking-wider">Active Alerts</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-black font-mono text-amber-400 tracking-tight">
            {alertsCount}
          </div>
          <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
            <span>Critical Severity</span>
            <span className="text-rose-400 font-mono font-bold">{criticalCount} Critical</span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-amber-500" />
        </div>
      </div>

      {/* Main Grid: Video Threat Radar & Traffic Ratio */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* SOC Live Threat Radar Feed (Video) */}
        <div className="lg:col-span-2 bg-[#0f172a] rounded-xl border border-[#1e293b] overflow-hidden shadow-xl flex flex-col">
          <div className="p-4 border-b border-[#1e293b] flex items-center justify-between bg-[#0b1120]">
            <div className="flex items-center gap-2">
              <Radio className="w-4 h-4 text-cyan-400 animate-pulse" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
                Cyber Surveillance & Threat Radar Feed
              </h3>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono bg-cyan-950/60 text-cyan-300 border border-cyan-800/40 px-2 py-0.5 rounded">
                HUD ACTIVE
              </span>
              <button
                onClick={togglePlay}
                className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
                title={isPlaying ? "Pause Video" : "Play Video"}
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              </button>
              <button
                onClick={toggleMute}
                className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
                title={isMuted ? "Unmute" : "Mute"}
              >
                {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div className="relative aspect-video bg-black overflow-hidden flex items-center justify-center group">
            <video
              ref={videoRef}
              src="/radar_video.mp4"
              autoPlay
              loop
              muted={isMuted}
              playsInline
              className="w-full h-full object-cover"
            />
            {/* Cyber Radar HUD Overlay */}
            <div className="absolute inset-0 pointer-events-none border border-cyan-500/20 bg-gradient-to-t from-black/60 via-transparent to-transparent flex flex-col justify-between p-4 font-mono">
              <div className="flex items-center justify-between text-[11px] text-cyan-400/90 drop-shadow">
                <span className="bg-black/50 px-2 py-0.5 rounded border border-cyan-500/30">
                  RADAR SECTOR 04 • LIVE SCAN
                </span>
                <span className="bg-black/50 px-2 py-0.5 rounded border border-cyan-500/30">
                  FPS: 60 • LATENCY: 12ms
                </span>
              </div>
              <div className="flex items-center justify-between text-[11px] text-slate-300 drop-shadow">
                <span className="bg-black/60 px-2.5 py-1 rounded border border-[#1e293b]">
                  MODEL: {activeRun?.model_name || "Random Forest"}
                </span>
                <span className="text-emerald-400 font-bold bg-black/60 px-2.5 py-1 rounded border border-emerald-500/30">
                  AI DEFENSE ONLINE
                </span>
              </div>
            </div>
          </div>
          <div className="p-3 bg-[#0b1120] text-xs text-slate-400 border-t border-[#1e293b] flex items-center justify-between">
            <span>Visual Network Packet Flow & Telemetry Analyzer</span>
            <button
              onClick={() => onNavigate("analytics")}
              className="text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1"
            >
              Detailed Analytics <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Normal vs Anomaly Donut */}
        <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 flex flex-col justify-between shadow-xl">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white tracking-wide font-mono uppercase">
                Traffic Verdict Ratio
              </h3>
              <span className="text-xs font-mono text-slate-400">
                {total} Records
              </span>
            </div>

            <div className="h-52 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
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

            <div className="space-y-2 mt-4">
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-[#080c17] border border-[#1e293b]">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-emerald-500" />
                  <span className="text-xs text-slate-300 font-medium">Normal Flows</span>
                </div>
                <span className="text-xs font-mono font-bold text-emerald-400">
                  {normal} ({(total > 0 ? (normal / total) * 100 : 0).toFixed(1)}%)
                </span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-[#080c17] border border-[#1e293b]">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500" />
                  <span className="text-xs text-slate-300 font-medium">Anomalous Flows</span>
                </div>
                <span className="text-xs font-mono font-bold text-rose-400">
                  {anomalies} ({(total > 0 ? (anomalies / total) * 100 : 0).toFixed(1)}%)
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={() => onNavigate("detection")}
            className="w-full mt-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg transition-colors border border-slate-700"
          >
            Inspect Individual Detections
          </button>
        </div>
      </div>

      {/* Attack Distribution & Top Ports */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Attack Category Breakdown */}
        <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white tracking-wide font-mono uppercase">
              Detected Attack Signatures
            </h3>
            <span className="text-xs text-slate-400">Random Forest Classifier</span>
          </div>

          {attackData.length > 0 ? (
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={attackData} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                  <XAxis type="number" stroke="#64748b" fontSize={11} />
                  <YAxis type="category" dataKey="name" stroke="#94a3b8" fontSize={11} width={80} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#0f172a",
                      borderColor: "#334155",
                      borderRadius: "8px",
                      color: "#fff",
                      fontSize: "12px"
                    }}
                  />
                  <Bar dataKey="count" fill="#06b6d4" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-56 flex items-center justify-center text-xs text-slate-500">
              No attack signatures detected in current run.
            </div>
          )}
        </div>

        {/* Top Targeted Destination Ports */}
        <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white tracking-wide font-mono uppercase">
              Top Targeted Destination Ports
            </h3>
            <span className="text-xs text-slate-400 font-mono">Malicious Ingress</span>
          </div>

          <div className="space-y-2.5">
            {summary?.top_attack_ports && summary.top_attack_ports.length > 0 ? (
              summary.top_attack_ports.map((p, idx) => {
                const portDescriptions = {
                  21: "FTP (File Transfer)",
                  22: "SSH (Remote Shell)",
                  53: "DNS (Domain Name System)",
                  80: "HTTP (Web Server)",
                  443: "HTTPS (Encrypted Web)",
                  8080: "HTTP-Alt / Proxy"
                };
                return (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 rounded-lg bg-[#080c17] border border-[#1e293b]"
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-8 h-8 rounded bg-cyan-950/80 border border-cyan-800/40 text-cyan-400 font-mono font-bold text-xs flex items-center justify-center">
                        {p.port}
                      </span>
                      <div>
                        <div className="text-xs font-semibold text-slate-200">
                          Port {p.port}
                        </div>
                        <div className="text-[11px] text-slate-400">
                          {portDescriptions[p.port] || "Custom / High Ephemeral Service"}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs font-mono font-bold text-rose-400">
                        {p.count} Anomalies
                      </div>
                      <div className="text-[10px] text-slate-500">
                        {((p.count / anomalies) * 100).toFixed(1)}% of attacks
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="py-12 text-center text-xs text-slate-500">
                No destination ports recorded.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
