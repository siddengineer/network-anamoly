import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import RecordModal from "./components/RecordModal";

// Pages
import Overview from "./pages/Overview";
import UploadDataset from "./pages/UploadDataset";
import TrafficAnalytics from "./pages/TrafficAnalytics";
import AnomalyDetection from "./pages/AnomalyDetection";
import SecurityAlerts from "./pages/SecurityAlerts";
import AICyberAssistant from "./pages/AICyberAssistant";
import ModelPerformance from "./pages/ModelPerformance";
import AnalysisHistory from "./pages/AnalysisHistory";
import Settings from "./pages/Settings";

// API
import {
  getHealth,
  getDashboardSummary,
  getDashboardTrends,
  getAnalysisHistory
} from "./services/api";

export default function App() {
  const [currentTab, setCurrentTab] = useState("overview");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Core Data State
  const [health, setHealth] = useState(null);
  const [historyRuns, setHistoryRuns] = useState([]);
  const [activeRun, setActiveRun] = useState(null);
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState(null);

  // Record Inspection Modal State
  const [selectedRecord, setSelectedRecord] = useState(null);

  // Chat Query handover
  const [chatInitialQuery, setChatInitialQuery] = useState("");
  const [chatRecordIndex, setChatRecordIndex] = useState(null);

  // Initial Fetch
  const loadGlobalData = async (preferredRunId = null) => {
    try {
      const h = await getHealth();
      setHealth(h);

      const history = await getAnalysisHistory();
      setHistoryRuns(history);

      let targetRun = null;
      if (preferredRunId) {
        targetRun = history.find((r) => r.id === preferredRunId);
      }
      if (!targetRun && history && history.length > 0) {
        targetRun = history[0];
      }
      setActiveRun(targetRun || null);

      if (targetRun) {
        const sum = await getDashboardSummary(targetRun.id);
        setSummary(sum);

        const tr = await getDashboardTrends(targetRun.id);
        setTrends(tr);
      }
    } catch (err) {
      console.error("Failed to load initial data", err);
    }
  };

  useEffect(() => {
    loadGlobalData();
  }, []);

  const handleSelectRun = async (runId) => {
    const target = historyRuns.find((r) => r.id === runId);
    if (target) {
      setActiveRun(target);
      try {
        const sum = await getDashboardSummary(target.id);
        setSummary(sum);
        const tr = await getDashboardTrends(target.id);
        setTrends(tr);
      } catch (err) {
        console.error("Failed to switch run", err);
      }
    }
  };

  const handleAnalysisComplete = async (newRun) => {
    await loadGlobalData(newRun.id);
    setCurrentTab("overview");
  };

  const handleAskAI = (query, recordIdx = null) => {
    setChatInitialQuery(query);
    setChatRecordIndex(recordIdx);
    setCurrentTab("assistant");
  };

  return (
    <div className="flex h-screen w-screen bg-[#080c17] text-slate-100 overflow-hidden font-sans">
      {/* Sidebar */}
      <Sidebar
        currentTab={currentTab}
        setCurrentTab={(tab) => {
          if (tab !== "assistant") {
            setChatInitialQuery("");
            setChatRecordIndex(null);
          }
          setCurrentTab(tab);
        }}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
        alertCount={summary?.active_alerts_count || 0}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <Header
          activeRun={activeRun}
          historyRuns={historyRuns}
          onSelectRun={handleSelectRun}
          onOpenUpload={() => setCurrentTab("upload")}
          health={health}
          onRefresh={() => loadGlobalData(activeRun?.id)}
        />

        {/* Dynamic Page Views */}
        <main className="flex-1 overflow-y-auto px-6 py-6 min-w-0">
          {currentTab === "overview" && (
            <Overview
              summary={summary}
              trends={trends}
              activeRun={activeRun}
              onNavigate={(tab) => setCurrentTab(tab)}
              onOpenUpload={() => setCurrentTab("upload")}
              onSelectRecord={(rec) => setSelectedRecord(rec)}
            />
          )}

          {currentTab === "upload" && (
            <UploadDataset onAnalysisComplete={handleAnalysisComplete} />
          )}

          {currentTab === "analytics" && (
            <TrafficAnalytics trends={trends} summary={summary} />
          )}

          {currentTab === "detection" && (
            <AnomalyDetection
              activeRun={activeRun}
              onSelectRecord={(rec) => setSelectedRecord(rec)}
            />
          )}

          {currentTab === "alerts" && (
            <SecurityAlerts
              activeRun={activeRun}
              onAskAI={(query, recIdx) => handleAskAI(query, recIdx)}
            />
          )}

          {currentTab === "assistant" && (
            <AICyberAssistant
              activeRun={activeRun}
              initialQuery={chatInitialQuery}
              recordIndex={chatRecordIndex}
            />
          )}

          {currentTab === "performance" && <ModelPerformance />}

          {currentTab === "history" && (
            <AnalysisHistory
              historyRuns={historyRuns}
              activeRun={activeRun}
              onSelectRun={handleSelectRun}
              onNavigate={(tab) => setCurrentTab(tab)}
            />
          )}

          {currentTab === "settings" && <Settings health={health} />}
        </main>
      </div>

      {/* Modal for Single Record Forensic Inspection */}
      {selectedRecord && (
        <RecordModal
          record={selectedRecord}
          onClose={() => setSelectedRecord(null)}
          onAskAI={(query, recIdx) => handleAskAI(query, recIdx)}
        />
      )}
    </div>
  );
}
