<template>
  <v-app-bar color="transparent" flat height="76" class="top-bar">
    <v-container class="app-topbar">
      <v-btn
        icon="mdi-menu"
        variant="text"
        class="d-lg-none menu-button"
        aria-label="Open navigation menu"
        @click="$emit('open-drawer')"
      />

      <router-link to="/" class="brand-lockup">
        <span class="brand-avatar">
          <BrandMark :size="38" />
        </span>
        <span class="brand-copy">
          <span class="brand-name">PortHound</span>
          <span class="brand-tagline">Reconnaissance platform</span>
        </span>
      </router-link>

      <nav class="primary-nav d-none d-lg-flex" aria-label="Primary navigation">
        <v-btn
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          :exact="item.to === '/'"
          :prepend-icon="item.icon"
          variant="text"
          class="nav-item"
        >
          {{ item.label }}
        </v-btn>
      </nav>

      <v-spacer />

      <div class="status-rail" aria-label="Connection status">
        <v-chip
          :color="authStateColor"
          variant="tonal"
          size="small"
          prepend-icon="mdi-shield-key-outline"
          class="auth-chip d-none d-sm-flex"
          :aria-label="authStateLabel"
          @click="$emit('open-auth')"
        >
          {{ authStateLabel }}
        </v-chip>
        <v-chip
          :color="wsStateColor"
          variant="tonal"
          size="small"
          prepend-icon="mdi-access-point"
          :aria-label="wsStateLabel"
        >
          <span class="status-label">{{ wsStateLabel }}</span>
        </v-chip>
        <v-chip
          v-if="compactApiBase"
          class="d-none d-xl-flex endpoint-chip"
          variant="outlined"
          size="small"
          prepend-icon="mdi-server-network"
        >
          {{ compactApiBase }}
        </v-chip>
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
      if (value === "authenticated") return "Token ready";
      if (value === "saved") return "Token saved";
      if (value === "required") return "Token required";
      if (value === "checking") return "Checking token";
      return "Token required";
    },
    authStateColor() {
      const value = String(this.authStatus || "").trim().toLowerCase();
      if (value === "authenticated") return "success";
      if (value === "saved") return "info";
      if (value === "required") return "warning";
      if (value === "checking") return "info";
      return "warning";
    },
    wsStateLabel() {
      const value = String(this.wsStatus || "").trim().toLowerCase();
      if (value === "online") return "Realtime online";
      if (value === "connecting") return "Connecting";
      if (value === "error") return "Realtime error";
      return "Realtime offline";
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
        return parsed.host;
      } catch {
        return raw;
      }
    },
  },
};
</script>

<style scoped>
.top-bar {
  overflow: visible;
  border-bottom: 1px solid rgba(172, 210, 208, 0.1);
  background: rgba(5, 14, 17, 0.82) !important;
  backdrop-filter: blur(22px) saturate(125%);
  box-shadow: 0 10px 38px rgba(1, 7, 9, 0.18);
}

.top-bar::after {
  content: "";
  position: absolute;
  right: 0;
  bottom: -1px;
  left: 0;
  height: 1px;
  pointer-events: none;
  background: linear-gradient(90deg, transparent 5%, rgba(var(--brand-cyan-rgb), 0.42), rgba(var(--brand-blue-rgb), 0.28), transparent 95%);
}

.app-topbar {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1480px !important;
  height: 100%;
  padding-inline: 24px !important;
}

.menu-button {
  margin-right: 6px;
}

.brand-lockup {
  display: inline-flex;
  align-items: center;
  min-width: 218px;
  color: inherit;
  text-decoration: none;
}

.brand-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  flex: 0 0 42px;
  margin-right: 12px;
  overflow: hidden;
  border: 1px solid rgba(var(--brand-cyan-rgb), 0.18);
  border-radius: 13px;
  background: linear-gradient(145deg, rgba(20, 42, 46, 0.88), rgba(8, 20, 24, 0.94));
  box-shadow: inset 0 1px rgba(255, 255, 255, 0.04), 0 8px 24px rgba(1, 8, 10, 0.3);
}

.brand-copy {
  display: grid;
  min-width: 0;
  line-height: 1.1;
}

.brand-name {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.brand-tagline {
  margin-top: 5px;
  color: rgba(157, 181, 180, 0.68);
  font-size: 0.59rem;
  font-weight: 750;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.primary-nav {
  align-items: center;
  flex: 1 1 auto;
  gap: 3px;
  max-width: min(760px, 52vw);
  overflow-x: auto;
  overflow-y: hidden;
  padding: 5px;
  border: 1px solid rgba(165, 203, 201, 0.08);
  border-radius: 14px;
  background: rgba(12, 26, 30, 0.54);
  scrollbar-width: none;
}

.primary-nav::-webkit-scrollbar {
  display: none;
}

.nav-item {
  flex: 0 0 auto;
  min-width: auto;
  min-height: 38px;
  padding-inline: 12px;
  border-radius: 10px;
  color: rgba(181, 202, 201, 0.72);
}

.nav-item :deep(.v-icon) {
  font-size: 17px;
}

.nav-item.v-btn--active {
  color: var(--text-strong);
  background: rgba(var(--brand-cyan-rgb), 0.1);
  box-shadow: inset 0 0 0 1px rgba(var(--brand-cyan-rgb), 0.12);
}

.status-rail {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  min-width: 0;
}

.auth-chip {
  cursor: pointer;
}

@media (max-width: 1320px) {
  .brand-lockup {
    min-width: 180px;
  }

  .brand-tagline,
  .endpoint-chip {
    display: none !important;
  }

  .primary-nav {
    max-width: min(640px, 50vw);
  }
}

.endpoint-chip {
  max-width: 210px;
  color: rgba(194, 216, 214, 0.82);
}

@media (max-width: 1279px) {
  .brand-lockup {
    min-width: 0;
  }
}

@media (max-width: 599px) {
  .app-topbar {
    padding-inline: 10px !important;
  }

  .brand-avatar {
    width: 38px;
    height: 38px;
    flex-basis: 38px;
    margin-right: 9px;
  }

  .brand-name {
    font-size: 0.92rem;
  }

  .brand-tagline {
    display: none;
  }
}

@media (max-width: 410px) {
  .status-label {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
  }

  .status-rail :deep(.v-chip) {
    padding-inline: 8px;
  }
}
</style>
