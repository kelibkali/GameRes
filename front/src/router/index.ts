import {createRouter, createWebHistory} from "vue-router";
import CaptchaPanel from "../components/CaptchaPanel.vue";
import MessagePanel from "../components/MessagePanel.vue";
import MainPage from "../views/MainPage.vue";

const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {path:"/",component:MainPage},
        {path:"/captcha",name:"CaptchaPanel",component : CaptchaPanel},
        {path:"/msg",name:"MessagePanel",component : MessagePanel},
    ]
})

export default router;