<template>
  <div v-if="hasControls" class="live-refresh-control d-flex align-center ga-2">
    <v-chip
      v-if="showLive"
      size="small"
      variant="outlined"
      :color="liveEnabled ? 'success' : 'error'"
      class="live-refresh-control__chip"
    >
      <svg
        class="live-refresh-control__icon"
        :class="{ 'live-refresh-control__icon--on': liveEnabled }"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path
          d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.45 10.9 1 1 0 0 0-1.86-.74A6 6 0 1 1 12 6c1.3 0 2.54.42 3.56 1.19L13.75 9H20V2.75l-2.35 3.6Z"
          fill="currentColor"
        />
      </svg>
      {{ liveEnabled ? `Live ${selectedIntervalLabel}` : "Live off" }}
    </v-chip>

    <v-btn
      v-if="showManual"
      size="small"
      variant="outlined"
      color="primary"
      prepend-icon="mdi-refresh"
      :loading="loading"
      :disabled="loading"
      @click="emitRefresh"
    >
      {{ refreshLabel }}
    </v-btn>

    <v-menu v-if="showLive" location="bottom end" :close-on-content-click="false">
      <template #activator="{ props }">
        <v-btn
          v-bind="props"
          size="small"
          variant="outlined"
          color="secondary"
          :aria-label="menuAriaLabel"
        >
          <v-icon icon="mdi-pencil-outline" />
        </v-btn>
      </template>

      <v-card class="pa-4 live-refresh-control__menu" min-width="280" rounded="lg">
        <div class="text-subtitle-2 mb-3">Live refresh</div>

        <v-switch
          v-model="liveEnabled"
          color="primary"
          label="Enable live refresh"
          hide-details
          class="mb-3"
        />

        <v-select
          v-model="intervalMs"
          :items="intervalOptionsNormalized"
          label="Interval"
          item-title="label"
          item-value="value"
          variant="outlined"
          density="comfortable"
          hide-details
          class="mb-3"
        />

        <v-btn
          block
          variant="tonal"
          color="primary"
          prepend-icon="mdi-refresh"
          :loading="loading"
          :disabled="loading"
          @click="emitRefresh"
        >
          Refresh now
        </v-btn>

        <div class="text-caption text-medium-emphasis mt-3">
          Auto refresh only runs while the panel is idle.
        </div>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
const DEFAULT_INTERVALS = [
  { label: "5s", value: 5000 },
  { label: "10s", value: 10000 },
  { label: "15s", value: 15000 },
  { label: "30s", value: 30000 },
  { label: "1m", value: 60000 },
  { label: "5m", value: 300000 },
];

export default {
  name: "LiveRefreshControl",
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    showManual: {
      type: Boolean,
      default: true,
    },
    showLive: {
      type: Boolean,
      default: false,
    },
    refreshLabel: {
      type: String,
      default: "Refresh",
    },
    menuAriaLabel: {
      type: String,
      default: "Edit live refresh settings",
    },
    defaultIntervalMs: {
      type: Number,
      default: 5000,
    },
    intervalOptions: {
      type: Array,
      default: () => DEFAULT_INTERVALS,
    },
  },
  emits: ["refresh"],
  data() {
    return {
      liveEnabled: false,
      intervalMs: 5000,
      timerId: null,
    };
  },
  computed: {
    hasControls() {
      return this.showManual || this.showLive;
    },
    intervalOptionsNormalized() {
      const options = Array.isArray(this.intervalOptions) ? this.intervalOptions : DEFAULT_INTERVALS;
      return options
        .map((item) => {
          if (item && typeof item === "object") {
            const value = Number(item.value);
            const label = String(item.label || "").trim();
            if (!Number.isFinite(value) || value <= 0) return null;
            return { label: label || this.formatIntervalLabel(value), value };
          }
          const value = Number(item);
          if (!Number.isFinite(value) || value <= 0) return null;
          return { label: this.formatIntervalLabel(value), value };
        })
        .filter(Boolean);
    },
    selectedIntervalLabel() {
      const match = this.intervalOptionsNormalized.find((item) => Number(item.value) === Number(this.intervalMs));
      if (match) return match.label;
      return this.formatIntervalLabel(this.intervalMs);
    },
  },
  watch: {
    liveEnabled() {
      this.restartTimer(true);
    },
    intervalMs() {
      this.restartTimer(false);
    },
    showLive() {
      this.restartTimer(false);
    },
    loading() {
      if (!this.liveEnabled) return;
      if (!this.timerId) {
        this.scheduleNext();
      }
    },
    defaultIntervalMs: {
      immediate: true,
      handler(value) {
        const parsed = Number(value);
        if (Number.isFinite(parsed) && parsed > 0) {
          this.intervalMs = parsed;
        }
      },
    },
  },
  mounted() {
    if (this.showLive && this.liveEnabled) {
      this.scheduleNext();
    }
  },
  beforeUnmount() {
    this.clearTimer();
  },
  methods: {
    formatIntervalLabel(value) {
      const numeric = Number(value);
      if (!Number.isFinite(numeric) || numeric <= 0) return "5s";
      if (numeric % 60000 === 0) {
        const minutes = numeric / 60000;
        return minutes === 1 ? "1m" : `${minutes}m`;
      }
      return `${Math.round(numeric / 1000)}s`;
    },
    emitRefresh() {
      this.$emit("refresh", { silent: true });
    },
    clearTimer() {
      if (this.timerId) {
        clearTimeout(this.timerId);
        this.timerId = null;
      }
    },
    restartTimer(refreshImmediately) {
      this.clearTimer();
      if (!this.showLive || !this.liveEnabled) return;
      if (refreshImmediately && !this.loading) {
        this.emitRefresh();
      }
      this.scheduleNext();
    },
    scheduleNext() {
      this.clearTimer();
      if (!this.showLive || !this.liveEnabled) return;
      const delay = Math.max(1000, Number(this.intervalMs) || 5000);
      this.timerId = setTimeout(() => {
        this.timerId = null;
        if (this.showLive && this.liveEnabled && !this.loading) {
          this.emitRefresh();
        }
        this.scheduleNext();
      }, delay);
    },
  },
};
</script>

<style scoped>
.live-refresh-control__chip {
  gap: 7px;
  font-weight: 700;
  letter-spacing: 0;
}

.live-refresh-control__icon {
  width: 15px;
  height: 15px;
  flex: 0 0 15px;
  color: rgb(var(--v-theme-error));
  filter: drop-shadow(0 0 4px rgba(var(--v-theme-error), 0.28));
}

.live-refresh-control__icon--on {
  color: rgb(var(--v-theme-success));
  filter: drop-shadow(0 0 5px rgba(var(--v-theme-success), 0.36));
  animation: live-refresh-spin 1.6s linear infinite;
}

.live-refresh-control__menu {
  border: 1px solid rgba(104, 178, 221, 0.2);
  background: linear-gradient(180deg, rgba(7, 14, 24, 0.98), rgba(4, 10, 18, 0.98));
  box-shadow: 0 18px 38px rgba(2, 8, 14, 0.34);
}

@keyframes live-refresh-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
