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
        <div class="brand-avatar mr-3">
          <BrandMark :size="44" />
        </div>
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
          color="secondary"
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
import BrandMark from "../brand/BrandMark.vue";

export default {
  name: "AppTopBar",
  components: {
    BrandMark,
  },
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
  },
};
</script>

<style scoped>
.top-bar {
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid rgba(var(--brand-sky-rgb), 0.18);
  backdrop-filter: blur(18px) saturate(130%);
  background:
    radial-gradient(circle at 18% 0%, rgba(var(--brand-cyan-rgb), 0.14), transparent 34%),
    radial-gradient(circle at 82% 0%, rgba(var(--brand-violet-rgb), 0.16), transparent 40%),
    linear-gradient(180deg, rgba(6, 11, 18, 0.94) 0%, rgba(9, 17, 29, 0.78) 72%, rgba(9, 17, 29, 0.18) 100%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.top-bar::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(
    90deg,
    rgba(var(--brand-cyan-rgb), 0),
    rgba(var(--brand-cyan-rgb), 0.95),
    rgba(var(--brand-blue-rgb), 0.94),
    rgba(var(--brand-violet-rgb), 0.96),
    rgba(var(--brand-cyan-rgb), 0)
  );
  pointer-events: none;
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

.brand-avatar {
  width: 44px;
  height: 44px;
  flex: 0 0 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  border: 1px solid rgba(var(--brand-cyan-rgb), 0.22);
  background:
    radial-gradient(circle at 24% 22%, rgba(var(--brand-cyan-rgb), 0.14), transparent 44%),
    linear-gradient(145deg, rgba(10, 16, 27, 0.92), rgba(7, 12, 21, 0.86));
  box-shadow:
    0 0 0 1px rgba(var(--brand-violet-rgb), 0.12),
    0 0 18px rgba(var(--brand-cyan-rgb), 0.16);
  overflow: hidden;
}

.brand-copy {
  min-width: 0;
}

.brand-copy .text-subtitle-1 {
  letter-spacing: 0.04em;
}

.brand-copy .text-caption {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.68rem !important;
}

.top-tabs :deep(.v-tab) {
  min-width: 72px;
  font-weight: 650;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.top-tabs :deep(.v-tab--selected) {
  color: rgba(var(--brand-cyan-rgb), 0.98);
  text-shadow: 0 0 14px rgba(var(--brand-cyan-rgb), 0.18);
}

.status-rail {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
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
