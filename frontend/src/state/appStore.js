import { reactive } from "vue";

const state = reactive({
  apiBase: "",
  wsStatus: "offline",
  authToken: "",
  authStatus: "open",
  authError: "",
  authPromptOpen: false,
});

const STORAGE_KEY_API = "porthound.apiBase";
const STORAGE_KEY_AUTH = "porthound.apiToken";
const WS_RECONNECT_DELAY_MS = 1800;
const WS_REFRESH_THROTTLE_MS = 800;
const WS_REFRESH_EVENT_TYPES = new Set([
  "welcome",
  "scan_map_snapshot",
  "scan_map_update",
]);

const tableRefreshSubscribers = new Set();

let wsClient = null;
let wsReconnectTimer = null;
let wsRefreshTimer = null;
let wsPendingRefreshPayload = null;

function suggestApiBaseFromLocation(locationLike = null) {
  const locationRef =
    locationLike ||
    (typeof window !== "undefined" && window.location ? window.location : null);
  if (!locationRef) return "";

  const protocol = String(locationRef.protocol || "http:");
  const hostname = String(locationRef.hostname || "127.0.0.1");
  const port = String(locationRef.port || "");
  const isDevPort = port === "8080" || port === "5173" || port === "3000";
  if (isDevPort) {
    return `${protocol}//${hostname}:45678`;
  }
  return String(locationRef.origin || `${protocol}//${hostname}${port ? `:${port}` : ""}`);
}

function initApiBase() {
  if (typeof window === "undefined") {
    state.apiBase = "";
    return;
  }
  const envBase =
    typeof process !== "undefined" && process.env
      ? process.env.VUE_APP_API_BASE
      : "";
  const storedApiBase = window.localStorage
    ? window.localStorage.getItem(STORAGE_KEY_API)
    : "";
  const base = storedApiBase || envBase || suggestApiBaseFromLocation(window.location) || "";
  state.apiBase = String(base || "").replace(/\/+$/, "");
}

function setApiBase(value) {
  const cleaned = String(value || "").trim().replace(/\/+$/, "");
  state.apiBase = cleaned;
  if (typeof window !== "undefined" && window.localStorage) {
    window.localStorage.setItem(STORAGE_KEY_API, cleaned);
  }
  reconnectRealtime();
}

function readStoredAuthToken() {
  if (typeof window === "undefined" || !window.sessionStorage) {
    return "";
  }
  return String(window.sessionStorage.getItem(STORAGE_KEY_AUTH) || "").trim();
}

function persistAuthToken(token) {
  if (typeof window === "undefined" || !window.sessionStorage) {
    return;
  }
  if (token) {
    window.sessionStorage.setItem(STORAGE_KEY_AUTH, token);
    return;
  }
  window.sessionStorage.removeItem(STORAGE_KEY_AUTH);
}

function setAuthToken(token, nextStatus = null) {
  const cleaned = String(token || "").trim();
  state.authToken = cleaned;
  persistAuthToken(cleaned);
  if (nextStatus) {
    state.authStatus = nextStatus;
  } else {
    state.authStatus = cleaned ? "saved" : "open";
  }
}

function initAuth() {
  if (typeof window === "undefined") {
    state.authToken = "";
    state.authStatus = "open";
    state.authError = "";
    state.authPromptOpen = false;
    return;
  }
  const storedToken = readStoredAuthToken();
  setAuthToken(storedToken, storedToken ? "saved" : "open");
  state.authError = "";
  state.authPromptOpen = false;
}

function setAuthPromptOpen(value) {
  state.authPromptOpen = Boolean(value);
  if (!state.authPromptOpen) {
    state.authError = "";
  }
}

function openAuthPrompt(message = "") {
  state.authError = String(message || "").trim();
  state.authPromptOpen = true;
}

function closeAuthPrompt() {
  state.authPromptOpen = false;
  state.authError = "";
}

function clearAuthToken() {
  setAuthToken("", "open");
  closeAuthPrompt();
}

function apiUrl(path) {
  const base = state.apiBase ? state.apiBase.replace(/\/+$/, "") : "";
  const safePath = path && path.startsWith("/") ? path : `/${path || ""}`;
  return `${base}${safePath}`;
}

