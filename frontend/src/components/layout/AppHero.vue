<template>
  <v-sheet class="hero-banner" rounded="xl">
    <v-row align="center" class="pa-6 pa-md-8">
      <v-col cols="12" md="7">
        <div class="text-overline text-primary">Network intelligence</div>
        <div class="text-h4 text-md-h3 font-weight-bold">PortHound Recon Console</div>
        <div class="text-body-1 text-medium-emphasis mt-2">
          Operational view for discovering hosts, services, and banners with
          continuous flow and precise target control.
        </div>
        <div class="d-flex flex-wrap ga-3 mt-4">
          <v-btn color="primary" variant="flat" to="/targets">Create Target</v-btn>
          <v-btn color="success" variant="outlined" to="/ports">View Ports</v-btn>
          <v-btn color="info" variant="outlined" to="/banners">View Banners</v-btn>
          <v-btn color="secondary" variant="text" to="/api">API Docs</v-btn>
        </div>
        <v-alert
          class="usage-notice mt-5"
          type="warning"
          variant="tonal"
          density="comfortable"
          icon="mdi-shield-check-outline"
        >
          Authorized use only. Run PortHound exclusively against systems, networks, and IP ranges
          for which you have explicit permission. Operators are responsible for complying with
          national regulations and the laws and rules of every country involved in the activity.
        </v-alert>
      </v-col>
      <v-col cols="12" md="5">
        <v-card variant="tonal" color="surface" class="pa-5 api-card">
          <div class="text-subtitle-2 font-weight-medium">API Base</div>
          <div class="text-caption text-medium-emphasis">
            Override the active API endpoint when the dashboard and backend are not on the same
            origin.
          </div>
          <v-text-field
            class="mt-3"
            :model-value="apiBaseDraft"
            label="API base URL"
            placeholder="http://127.0.0.1:45678"
            variant="outlined"
            density="comfortable"
            hide-details="auto"
            autocapitalize="off"
            spellcheck="false"
            @update:model-value="$emit('update:api-base-draft', $event)"
          />
          <div class="d-flex flex-wrap ga-2 mt-3">
            <v-btn
              color="primary"
              variant="flat"
              size="small"
              prepend-icon="mdi-content-save"
              @click="$emit('save-api-base')"
            >
              Save Endpoint
            </v-btn>
            <v-btn
              color="secondary"
              variant="outlined"
              size="small"
              prepend-icon="mdi-restore"
              @click="$emit('reset-api-base')"
            >
              Reset
            </v-btn>
          </div>
          <v-divider class="my-4" />
          <div class="text-subtitle-2 font-weight-medium">Direct Access</div>
          <div class="text-caption text-medium-emphasis">
            Open the active PortHound endpoint directly from here.
          </div>
          <div class="text-body-2 font-weight-medium mt-4 direct-link-value">
            {{ appLinkLabel }}
          </div>
          <div class="d-flex flex-wrap ga-2 mt-4">
            <v-btn
              color="primary"
              variant="flat"
              :href="appLink"
              target="_blank"
              rel="noopener noreferrer"
            >
              Open Live App
            </v-btn>
          </div>
          <v-divider class="my-4" />
          <div class="text-subtitle-2 font-weight-medium">API Token</div>
          <div class="text-caption text-medium-emphasis">
            Store a local access token for protected requests.
          </div>
          <div class="d-flex flex-wrap ga-2 mt-3">
            <v-btn
              color="info"
              variant="outlined"
              size="small"
              prepend-icon="mdi-shield-key-outline"
              @click="$emit('open-auth')"
            >
              Set Token
            </v-btn>
          </div>
          <v-divider class="my-4" />
          <div class="text-subtitle-2 font-weight-medium">Support PortHound</div>
          <div class="text-caption text-medium-emphasis">
            Optional BTC donation for project maintenance.
          </div>
          <div class="btc-address mt-3">{{ btcAddress }}</div>
          <div class="d-flex flex-wrap ga-2 mt-3">
            <v-btn
              color="secondary"
              variant="flat"
              size="small"
              prepend-icon="mdi-content-copy"
              @click="copyBtcAddress"
            >
              Copy BTC
            </v-btn>
            <v-btn
              color="secondary"
              variant="outlined"
              size="small"
              prepend-icon="mdi-currency-btc"
              :href="btcExplorerLink"
              target="_blank"
              rel="noopener noreferrer"
            >
              Open BTC Link
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script>
export default {
  name: "AppHero",
  props: {
    apiBaseDraft: {
      type: String,
      default: "",
    },
    apiBaseLabel: {
      type: String,
      default: "",
    },
  },
  emits: ["open-auth", "update:api-base-draft", "save-api-base", "reset-api-base"],
  data() {
    return {
      btcAddress: "bc1q3lhxpr9yantvefmvhpd2h4lu0ykf3t45zvuve2",
    };
  },
  computed: {
    appLink() {
      const value = String(this.apiBaseLabel || "").trim();
      return value || "/";
    },
    appLinkLabel() {
      const value = String(this.appLink || "").trim();
      return value || "/";
    },
    btcExplorerLink() {
      return `https://mempool.space/address/${this.btcAddress}`;
    },
  },
  methods: {
    copyBtcAddress() {
      const value = String(this.btcAddress || "").trim();
      if (!value) return;
      if (typeof navigator === "undefined") return;
      if (!navigator.clipboard || !navigator.clipboard.writeText) return;
      navigator.clipboard.writeText(value).catch(() => {});
    },
  },
};
</script>

<style scoped>
.hero-banner {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(110% 140% at -8% -24%, rgba(52, 230, 255, 0.2), transparent 58%),
    radial-gradient(90% 110% at 110% -30%, rgba(149, 115, 255, 0.18), transparent 63%),
    linear-gradient(122deg, rgba(9, 14, 23, 0.98), rgba(7, 12, 20, 0.98));
  border: 1px solid rgba(102, 212, 255, 0.22);
  box-shadow: 0 28px 56px rgba(2, 7, 14, 0.44), inset 0 0 0 1px rgba(255, 255, 255, 0.03);
}

.hero-banner::before {
  content: "";
  position: absolute;
  left: -8%;
  right: -8%;
  bottom: -80px;
  height: 220px;
  background: radial-gradient(
    60% 100% at 50% 100%,
    rgba(149, 115, 255, 0.2),
    rgba(149, 115, 255, 0)
  );
  pointer-events: none;
}

.api-card {
  border: 1px solid rgba(102, 212, 255, 0.22);
  background: linear-gradient(180deg, rgba(14, 22, 36, 0.92), rgba(10, 15, 25, 0.84));
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.03);
}

.usage-notice {
  border: 1px solid rgba(149, 115, 255, 0.22);
  background:
    linear-gradient(180deg, rgba(23, 18, 46, 0.82), rgba(12, 15, 28, 0.64)) !important;
}

.direct-link-value {
  padding: 0.9rem 1rem;
  border-radius: 14px;
  border: 1px solid rgba(102, 212, 255, 0.18);
  background: rgba(10, 17, 27, 0.78);
  color: rgba(231, 238, 255, 0.96);
  word-break: break-all;
}

.btc-address {
  padding: 0.78rem 0.9rem;
  border-radius: 12px;
  border: 1px solid rgba(149, 115, 255, 0.22);
  background: rgba(20, 18, 40, 0.68);
  color: rgba(232, 238, 255, 0.96);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.85rem;
  word-break: break-all;
}

.hero-banner :deep(.v-btn) {
  letter-spacing: 0.04em;
}
</style>
