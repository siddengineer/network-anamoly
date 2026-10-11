import React, { useState, useRef } from "react";
import {
  UploadCloud,
  FileSpreadsheet,
  CheckCircle2,
  AlertCircle,
  Play,
  RotateCcw,
  Cpu,
  Layers,
  Sparkles,
  ArrowRight,
  ShieldCheck
} from "lucide-react";
import { previewDataset, analyzeTraffic } from "../services/api";

export default function UploadDataset({ onAnalysisComplete }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [modelType, setModelType] = useState("random_forest");
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = async (selectedFile) => {
    if (!selectedFile) return;
    setError(null);
    setFile(selectedFile);
    setIsValidating(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const res = await previewDataset(formData);
      setPreview(res);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to validate dataset format.");
      setPreview(null);
    } finally {
      setIsValidating(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    setError(null);

    try {
      const formData = new FormData();
      if (file) {
        formData.append("file", file);
      }
      formData.append("model_type", modelType);

      const res = await analyzeTraffic(formData);
      if (onAnalysisComplete) {
        onAnalysisComplete(res);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis execution failed.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleAnalyzeDefaultDataset = async () => {
    setIsAnalyzing(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("model_type", modelType);
      const res = await analyzeTraffic(formData);
      if (onAnalysisComplete) {
        onAnalysisComplete(res);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to analyze pre-existing dataset.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
          <UploadCloud className="w-5 h-5 text-cyan-400" />
          Network Dataset Upload & Validation
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Upload real network flow datasets in Excel (.xlsx, .xls) or CSV (.csv) format. Preprocess schema, inspect sample flow records, and execute machine learning anomaly detection.
        </p>
      </div>

      {/* Quick Action: Workspace Dataset Banner */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-cyan-950/40 via-[#0f172a] to-indigo-950/40 border border-cyan-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
            <FileSpreadsheet className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              Existing Dataset Located: <span className="text-cyan-400 font-mono">CIC-IDS2017.xlsx</span>
            </h4>
            <p className="text-xs text-slate-400">
              Contains 1,000 real traffic records (Benign, DoS, DDoS, PortScan, Brute-Force signatures). Ready for instant analysis.
            </p>
          </div>
        </div>

        <button
          onClick={handleAnalyzeDefaultDataset}
          disabled={isAnalyzing}
          className="px-4 py-2.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-md shadow-cyan-900/50 flex items-center justify-center gap-2 flex-shrink-0"
        >
          {isAnalyzing ? (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <Play className="w-4 h-4 fill-current" />
          )}
          Analyze CIC-IDS2017.xlsx Now
        </button>
      </div>

      {/* Upload Drag & Drop Area */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
          dragActive
            ? "border-cyan-400 bg-cyan-500/10"
            : "border-[#1e293b] hover:border-[#334155] bg-[#0f172a]/60 hover:bg-[#0f172a]"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx,.xls,.csv"
          className="hidden"
          onChange={(e) => handleFileChange(e.target.files[0])}
        />
        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="w-14 h-14 rounded-full bg-slate-800/80 border border-slate-700 flex items-center justify-center text-cyan-400">
            <UploadCloud className="w-7 h-7" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-200">
              Drag & drop your network flow file here, or{" "}
              <span className="text-cyan-400 font-bold hover:underline">browse from device</span>
            </p>
            <p className="text-xs text-slate-500 mt-1">
              Supports Excel (.xlsx, .xls) and CSV (.csv) format • Max file size: 50MB
            </p>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="p-4 rounded-lg bg-rose-950/30 border border-rose-500/40 text-rose-300 text-xs flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Validation & Preview Section */}
      {isValidating && (
        <div className="p-6 text-center text-xs text-slate-400 flex items-center justify-center gap-2">
          <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
          Parsing headers and validating network flow features...
        </div>
      )}

      {preview && !isValidating && (
        <div className="space-y-6">
          {/* File Metadata & Schema Match Card */}
          <div className="p-5 rounded-xl bg-[#0f172a] border border-[#1e293b] space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-[#1e293b] gap-2">
              <div className="flex items-center gap-2">
                <FileSpreadsheet className="w-5 h-5 text-emerald-400" />
                <span className="text-sm font-bold text-white font-mono">{preview.filename}</span>
                <span className="text-xs text-slate-400">
                  ({(preview.file_size / 1024).toFixed(1)} KB)
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono px-2.5 py-1 rounded bg-[#080c17] text-slate-300 border border-[#1e293b]">
                  {preview.row_count.toLocaleString()} Records
                </span>
                <span className="text-xs font-mono px-2.5 py-1 rounded bg-[#080c17] text-slate-300 border border-[#1e293b]">
                  {preview.column_count} Columns
                </span>
              </div>
            </div>

            {/* Validation Verdict */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {preview.is_valid ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-rose-400" />
                )}
                <div>
                  <h4 className="text-xs font-bold text-slate-200">
                    {preview.is_valid
                      ? "Schema Validation Passed: Ready for Analysis"
                      : "Schema Incompatible: Missing Required Features"}
                  </h4>
                  <p className="text-[11px] text-slate-400">
                    {preview.is_valid
                      ? "All canonical flow duration, packet volume, and packet length attributes successfully mapped."
                      : `Missing: ${preview.missing_required.join(", ")}`}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Model Selector Card */}
          <div className="p-5 rounded-xl bg-[#0f172a] border border-[#1e293b] space-y-4">
            <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-cyan-400" /> Select Machine Learning Engine
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Random Forest Option */}
              <div
                onClick={() => setModelType("random_forest")}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  modelType === "random_forest"
                    ? "border-cyan-500 bg-cyan-950/20 text-white shadow-lg shadow-cyan-950/50"
                    : "border-[#1e293b] bg-[#080c17] text-slate-400 hover:border-slate-700"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-bold text-cyan-400">Random Forest Classifier</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300">
                    Supervised (88% Acc)
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Trained on labeled attack flows. Classifies normal versus multi-class attacks including DoS Hulk, DDoS, PortScan, FTP-Patator, and SSH-Patator with high confidence.
                </p>
              </div>

              {/* Isolation Forest Option */}
              <div
                onClick={() => setModelType("isolation_forest")}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  modelType === "isolation_forest"
                    ? "border-cyan-500 bg-cyan-950/20 text-white shadow-lg shadow-cyan-950/50"
                    : "border-[#1e293b] bg-[#080c17] text-slate-400 hover:border-slate-700"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-bold text-purple-400">Isolation Forest Detector</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300">
                    Unsupervised
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Detects statistical anomalies without relying on ground truth labels. Isolates unusual packet length and flow duration outliers in high-dimensional space.
                </p>
              </div>
            </div>

            {/* Run Analysis CTA */}
            <div className="pt-2 flex justify-end">
              <button
                onClick={handleRunAnalysis}
                disabled={!preview.is_valid || isAnalyzing}
                className="px-6 py-3 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-lg shadow-cyan-900/50 flex items-center gap-2"
              >
                {isAnalyzing ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Play className="w-4 h-4 fill-current" />
                )}
                Analyze Traffic with {modelType === "random_forest" ? "Random Forest" : "Isolation Forest"}
              </button>
            </div>
          </div>

          {/* First 10-20 Records Preview Table */}
          <div className="bg-[#0f172a] rounded-xl border border-[#1e293b] overflow-hidden shadow-xl">
            <div className="p-4 border-b border-[#1e293b] flex items-center justify-between bg-[#0b1120]">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
                Dataset Live Preview (First 20 Records)
              </h3>
              <span className="text-xs text-slate-400 font-mono">
                Raw Unprocessed Feed
              </span>
            </div>

            <div className="overflow-x-auto max-h-80">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#080c17] text-slate-400 font-mono border-b border-[#1e293b] sticky top-0">
                  <tr>
                    <th className="px-3 py-2 font-medium">#</th>
                    {preview.columns.map((col, idx) => (
                      <th key={idx} className="px-3 py-2 font-medium whitespace-nowrap">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1e293b] font-mono text-slate-300">
                  {preview.preview_records.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-slate-800/40">
                      <td className="px-3 py-2 text-slate-500">{rIdx + 1}</td>
                      {preview.columns.map((col, cIdx) => (
                        <td key={cIdx} className="px-3 py-2 whitespace-nowrap">
                          {String(row[col] ?? "")}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
