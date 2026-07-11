<template>
  <v-sheet class="hero-banner" rounded="xl">
    <div class="signal-field" aria-hidden="true">
      <span class="signal-ring signal-ring--outer" />
      <span class="signal-ring signal-ring--inner" />
      <span class="signal-sweep" />
      <span class="signal-node signal-node--one" />
      <span class="signal-node signal-node--two" />
      <span class="signal-node signal-node--three" />
    </div>

    <v-row align="stretch" class="hero-grid">
      <v-col cols="12" md="7" class="hero-copy-col">
        <div class="hero-copy">
          <div class="hero-eyebrow">
            <span class="hero-eyebrow__dot" />
            Network reconnaissance workspace
          </div>
          <h1>Know what is exposed.<br><span>Act with precision.</span></h1>
          <p class="hero-description">
            Discover hosts, inspect services, and turn raw banner data into a clear operational
            picture from one focused console.
          </p>

          <div class="hero-actions">
            <v-btn color="primary" size="large" variant="flat" to="/targets" append-icon="mdi-arrow-right">
              Create target
            </v-btn>
            <v-btn color="primary" size="large" variant="outlined" to="/ports" prepend-icon="mdi-radar">
              Explore ports
            </v-btn>
            <v-btn color="secondary" size="large" variant="text" to="/api">
              API reference
            </v-btn>
          </div>

          <div class="usage-notice">
            <span class="usage-notice__icon">
              <v-icon icon="mdi-shield-check-outline" size="19" />
            </span>
            <div>
              <strong>Operate with authorization.</strong>
              <span>Only scan systems, networks, and ranges you are explicitly permitted to assess.</span>
            </div>
          </div>
        </div>
      </v-col>

      <v-col cols="12" md="5" class="connection-col">
        <v-card variant="flat" class="connection-card">
          <div class="connection-head">
            <div class="connection-title">
              <span class="connection-icon">
                <v-icon icon="mdi-server-network" size="20" />
              </span>
              <div>
                <div class="connection-title__label">Connection center</div>
                <div class="connection-title__meta">Scanner endpoint and access</div>
              </div>
            </div>
            <v-chip color="success" size="small" variant="tonal">
              <span class="connection-dot" />
              Configured
            </v-chip>
          </div>

          <div class="field-label">API endpoint</div>
          <v-text-field
            :model-value="apiBaseDraft"
            placeholder="http://127.0.0.1:45678"
            variant="outlined"
            density="comfortable"
            hide-details="auto"
            autocapitalize="off"
            spellcheck="false"
            prepend-inner-icon="mdi-link-variant"
            @update:model-value="$emit('update:api-base-draft', $event)"
          />
          <div class="endpoint-actions">
            <v-btn color="primary" variant="flat" prepend-icon="mdi-content-save" @click="$emit('save-api-base')">
              Save endpoint
            </v-btn>
            <v-btn color="secondary" variant="text" prepend-icon="mdi-restore" @click="$emit('reset-api-base')">
              Reset
            </v-btn>
          </div>

          <div class="connection-divider" />

          <div class="connection-options">
            <a class="connection-option" :href="appLink" target="_blank" rel="noopener noreferrer">
              <span class="connection-option__icon"><v-icon icon="mdi-open-in-new" size="19" /></span>
              <span class="connection-option__copy">
                <strong>Open live app</strong>
                <small>{{ endpointHost }}</small>
              </span>
              <v-icon icon="mdi-chevron-right" size="18" />
            </a>
            <button type="button" class="connection-option" @click="$emit('open-auth')">
              <span class="connection-option__icon"><v-icon icon="mdi-shield-key-outline" size="19" /></span>
              <span class="connection-option__copy">
                <strong>Access token</strong>
                <small>Configure protected requests</small>
              </span>
              <v-icon icon="mdi-chevron-right" size="18" />
            </button>
          </div>

          <div class="support-strip">
            <span class="support-strip__icon"><v-icon icon="mdi-currency-btc" size="18" /></span>
            <span class="support-strip__copy">
              <strong>Support development</strong>
              <small>{{ compactBtcAddress }}</small>
            </span>
            <v-btn
              icon="mdi-content-copy"
              size="small"
              variant="text"
              :aria-label="copied ? 'Bitcoin address copied' : 'Copy Bitcoin address'"
              @click="copyBtcAddress"
            />
            <v-btn
              icon="mdi-open-in-new"
              size="small"
              variant="text"
              aria-label="Open Bitcoin address"
              :href="btcExplorerLink"
              target="_blank"
              rel="noopener noreferrer"
            />
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
      copied: false,
      copyTimer: null,
    };
  },
  computed: {
    appLink() {
      const value = String(this.apiBaseLabel || "").trim();
      return value || "/";
    },
    endpointHost() {
      const value = String(this.appLink || "").trim();
      try {
        return new URL(value).host;
      } catch {
        return value || "Current origin";
      }
    },
    compactBtcAddress() {
      return `${this.btcAddress.slice(0, 9)}...${this.btcAddress.slice(-6)}`;
    },
    btcExplorerLink() {
      return `https://mempool.space/address/${this.btcAddress}`;
    },
  },
  beforeUnmount() {
    if (this.copyTimer) clearTimeout(this.copyTimer);
  },
  methods: {
    copyBtcAddress() {
      const value = String(this.btcAddress || "").trim();
      if (!value || typeof navigator === "undefined") return;
      if (!navigator.clipboard || !navigator.clipboard.writeText) return;
      navigator.clipboard.writeText(value).then(() => {
        this.copied = true;
        if (this.copyTimer) clearTimeout(this.copyTimer);
        this.copyTimer = setTimeout(() => {
          this.copied = false;
          this.copyTimer = null;
        }, 1800);
      }).catch(() => {});
    },
  },
};
</script>

