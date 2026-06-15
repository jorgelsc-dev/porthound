import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import "./styles/app.css";

import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import router from "./router";
import store from "./state/appStore";

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: "porthoundDark",
    themes: {
      porthoundDark: {
        dark: true,
        colors: {
          background: "#05080f",
          surface: "#111827",
          primary: "#34e6ff",
          secondary: "#8d73ff",
          error: "#ff647a",
          info: "#4d8cff",
          success: "#43d7be",
          warning: "#f3b15b",
        },
      },
    },
  },
});

store.initApiBase();
store.initAuth();
store.initRealtime();

createApp(App).use(vuetify).use(router).mount("#app");
