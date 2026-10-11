import React, { useState, useEffect } from "react";
import {
  BellRing,
  AlertTriangle,
  ShieldAlert,
  CheckCircle2,
  Clock,
  Search,
  Filter,
  Save,
  MessageSquare,
  BotMessageSquare
} from "lucide-react";
import { getAlerts, updateAlert } from "../services/api";

export default function SecurityAlerts({ activeRun, onAskAI }) {
  const [alerts, setAlerts] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  // Filters
  const [statusFilter, setStatusFilter] = useState("all");
  const [severityFilter, setSeverityFilter] = useState("all");
  const [search, setSearch] = useState("");

  // Notes state
  const [notesState, setNotesState] = useState({});
  const [savedStatus, setSavedStatus] = useState({});

  const fetchAlerts = async () => {
    setIsLoading(true);
    try {
      const params = {
        run_id: activeRun?.id,
        page,
        page_size: pageSize,
      };
      if (statusFilter !== "all") params.status = statusFilter;
      if (severityFilter !== "all") params.severity = severityFilter;
      if (search.trim()) params.search = search.trim();

      const data = await getAlerts(params);
      setAlerts(data.alerts || []);
      setTotal(data.total || 0);
      setTotalPages(data.total_pages || 1);

      // Initialize notes state
      const initialNotes = {};
      data.alerts.forEach((a) => {
        initialNotes[a.id] = a.notes || "";
      });
      setNotesState(initialNotes);
    } catch (err) {
      console.error("Failed to load alerts", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, [activeRun?.id, page, pageSize, statusFilter, severityFilter]);

  const handleStatusChange = async (alertId, newStatus) => {
    try {
      await updateAlert(alertId, { investigation_status: newStatus });
      setAlerts((prev) =>
        prev.map((a) => (a.id === alertId ? { ...a, investigation_status: newStatus } : a))
      );
    } catch (err) {
      console.error("Failed to update status", err);
    }
  };

  const handleSaveNotes = async (alertId) => {
    try {
      await updateAlert(alertId, { notes: notesState[alertId] });
      setSavedStatus((prev) => ({ ...prev, [alertId]: true }));
      setTimeout(() => {
        setSavedStatus((prev) => ({ ...prev, [alertId]: false }));
      }, 2000);
    } catch (err) {
      console.error("Failed to save notes", err);
    }
  };

  const severityBadge = (sev) => {
    switch (sev) {
      case "critical":
        return "bg-rose-500/20 text-rose-400 border-rose-500/30";
      case "high":
        return "bg-orange-500/20 text-orange-400 border-orange-500/30";
      case "medium":
        return "bg-amber-500/20 text-amber-400 border-amber-500/30";
      default:
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
    }
  };

  return (
    <div className="space-y-6 pb-12 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
            <BellRing className="w-5 h-5 text-rose-400" />
            Security Operations Center (SOC) Alerts
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Triaged security incidents generated automatically from anomalous flows. Update investigation lifecycle status and attach analyst notes.
          </p>
        </div>

        {/* Status Filter Tabs */}
        <div className="flex items-center gap-1 bg-[#0f172a] p-1 rounded-lg border border-[#1e293b]">
          {["all", "New", "Investigating", "Resolved"].map((st) => (
            <button
              key={st}
              onClick={() => {
                setStatusFilter(st);
                setPage(1);
              }}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                statusFilter === st
                  ? "bg-cyan-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {st === "all" ? "All Statuses" : st}
            </button>
          ))}
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-[#0f172a] p-4 rounded-xl border border-[#1e293b] flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search alerts by title, evidence, or port..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && fetchAlerts()}
            className="w-full bg-[#080c17] text-xs text-slate-200 pl-9 pr-3 py-2 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
          />
        </div>

        <select
          value={severityFilter}
          onChange={(e) => {
            setSeverityFilter(e.target.value);
            setPage(1);
          }}
          className="bg-[#080c17] text-xs text-slate-200 px-3 py-2 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
        >
          <option value="all">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      {/* Alerts Feed */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="p-16 text-center text-xs text-slate-500 bg-[#0f172a] rounded-xl border border-[#1e293b]">
            <div className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
              Loading security alerts...
            </div>
          </div>
        ) : alerts.length > 0 ? (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-[#0f172a] rounded-xl border border-[#1e293b] p-5 shadow-xl space-y-4 hover:border-slate-700 transition-all"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#1e293b]">
                <div className="flex items-center gap-3">
                  <span
                    className={`px-2.5 py-1 rounded-full text-xs font-bold uppercase font-mono border ${severityBadge(
                      alert.severity
                    )}`}
                  >
                    {alert.severity}
                  </span>
                  <div>
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      {alert.alert_title}
                    </h3>
                    <p className="text-[11px] font-mono text-slate-400">
                      Alert ID: {alert.id.slice(0, 8)} • Flow Record #{alert.record_index} • Port {alert.destination_port}
                    </p>
                  </div>
                </div>

                {/* Status Selector */}
                <div className="flex items-center gap-3">
                  <select
                    value={alert.investigation_status}
                    onChange={(e) => handleStatusChange(alert.id, e.target.value)}
                    className={`text-xs font-semibold rounded-lg px-2.5 py-1.5 border focus:outline-none ${
                      alert.investigation_status === "New"
                        ? "bg-rose-950/40 text-rose-300 border-rose-800/50"
                        : alert.investigation_status === "Investigating"
                        ? "bg-amber-950/40 text-amber-300 border-amber-800/50"
                        : "bg-emerald-950/40 text-emerald-300 border-emerald-800/50"
                    }`}
                  >
                    <option value="New">Status: New</option>
                    <option value="Investigating">Status: Investigating</option>
                    <option value="Resolved">Status: Resolved</option>
                  </select>

                  <button
                    onClick={() =>
                      onAskAI(
                        `Investigate Alert "${alert.alert_title}" on Port ${alert.destination_port}. Evidence: ${alert.evidence_summary}. What defensive remediation steps should we take?`,
                        alert.record_index
                      )
                    }
                    className="p-1.5 rounded-lg bg-indigo-950/60 hover:bg-indigo-900/60 text-indigo-300 border border-indigo-800/40"
                    title="Ask AI about this alert"
                  >
                    <BotMessageSquare className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Evidence Summary */}
              <div className="p-3 rounded-lg bg-[#080c17] border border-[#1e293b] text-xs text-slate-300 leading-relaxed font-mono">
                <span className="text-cyan-400 font-bold">Evidence: </span>
                {alert.evidence_summary}
              </div>

              {/* Analyst Notes Field */}
              <div className="flex items-center gap-2 pt-1">
                <input
                  type="text"
                  placeholder="Attach analyst incident notes or IP block tickets..."
                  value={notesState[alert.id] || ""}
                  onChange={(e) =>
                    setNotesState((prev) => ({ ...prev, [alert.id]: e.target.value }))
                  }
                  onKeyDown={(e) => e.key === "Enter" && handleSaveNotes(alert.id)}
                  className="flex-1 bg-[#080c17] text-xs text-slate-200 px-3 py-1.5 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500"
                />
                <button
                  onClick={() => handleSaveNotes(alert.id)}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded-lg flex items-center gap-1.5 border border-slate-700 transition"
                >
                  <Save className="w-3.5 h-3.5" />
                  {savedStatus[alert.id] ? "Saved!" : "Save Note"}
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="p-16 text-center text-xs text-slate-500 bg-[#0f172a] rounded-xl border border-[#1e293b]">
            No alerts found matching the current criteria.
          </div>
        )}
      </div>
    </div>
  );
}