function parseJsonSafe(text) {
  try {
    return text ? JSON.parse(text) : null;
  } catch {
    return null;
  }
}

function buildHttpError(res, text, data) {
  const trimmed = (text || "").trim();
  const looksLikeHtml =
    trimmed.startsWith("<!DOCTYPE") ||
    trimmed.startsWith("<html") ||
    trimmed.startsWith("<!doctype");
  const message =
    (data && data.status) ||
    (looksLikeHtml
      ? `HTTP ${res.status} ${res.statusText}`
      : trimmed || `HTTP ${res.status} ${res.statusText}`);
  const error = new Error(message);
  error.status = res.status;
  error.payload = data;
  return error;
}

function applyAuthHeader(headers = {}, token = state.authToken) {
  const nextHeaders = { ...headers };
  const normalized = String(token || "").trim();
  if (
    normalized &&
    !Object.prototype.hasOwnProperty.call(nextHeaders, "Authorization") &&
    !Object.prototype.hasOwnProperty.call(nextHeaders, "authorization") &&
    !Object.prototype.hasOwnProperty.call(nextHeaders, "X-API-Key") &&
    !Object.prototype.hasOwnProperty.call(nextHeaders, "x-api-key")
  ) {
    nextHeaders.Authorization = `Bearer ${normalized}`;
  }
  return nextHeaders;
}

function fetchJsonPromise(path, options = {}) {
  const opts = { ...options };
  const token = Object.prototype.hasOwnProperty.call(opts, "token") ? opts.token : state.authToken;
  const attachAuth = opts.attachAuth !== false;
  const handleUnauthorized = opts.handleUnauthorized !== false;
  delete opts.token;
  delete opts.attachAuth;
  delete opts.handleUnauthorized;
  opts.headers = { ...(opts.headers || {}) };
  if (attachAuth) {
    opts.headers = applyAuthHeader(opts.headers, token);
  }
  if (
    opts.body &&
    !Object.prototype.hasOwnProperty.call(opts.headers, "Content-Type") &&
    !Object.prototype.hasOwnProperty.call(opts.headers, "content-type")
  ) {
    opts.headers["Content-Type"] = "application/json";
  }
  return fetch(apiUrl(path), opts)
    .then((res) =>
      res.text().then((text) => {
        const data = parseJsonSafe(text);
        if (!res.ok) {
          if (res.status === 401 && handleUnauthorized) {
            const message = (data && data.message) || (data && data.status) || "Unauthorized";
            openAuthPrompt(message);
            state.authStatus = "required";
            state.authError = message;
          }
          throw buildHttpError(res, text, data);
        }
        return data;
      })
    );
}

function fetchJson(path, options = {}) {
  return fetchJsonPromise(path, options);
}

function authenticateApiToken(rawToken) {
  const token = String(rawToken || "").trim();
  if (!token) {
    clearAuthToken();
    return Promise.resolve(null);
  }

  return fetchJsonPromise("/api/ws/clients", {
    method: "GET",
    token,
    attachAuth: true,
    handleUnauthorized: false,
  })
    .then((payload) => {
      setAuthToken(token, "authenticated");
      state.authError = "";
      closeAuthPrompt();
      return payload;
    })
    .catch((error) => {
      const message = String((error && error.message) || "Unable to validate API token").trim();
      state.authError = message;
      state.authPromptOpen = true;
      if ((error && error.status) === 401 && token === state.authToken) {
        state.authStatus = "required";
      } else if ((error && error.status) === 401 && !state.authToken) {
        state.authStatus = "required";
      }
      throw error;
    });
}

function extractArray(payload) {
  if (Array.isArray(payload)) return payload;
  if (payload && Array.isArray(payload.datas)) return payload.datas;
  return [];
}

function notifyTableRefresh(payload) {
  if (!tableRefreshSubscribers.size) return;
  tableRefreshSubscribers.forEach((subscriber) => {
    try {
      subscriber(payload);
    } catch {
      // ignore subscriber-level failures
    }
  });
}

function scheduleTableRefresh(payload) {
  wsPendingRefreshPayload = payload;
  if (wsRefreshTimer) return;
  wsRefreshTimer = setTimeout(() => {
    wsRefreshTimer = null;
    const pending = wsPendingRefreshPayload;
    wsPendingRefreshPayload = null;
    notifyTableRefresh(pending);
  }, WS_REFRESH_THROTTLE_MS);
}

