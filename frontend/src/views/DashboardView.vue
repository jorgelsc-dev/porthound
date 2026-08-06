<template>
  <div class="dashboard-page">
    <ViewHeader
      overline="Operational snapshot"
      title="Dashboard"
      description="Live counts, targets, and banners from the scanner backend."
      :refresh-loading="loading"
      @refresh="load"
    />

    <v-row density="comfortable" class="metric-grid">
      <v-col
        v-for="metric in metricCards"
        :key="metric.key"
        cols="12"
        sm="6"
        md="3"
      >
        <div v-if="loading" class="metric-skeleton">
          <div class="metric-skeleton__chrome">
            <div>
              <div class="metric-skeleton__line metric-skeleton__line--label"></div>
              <div class="metric-skeleton__line metric-skeleton__line--value"></div>
            </div>
            <div class="metric-skeleton__orb"></div>
          </div>
          <div class="metric-skeleton__line metric-skeleton__line--footer"></div>
        </div>
        <v-card v-else variant="flat" class="metric-card" :class="`metric-card--${metric.tone}`">
          <div class="metric-card__head">
            <div class="metric-card__label">{{ metric.label }}</div>
            <span class="metric-card__icon">
              <v-icon :icon="metric.icon" size="20" />
            </span>
          </div>
          <div class="metric-card__value">{{ metric.value }}</div>
          <div class="metric-card__footer">
            <span class="metric-card__pulse" />
            {{ metric.helper }}
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-if="error" type="error" variant="tonal" class="my-6">
      {{ error }}
    </v-alert>

    <v-row class="mt-4 dashboard-overview" density="comfortable">
      <v-col cols="12" lg="8">
        <MapPanel class="dashboard-map" />
      </v-col>
      <v-col cols="12" lg="4">
        <DataPanel
          class="command-panel"
          title="Command center"
          subtitle="Move quickly across the active workspace."
          :loading="loading"
          :show-refresh="false"
          :last-updated="lastUpdated"
        >
          <div class="quick-link-grid">
            <v-btn v-for="item in quickLinks" :key="item.to" :to="item.to" variant="text" class="quick-link">
              <span class="quick-link__icon"><v-icon :icon="item.icon" size="19" /></span>
              <span class="quick-link__copy">
                <strong>{{ item.label }}</strong>
                <small>{{ item.meta }}</small>
              </span>
              <v-icon icon="mdi-chevron-right" size="18" />
            </v-btn>
          </div>
          <v-divider class="my-5" />
          <div class="command-section-label">Protocol inventory</div>
          <div class="protocol-list">
            <v-chip v-for="chip in protocolChips" :key="chip.proto" size="small" variant="tonal" color="info">
              {{ chip.proto.toUpperCase() }}: {{ chip.count }}
            </v-chip>
            <div v-if="!protocolChips.length" class="empty-inline-state">
              <v-icon icon="mdi-lan-disconnect" size="18" />
              No protocol data yet
            </div>
          </div>
          <v-divider class="my-5" />
          <div class="command-section-label">Connection health</div>
          <div class="connection-summary">
            <div class="connection-summary__row">
              <span class="summary-icon"><v-icon icon="mdi-server-network" size="18" /></span>
              <span class="summary-copy"><small>API endpoint</small><strong>{{ apiHost }}</strong></span>
              <span class="health-dot" :class="error ? 'health-dot--idle' : 'health-dot--online'" />
            </div>
            <div class="connection-summary__row">
              <span class="summary-icon"><v-icon icon="mdi-access-point" size="18" /></span>
              <span class="summary-copy"><small>Realtime channel</small><strong>{{ realtimeLabel }}</strong></span>
              <span class="health-dot" :class="realtimeOnline ? 'health-dot--online' : 'health-dot--idle'" />
            </div>
          </div>
        </DataPanel>
      </v-col>
    </v-row>

    <v-row class="mt-4" density="comfortable">
      <v-col cols="12" md="6">
        <v-row density="comfortable" class="mb-2">
          <v-col cols="12" md="8">
            <v-text-field
              v-model.trim="targetFilters.query"
              label="Search targets"
              placeholder="network, proto, type..."
              prepend-inner-icon="mdi-magnify"
              :loading="loading"
              clearable
              variant="outlined"
              density="comfortable"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="targetFilters.proto"
              :items="targetProtoFilterOptions"
              label="Proto"
              item-title="label"
              item-value="value"
              :loading="loading"
              clearable
              variant="outlined"
              density="comfortable"
            />
          </v-col>
        </v-row>
        <EntityTablePanel
          title="Recent Targets"
          subtitle="Latest configured network scopes."
          :rows="filteredRecentTargets"
          :columns="targetColumns"
          :loading="loading"
          :error="error"
          :show-refresh="false"
          :live-refresh="true"
          empty-text="No targets"
          @refresh="load"
        >
          <template #cell-progress="{ value }">
            <ProgressCell :value="value" />
          </template>
          <template #cell-status="{ value }">
            <v-chip size="small" :color="statusColor(value)" variant="tonal">
              {{ normalizeStatus(value) }}
            </v-chip>
          </template>
          <template #cell-actions="{ item }">
            <div class="target-actions">
              <v-btn
                size="x-small"
                color="success"
                variant="tonal"
                :loading="isActionLoading(item.id, 'start')"
                :disabled="loading || normalizeStatus(item.status) === 'active'"
                @click="runTargetAction(item, 'start')"
              >
                Start
              </v-btn>
              <v-btn
                size="x-small"
                color="warning"
                variant="tonal"
                :loading="isActionLoading(item.id, 'stop')"
                :disabled="loading || normalizeStatus(item.status) === 'stopped'"
                @click="runTargetAction(item, 'stop')"
              >
                Stop
              </v-btn>
            </div>
          </template>
        </EntityTablePanel>
      </v-col>
      <v-col cols="12" md="6">
        <v-row density="comfortable" class="mb-2">
          <v-col cols="12" md="8">
            <v-text-field
              v-model.trim="bannerFilters.query"
              label="Search banners"
              placeholder="ip, banner, port..."
              prepend-inner-icon="mdi-magnify"
              :loading="loading"
              clearable
              variant="outlined"
              density="comfortable"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="bannerFilters.proto"
              :items="bannerProtoFilterOptions"
              label="Proto"
              item-title="label"
              item-value="value"
              :loading="loading"
              clearable
              variant="outlined"
              density="comfortable"
            />
          </v-col>
        </v-row>
        <EntityTablePanel
          title="Latest Banners"
          subtitle="Recent banner responses from scanned services."
          :rows="filteredRecentBanners"
          :columns="bannerColumns"
          :loading="loading"
          :error="error"
          :show-refresh="false"
          :live-refresh="true"
          empty-text="No banners"
          @refresh="load"
        >
          <template #cell-response_plain="{ item, value }">
            <div class="banner-preview">
              <span class="banner-cell">{{ value || "-" }}</span>
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
        </EntityTablePanel>
      </v-col>
    </v-row>

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
import MapPanel from "../components/MapPanel.vue";
import ViewHeader from "../components/ui/ViewHeader.vue";
import DataPanel from "../components/ui/DataPanel.vue";
import EntityTablePanel from "../components/ui/EntityTablePanel.vue";
import ProgressCell from "../components/ui/ProgressCell.vue";

