import {createRouter, createWebHistory} from "vue-router";
import LoginPanel from "../components/LoginPanel.vue";


const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {path:"/",name:"LoginPanel",component : LoginPanel}
    ]
})

export default router;