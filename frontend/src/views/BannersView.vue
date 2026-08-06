<template>
  <div>
    <ViewHeader
      overline="Banners"
      title="Banner Intelligence"
      description="Review captured service banners and HTTP favicons."
      :refresh-loading="loading"
      @refresh="load"
    />

    <v-tabs v-model="tab" color="primary" class="mb-4">
      <v-tab value="banners" :disabled="loading">Banners</v-tab>
      <v-tab value="favicons" :disabled="loading">Favicons</v-tab>
    </v-tabs>

    <v-row density="comfortable" class="mb-3">
      <v-col cols="12" md="6">
        <v-text-field
          v-model.trim="tableFilters.query"
          label="Search"
          placeholder="IP, port, banner, URL..."
          prepend-inner-icon="mdi-magnify"
          :loading="loading"
          clearable
          variant="outlined"
          density="comfortable"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="tableFilters.proto"
          :items="protoFilterOptions"
          label="Proto"
          item-title="label"
          item-value="value"
          :loading="loading"
          clearable
          variant="outlined"
          density="comfortable"
        />
      </v-col>
      <v-col v-if="tab === 'favicons'" cols="12" md="3">
        <v-select
          v-model="tableFilters.mime"
          :items="mimeFilterOptions"
          label="MIME"
          item-title="label"
          item-value="value"
          :loading="loading"
          clearable
          variant="outlined"
          density="comfortable"
        />
      </v-col>
      <v-col cols="12" md="3" class="d-flex align-center">
        <v-btn
          color="error"
          variant="outlined"
          prepend-icon="mdi-delete-sweep-outline"
          :loading="clearing"
          :disabled="loading || clearing || !activeDatasetRows.length"
          @click="clearActiveDataset"
        >
          Clear {{ activeDatasetLabel }}
        </v-btn>
      </v-col>
    </v-row>

    <EntityTablePanel
      v-if="tab === 'banners'"
      title="Captured Banners"
      subtitle="Service responses captured by banner grabbers. Control banner collection per endpoint."
      :rows="filteredBanners"
      :columns="bannerColumns"
      :loading="loading"
      :error="error"
      :last-updated="lastUpdated"
      :live-refresh="true"
      :show-export="true"
      export-filename="porthound-banners"
      :export-rows="filteredBanners"
      empty-text="No banners found"
      @refresh="load"
    >
      <template #cell-response_plain="{ item, value }">
        <div class="banner-preview">
          <span class="banner-text">{{ value || "-" }}</span>
          <v-btn
            v-if="hasBannerText(value)"
            icon="mdi-arrow-expand"
            size="x-small"
            variant="text"
            aria-label="View full banner"
            title="View full banner"
            @click="openBannerDialog(item)"
          />
        </div>
      </template>
      <template #cell-scan_state="{ value }">
        <v-chip size="x-small" :color="scanStatusColor(value)" variant="tonal">
          {{ scanStatusLabel(value) }}
        </v-chip>
      </template>
      <template #cell-scan_progress="{ value }">
        {{ formatProgress(value) }}
      </template>
      <template #cell-actions="{ item }">
        <div class="banner-actions">
          <v-btn
            size="x-small"
            color="success"
            variant="tonal"
            :loading="isBannerActionLoading(item.port_id, 'start')"
            :disabled="loading || !item.port_id || normalizePortScanState(item.scan_state) === 'active'"
            @click="runBannerAction(item, 'start')"
          >
            Start
          </v-btn>
          <v-btn
            size="x-small"
            color="warning"
            variant="tonal"
            :loading="isBannerActionLoading(item.port_id, 'stop')"
            :disabled="loading || !item.port_id || normalizePortScanState(item.scan_state) === 'stopped'"
            @click="runBannerAction(item, 'stop')"
          >
            Stop
          </v-btn>
          <v-btn
            size="x-small"
            color="info"
            variant="tonal"
            :loading="isBannerActionLoading(item.port_id, 'restart')"
            :disabled="loading || !item.port_id"
            @click="runBannerAction(item, 'restart')"
          >
            Restart
          </v-btn>
        </div>
      </template>
    </EntityTablePanel>

    <EntityTablePanel
      v-else
      title="Captured Favicons"
      subtitle="Favicons discovered on HTTP services."
      :rows="filteredFavicons"
      :columns="faviconColumns"
      :loading="loading"
      :error="error"
      :last-updated="lastUpdated"
      :live-refresh="true"
      :show-export="true"
      export-filename="porthound-favicons"
      :export-rows="filteredFavicons"
      empty-text="No favicons found"
      @refresh="load"
    >
      <template #cell-preview="{ item }">
        <button
          type="button"
          class="favicon-button"
          :title="`Open favicon ${item.id}`"
          :aria-label="`Open favicon ${item.id}`"
          @click="openFavicon(item)"
        >
          <img :src="faviconSrc(item)" alt="favicon" class="favicon-thumb" />
        </button>
      </template>
      <template #cell-size="{ value }">
        {{ formatSize(value) }}
      </template>
      <template #cell-actions="{ item }">
        <v-btn
          size="x-small"
          color="secondary"
          variant="tonal"
          prepend-icon="mdi-download"
          @click="downloadFavicon(item)"
        >
          Raw
        </v-btn>
      </template>
    </EntityTablePanel>

    <v-dialog v-model="bannerDialog.open" max-width="960">
      <v-card class="banner-dialog">
        <v-card-title class="banner-dialog__title">
          <div>
            <div class="text-overline text-primary">Full Banner</div>
            <div class="text-h6">
              {{ bannerDialog.ip || "-" }}:{{ bannerDialog.port || "-" }}
              <span class="text-medium-emphasis">{{ bannerDialog.proto || "" }}</span>
            </div>
          </div>
          <v-btn
            icon="mdi-close"
            variant="text"
            aria-label="Close banner details"
            title="Close"
            @click="bannerDialog.open = false"
          />
        </v-card-title>
        <v-card-text>
          <pre class="banner-dialog__content">{{ bannerDialog.text || "-" }}</pre>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="secondary"
            variant="tonal"
            prepend-icon="mdi-content-copy"
            :disabled="!bannerDialog.text"
            @click="copyBannerDialogText"
          >
            Copy
          </v-btn>
          <v-btn color="primary" variant="flat" @click="bannerDialog.open = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import store from "../state/appStore";
