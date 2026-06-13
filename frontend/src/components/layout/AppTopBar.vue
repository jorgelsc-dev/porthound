<template>
  <v-app-bar color="transparent" flat height="74" class="top-bar">
    <v-container class="d-flex align-center app-topbar">
      <v-btn
        icon="mdi-menu"
        variant="text"
        class="d-md-none"
        aria-label="Open navigation menu"
        @click="$emit('open-drawer')"
      />
      <div class="brand-lockup">
        <v-avatar size="44" class="mr-3">
          <v-img :src="brandIconSrc" alt="PortHound" />
        </v-avatar>
        <div class="brand-copy">
          <div class="text-subtitle-1 font-weight-bold">PortHound</div>
          <div class="text-caption text-medium-emphasis">Network Scanner &amp; Banner Intel</div>
        </div>
      </div>

      <v-spacer />

      <v-tabs
        class="d-none d-md-flex top-tabs"
        color="primary"
        density="compact"
        align-with-title
      >
        <v-tab
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          :exact="item.to === '/'"
        >
          {{ item.label }}
        </v-tab>
      </v-tabs>

      <v-spacer />

      <div class="status-rail">
        <v-chip
          :color="authStateColor"
          variant="tonal"
          size="small"
          prepend-icon="mdi-shield-key-outline"
          class="auth-chip"
          @click="$emit('open-auth')"
        >
          {{ authStateLabel }}
        </v-chip>
        <v-chip
          :color="wsStateColor"
          variant="tonal"
          size="small"
          prepend-icon="mdi-access-point"
        >
          {{ wsStateLabel }}
        </v-chip>
        <v-chip
          v-if="compactApiBase"
          class="d-none d-lg-flex"
          variant="outlined"
          size="small"
          prepend-icon="mdi-link-variant"
        >
          {{ compactApiBase }}
        </v-chip>
        <v-btn
          class="d-none d-lg-flex ml-1"
          color="warning"
          variant="outlined"
          size="small"
          prepend-icon="mdi-currency-btc"
          :href="btcSupportLink"
          target="_blank"
          rel="noopener noreferrer"
        >
          Support BTC
        </v-btn>
      </div>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  name: "AppTopBar",
  props: {
    navItems: {
      type: Array,
      default: () => [],
    },
    authStatus: {
      type: String,
      default: "open",
    },
    apiBaseLabel: {
      type: String,
      default: "",
    },
    wsStatus: {
      type: String,
      default: "offline",
    },
  },
  emits: ["open-auth", "open-drawer"],
  computed: {
    authStateLabel() {
      const value = String(this.authStatus || "").trim().toLowerCase();
      if (value === "authenticated") return "Token Ready";
      if (value === "saved") return "Token Saved";
      if (value === "required") return "Token Required";
      if (value === "checking") return "Checking Token";
      return "Auth Open";
    },
    authStateColor() {
      const value = String(this.authStatus || "").trim().toLowerCase();
      if (value === "authenticated") return "success";
      if (value === "saved") return "info";
      if (value === "required") return "warning";
      if (value === "checking") return "secondary";
      return "secondary";
    },
    wsStateLabel() {
      const value = String(this.wsStatus || "").trim().toLowerCase();
      if (value === "online") return "WS Online";
      if (value === "connecting") return "WS Connecting";
      if (value === "error") return "WS Error";
      return "WS Offline";
    },
    wsStateColor() {
      const value = String(this.wsStatus || "").trim().toLowerCase();
      if (value === "online") return "success";
      if (value === "connecting") return "info";
      if (value === "error") return "error";
      return "warning";
    },
    compactApiBase() {
      const raw = String(this.apiBaseLabel || "").trim();
      if (!raw) return "";
      try {
        const parsed = new URL(raw);
        return `${parsed.protocol}//${parsed.host}`;
      } catch {
        return raw;
      }
    },
    btcSupportLink() {
      return "https://mempool.space/address/bc1q3lhxpr9yantvefmvhpd2h4lu0ykf3t45zvuve2";
    },
    brandIconSrc() {
      const base = (typeof process !== "undefined" && process.env && process.env.BASE_URL)
        ? process.env.BASE_URL
        : "/";
      return `${String(base).replace(/\/?$/, "/")}brand-icon.png`;
    },
  },
};
</script>

<style scoped>
.top-bar {
  border-bottom: 1px solid rgba(97, 176, 221, 0.2);
  backdrop-filter: blur(16px);
  background: linear-gradient(
    180deg,
    rgba(10, 16, 27, 0.93) 0%,
    rgba(10, 16, 27, 0.72) 72%,
    rgba(10, 16, 27, 0.2) 100%
  );
}

.app-topbar {
  max-width: 1560px;
  width: 100%;
}

.brand-lockup {
  display: flex;
  align-items: center;
  min-width: 0;
}

.brand-copy {
  min-width: 0;
}

.top-tabs :deep(.v-tab) {
  min-width: 72px;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.status-rail {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  min-width: 0;
  flex-wrap: wrap;
}

.auth-chip {
  cursor: pointer;
}

@media (max-width: 959px) {
  .top-bar {
    height: auto !important;
  }

  .app-topbar {
    flex-wrap: wrap;
    row-gap: 10px;
    padding-top: 10px;
    padding-bottom: 10px;
  }

  .top-tabs {
    display: none !important;
  }

  .brand-lockup {
    flex: 1 1 auto;
    min-width: 0;
  }

  .brand-copy .text-subtitle-1 {
    font-size: 0.98rem !important;
  }

  .brand-copy .text-caption {
    display: block;
    max-width: 180px;
    line-height: 1.35;
    white-space: normal;
  }

  .status-rail {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 2px;
  }

  .status-rail::-webkit-scrollbar {
    height: 4px;
  }

  .status-rail :deep(.v-chip),
  .status-rail :deep(.v-btn) {
    flex: 0 0 auto;
  }
}
</style>
