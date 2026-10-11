import axios from "axios";

const API = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json"
  }
});

export const getHealth = async () => {
  const res = await API.get("/health");
  return res.data;
};

export const getDashboardSummary = async (runId) => {
  const res = await API.get("/dashboard/summary", { params: { run_id: runId } });
  return res.data;
};

export const getDashboardTrends = async (runId) => {
  const res = await API.get("/dashboard/trends", { params: { run_id: runId } });
  return res.data;
};

export const previewDataset = async (formData) => {
  const res = await API.post("/datasets/preview", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return res.data;
};

export const uploadDataset = async (formData) => {
  const res = await API.post("/datasets/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return res.data;
};

export const listDatasets = async () => {
  const res = await API.get("/datasets");
  return res.data;
};

export const analyzeTraffic = async (formData) => {
  const res = await API.post("/detection/analyze", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return res.data;
};

export const getDetectionResults = async (params) => {
  const res = await API.get("/detection/results", { params });
  return res.data;
};

export const getSingleRecord = async (recordId) => {
  const res = await API.get(`/detection/results/${recordId}`);
  return res.data;
};

export const getAlerts = async (params) => {
  const res = await API.get("/alerts", { params });
  return res.data;
};

export const updateAlert = async (alertId, updateData) => {
  const res = await API.patch(`/alerts/${alertId}`, updateData);
  return res.data;
};

export const getModelPerformance = async () => {
  const res = await API.get("/models/performance");
  return res.data;
};

export const triggerRetrain = async () => {
  const res = await API.post("/models/train");
  return res.data;
};

export const getAnalysisHistory = async () => {
  const res = await API.get("/history");
  return res.data;
};

export const exportReportCsvUrl = (runId) => {
  return `/api/reports/export?run_id=${encodeURIComponent(runId)}`;
};

export const sendChatMessage = async (payload) => {
  const res = await API.post("/chat", payload);
  return res.data;
};

export const getChatHistory = async (sessionId) => {
  const res = await API.get(`/chat/history/${sessionId}`);
  return res.data;
};

export const listChatSessions = async () => {
  const res = await API.get("/chat/sessions");
  return res.data;
};

export const createChatSession = async () => {
  const res = await API.post("/chat/sessions");
  return res.data;
};

export default API;
