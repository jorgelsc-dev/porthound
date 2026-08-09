<template>
  <div>
    <ViewHeader
      overline="Access"
      title="Frontend Authentication"
      description="Manage the security code required by PortHound frontend requests."
      :refresh-loading="loading"
      @refresh="load"
    >
      <template #actions>
        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-shield-key-outline"
          @click="store.openAuthPrompt()"
        >
          Security code
        </v-btn>
      </template>
    </ViewHeader>

    <v-row density="comfortable">
      <v-col cols="12" lg="7">
        <DataPanel
          title="Current Tab"
          subtitle="The security code stays only in memory for this browser tab."
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
              <span>Code</span>
              <strong>{{ authStateLabel }}</strong>
            </div>
            <div class="security-metric">
              <span>Realtime</span>
              <strong>{{ wsStateLabel }}</strong>
            </div>
            <div class="security-metric">
              <span>Storage</span>
              <strong>Memory</strong>
            </div>
          </div>

          <div class="row-actions mt-4">
            <v-btn
              color="primary"
              variant="flat"
              prepend-icon="mdi-shield-key-outline"
              @click="store.openAuthPrompt()"
            >
              Enter code
            </v-btn>
            <v-btn
              color="warning"
              variant="tonal"
              prepend-icon="mdi-delete-outline"
              :disabled="!hasToken"
              @click="store.clearAuthToken()"
            >
              Clear
            </v-btn>
          </div>
        </DataPanel>
      </v-col>

      <v-col cols="12" lg="5">
        <DataPanel
          title="Terminal Code"
          subtitle="PortHound prints the frontend security code when it starts."
          :show-refresh="false"
        >
          <div class="terminal-token-note">
            <v-icon icon="mdi-console" size="22" />
            <div>
              <strong>Copy the security code from your terminal.</strong>
              <span>Paste it in the dialog to unlock API and WebSocket communication in this browser.</span>
            </div>
          </div>
        </DataPanel>

        <DataPanel
          title="Runtime Control"
          subtitle="Stop the local PortHound process from this authenticated browser tab."
          :show-refresh="false"
          class="mt-4"
        >
          <v-alert type="warning" variant="tonal" class="mb-4">
            This sends a graceful shutdown request to the local backend and disconnects the current UI session.
          </v-alert>

          <div class="row-actions">
            <v-btn
              color="error"
              variant="flat"
              prepend-icon="mdi-power"
              :loading="shutdownLoading"
              :disabled="!hasToken || shutdownRequested"
              @click="requestShutdown"
            >
              Stop PortHound
            </v-btn>
          </div>

          <div v-if="shutdownMessage" class="shutdown-note mt-3">
            {{ shutdownMessage }}
          </div>
          <div v-if="shutdownError" class="shutdown-error mt-3">
            {{ shutdownError }}
          </div>
        </DataPanel>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import store from "../state/appStore";
import ViewHeader from "../components/ui/ViewHeader.vue";
import DataPanel from "../components/ui/DataPanel.vue";

export default {
  name: "SecurityView",
  components: {
    ViewHeader,
    DataPanel,
  },
  data() {
    return {
      store,
      loading: false,
      accessError: "",
      lastUpdated: "",
      shutdownLoading: false,
      shutdownRequested: false,
      shutdownMessage: "",
      shutdownError: "",
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
      if (value === "checking") return "Checking";
      return "Required";
    },
    wsStateLabel() {
      const value = String(this.store.state.wsStatus || "offline").trim().toLowerCase();
      if (value === "online") return "Online";
      if (value === "connecting") return "Connecting";
      if (value === "error") return "Error";
      return "Offline";
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    load() {
      this.loading = true;
      this.accessError = "";
      return this.store
        .fetchJsonPromise("/api/ws/clients", { handleUnauthorized: false })
        .then(() => {
          this.lastUpdated = new Date().toLocaleTimeString();
        })
        .catch((err) => {
          this.accessError = err.message || "Security code required";
        })
        .finally(() => {
          this.loading = false;
        });
    },
    requestShutdown() {
      if (this.shutdownLoading || this.shutdownRequested) return;
      this.shutdownError = "";
      const confirmed =
        typeof window === "undefined"
          ? true
          : window.confirm("Stop PortHound on this machine now?");
      if (!confirmed) return;
      this.shutdownLoading = true;
      return this.store
        .requestRuntimeShutdown()
        .then((payload) => {
          this.shutdownRequested = true;
          this.shutdownMessage =
            String((payload && payload.message) || "PortHound shutdown scheduled.").trim() ||
            "PortHound shutdown scheduled.";
        })
        .catch((err) => {
          this.shutdownError = err.message || "Unable to stop PortHound";
        })
        .finally(() => {
          this.shutdownLoading = false;
        });
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

.terminal-token-note {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  border: 1px solid rgba(var(--brand-cyan-rgb), 0.14);
  border-radius: 12px;
  padding: 14px;
  color: rgba(214, 228, 226, 0.9);
  background: rgba(var(--brand-cyan-rgb), 0.05);
}

.terminal-token-note strong,
.terminal-token-note span {
  display: block;
}

.terminal-token-note span {
  margin-top: 4px;
  color: var(--text-dim);
  line-height: 1.45;
}

.shutdown-note {
  color: rgba(214, 228, 226, 0.92);
  line-height: 1.45;
}

.shutdown-error {
  color: rgb(255, 167, 167);
  line-height: 1.45;
}

@media (max-width: 640px) {
  .security-grid {
    grid-template-columns: 1fr;
  }
}
</style>