<style scoped>
.hero-banner {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(164, 207, 204, 0.14);
  background:
    radial-gradient(90% 130% at 0% 0%, rgba(var(--brand-cyan-rgb), 0.12), transparent 60%),
    radial-gradient(70% 100% at 100% 0%, rgba(var(--brand-blue-rgb), 0.12), transparent 64%),
    linear-gradient(135deg, rgba(10, 24, 28, 0.98), rgba(6, 16, 20, 0.98));
  box-shadow: 0 30px 72px rgba(1, 7, 9, 0.38), inset 0 1px rgba(255, 255, 255, 0.035);
}

.hero-banner::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.18;
  background-image:
    linear-gradient(rgba(172, 220, 213, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(172, 220, 213, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: linear-gradient(90deg, rgba(0, 0, 0, 0.8), transparent 72%);
}

.hero-grid {
  position: relative;
  z-index: 2;
  margin: 0;
}

.hero-copy-col,
.connection-col {
  padding: 0;
}

.hero-copy {
  display: flex;
  min-height: 100%;
  flex-direction: column;
  justify-content: center;
  padding: 54px 54px 50px;
}

.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  align-self: flex-start;
  gap: 9px;
  padding: 7px 11px;
  border: 1px solid rgba(var(--brand-cyan-rgb), 0.14);
  border-radius: 999px;
  color: rgba(191, 226, 220, 0.86);
  font-size: 0.68rem;
  font-weight: 750;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  background: rgba(var(--brand-cyan-rgb), 0.055);
}

.hero-eyebrow__dot,
.connection-dot {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: var(--brand-cyan);
  box-shadow: 0 0 12px rgba(var(--brand-cyan-rgb), 0.65);
}

.hero-copy h1 {
  max-width: 720px;
  margin: 24px 0 0;
  color: var(--text-strong);
  font-family: var(--font-heading);
  font-size: clamp(2.55rem, 4.5vw, 4.6rem);
  font-weight: 650;
  line-height: 0.98;
  letter-spacing: -0.055em;
}

.hero-copy h1 span {
  color: rgba(187, 211, 208, 0.68);
}

.hero-description {
  max-width: 640px;
  margin: 22px 0 0;
  color: rgba(181, 203, 201, 0.76);
  font-size: clamp(0.96rem, 1.4vw, 1.08rem);
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 30px;
}

.usage-notice {
  display: flex;
  max-width: 660px;
  align-items: flex-start;
  gap: 11px;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid rgba(164, 204, 202, 0.12);
  color: rgba(183, 199, 193, 0.7);
}

.usage-notice__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex: 0 0 32px;
  border-radius: 10px;
  color: var(--brand-amber);
  background: rgba(var(--brand-amber-rgb), 0.09);
}

.usage-notice strong,
.usage-notice span {
  display: block;
}

.usage-notice strong {
  color: rgba(229, 222, 205, 0.9);
  font-size: 0.78rem;
}

.usage-notice span {
  margin-top: 2px;
  font-size: 0.73rem;
  line-height: 1.5;
}

.connection-col {
  display: flex;
}

.connection-card {
  width: 100%;
  margin: 22px 22px 22px 0;
  padding: 28px;
  border: 1px solid rgba(161, 207, 202, 0.14);
  border-radius: 20px !important;
  background: linear-gradient(155deg, rgba(15, 32, 37, 0.96), rgba(8, 20, 24, 0.98));
  box-shadow: 0 24px 50px rgba(1, 7, 9, 0.28), inset 0 1px rgba(255, 255, 255, 0.035);
}

