import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router";
import ElementPlus from "element-plus"
import 'element-plus/dist/index.css'
import {useAuthStore} from "./stores/auth.ts";
import {createPinia} from "pinia";

const app = createApp(App)

const pinia = createPinia()

app.use(pinia)

const authStore = useAuthStore()

authStore.initAuthFromServer()


app.use(router)
app.use(ElementPlus)

app.mount("#app")