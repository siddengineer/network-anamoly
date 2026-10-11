import React from "react";
import {
  X,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  BotMessageSquare,
  Activity,
  Layers,
  Clock,
  ArrowRight
} from "lucide-react";

export default function RecordModal({ record, onClose, onAskAI }) {
  if (!record) return null;

  const isAnomaly = record.is_anomaly;
  const severityColors = {
    critical: "bg-red-500/20 text-red-400 border-red-500/40",
    high: "bg-orange-500/20 text-orange-400 border-orange-500/40",
    medium: "bg-amber-500/20 text-amber-400 border-amber-500/40",
    low: "bg-emerald-500/20 text-emerald-400 border-emerald-500/40"
  };

  const features = [
    { label: "Destination Port", value: record.destination_port },
    { label: "Flow Duration", value: `${record.flow_duration?.toLocaleString()} µs` },
    { label: "Total Fwd Packets", value: record.total_fwd_packets },
    { label: "Total Backward Packets", value: record.total_backward_packets },
    { label: "Total Length Fwd Packets", value: record.total_fwd_len?.toLocaleString() },
    { label: "Total Length Bwd Packets", value: record.total_bwd_len?.toLocaleString() },
    { label: "Fwd Packet Length Max", value: record.fwd_pkt_len_max },
    { label: "Fwd Packet Length Min", value: record.fwd_pkt_len_min },
    { label: "Fwd Packet Length Mean", value: record.fwd_pkt_len_mean?.toFixed(2) },
    { label: "Fwd Packet Length Std", value: record.fwd_pkt_len_std?.toFixed(2) },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-[#0f172a] border border-[#1e293b] rounded-xl max-w-2xl w-full shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="p-5 border-b border-[#1e293b] flex items-center justify-between bg-[#0b1120]">
          <div className="flex items-center gap-3">
            <div
              className={`p-2 rounded-lg border ${
                isAnomaly
                  ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
                  : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
              }`}
            >
              {isAnomaly ? <ShieldAlert className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
            </div>
            <div>
              <h3 className="text-base font-semibold text-white flex items-center gap-2">
                Flow Record #{record.record_index}
                <span
                  className={`text-xs px-2 py-0.5 rounded-full border uppercase font-mono ${
                    severityColors[record.severity] || severityColors.low
                  }`}
                >
                  {record.severity} Severity
                </span>
              </h3>
              <p className="text-xs text-slate-400">
                Predicted: <strong className="text-cyan-400">{record.predicted_label}</strong>
                {record.true_label && ` • Ground Truth: ${record.true_label}`}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Verdict Banner */}
          <div
            className={`p-4 rounded-lg border flex items-center justify-between ${
              isAnomaly
                ? "bg-rose-950/20 border-rose-900/40 text-rose-300"
                : "bg-emerald-950/20 border-emerald-900/40 text-emerald-300"
            }`}
          >
            <div>
              <div className="text-xs uppercase font-mono tracking-wider opacity-80">
                ML Classification Result
              </div>
              <div className="text-lg font-bold">
                {record.predicted_label} {isAnomaly ? "(Anomalous Traffic Flow)" : "(Normal Traffic Flow)"}
              </div>
            </div>
            <div className="text-right">
              <div className="text-xs uppercase font-mono tracking-wider opacity-80">
                Confidence / Score
              </div>
              <div className="text-lg font-mono font-bold">
                {(record.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Flow Features Grid */}
          <div>
            <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
              <Activity className="w-4 h-4 text-cyan-400" /> Network Flow Metrics
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-2 gap-3">
              {features.map((f, i) => (
                <div
                  key={i}
                  className="bg-[#080c17] p-3 rounded-lg border border-[#1e293b] flex flex-col justify-between"
                >
                  <span className="text-[11px] text-slate-400 font-medium">{f.label}</span>
                  <span className="text-sm font-mono font-semibold text-slate-200 mt-1">
                    {f.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-[#1e293b] bg-[#0b1120] flex items-center justify-between">
          <button
            onClick={() => {
              onClose();
              onAskAI(`Explain suspicious Record #${record.record_index} targeting Port ${record.destination_port} with predicted label ${record.predicted_label}. Why was it classified this way?`, record.record_index);
            }}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-indigo-600/20 transition-colors"
          >
            <BotMessageSquare className="w-4 h-4" />
            Ask AI Assistant to Analyze This Record
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