.connection-head,
.connection-title,
.support-strip {
  display: flex;
  align-items: center;
}

.connection-head {
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 26px;
}

.connection-title {
  gap: 12px;
}

.connection-icon,
.connection-option__icon,
.support-strip__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
  color: var(--brand-cyan);
  background: rgba(var(--brand-cyan-rgb), 0.09);
}

.connection-icon {
  width: 40px;
  height: 40px;
}

.connection-title__label {
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 650;
}

.connection-title__meta {
  margin-top: 3px;
  color: var(--text-dim);
  font-size: 0.68rem;
}

.connection-head :deep(.v-chip__content) {
  display: flex;
  align-items: center;
  gap: 7px;
}

.field-label {
  margin-bottom: 9px;
  color: rgba(188, 209, 207, 0.76);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.endpoint-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.connection-divider {
  height: 1px;
  margin: 24px 0;
  background: rgba(164, 204, 202, 0.1);
}

.connection-options {
  display: grid;
  gap: 8px;
}

.connection-option {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid rgba(162, 204, 201, 0.1);
  border-radius: 13px;
  color: var(--text-soft);
  font-family: inherit;
  text-align: left;
  text-decoration: none;
  background: rgba(5, 15, 18, 0.42);
  cursor: pointer;
  transition: border-color 0.18s ease, background 0.18s ease, transform 0.18s ease;
}

.connection-option:hover {
  border-color: rgba(var(--brand-cyan-rgb), 0.25);
  background: rgba(var(--brand-cyan-rgb), 0.06);
  transform: translateX(2px);
}

.connection-option__icon {
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
}

.connection-option__copy,
.support-strip__copy {
  display: grid;
  min-width: 0;
  flex: 1;
}

.connection-option strong,
.support-strip strong {
  font-size: 0.75rem;
  font-weight: 700;
}

.connection-option small,
.support-strip small {
  margin-top: 2px;
  overflow: hidden;
  color: var(--text-dim);
  font-size: 0.65rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.support-strip {
  gap: 9px;
  margin-top: 16px;
  padding: 11px 8px 11px 12px;
  border-radius: 13px;
  color: rgba(219, 228, 225, 0.82);
  background: rgba(var(--brand-amber-rgb), 0.045);
}

.support-strip__icon {
  width: 30px;
  height: 30px;
  flex: 0 0 30px;
  color: var(--brand-amber);
  background: rgba(var(--brand-amber-rgb), 0.1);
}

.signal-field {
  position: absolute;
  top: 50%;
  left: 47%;
  width: 420px;
  height: 420px;
  pointer-events: none;
  opacity: 0.32;
  transform: translate(-50%, -50%);
}

.signal-ring,
.signal-sweep {
  position: absolute;
  border-radius: 50%;
}

.signal-ring {
  border: 1px solid rgba(var(--brand-cyan-rgb), 0.15);
}

.signal-ring--outer {
  inset: 0;
}

.signal-ring--inner {
  inset: 25%;
}

.signal-sweep {
  inset: 8%;
  background: conic-gradient(from 210deg, transparent 0 78%, rgba(var(--brand-cyan-rgb), 0.16), transparent 94%);
  animation: signal-spin 12s linear infinite;
}

.signal-node {
  position: absolute;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--brand-cyan);
  box-shadow: 0 0 18px rgba(var(--brand-cyan-rgb), 0.7);
}

.signal-node--one {
  top: 14%;
  left: 47%;
}

.signal-node--two {
  right: 10%;
  bottom: 30%;
}

.signal-node--three {
  bottom: 18%;
  left: 22%;
}

@keyframes signal-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 959px) {
  .hero-copy {
    padding: 42px 32px 34px;
  }

  .connection-card {
    margin: 0 18px 18px;
  }

  .signal-field {
    top: 24%;
    left: 78%;
  }
}

@media (max-width: 599px) {
  .hero-copy {
    padding: 32px 22px 28px;
  }

  .hero-copy h1 {
    font-size: clamp(2.3rem, 12vw, 3.3rem);
  }

  .hero-actions :deep(.v-btn) {
    width: 100%;
  }

  .connection-card {
    margin: 0 10px 10px;
    padding: 20px;
  }

  .connection-head {
    align-items: flex-start;
  }

  .connection-head :deep(.v-chip) {
    display: none;
  }
}
</style>