import ViewHeader from "../components/ui/ViewHeader.vue";
import EntityTablePanel from "../components/ui/EntityTablePanel.vue";
import { downloadUrl } from "../utils/exportData";

export default {
  name: "BannersView",
  components: {
    ViewHeader,
    EntityTablePanel,
  },
  data() {
    return {
      store,
      tab: "banners",
      loading: false,
      clearing: false,
      error: "",
      lastUpdated: "",
      banners: [],
      favicons: [],
      bannerColumns: [
        { key: "id", label: "ID" },
        { key: "ip", label: "IP" },
        { key: "port", label: "Port" },
        { key: "proto", label: "Proto" },
        { key: "scan_state", label: "Scan Status" },
        { key: "scan_progress", label: "Banner Progress" },
        { key: "response_plain", label: "Banner" },
        { key: "actions", label: "Actions" },
      ],
      faviconColumns: [
        { key: "id", label: "ID" },
        { key: "ip", label: "IP" },
        { key: "port", label: "Port" },
        { key: "proto", label: "Proto" },
        { key: "preview", label: "Preview" },
        { key: "icon_url", label: "Icon URL" },
        { key: "mime_type", label: "MIME" },
        { key: "size", label: "Size" },
        { key: "actions", label: "Actions" },
      ],
      tableFilters: {
        query: "",
        proto: "",
        mime: "",
      },
      bannerActionLoading: {
        id: null,
        action: "",
      },
      bannerDialog: {
        open: false,
        ip: "",
        port: "",
        proto: "",
        text: "",
      },
      wsRefreshTimer: null,
      stopTableRefreshSubscription: null,
    };
  },
  computed: {
    apiBase() {
      return this.store.state.apiBase;
    },
    protoFilterOptions() {
      const source = this.tab === "favicons" ? this.favicons : this.banners;
      const values = [...new Set(source.map((item) => String(item.proto || "").trim().toLowerCase()))]
        .filter(Boolean)
        .sort();
      return [{ label: "All", value: "" }, ...values.map((value) => ({ label: value.toUpperCase(), value }))];
    },
    mimeFilterOptions() {
      const values = [...new Set(this.favicons.map((item) => String(item.mime_type || "").trim().toLowerCase()))]
        .filter(Boolean)
        .sort();
      return [{ label: "All", value: "" }, ...values.map((value) => ({ label: value, value }))];
    },
    filteredBanners() {
      const query = String(this.tableFilters.query || "").trim().toLowerCase();
      const proto = String(this.tableFilters.proto || "").trim().toLowerCase();
      return this.banners.filter((item) => {
        if (proto && String(item.proto || "").trim().toLowerCase() !== proto) return false;
        if (!query) return true;
        const haystack = [
          item.id,
          item.ip,
          item.port,
          item.proto,
          item.response_plain,
        ]
          .map((value) => String(value == null ? "" : value).toLowerCase())
          .join(" ");
        return haystack.includes(query);
      });
    },
    filteredFavicons() {
      const query = String(this.tableFilters.query || "").trim().toLowerCase();
      const proto = String(this.tableFilters.proto || "").trim().toLowerCase();
      const mime = String(this.tableFilters.mime || "").trim().toLowerCase();
      return this.favicons.filter((item) => {
        if (proto && String(item.proto || "").trim().toLowerCase() !== proto) return false;
        if (mime && String(item.mime_type || "").trim().toLowerCase() !== mime) return false;
        if (!query) return true;
        const haystack = [
          item.id,
          item.ip,
          item.port,
          item.proto,
          item.icon_url,
          item.mime_type,
          item.sha256,
          item.size,
        ]
          .map((value) => String(value == null ? "" : value).toLowerCase())
          .join(" ");
        return haystack.includes(query);
      });
    },
    activeDatasetRows() {
      return this.tab === "favicons" ? this.favicons : this.banners;
    },
    activeDatasetLabel() {
      return this.tab === "favicons" ? "Favicons" : "Banners";
    },
    activeDatasetEndpoint() {
      return this.tab === "favicons" ? "/favicons/" : "/banners/";
    },
  },
  watch: {
    apiBase() {
      this.load();
    },
    tab() {
      this.tableFilters.mime = "";
    },
  },
  mounted() {
    this.load();
    this.stopTableRefreshSubscription = this.store.subscribeTableRefresh(
      this.handleWsRefresh
    );
  },
  beforeUnmount() {
    if (this.wsRefreshTimer) {
      clearTimeout(this.wsRefreshTimer);
      this.wsRefreshTimer = null;
    }
    if (typeof this.stopTableRefreshSubscription === "function") {
      this.stopTableRefreshSubscription();
      this.stopTableRefreshSubscription = null;
    }
  },
  methods: {
    normalizePortScanState(value) {
      const raw = String(value || "active").trim().toLowerCase();
      if (raw === "restarting") return "restarting";
      if (raw === "stopped") return "stopped";
      return "active";
    },
    scanStatusLabel(value) {
      const status = this.normalizePortScanState(value);
      if (status === "restarting") return "restarting";
      if (status === "stopped") return "stopped";
      return "active";
    },
    scanStatusColor(value) {
      const status = this.normalizePortScanState(value);
      if (status === "restarting") return "info";
      if (status === "stopped") return "warning";
      return "success";
    },
    formatProgress(value) {
      const numeric = Number(value);
      if (!Number.isFinite(numeric)) return "-";
      return `${numeric.toFixed(0)}%`;
    },
    hasBannerText(value) {
      return String(value || "").trim().length > 0;
    },
    openBannerDialog(item) {
      this.bannerDialog = {
        open: true,
        ip: String(item?.ip || ""),
        port: String(item?.port ?? ""),
        proto: String(item?.proto || "").toUpperCase(),
        text: String(item?.response_plain || ""),
      };
    },
    copyBannerDialogText() {
      if (!this.bannerDialog.text || typeof navigator === "undefined" || !navigator.clipboard) {
        return Promise.resolve();
      }
      return navigator.clipboard.writeText(this.bannerDialog.text).catch(() => {});
    },
    isBannerActionLoading(id, action) {
      return this.bannerActionLoading.id === id && this.bannerActionLoading.action === action;
    },
    handleWsRefresh() {
      if (this.loading) return;
      if (this.wsRefreshTimer) return;
      this.wsRefreshTimer = setTimeout(() => {
        this.wsRefreshTimer = null;
        this.load({ silent: true });
      }, 350);
    },
    faviconSrc(item) {
      return this.store.apiUrl(`/favicons/raw/?id=${item.id}`);
    },
    openFavicon(item) {
      if (typeof window === "undefined") return;
      window.open(this.faviconSrc(item), "_blank", "noopener,noreferrer");
    },
    downloadFavicon(item) {
      const id = Number(item && item.id);
      if (!Number.isFinite(id) || id <= 0) return;
      const mime = String(item && item.mime_type || "").toLowerCase();
      let extension = "ico";
      if (mime.includes("png")) extension = "png";
      if (mime.includes("gif")) extension = "gif";
      if (mime.includes("jpeg") || mime.includes("jpg")) extension = "jpg";
      if (mime.includes("svg")) extension = "svg";
      downloadUrl(this.faviconSrc(item), `porthound-favicon-${id}.${extension}`);
    },
    formatSize(value) {
      const bytes = Number(value || 0);
      if (!Number.isFinite(bytes) || bytes <= 0) return "-";
      if (bytes < 1024) return `${bytes} B`;
      return `${(bytes / 1024).toFixed(1)} KB`;
    },
    runBannerAction(item, action) {
      const endpointId = Number(item && item.port_id);
      if (!Number.isFinite(endpointId) || endpointId <= 0) {
        this.error = "Banner endpoint is not linked to a port scan row";
        return Promise.resolve();
      }
      const proto = String(item && item.proto || "").trim().toUpperCase() || "endpoint";
      const ip = String(item && item.ip || "").trim() || "n/a";
      const port = String(item && item.port != null ? item.port : "").trim() || "n/a";
      if (action === "stop") {
        const ok = typeof window !== "undefined"
          ? window.confirm(`Stop banner collection for ${proto} ${ip}:${port}?`)
          : true;
        if (!ok) return Promise.resolve();
      }
      if (action === "restart") {
        const ok = typeof window !== "undefined"
          ? window.confirm(`Restart banner collection for ${proto} ${ip}:${port} and clear previous banner artifacts?`)
          : true;
        if (!ok) return Promise.resolve();
      }
      this.error = "";
      this.bannerActionLoading = { id: endpointId, action };
      return this.store
        .fetchJsonPromise("/banner/action/", {
          method: "POST",
          body: JSON.stringify({
            id: endpointId,
            action,
            clean_results: action === "restart",
          }),
        })
        .then(() => this.load())
        .catch((err) => {
          this.error = err.message || `Failed to ${action} banner scan`;
        })
        .finally(() => {
          this.bannerActionLoading = { id: null, action: "" };
        });
    },
    clearActiveDataset() {
      const label = this.activeDatasetLabel;
      const ok = typeof window !== "undefined"
        ? window.confirm(`Delete all ${label.toLowerCase()} from the local database?`)
        : true;
      if (!ok) return Promise.resolve();
      this.error = "";
      this.clearing = true;
      return this.store
        .fetchJsonPromise(this.activeDatasetEndpoint, {
          method: "DELETE",
        })
        .then(() => this.load())
        .catch((err) => {
          this.error = err.message || `Failed to clear ${label.toLowerCase()}`;
        })
        .finally(() => {
          this.clearing = false;
        });
    },
    load(options = {}) {
      const softRefresh = this.store.shouldUseSoftRefresh(options);
      if (!softRefresh) {
        this.loading = true;
      }
      this.error = "";
      return Promise.allSettled([
        this.store.fetchJsonPromise("/banners/"),
        this.store.fetchJsonPromise("/favicons/"),
      ])
        .then(([bannersRes, faviconsRes]) => {
          const errors = [];
          if (bannersRes.status === "fulfilled") {
            this.banners = this.store.extractArray(bannersRes.value);
          } else {
            if (!softRefresh) {
              this.banners = [];
            }
            errors.push(
              (bannersRes.reason && bannersRes.reason.message) ||
                "Failed to load banners"
            );
          }
          if (faviconsRes.status === "fulfilled") {
            this.favicons = this.store.extractArray(faviconsRes.value);
          } else {
            if (!softRefresh) {
              this.favicons = [];
            }
            errors.push(
              (faviconsRes.reason && faviconsRes.reason.message) ||
                "Failed to load favicons"
            );
          }
          this.lastUpdated = new Date().toLocaleTimeString();
          this.error = errors.join(" | ");
        })
        .finally(() => {
          if (!softRefresh) {
            this.loading = false;
          }
        });
    },
  },
};
</script>

<style scoped>
.banner-preview {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
}

.banner-text {
  display: inline-block;
  max-width: 480px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.banner-dialog {
  border: 1px solid rgba(106, 180, 222, 0.22);
  background: linear-gradient(180deg, rgba(8, 16, 29, 0.99), rgba(5, 12, 22, 0.99));
}

.banner-dialog__title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.banner-dialog__content {
  max-height: min(64vh, 680px);
  overflow: auto;
  margin: 0;
  padding: 14px;
  border: 1px solid rgba(130, 170, 200, 0.22);
  border-radius: 8px;
  background: rgba(3, 8, 14, 0.78);
  color: rgba(231, 242, 252, 0.94);
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.82rem;
  line-height: 1.45;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.banner-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.favicon-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border: 1px solid rgba(130, 170, 200, 0.3);
  border-radius: 8px;
  background: rgba(6, 12, 22, 0.65);
  cursor: pointer;
}

.favicon-thumb {
  width: 18px;
  height: 18px;
  object-fit: contain;
}
</style>
