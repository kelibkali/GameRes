import {createRouter, createWebHistory} from "vue-router";
import LoginPanel from "../components/LoginPanel.vue";
import CaptchaPanel from "../components/CaptchaPanel.vue";
import MessagePanel from "../components/MessagePanel.vue";


const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {path:"/",name:"LoginPanel",component : LoginPanel},
        {path:"/captcha",name:"CaptchaPanel",component : CaptchaPanel},
        {path:"/msg",name:"MessagePanel",component : MessagePanel},
    ]
})

export default router;