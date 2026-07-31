<template>
  <div>
    <ViewHeader
      overline="Security"
      title="Security & Agents"
      description="Manage API access state, agent credentials, and cluster runtime controls."
      :refresh-loading="loading"
      @refresh="load"
    >
      <template #actions>
        <v-btn
          color="primary"
          variant="outlined"
          prepend-icon="mdi-shield-key-outline"
          @click="store.openAuthPrompt()"
        >
          Token
        </v-btn>
        <v-btn
          color="primary"
          variant="outlined"
          prepend-icon="mdi-refresh"
          :loading="loading"
          @click="load"
        >
          Refresh
        </v-btn>
      </template>
    </ViewHeader>

    <v-row density="comfortable" class="mb-4">
      <v-col cols="12" lg="6">
        <DataPanel
          title="Access State"
          subtitle="Current browser session and backend connection."
          :loading="loading"
          :error="accessError"
          :last-updated="lastUpdated"
          :show-refresh="false"
        >
          <div class="security-grid">
            <div class="security-metric">
              <span>API</span>
              <strong>{{ apiBaseLabel }}</strong>
            </div>
            <div class="security-metric">
              <span>Token</span>
              <strong>{{ authStateLabel }}</strong>
            </div>
            <div class="security-metric">
              <span>Realtime</span>
              <strong>{{ wsStateLabel }}</strong>
            </div>
            <div class="security-metric">
              <span>Storage</span>
              <strong>Session only</strong>
            </div>
          </div>
          <div class="row-actions mt-4">
            <v-btn
              color="primary"
              variant="flat"
              prepend-icon="mdi-shield-key-outline"
              @click="store.openAuthPrompt()"
            >
              Manage token
            </v-btn>
            <v-btn
              color="warning"
              variant="tonal"
              prepend-icon="mdi-delete-outline"
              :disabled="!hasToken"
              @click="store.clearAuthToken()"
            >
              Clear token
            </v-btn>
          </div>
        </DataPanel>
      </v-col>

      <v-col cols="12" lg="6">
        <DataPanel
          title="Local Agent Runtime"
          subtitle="Runtime snapshot for agent mode."
          :loading="loading"
          :error="agentStatusError"
          :last-updated="lastUpdated"
          :show-refresh="false"
        >
          <div class="security-grid">
            <div class="security-metric">
              <span>Role</span>
              <strong>{{ agentStatus.role || "-" }}</strong>
            </div>
            <div class="security-metric">
              <span>Runtime</span>
              <strong>{{ agentRuntimeAlive ? "Online" : "Offline" }}</strong>
            </div>
            <div class="security-metric">
              <span>Agent ID</span>
              <strong>{{ agentIdentity.agent_id || "-" }}</strong>
            </div>
            <div class="security-metric">
              <span>Master</span>
              <strong>{{ agentIdentity.master || "-" }}</strong>
            </div>
          </div>
        </DataPanel>
      </v-col>
    </v-row>

    <DataPanel
      title="Create Agent Credential"
      subtitle="Create or rotate token credentials for distributed workers."
      :loading="savingCredential"
      :error="credentialFormError"
      :show-refresh="false"
      class="mb-4"
    >
      <v-form @submit.prevent="createCredential">
        <v-row density="comfortable">
          <v-col cols="12" md="4">
            <v-text-field
              v-model.trim="credentialForm.agent_id"
              label="Agent ID"
              placeholder="edge-agent-01"
              variant="outlined"
              density="comfortable"
              :disabled="savingCredential"
            />
          </v-col>
          <v-col cols="12" md="5">
            <v-text-field
              v-model.trim="credentialForm.token"
              label="Custom token"
              placeholder="Leave empty to generate"
              variant="outlined"
              density="comfortable"
              autocomplete="off"
              :disabled="savingCredential"
            />
          </v-col>
          <v-col cols="12" md="3" class="d-flex align-center">
            <v-btn
              color="primary"
              variant="flat"
              type="submit"
              prepend-icon="mdi-account-key-outline"
              :loading="savingCredential"
            >
              Create
            </v-btn>
          </v-col>
        </v-row>
      </v-form>

      <div v-if="generatedCredential" class="generated-block mt-3">
        <div class="generated-block__head">
          <v-chip size="small" color="success" variant="tonal">
            {{ generatedCredential.agent_id }}
          </v-chip>
          <v-btn
            size="small"
            color="primary"
            variant="tonal"
            prepend-icon="mdi-content-copy"
            @click="copyGeneratedCommand"
          >
            Copy
          </v-btn>
        </div>
        <v-textarea
          :model-value="generatedCommand"
          readonly
          rows="4"
          auto-grow
          variant="outlined"
          density="compact"
          class="mt-3"
        />
      </div>
    </DataPanel>

    <v-row density="comfortable">
      <v-col cols="12" xl="6">
        <EntityTablePanel
          title="Agent Credentials"
          subtitle="Active tokens can register, pull tasks, and submit results."
          :rows="credentials"
          :columns="credentialColumns"
          :loading="loading"
          :error="credentialsError"
          :last-updated="lastUpdated"
          empty-text="No credentials"
          live-refresh
          @refresh="load"
        >
          <template #cell-active="{ value }">
            <v-chip size="x-small" :color="value ? 'success' : 'warning'" variant="tonal">
              {{ value ? "active" : "revoked" }}
            </v-chip>
          </template>
          <template #cell-actions="{ item }">
            <div class="row-actions">
              <v-btn
                size="x-small"
                color="info"
                variant="tonal"
                prepend-icon="mdi-rotate-right"
                :loading="isActionLoading(item.agent_id, 'rotate')"
                :disabled="loading || savingCredential"
                @click="rotateCredential(item)"
              >
                Rotate
              </v-btn>
              <v-btn
                size="x-small"
                color="warning"
                variant="tonal"
                prepend-icon="mdi-account-cancel-outline"
                :loading="isActionLoading(item.agent_id, 'revoke')"
                :disabled="loading || savingCredential || !item.active"
                @click="revokeCredential(item)"
              >
                Revoke
              </v-btn>
            </div>
          </template>
        </EntityTablePanel>
      </v-col>

      <v-col cols="12" xl="6">
        <EntityTablePanel
          title="Cluster Agents"
          subtitle="Connected workers and task leases."
          :rows="agents"
          :columns="agentColumns"
          :loading="loading"
          :error="agentsError"
          :last-updated="lastUpdated"
          empty-text="No agents"
          live-refresh
          @refresh="load"
        >
          <template #cell-status="{ value }">
            <v-chip size="x-small" :color="agentStatusColor(value)" variant="tonal">
              {{ value || "-" }}
            </v-chip>
          </template>
          <template #cell-active_tasks="{ item }">
            {{ formatTasks(item.active_tasks) }}
          </template>
          <template #cell-actions="{ item }">
            <div class="row-actions">
              <v-btn
                size="x-small"
                color="warning"
                variant="tonal"
                prepend-icon="mdi-stop-circle-outline"
                :loading="isActionLoading(item.agent_id, 'stop')"
                :disabled="loading"
                @click="controlAgent(item, 'stop')"
              >
                Stop
              </v-btn>
              <v-btn
                size="x-small"
                color="error"
                variant="tonal"
                prepend-icon="mdi-delete-outline"
                :loading="isActionLoading(item.agent_id, 'delete')"
                :disabled="loading"
                @click="controlAgent(item, 'delete')"
              >
                Delete
              </v-btn>
            </div>
          </template>
        </EntityTablePanel>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import store from "../state/appStore";
