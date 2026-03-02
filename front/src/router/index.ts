import {createRouter, createWebHistory} from "vue-router";
import CaptchaPanel from "../components/CaptchaPanel.vue";
import MessagePanel from "../components/MessagePanel.vue";
import GameListView from "../views/GameListView.vue";
import GameRecommendView from "../views/GameRecommendView.vue";

const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {path:"/",component:GameRecommendView},
        {path:"/gameList",component:GameListView},
        {path:"/captcha",name:"CaptchaPanel",component : CaptchaPanel},
        {path:"/msg",name:"MessagePanel",component : MessagePanel},
    ]
})

export default router;