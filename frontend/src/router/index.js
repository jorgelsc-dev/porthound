import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", name: "dashboard", component: () => import("../views/DashboardView.vue") },
  { path: "/targets", name: "targets", component: () => import("../views/TargetsView.vue") },
  { path: "/ports", name: "ports", component: () => import("../views/PortsView.vue") },
  { path: "/banners", name: "banners", component: () => import("../views/BannersView.vue") },
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