export default {
  name: "DashboardView",
  components: {
    MapPanel,
    ViewHeader,
    DataPanel,
    EntityTablePanel,
    ProgressCell,
  },
  data() {
    return {
      store,
      loading: false,
      error: "",
      lastUpdated: "n/a",
      counts: {
        count_targets: 0,
        count_ports: 0,
        count_banners: 0,
      },
      targets: [],
      banners: [],
      portsByProto: {},
      wsClients: [],
      targetColumns: [
        { key: "network", label: "Network" },
        { key: "type", label: "Type" },
        { key: "proto", label: "Proto" },
        { key: "status", label: "Status" },
        { key: "progress", label: "Progress" },
        { key: "actions", label: "Actions" },
      ],
      bannerColumns: [
        { key: "ip", label: "IP" },
        { key: "port", label: "Port" },
        { key: "response_plain", label: "Banner" },
      ],
      quickLinks: [
        { label: "Targets", meta: "Manage scan scopes", to: "/targets", icon: "mdi-target" },
        { label: "Ports", meta: "Inspect open services", to: "/ports", icon: "mdi-ethernet" },
        { label: "Banners", meta: "Review service intel", to: "/banners", icon: "mdi-card-text" },
        { label: "API", meta: "Browse endpoints", to: "/api", icon: "mdi-api" },
      ],
      targetFilters: {
        query: "",
        proto: "",
      },
      bannerFilters: {
        query: "",
        proto: "",
      },
      actionLoading: {
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
    apiHost() {
      const value = String(this.apiBase || "").trim();
      if (!value) return "Current origin";
      try {
        return new URL(value).host;
      } catch {
        return value;
      }
    },
    realtimeOnline() {
      return String(this.store.state.wsStatus || "").trim().toLowerCase() === "online";
    },
    realtimeLabel() {
      const value = String(this.store.state.wsStatus || "offline").trim().toLowerCase();
      if (value === "online") return "Online";
      if (value === "connecting") return "Connecting";
      if (value === "error") return "Connection error";
      return "Offline";
    },
    metricCards() {
      return [
        {
          key: "targets",
          label: "Targets",
          value: this.counts.count_targets,
          icon: "mdi-target",
          tone: "mint",
          helper: "Configured scopes",
        },
        {
          key: "ports",
          label: "Ports",
          value: this.counts.count_ports,
          icon: "mdi-ethernet",
          tone: "sky",
          helper: "Discovered services",
        },
        {
          key: "banners",
          label: "Banners",
          value: this.counts.count_banners,
          icon: "mdi-card-text",
          tone: "blue",
          helper: "Captured responses",
        },
        {
          key: "ws",
          label: "WS Clients",
          value: this.wsClients.length,
          icon: "mdi-access-point",
          tone: "amber",
          helper: "Realtime observers",
        },
      ];
    },
    protocolChips() {
      const entries = Object.entries(this.portsByProto || {});
      return entries
        .map(([proto, rows]) => ({ proto, count: Array.isArray(rows) ? rows.length : 0 }))
        .sort((a, b) => a.proto.localeCompare(b.proto));
    },
    targetProtoFilterOptions() {
      const values = [...new Set(this.targets.map((item) => String(item.proto || "").trim().toLowerCase()))]
        .filter(Boolean)
        .sort();
      return [{ label: "All", value: "" }, ...values.map((value) => ({ label: value.toUpperCase(), value }))];
    },
    bannerProtoFilterOptions() {
      const values = [...new Set(this.banners.map((item) => String(item.proto || "").trim().toLowerCase()))]
        .filter(Boolean)
        .sort();
      return [{ label: "All", value: "" }, ...values.map((value) => ({ label: value.toUpperCase(), value }))];
    },
    filteredRecentTargets() {
      const query = String(this.targetFilters.query || "").trim().toLowerCase();
      const proto = String(this.targetFilters.proto || "").trim().toLowerCase();
      return this.targets
        .filter((item) => {
          if (proto && String(item.proto || "").trim().toLowerCase() !== proto) return false;
          if (!query) return true;
          const haystack = [
            item.network,
            item.type,
            item.proto,
            item.status,
            item.progress,
            item.port_mode,
            item.port_start,
            item.port_end,
          ]
            .map((value) => String(value == null ? "" : value).toLowerCase())
            .join(" ");
          return haystack.includes(query);
        })
        .slice(0, 6);
    },
    filteredRecentBanners() {
      const query = String(this.bannerFilters.query || "").trim().toLowerCase();
      const proto = String(this.bannerFilters.proto || "").trim().toLowerCase();
      return this.banners
        .filter((item) => {
          if (proto && String(item.proto || "").trim().toLowerCase() !== proto) return false;
          if (!query) return true;
          const haystack = [
            item.ip,
            item.port,
            item.proto,
            item.response_plain,
          ]
            .map((value) => String(value == null ? "" : value).toLowerCase())
            .join(" ");
          return haystack.includes(query);
        })
        .slice(0, 6);
    },
  },
  watch: {
    apiBase() {
      this.load();
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
    normalizeStatus(value) {
      const raw = String(value || "active").trim().toLowerCase();
      if (raw === "restarting") return "restarting";
      if (raw === "stopped") return "stopped";
      return "active";
    },
    statusColor(value) {
      const status = this.normalizeStatus(value);
      if (status === "active") return "success";
      if (status === "restarting") return "info";
      return "warning";
    },
    isActionLoading(id, action) {
      return this.actionLoading.id === id && this.actionLoading.action === action;
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
    handleWsRefresh() {
      if (this.loading) return;
      if (this.wsRefreshTimer) return;
      this.wsRefreshTimer = setTimeout(() => {
        this.wsRefreshTimer = null;
        this.load({ silent: true });
      }, 350);
    },
    extractPortsMap(rawPorts) {
      if (Array.isArray(rawPorts)) {
        return rawPorts.reduce((acc, row) => {
          const proto = String((row && row.proto) || "").trim().toLowerCase();
          if (!proto) return acc;
          if (!acc[proto]) acc[proto] = [];
          acc[proto].push(row);
          return acc;
        }, {});
      }
      if (!rawPorts || typeof rawPorts !== "object") return {};
      const mapped = {};
      Object.keys(rawPorts).forEach((proto) => {
        mapped[proto] = Array.isArray(rawPorts[proto]) ? rawPorts[proto] : [];
      });
      return mapped;
    },
    normalizeProtocols(raw) {
      const items = this.store.extractArray(raw);
      const unique = [...new Set(items.map((item) => String(item).trim().toLowerCase()))];
      return unique.filter(Boolean);
    },
    runTargetAction(item, action) {
      const targetId = Number(item && item.id);
      if (!Number.isFinite(targetId) || targetId <= 0) {
        this.error = "Invalid target id";
        return Promise.resolve();
      }
      this.error = "";
      this.actionLoading.id = targetId;
      this.actionLoading.action = action;
      return this.store
        .fetchJsonPromise("/target/action/", {
          method: "POST",
          body: JSON.stringify({
            id: targetId,
            action,
            clean_results: false,
          }),
        })
        .then(() => this.load())
        .catch((err) => {
          this.error = err.message || `Failed to ${action} target`;
        })
        .finally(() => {
          this.actionLoading.id = null;
          this.actionLoading.action = "";
        });
    },
    load(options = {}) {
      const softRefresh = this.store.shouldUseSoftRefresh(options);
      if (!softRefresh) {
        this.loading = true;
        this.error = "";
      }
      return this.store
        .fetchJsonPromise("/api/dashboard/")
        .then((dashboard) => {
          const counts = dashboard.counts || {};
          this.counts = {
            count_targets: counts.count_targets || 0,
            count_ports: counts.count_ports || 0,
            count_banners: counts.count_banners || 0,
          };
          this.targets = this.store.extractArray(dashboard.targets);
          this.banners = this.store.extractArray(dashboard.banners);
          this.wsClients = this.store.extractArray(dashboard.ws_clients);
          this.portsByProto = this.extractPortsMap(dashboard.ports);
          this.error = "";
          this.lastUpdated = new Date().toLocaleTimeString();
        })
        .catch(() =>
          Promise.all([
            this.store.fetchJsonPromise("/"),
            this.store.fetchJsonPromise("/targets/"),
            this.store.fetchJsonPromise("/banners/"),
            this.store.fetchJsonPromise("/api/ws/clients"),
            this.store.fetchJsonPromise("/protocols/"),
          ])
            .then(([counts, targets, banners, ws, protocolsRes]) => {
              const protocols = this.normalizeProtocols(protocolsRes);
              return Promise.all(
                protocols.map((proto) => this.store.fetchJsonPromise(`/ports/${proto}/`))
              ).then((portsResponses) => {
                const portsByProto = {};
                protocols.forEach((proto, index) => {
                  portsByProto[proto] = this.store.extractArray(portsResponses[index]);
                });
                this.counts = {
                  count_targets: counts.count_targets || 0,
                  count_ports: counts.count_ports || 0,
                  count_banners: counts.count_banners || 0,
                };
                this.targets = this.store.extractArray(targets);
                this.banners = this.store.extractArray(banners);
                this.wsClients = this.store.extractArray(ws);
                this.portsByProto = portsByProto;
              });
            })
            .then(() => {
              this.error = "";
              this.lastUpdated = new Date().toLocaleTimeString();
            })
            .catch((fallbackErr) => {
              if (!softRefresh) {
                this.error = fallbackErr.message || "Failed to load dashboard";
              }
            })
        )
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
.metric-card,
.metric-skeleton {
  min-height: 136px;
  border-radius: 17px;
}

.metric-card {
  --metric-rgb: var(--brand-cyan-rgb);
  position: relative;
  overflow: hidden;
  padding: 18px;
  border-color: rgba(var(--metric-rgb), 0.15);
  background:
    radial-gradient(120% 120% at 100% 0%, rgba(var(--metric-rgb), 0.1), transparent 58%),
    linear-gradient(145deg, rgba(18, 37, 42, 0.94), rgba(10, 23, 27, 0.96));
  box-shadow: 0 16px 36px rgba(1, 7, 9, 0.24), inset 0 1px rgba(255, 255, 255, 0.03);
}

.metric-card::after {
  content: "";
  position: absolute;
  inset: auto 18px 0;
  height: 2px;
  border-radius: 999px 999px 0 0;
  background: rgba(var(--metric-rgb), 0.72);
  box-shadow: 0 0 18px rgba(var(--metric-rgb), 0.28);
}

.metric-card--sky {
  --metric-rgb: var(--brand-sky-rgb);
}

.metric-card--blue {
  --metric-rgb: var(--brand-blue-rgb);
}

.metric-card--amber {
  --metric-rgb: var(--brand-amber-rgb);
}

.metric-card__head,
.metric-card__footer {
  display: flex;
  align-items: center;
}

.metric-card__head {
  justify-content: space-between;
  gap: 12px;
}

.metric-card__label {
  color: rgba(182, 204, 202, 0.72);
  font-size: 0.73rem;
  font-weight: 650;
}

.metric-card__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: 1px solid rgba(var(--metric-rgb), 0.12);
  border-radius: 12px;
  color: rgb(var(--metric-rgb));
  background: rgba(var(--metric-rgb), 0.08);
}

.metric-card__value {
  margin-top: -6px;
  color: var(--text-strong);
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 650;
  line-height: 1;
  letter-spacing: -0.045em;
}

.metric-card__footer {
  gap: 7px;
  margin-top: 10px;
  color: var(--text-dim);
  font-size: 0.65rem;
}

.metric-card__pulse {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: rgb(var(--metric-rgb));
  box-shadow: 0 0 10px rgba(var(--metric-rgb), 0.55);
}

.dashboard-map,
.command-panel {
  width: 100%;
}

.quick-link-grid {
  display: grid;
  gap: 8px;
}

.quick-link {
  width: 100%;
  height: auto !important;
  min-height: 58px;
  padding: 8px 10px !important;
  border: 1px solid rgba(164, 204, 202, 0.1);
  border-radius: 13px;
  background: rgba(5, 15, 18, 0.36);
}

.quick-link:hover {
  border-color: rgba(var(--brand-cyan-rgb), 0.22);
  background: rgba(var(--brand-cyan-rgb), 0.05);
}

.quick-link :deep(.v-btn__content) {
  width: 100%;
  justify-content: flex-start;
  gap: 11px;
}

.quick-link__icon,
.summary-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  border-radius: 10px;
  color: var(--brand-cyan);
  background: rgba(var(--brand-cyan-rgb), 0.08);
}

.quick-link__copy,
.summary-copy {
  display: grid;
  min-width: 0;
  flex: 1;
  text-align: left;
}

.quick-link__copy strong,
.summary-copy strong {
  overflow: hidden;
  color: var(--text-soft);
  font-size: 0.72rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.quick-link__copy small,
.summary-copy small {
  margin-top: 3px;
  color: var(--text-dim);
  font-size: 0.62rem;
  font-weight: 500;
}

.command-section-label {
  color: rgba(189, 211, 208, 0.82);
  font-size: 0.68rem;
  font-weight: 720;
  letter-spacing: 0.055em;
  text-transform: uppercase;
}

.protocol-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.empty-inline-state {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 9px;
  padding: 13px;
  border-radius: 12px;
  color: var(--text-dim);
  font-size: 0.7rem;
  background: rgba(5, 15, 18, 0.36);
}

.connection-summary {
  display: grid;
  gap: 8px;
  margin-top: 12px;
}

.connection-summary__row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px;
  border: 1px solid rgba(164, 204, 202, 0.08);
  border-radius: 12px;
  background: rgba(5, 15, 18, 0.32);
}

.health-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: 50%;
}

.health-dot--online {
  background: var(--brand-cyan);
  box-shadow: 0 0 10px rgba(var(--brand-cyan-rgb), 0.55);
}

.health-dot--idle {
  background: var(--brand-amber);
  box-shadow: 0 0 10px rgba(var(--brand-amber-rgb), 0.42);
}

.target-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.metric-skeleton {
  border: 1px solid rgba(106, 179, 221, 0.2);
  padding: 20px;
  background: linear-gradient(160deg, rgba(12, 20, 31, 0.92), rgba(9, 16, 26, 0.82));
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 1px 0 rgba(131, 204, 239, 0.06);
}

.metric-skeleton::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: linear-gradient(rgba(129, 181, 220, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(129, 181, 220, 0.04) 1px, transparent 1px);
  background-size: 24px 24px;
  opacity: 0.24;
}

.metric-skeleton::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    rgba(24, 40, 58, 0) 0%,
    rgba(84, 164, 210, 0.08) 35%,
    rgba(131, 233, 255, 0.2) 50%,
    rgba(24, 40, 58, 0) 82%
  );
  animation: metric-skeleton-sweep 1.5s linear infinite;
}

.metric-skeleton__chrome {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  position: relative;
  z-index: 1;
}

.metric-skeleton__orb {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: radial-gradient(circle at 35% 35%, rgba(129, 242, 255, 0.82), rgba(54, 152, 219, 0.38));
  box-shadow: inset 0 0 0 1px rgba(133, 206, 243, 0.18), 0 0 24px rgba(60, 168, 224, 0.14);
}

.metric-skeleton__line {
  height: 12px;
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    rgba(57, 106, 151, 0.36),
    rgba(112, 188, 229, 0.36),
    rgba(57, 106, 151, 0.36)
  );
  background-size: 220% 100%;
  animation: metric-skeleton-slide 1.2s ease-in-out infinite;
}

.metric-skeleton__line--label {
  width: 44%;
}

.metric-skeleton__line--value {
  width: 60%;
  margin-top: 14px;
  height: 18px;
}

.metric-skeleton__line--footer {
  width: 74%;
  margin-top: 18px;
  position: relative;
  z-index: 1;
}

.banner-preview {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
}

.banner-cell {
  display: inline-block;
  max-width: 320px;
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

@keyframes metric-skeleton-slide {
  0% {
    background-position: 120% 0;
  }
  100% {
    background-position: -120% 0;
  }
}

@keyframes metric-skeleton-sweep {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(100%);
  }
}
</style>
