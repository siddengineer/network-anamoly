import React, { useState, useEffect } from "react";
import {
  ShieldAlert,
  Search,
  Filter,
  Download,
  ChevronLeft,
  ChevronRight,
  Eye,
  CheckCircle2,
  AlertTriangle,
  RotateCcw
} from "lucide-react";
import { getDetectionResults, exportReportCsvUrl } from "../services/api";

export default function AnomalyDetection({ activeRun, onSelectRecord }) {
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  // Filters
  const [search, setSearch] = useState("");
  const [anomalyFilter, setAnomalyFilter] = useState("all");
  const [severityFilter, setSeverityFilter] = useState("all");
  const [labelFilter, setLabelFilter] = useState("all");

  const fetchRecords = async () => {
    setIsLoading(true);
    try {
      const params = {
        run_id: activeRun?.id,
        page,
        page_size: pageSize,
      };
      if (search.trim()) params.search = search.trim();
      if (anomalyFilter === "anomalies") params.is_anomaly = "true";
      if (anomalyFilter === "normal") params.is_anomaly = "false";
      if (severityFilter !== "all") params.severity = severityFilter;
      if (labelFilter !== "all") params.predicted_label = labelFilter;

      const data = await getDetectionResults(params);
      setRecords(data.records || []);
      setTotal(data.total || 0);
      setTotalPages(data.total_pages || 1);
    } catch (err) {
      console.error("Failed to load records", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, [activeRun?.id, page, pageSize, anomalyFilter, severityFilter, labelFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    fetchRecords();
  };

  const handleResetFilters = () => {
    setSearch("");
    setAnomalyFilter("all");
    setSeverityFilter("all");
    setLabelFilter("all");
    setPage(1);
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
            <ShieldAlert className="w-5 h-5 text-cyan-400" />
            Anomaly Detection & Flow Records
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Searchable, filterable network flow predictions calculated directly by the machine learning model.
          </p>
        </div>

        {activeRun && (
          <a
            href={exportReportCsvUrl(activeRun.id)}
            download
            className="flex items-center gap-2 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-[#334155] transition-colors self-start sm:self-auto"
          >
            <Download className="w-4 h-4 text-cyan-400" />
            Export Results (CSV)
          </a>
        )}
      </div>

      {/* Filter Toolbar */}
      <div className="bg-[#0f172a] p-4 rounded-xl border border-[#1e293b] space-y-3 shadow-lg">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search by label or keyword (e.g. DDoS, PortScan, FTP-Patator)..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#080c17] text-xs text-slate-200 pl-9 pr-3 py-2 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Anomaly verdict filter */}
            <select
              value={anomalyFilter}
              onChange={(e) => {
                setAnomalyFilter(e.target.value);
                setPage(1);
              }}
              className="bg-[#080c17] text-xs text-slate-200 px-3 py-2 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
            >
              <option value="all">Verdict: All Traffic</option>
              <option value="anomalies">Anomalies Only</option>
              <option value="normal">Normal Only</option>
            </select>

            {/* Severity Filter */}
            <select
              value={severityFilter}
              onChange={(e) => {
                setSeverityFilter(e.target.value);
                setPage(1);
              }}
              className="bg-[#080c17] text-xs text-slate-200 px-3 py-2 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
            >
              <option value="all">Severity: All</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>

            {/* Attack Label Filter */}
            <select
              value={labelFilter}
              onChange={(e) => {
                setLabelFilter(e.target.value);
                setPage(1);
              }}
              className="bg-[#080c17] text-xs text-slate-200 px-3 py-2 rounded-lg border border-[#1e293b] focus:outline-none focus:border-cyan-500 font-mono"
            >
              <option value="all">Label: All Signatures</option>
              <option value="BENIGN">BENIGN</option>
              <option value="DoS Hulk">DoS Hulk</option>
              <option value="DDoS">DDoS</option>
              <option value="PortScan">PortScan</option>
              <option value="FTP-Patator">FTP-Patator</option>
              <option value="SSH-Patator">SSH-Patator</option>
              <option value="ANOMALOUS">ANOMALOUS</option>
            </select>

            <button
              type="button"
              onClick={handleResetFilters}
              className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
              title="Reset filters"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>

      {/* Table Card */}
      <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#0b1120] text-slate-400 font-mono border-b border-[#1e293b]">
              <tr>
                <th className="px-4 py-3 font-medium">Record #</th>
                <th className="px-4 py-3 font-medium">Dest Port</th>
                <th className="px-4 py-3 font-medium">Flow Duration</th>
                <th className="px-4 py-3 font-medium">Total Packets</th>
                <th className="px-4 py-3 font-medium">Fwd Pkt Mean</th>
                <th className="px-4 py-3 font-medium">Predicted Class</th>
                <th className="px-4 py-3 font-medium">Score / Conf</th>
                <th className="px-4 py-3 font-medium">Severity</th>
                <th className="px-4 py-3 font-medium text-right">Inspect</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e293b] font-mono text-slate-300">
              {isLoading ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-slate-500">
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
                      Loading records...
                    </div>
                  </td>
                </tr>
              ) : records.length > 0 ? (
                records.map((r) => {
                  const isAnomaly = r.is_anomaly;
                  return (
                    <tr
                      key={r.id || r.record_index}
                      onClick={() => onSelectRecord(r)}
                      className="hover:bg-slate-800/40 cursor-pointer transition-colors"
                    >
                      <td className="px-4 py-3 text-slate-500">#{r.record_index}</td>
                      <td className="px-4 py-3 font-bold text-white">
                        <span className="px-2 py-0.5 rounded bg-slate-800 text-cyan-300 border border-slate-700">
                          {r.destination_port}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-slate-400">
                        {r.flow_duration?.toLocaleString()} µs
                      </td>
                      <td className="px-4 py-3 text-slate-300">
                        {r.total_fwd_packets + r.total_backward_packets} ({r.total_fwd_packets}F / {r.total_backward_packets}B)
                      </td>
                      <td className="px-4 py-3 text-slate-400">
                        {r.fwd_pkt_len_mean?.toFixed(1)}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`font-semibold ${
                            isAnomaly ? "text-rose-400" : "text-emerald-400"
                          }`}
                        >
                          {r.predicted_label}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-bold">
                        {(r.confidence * 100).toFixed(1)}%
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border ${severityBadge(
                            r.severity
                          )}`}
                        >
                          {r.severity}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectRecord(r);
                          }}
                          className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-slate-500">
                    No records match the current filter criteria.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-4 bg-[#0b1120] border-t border-[#1e293b] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
          <div>
            Showing <strong className="text-white">{records.length}</strong> of{" "}
            <strong className="text-white">{total.toLocaleString()}</strong> flow records
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <span>Rows per page:</span>
              <select
                value={pageSize}
                onChange={(e) => {
                  setPageSize(Number(e.target.value));
                  setPage(1);
                }}
                className="bg-[#080c17] border border-[#1e293b] text-slate-200 rounded px-2 py-1 focus:outline-none"
              >
                <option value={25}>25</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>

            <div className="flex items-center gap-1 font-mono">
              <button
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
                className="p-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="px-2">
                Page {page} / {totalPages}
              </span>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage(page + 1)}
                className="p-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
