<template>
  <div class="view-header">
    <div class="view-header__copy">
      <div v-if="overline" class="view-kicker">
        <span />
        {{ overline }}
      </div>
      <div class="view-title">{{ title }}</div>
      <div v-if="description" class="view-description">
        {{ description }}
      </div>
    </div>
    <div class="header-actions">
      <slot name="actions">
        <v-btn
          v-if="showRefresh"
          variant="outlined"
          color="primary"
          prepend-icon="mdi-refresh"
          :loading="refreshLoading"
          @click="$emit('refresh')"
        >
          {{ refreshLabel }}
        </v-btn>
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "ViewHeader",
  props: {
    overline: {
      type: String,
      default: "",
    },
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      default: "",
    },
    showRefresh: {
      type: Boolean,
      default: true,
    },
    refreshLabel: {
      type: String,
      default: "Refresh",
    },
    refreshLoading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["refresh"],
};
</script>

<style scoped>
.view-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(164, 204, 202, 0.11);
}

.view-header__copy {
  min-width: 0;
}

.view-kicker {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 7px;
  color: var(--brand-cyan);
  font-size: 0.65rem;
  font-weight: 750;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.view-kicker span {
  width: 18px;
  height: 1px;
  background: var(--brand-cyan);
}

.view-title {
  color: var(--text-strong);
  font-family: var(--font-heading);
  font-size: clamp(1.65rem, 3vw, 2.2rem);
  font-weight: 650;
  line-height: 1.08;
  letter-spacing: -0.04em;
}

.view-description {
  max-width: 720px;
  margin-top: 7px;
  color: var(--text-dim);
  font-size: 0.86rem;
  line-height: 1.55;
}

.header-actions {
  display: flex;
  min-height: 40px;
  flex: 0 0 auto;
  align-items: center;
  gap: 8px;
}

@media (max-width: 599px) {
  .view-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
  }
}
</style>
