function normalizeRows(rows) {
  return Array.isArray(rows) ? rows : [];
}

function normalizeColumns(columns, rows) {
  if (Array.isArray(columns) && columns.length) {
    return columns
      .filter((column) => column && column.key && column.key !== "actions")
      .map((column) => ({
        key: String(column.key),
        label: String(column.label || column.key),
      }));
  }

  const keys = [];
  const seen = new Set();
  normalizeRows(rows).forEach((row) => {
    if (!row || typeof row !== "object") return;
    Object.keys(row).forEach((key) => {
      if (seen.has(key)) return;
      seen.add(key);
      keys.push(key);
    });
  });
  return keys.map((key) => ({ key, label: key }));
}

function getByPath(item, path) {
  if (!item || !path) return "";
  return String(path)
    .split(".")
    .reduce((acc, key) => (acc && acc[key] !== undefined ? acc[key] : undefined), item);
}

function normalizeCellValue(value) {
  if (value === null || value === undefined) return "";
  if (value instanceof Date) return value.toISOString();
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function csvEscape(value) {
  const text = normalizeCellValue(value);
  if (!/[",\n\r]/.test(text)) return text;
  return `"${text.replace(/"/g, '""')}"`;
}

function safeFilename(value) {
  const cleaned = String(value || "porthound-export")
    .trim()
    .replace(/[^a-zA-Z0-9._-]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return cleaned || "porthound-export";
}

function timestampSuffix(date = new Date()) {
  return date.toISOString().replace(/[:.]/g, "-");
}

function downloadBlob(blob, filename) {
  if (typeof window === "undefined" || typeof document === "undefined") return;
  const url = window.URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.rel = "noopener";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.setTimeout(() => window.URL.revokeObjectURL(url), 1000);
}

export function downloadRowsAsJson(filenameBase, rows) {
  const normalizedRows = normalizeRows(rows);
  const body = JSON.stringify(
    {
      exported_at: new Date().toISOString(),
      count: normalizedRows.length,
      datas: normalizedRows,
    },
    null,
    2
  );
  const blob = new Blob([body], { type: "application/json;charset=utf-8" });
  downloadBlob(blob, `${safeFilename(filenameBase)}-${timestampSuffix()}.json`);
}

export function downloadRowsAsCsv(filenameBase, rows, columns = []) {
  const normalizedRows = normalizeRows(rows);
  const normalizedColumns = normalizeColumns(columns, normalizedRows);
  const header = normalizedColumns.map((column) => csvEscape(column.label)).join(",");
  const lines = normalizedRows.map((row) =>
    normalizedColumns
      .map((column) => csvEscape(getByPath(row, column.key)))
      .join(",")
  );
  const csv = [header, ...lines].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  downloadBlob(blob, `${safeFilename(filenameBase)}-${timestampSuffix()}.csv`);
}

export function downloadUrl(url, filename) {
  if (typeof document === "undefined") return;
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = safeFilename(filename);
  anchor.rel = "noopener noreferrer";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
}
