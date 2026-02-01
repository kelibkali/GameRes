import {createRouter, createWebHistory} from "vue-router";
import CaptchaPanel from "../components/CaptchaPanel.vue";
import MessagePanel from "../components/MessagePanel.vue";
import LoginView from "../views/LoginView.vue";

const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {path:"/captcha",name:"CaptchaPanel",component : CaptchaPanel},
        {path:"/msg",name:"MessagePanel",component : MessagePanel},
        {
            path: '/',
            component: LoginView,
        }
    ]
})

export default router;