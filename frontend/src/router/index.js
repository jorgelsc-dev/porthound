import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "../views/DashboardView.vue";
import TargetsView from "../views/TargetsView.vue";
import PortsView from "../views/PortsView.vue";
import BannersView from "../views/BannersView.vue";
import ApiView from "../views/ApiView.vue";

const routes = [
  { path: "/", name: "dashboard", component: DashboardView },
  { path: "/targets", name: "targets", component: TargetsView },
  { path: "/ports", name: "ports", component: PortsView },
  { path: "/banners", name: "banners", component: BannersView },
  { path: "/api", name: "api", component: ApiView },
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