import ViewHeader from "../components/ui/ViewHeader.vue";
import DataPanel from "../components/ui/DataPanel.vue";
import EntityTablePanel from "../components/ui/EntityTablePanel.vue";

export default {
  name: "SecurityView",
  components: {
    ViewHeader,
    DataPanel,
    EntityTablePanel,
  },
  data() {
    return {
      store,
      loading: false,
      savingCredential: false,
      actionLoading: "",
      accessError: "",
      agentsError: "",
      credentialsError: "",
      agentStatusError: "",
      credentialFormError: "",
      lastUpdated: "",
      agents: [],
      credentials: [],
      agentStatus: {},
      generatedCredential: null,
      credentialForm: {
        agent_id: "",
        token: "",
      },
      credentialColumns: [
        { key: "id", label: "ID" },
        { key: "agent_id", label: "Agent ID" },
        { key: "active", label: "State" },
        { key: "last_used_at", label: "Last Used" },
        { key: "updated_at", label: "Updated" },
        { key: "actions", label: "Actions" },
      ],
      agentColumns: [
        { key: "agent_id", label: "Agent ID" },
        { key: "status", label: "Status" },
        { key: "auth_mode", label: "Auth" },
        { key: "last_seen_iso", label: "Last Seen" },
        { key: "active_tasks", label: "Tasks" },
        { key: "actions", label: "Actions" },
      ],
      wsRefreshTimer: null,
      stopTableRefreshSubscription: null,
    };
  },
  computed: {
    apiBaseLabel() {
      return this.store.state.apiBase || this.store.suggestApiBaseFromLocation();
    },
    hasToken() {
      return Boolean(String(this.store.state.authToken || "").trim());
    },
    authStateLabel() {
      const value = String(this.store.state.authStatus || "open").trim().toLowerCase();
      if (value === "authenticated") return "Validated";
      if (value === "saved") return "Saved";
      if (value === "required") return "Required";
      return "Open";
    },
    wsStateLabel() {
      const value = String(this.store.state.wsStatus || "offline").trim().toLowerCase();
      if (value === "online") return "Online";
      if (value === "connecting") return "Connecting";
      if (value === "error") return "Error";
      return "Offline";
    },
    agentRuntime() {
      return (this.agentStatus && this.agentStatus.agent_runtime) || {};
    },
    agentRuntimeAlive() {
      return Boolean(this.agentRuntime && this.agentRuntime.alive);
    },
    agentIdentity() {
      return (this.agentStatus && this.agentStatus.agent) || {};
    },
    generatedCommand() {
      const credential = this.generatedCredential || {};
      const agentId = String(credential.agent_id || "").trim();
      const token = String(credential.token || credential.agent_key || "").trim();
      const master = this.apiBaseLabel || "http://127.0.0.1:45678";
      if (!agentId || !token) return "";
      return [
        `PORTHOUND_MASTER='${master}'`,
        `PORTHOUND_AGENT_ID='${agentId}'`,
        `PORTHOUND_AGENT_TOKEN='${token}'`,
        "porthound --role agent",
      ].join(" ");
    },
  },
  watch: {
    apiBaseLabel() {
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
    handleWsRefresh() {
      if (this.loading) return;
      if (this.wsRefreshTimer) return;
      this.wsRefreshTimer = setTimeout(() => {
        this.wsRefreshTimer = null;
        this.load();
      }, 500);
    },
    isActionLoading(agentId, action) {
      return this.actionLoading === `${agentId}:${action}`;
    },
    agentStatusColor(status) {
      const normalized = String(status || "").trim().toLowerCase();
      if (normalized === "online") return "success";
      if (normalized === "stale") return "warning";
      if (normalized === "offline") return "error";
      return "grey";
    },
    formatTasks(tasks) {
      const rows = Array.isArray(tasks) ? tasks : [];
      if (!rows.length) return "-";
      return rows
        .map((item) => `#${item.master_target_id || "?"}:${item.proto || "?"}`)
        .join(", ");
    },
    extractCredential(payload) {
      if (payload && payload.credential) return payload.credential;
      return payload || {};
    },
    load() {
      this.loading = true;
      this.accessError = "";
      this.agentsError = "";
      this.credentialsError = "";
      this.agentStatusError = "";
      return Promise.allSettled([
        this.store.fetchJsonPromise("/api/cluster/agents"),
        this.store.fetchJsonPromise("/api/cluster/agent/credentials"),
        this.store.fetchJsonPromise("/api/agent/status", { handleUnauthorized: false }),
      ])
        .then(([agentsRes, credentialsRes, agentStatusRes]) => {
          if (agentsRes.status === "fulfilled") {
            this.agents = this.store.extractArray(agentsRes.value);
          } else {
            this.agents = [];
            this.agentsError = agentsRes.reason && agentsRes.reason.message
              ? agentsRes.reason.message
              : "Failed to load agents";
          }

          if (credentialsRes.status === "fulfilled") {
            this.credentials = this.store.extractArray(credentialsRes.value);
          } else {
            this.credentials = [];
            this.credentialsError = credentialsRes.reason && credentialsRes.reason.message
              ? credentialsRes.reason.message
              : "Failed to load credentials";
          }

          if (agentStatusRes.status === "fulfilled") {
            this.agentStatus = agentStatusRes.value || {};
          } else {
            this.agentStatus = {};
            this.agentStatusError = agentStatusRes.reason && agentStatusRes.reason.message
              ? agentStatusRes.reason.message
              : "Failed to load agent runtime";
          }

          this.lastUpdated = new Date().toLocaleTimeString();
        })
        .finally(() => {
          this.loading = false;
        });
    },
    createCredential() {
      this.credentialFormError = "";
      this.savingCredential = true;
      const payload = {};
      if (this.credentialForm.agent_id) payload.agent_id = this.credentialForm.agent_id;
      if (this.credentialForm.token) payload.token = this.credentialForm.token;
      return this.store
        .fetchJsonPromise("/api/cluster/agent/credentials", {
          method: "POST",
          body: JSON.stringify(payload),
        })
        .then((res) => {
          this.generatedCredential = this.extractCredential(res);
          this.credentialForm.token = "";
          return this.load();
        })
        .catch((err) => {
          this.credentialFormError = err.message || "Failed to create credential";
        })
        .finally(() => {
          this.savingCredential = false;
        });
    },
    rotateCredential(item) {
      const agentId = String(item && item.agent_id || "").trim();
      if (!agentId) return Promise.resolve();
      const ok = typeof window !== "undefined"
        ? window.confirm(`Rotate credential for ${agentId}?`)
        : true;
      if (!ok) return Promise.resolve();
      this.actionLoading = `${agentId}:rotate`;
      return this.store
        .fetchJsonPromise("/api/cluster/agent/credentials", {
          method: "POST",
          body: JSON.stringify({ agent_id: agentId }),
        })
        .then((res) => {
          this.generatedCredential = this.extractCredential(res);
          return this.load();
        })
        .catch((err) => {
          this.credentialsError = err.message || "Failed to rotate credential";
        })
        .finally(() => {
          this.actionLoading = "";
        });
    },
    revokeCredential(item) {
      const agentId = String(item && item.agent_id || "").trim();
      if (!agentId) return Promise.resolve();
      const ok = typeof window !== "undefined"
        ? window.confirm(`Revoke credential for ${agentId}?`)
        : true;
      if (!ok) return Promise.resolve();
      this.actionLoading = `${agentId}:revoke`;
      return this.store
        .fetchJsonPromise("/api/cluster/agent/credentials", {
          method: "DELETE",
          body: JSON.stringify({ id: item.id, agent_id: agentId }),
        })
        .then(() => this.load())
        .catch((err) => {
          this.credentialsError = err.message || "Failed to revoke credential";
        })
        .finally(() => {
          this.actionLoading = "";
        });
    },
    controlAgent(item, action) {
      const agentId = String(item && item.agent_id || "").trim();
      if (!agentId) return Promise.resolve();
      const ok = typeof window !== "undefined"
        ? window.confirm(`${action === "delete" ? "Delete" : "Stop"} agent ${agentId}?`)
        : true;
      if (!ok) return Promise.resolve();
      this.actionLoading = `${agentId}:${action}`;
      return this.store
        .fetchJsonPromise("/api/cluster/agent/control", {
          method: "POST",
          body: JSON.stringify({ agent_id: agentId, action }),
        })
        .then(() => this.load())
        .catch((err) => {
          this.agentsError = err.message || `Failed to ${action} agent`;
        })
        .finally(() => {
          this.actionLoading = "";
        });
    },
    copyGeneratedCommand() {
      const command = this.generatedCommand;
      if (!command || typeof navigator === "undefined" || !navigator.clipboard) return;
      navigator.clipboard.writeText(command).catch(() => null);
    },
  },
};
</script>

<style scoped>
.security-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.security-metric {
  min-width: 0;
  border: 1px solid rgba(164, 204, 202, 0.12);
  border-radius: 12px;
  padding: 12px;
  background: rgba(12, 26, 30, 0.42);
}

.security-metric span,
.security-metric strong {
  display: block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.security-metric span {
  color: var(--text-dim);
  font-size: 0.72rem;
}

.security-metric strong {
  margin-top: 6px;
  color: var(--text-strong);
  font-size: 0.92rem;
}

.row-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.generated-block {
  border: 1px solid rgba(var(--brand-cyan-rgb), 0.18);
  border-radius: 14px;
  padding: 14px;
  background: rgba(var(--brand-cyan-rgb), 0.05);
}

.generated-block__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

@media (max-width: 640px) {
  .security-grid {
    grid-template-columns: 1fr;
  }
}
</style>
