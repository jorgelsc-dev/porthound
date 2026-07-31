import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", name: "dashboard", component: () => import("../views/DashboardView.vue") },
  { path: "/explorer", name: "explorer", component: () => import("../views/ExplorerView.vue") },
  { path: "/targets", name: "targets", component: () => import("../views/TargetsView.vue") },
  { path: "/ports", name: "ports", component: () => import("../views/PortsView.vue") },
  { path: "/banners", name: "banners", component: () => import("../views/BannersView.vue") },
  { path: "/tags", name: "tags", component: () => import("../views/TagsView.vue") },
  { path: "/catalog", name: "catalog", component: () => import("../views/CatalogView.vue") },
  { path: "/files", name: "files", component: () => import("../views/FileCatalogView.vue") },
  { path: "/map", name: "map", component: () => import("../views/MapWorldView.vue") },
  { path: "/charts", name: "charts", component: () => import("../views/ChartsView.vue") },
  { path: "/security", name: "security", component: () => import("../views/SecurityView.vue") },
  { path: "/agents", redirect: "/security" },
  { path: "/api", name: "api", component: () => import("../views/ApiView.vue") },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL || "/"),
  routes,
  scrollBehavior() {
    return { left: 0, top: 0 };
  },
});

export default router;
