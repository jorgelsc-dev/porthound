<template>
  <v-app class="porthound-app">
    <AppSidebar
      :open="drawer"
      :nav-items="navItems"
      @update:open="drawer = $event"
    />

    <AppTopBar
      :nav-items="navItems"
      :auth-status="authStatus"
      :api-base-label="apiBaseLabel"
      :ws-status="wsStatus"
      @open-drawer="drawer = true"
      @open-auth="openAuthPrompt"
    />

    <v-main class="app-main">
      <v-container class="app-container">
        <AppHero
          v-if="showHero"
          :api-base-draft="apiBaseDraft"
          :api-base-label="apiBaseLabel"
          @update:api-base-draft="apiBaseDraft = $event"
          @save-api-base="applyApiBase"
          @reset-api-base="resetApiBase"
          @open-auth="openAuthPrompt"
        />

        <div :class="showHero ? 'mt-8' : 'mt-3'">
          <router-view v-slot="{ Component }">
            <transition name="view-fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </v-container>
    </v-main>

    <v-dialog
      :model-value="authPromptOpen"
      max-width="520"
      @update:model-value="store.setAuthPromptOpen($event)"
    >
      <v-card class="auth-dialog-card" rounded="xl">
        <div class="auth-dialog-topline" />
        <v-card-title class="text-h5 pt-6">API Access Token</v-card-title>
        <v-card-text class="pt-4">
          <p class="auth-dialog-copy">
            Save a local token to automatically authorize protected requests. It stays in
            `sessionStorage` and is sent as `Authorization: Bearer` when the backend requires it.
          </p>
          <v-text-field
            ref="authInput"
            v-model="accessTokenInput"
            label="Access token"
            variant="outlined"
            density="comfortable"
            autocapitalize="off"
            autocomplete="one-time-code"
            spellcheck="false"
            :error-messages="authError ? [authError] : []"
            :loading="authSubmitting"
            @keyup.enter="submitAccessToken"
          />
        </v-card-text>
        <v-card-actions class="px-6 pb-6">
          <v-btn color="secondary" variant="text" :disabled="authSubmitting" @click="store.closeAuthPrompt()">
            Close
          </v-btn>
          <v-btn
            color="secondary"
            variant="text"
            :disabled="authSubmitting"
            @click="clearAccessToken"
          >
            Clear
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            size="large"
            variant="flat"
            :loading="authSubmitting"
            @click="submitAccessToken"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import { nextTick } from "vue";
import store from "./state/appStore";
import AppSidebar from "./components/layout/AppSidebar.vue";
import AppTopBar from "./components/layout/AppTopBar.vue";
import AppHero from "./components/layout/AppHero.vue";

export default {
  name: "App",
  components: {
    AppSidebar,
    AppTopBar,
    AppHero,
  },
  data() {
    return {
      store,
      drawer: false,
      apiBaseDraft: store.state.apiBase,
      accessTokenInput: store.state.authToken,
      authSubmitting: false,
      navItems: [
        { label: "Dashboard", to: "/", icon: "mdi-view-dashboard" },
        { label: "Targets", to: "/targets", icon: "mdi-target" },
        { label: "Ports", to: "/ports", icon: "mdi-ethernet" },
        { label: "Banners", to: "/banners", icon: "mdi-card-text" },
        { label: "API", to: "/api", icon: "mdi-api" },
      ],
    };
  },
  computed: {
    apiBaseLabel() {
      return this.store.state.apiBase || "";
    },
    authError() {
      return this.store.state.authError || "";
    },
    authPromptOpen() {
      return Boolean(this.store.state.authPromptOpen);
    },
    authStatus() {
      return this.store.state.authStatus || "open";
    },
    wsStatus() {
      return this.store.state.wsStatus || "offline";
    },
    showHero() {
      const name = String((this.$route && this.$route.name) || "").toLowerCase();
      return name === "dashboard";
    },
  },
  watch: {
    "store.state.apiBase"(value) {
      this.apiBaseDraft = value;
    },
    authPromptOpen: {
      immediate: true,
      handler(isOpen) {
        if (!isOpen) return;
        this.accessTokenInput = this.store.state.authToken || this.accessTokenInput || "";
        nextTick(() => {
          const field = this.$refs.authInput;
          if (field && typeof field.focus === "function") {
            field.focus();
          }
        });
      },
    },
  },
  methods: {
    applyApiBase() {
      this.store.setApiBase(this.apiBaseDraft);
    },
    resetApiBase() {
      this.apiBaseDraft = this.store.suggestApiBaseFromLocation();
      this.store.setApiBase(this.apiBaseDraft);
    },
    openAuthPrompt() {
      this.accessTokenInput = this.store.state.authToken || this.accessTokenInput || "";
      this.store.openAuthPrompt();
    },
    submitAccessToken() {
      if (this.authSubmitting) return;
      this.authSubmitting = true;
      this.store
        .authenticateApiToken(this.accessTokenInput)
        .then(() => {
          this.accessTokenInput = this.store.state.authToken || "";
        })
        .catch(() => null)
        .finally(() => {
          this.authSubmitting = false;
        });
    },
    clearAccessToken() {
      this.accessTokenInput = "";
      this.store.clearAuthToken();
    },
  },
};
</script>

<style scoped>
.app-container {
  max-width: 1560px;
  width: 100%;
}

.app-main {
  padding-bottom: 40px;
}

.auth-dialog-card {
  overflow: hidden;
  border: 1px solid rgba(102, 212, 255, 0.22);
  background:
    radial-gradient(circle at top right, rgba(52, 230, 255, 0.12), transparent 40%),
    radial-gradient(circle at bottom left, rgba(149, 115, 255, 0.12), transparent 44%),
    linear-gradient(160deg, rgba(9, 14, 22, 0.96), rgba(12, 19, 31, 0.98));
}

.auth-dialog-topline {
  height: 6px;
  border-radius: 999px 999px 0 0;
  background: linear-gradient(90deg, rgba(52, 230, 255, 0.92), rgba(149, 115, 255, 0.92));
}

.auth-dialog-copy {
  color: rgba(210, 223, 238, 0.88);
}

.view-fade-enter-active,
.view-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.22s ease;
}

.view-fade-enter-from,
.view-fade-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

@media (max-width: 959px) {
  .app-main {
    padding-bottom: 24px;
  }
}
</style>
