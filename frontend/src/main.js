import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";

import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./state/appStore";
import "./styles/app.css";

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
          background: "#071014",
          surface: "#0d1b20",
          primary: "#68e5bd",
          "on-primary": "#04130f",
          secondary: "#78a7ff",
          "on-secondary": "#071014",
          error: "#ff7382",
          info: "#57c7e6",
          success: "#68e5bd",
          warning: "#f4bd6a",
        },
      },
    },
  },
});

store.initApiBase();
store.initAuth();
store.initRealtime();

createApp(App).use(vuetify).use(router).mount("#app");
