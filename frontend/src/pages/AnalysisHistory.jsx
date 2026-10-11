import React from "react";
import {
  History,
  Download,
  CheckCircle2,
  Cpu,
  Layers,
  ArrowRight,
  ExternalLink
} from "lucide-react";
import { exportReportCsvUrl } from "../services/api";

export default function AnalysisHistory({ historyRuns, activeRun, onSelectRun, onNavigate }) {
  return (
    <div className="space-y-6 pb-12 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
          <History className="w-5 h-5 text-cyan-400" />
          Detection Runs & Telemetry History
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Complete audit trail of all machine learning inference runs, datasets processed, anomaly rates, and security alerts.
        </p>
      </div>

      {/* History Table Card */}
      <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0b1120] text-slate-400 border-b border-[#1e293b]">
              <tr>
                <th className="px-4 py-3">Run ID</th>
                <th className="px-4 py-3">Timestamp</th>
                <th className="px-4 py-3">Dataset Name</th>
                <th className="px-4 py-3">Model Core</th>
                <th className="px-4 py-3">Total Rows</th>
                <th className="px-4 py-3">Anomalies</th>
                <th className="px-4 py-3">Anomaly %</th>
                <th className="px-4 py-3">Latency</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e293b] text-slate-300">
              {historyRuns && historyRuns.length > 0 ? (
                historyRuns.map((r) => {
                  const isActive = activeRun?.id === r.id;
                  return (
                    <tr
                      key={r.id}
                      className={`hover:bg-slate-800/40 transition-colors ${
                        isActive ? "bg-cyan-950/20" : ""
                      }`}
                    >
                      <td className="px-4 py-3 text-cyan-400 font-bold">
                        {r.id.slice(0, 8)}
                        {isActive && (
                          <span className="ml-2 text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                            Active
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-slate-400">
                        {new Date(r.created_at).toLocaleString()}
                      </td>
                      <td className="px-4 py-3 font-semibold text-white">
                        {r.dataset_name}
                      </td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 text-[11px]">
                          {r.model_name.includes("Classifier") ? "Random Forest" : "Isolation Forest"}
                        </span>
                      </td>
                      <td className="px-4 py-3">{r.total_records.toLocaleString()}</td>
                      <td className="px-4 py-3 text-rose-400 font-bold">
                        {r.anomaly_count.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 font-bold text-rose-400">
                        {r.anomaly_percentage.toFixed(1)}%
                      </td>
                      <td className="px-4 py-3 text-slate-400">{r.duration_ms} ms</td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => {
                              onSelectRun(r.id);
                              onNavigate("overview");
                            }}
                            className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-sans border border-slate-700 transition"
                          >
                            Load Run
                          </button>
                          <a
                            href={exportReportCsvUrl(r.id)}
                            download
                            className="p-1 rounded text-cyan-400 hover:text-cyan-300 hover:bg-slate-800"
                            title="Export CSV"
                          >
                            <Download className="w-3.5 h-3.5" />
                          </a>
                        </div>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-slate-500 font-sans">
                    No detection runs recorded in database.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