function wsUrl() {
  let base = state.apiBase;
  if (!base && typeof window !== "undefined") {
    base = window.location.origin;
  }
  try {
    const parsed = new URL(base);
    const protocol = parsed.protocol === "https:" ? "wss:" : "ws:";
    return `${protocol}//${parsed.host}/ws/`;
  } catch {
    if (typeof window !== "undefined") {
      const protocol = window.location.protocol === "https:" ? "wss" : "ws";
      return `${protocol}://${window.location.host}/ws/`;
    }
  }
  return "ws://127.0.0.1:45678/ws/";
}

function clearReconnectTimer() {
  if (!wsReconnectTimer) return;
  clearTimeout(wsReconnectTimer);
  wsReconnectTimer = null;
}

function scheduleReconnect() {
  if (typeof window === "undefined") return;
  if (wsReconnectTimer) return;
  clearReconnectTimer();
  state.wsStatus = "offline";
  wsReconnectTimer = setTimeout(() => {
    wsReconnectTimer = null;
    connectRealtime();
  }, WS_RECONNECT_DELAY_MS);
}

function destroyRealtime() {
  clearReconnectTimer();
  if (wsRefreshTimer) {
    clearTimeout(wsRefreshTimer);
    wsRefreshTimer = null;
  }
  wsPendingRefreshPayload = null;
  if (!wsClient) {
    state.wsStatus = "offline";
    return;
  }
  const socket = wsClient;
  wsClient = null;
  try {
    socket.close();
  } catch {
    // ignore close failures
  } finally {
    state.wsStatus = "offline";
  }
}

function reconnectRealtime() {
  if (typeof window === "undefined") return;
  destroyRealtime();
  connectRealtime();
}

function connectRealtime() {
  if (typeof window === "undefined" || typeof window.WebSocket === "undefined") {
    state.wsStatus = "offline";
    return;
  }
  if (
    wsClient &&
    (wsClient.readyState === window.WebSocket.OPEN ||
      wsClient.readyState === window.WebSocket.CONNECTING)
  ) {
    return;
  }

  let socket = null;
  try {
    socket = new window.WebSocket(wsUrl());
  } catch {
    state.wsStatus = "error";
    scheduleReconnect();
    return;
  }

  wsClient = socket;
  state.wsStatus = "connecting";

  socket.addEventListener("open", () => {
    if (wsClient !== socket) return;
    clearReconnectTimer();
    state.wsStatus = "online";
    try {
      socket.send(JSON.stringify({ action: "scan_map_snapshot", limit: 300 }));
    } catch {
      state.wsStatus = "error";
    }
  });

  socket.addEventListener("message", (event) => {
    if (wsClient !== socket) return;
    const payload = parseJsonSafe(event.data);
    if (!payload || typeof payload !== "object") return;
    const type = String(payload.type || "").trim().toLowerCase();
    if (!WS_REFRESH_EVENT_TYPES.has(type)) return;
    scheduleTableRefresh({
      type,
      payload,
      receivedAt: Date.now(),
    });
  });

  socket.addEventListener("error", () => {
    if (wsClient !== socket) return;
    state.wsStatus = "error";
  });

  socket.addEventListener("close", () => {
    if (wsClient !== socket) return;
    wsClient = null;
    state.wsStatus = "offline";
    scheduleReconnect();
  });
}

function initRealtime() {
  connectRealtime();
}

function subscribeTableRefresh(handler) {
  if (typeof handler !== "function") {
    return () => {};
  }
  tableRefreshSubscribers.add(handler);
  return () => {
    tableRefreshSubscribers.delete(handler);
  };
}

export default {
  state,
  suggestApiBaseFromLocation,
  initApiBase,
  initAuth,
  initRealtime,
  setApiBase,
  setAuthPromptOpen,
  openAuthPrompt,
  closeAuthPrompt,
  clearAuthToken,
  authenticateApiToken,
  apiUrl,
  fetchJsonPromise,
  fetchJson,
  extractArray,
  reconnectRealtime,
  destroyRealtime,
  subscribeTableRefresh,
};
