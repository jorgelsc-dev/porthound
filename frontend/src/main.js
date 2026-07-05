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
          background: "#06111d",
          surface: "#0f1d2d",
          primary: "#0fe8ff",
          secondary: "#8e63ff",
          error: "#ff647a",
          info: "#4b8fff",
          success: "#4ad7b7",
          warning: "#f5bb62",
        },
      },
    },
  },
});

store.initApiBase();
store.initAuth();
store.initRealtime();

createApp(App).use(vuetify).use(router).mount("#app");
