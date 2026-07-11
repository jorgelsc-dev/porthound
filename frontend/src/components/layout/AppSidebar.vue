<template>
  <v-navigation-drawer v-model="localOpen" temporary width="304" class="d-lg-none mobile-drawer">
    <div class="drawer-header">
      <div class="drawer-brand">
        <BrandMark :size="44" />
        <div>
          <div class="drawer-brand__name">PortHound</div>
          <div class="drawer-brand__meta">Operations console</div>
        </div>
      </div>
      <v-btn icon="mdi-close" size="small" variant="text" aria-label="Close navigation" @click="closeDrawer" />
    </div>

    <div class="drawer-label">Workspace</div>
    <v-list nav density="comfortable" class="drawer-list">
      <v-list-item
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        :prepend-icon="item.icon"
        :title="item.label"
        rounded="lg"
        @click="closeDrawer"
      />
    </v-list>

    <template #append>
      <div class="drawer-notice">
        <v-icon icon="mdi-shield-check-outline" size="18" />
        <div>
          <strong>Authorized use only</strong>
          <span>Scan systems you own or have explicit permission to assess.</span>
        </div>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import BrandMark from "../brand/BrandMark.vue";

export default {
  name: "AppSidebar",
  components: {
    BrandMark,
  },
  props: {
    open: {
      type: Boolean,
      default: false,
    },
    navItems: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["update:open"],
  computed: {
    localOpen: {
      get() {
        return this.open;
      },
      set(value) {
        this.$emit("update:open", value);
      },
    },
  },
  methods: {
    closeDrawer() {
      this.$emit("update:open", false);
    },
  },
};
</script>

<style scoped>
.mobile-drawer {
  border-right: 1px solid rgba(168, 206, 204, 0.12);
  background: linear-gradient(180deg, rgba(8, 20, 23, 0.99), rgba(5, 14, 17, 0.99)) !important;
  backdrop-filter: blur(20px) saturate(120%);
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 18px 18px;
  border-bottom: 1px solid rgba(166, 204, 202, 0.1);
}

.drawer-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.drawer-brand__name {
  font-family: var(--font-heading);
  font-size: 1.05rem;
  font-weight: 700;
}

.drawer-brand__meta,
.drawer-label {
  color: var(--text-dim);
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.drawer-label {
  padding: 22px 22px 8px;
}

.drawer-list {
  padding: 0 10px;
}

.drawer-list :deep(.v-list-item) {
  min-height: 50px;
  margin: 4px 0;
  color: rgba(205, 224, 221, 0.8);
}

.drawer-list :deep(.v-list-item--active) {
  color: var(--text-strong);
  background: rgba(var(--brand-cyan-rgb), 0.1);
  box-shadow: inset 0 0 0 1px rgba(var(--brand-cyan-rgb), 0.12);
}

.drawer-notice {
  display: flex;
  gap: 10px;
  margin: 16px;
  padding: 14px;
  border: 1px solid rgba(var(--brand-amber-rgb), 0.18);
  border-radius: 14px;
  color: rgba(229, 210, 174, 0.88);
  background: rgba(var(--brand-amber-rgb), 0.06);
}

.drawer-notice strong,
.drawer-notice span {
  display: block;
}

.drawer-notice strong {
  font-size: 0.75rem;
}

.drawer-notice span {
  margin-top: 3px;
  color: rgba(197, 183, 156, 0.72);
  font-size: 0.69rem;
  line-height: 1.45;
}
</style>
