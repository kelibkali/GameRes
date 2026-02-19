<script setup lang="ts">
import CloseButton from "../components/CloseButton.vue";
import {userLogout} from "../services/UserApi.ts";
import {onMounted} from "vue";
import {loginSteam, logoutSteam} from "../services/SteamApi.ts";

//TODO:获取登录状态

const props = defineProps({
  show:{
    type: Boolean,
    required:true,
    default: false,
  },
  user:{
    type: Object,
    required:true,
    default:{
      userID: "",
      email: "",
      username: "",
      steamID:"",
      steamLogin:false,
    }
  }
})

const emit = defineEmits<{
  closePanel:[],
  refreshPanel:[],
}>()

const handleClosePanel = ()=> {
  emit("closePanel")
}

const handleLoginSteam = async ()=>{
  await loginSteam()
}

const handleLogoutSteam = async ()=>{
  await logoutSteam()
  emit("refreshPanel")
}

const handleUserLogout = async ()=>{
  await userLogout()
  emit("closePanel")
  emit("refreshPanel")
}

onMounted(() => {

})

</script>

<template>
  <transition name="fade">
    <div class="container" v-if="props.show">
      <div class="top-bar-black">
        <div class="title">
          用户信息
        </div>
        <CloseButton class="close-btn" @click="handleClosePanel">
        </CloseButton>
      </div>
      <div class="top-bar-yellow">
      </div>
      <div class="panel-content">
        <div class="field-row">
          <span class="field-label">
            邮箱
          </span>
          <div class="line"></div>
          <span class="field-value">
            {{user.email}}
          </span>
        </div>
        <div class="field-row">
          <span class="field-label">
            用户名
          </span>
          <div class="line"></div>
          <span class="field-value">
            {{user.username}}
          </span>
        </div>
        <div class="field-row">
          <span class="field-label">
            {{user.steamLogin ? "SteamID" :"" }}
          </span>
          <div class="line"></div>
          <span class="field-value">
            {{user.steamLogin ? user.steamID :"没有登录steam" }}
          </span>
        </div>
      <div class="button-container">
        <el-button data-icon class="login-button" v-if="!user.steamLogin" @click="handleLoginSteam">
          绑定Steam
        </el-button>
        <el-button data-icon class="login-button" v-else @click="handleLogoutSteam">
          解绑Steam
        </el-button>
        <el-button data-icon class="login-button" @click="handleUserLogout">
          退出登录
        </el-button>
      </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>

@import "../css/form-login.css";
@import "../css/login-button.css";

.container{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 38rem;
  height: 35rem;

  box-shadow: rgba(0,0,0, 0.25) 0 0 0.75rem;

  overflow: hidden;

  border-radius: 7px;

  background: #fff;
}

.container::before{
  content: '';
  position: absolute;
  width: 38rem;
  height: 35rem;
  background-image: url("../assets/points-bg.png");
  background-size: 1em 1em;
  background-position: bottom;
  mask-image: linear-gradient(180deg,transparent 0,transparent 50%,black 90%,black);
  opacity: 0.08;
}

.title{
  font-size: 2.6rem;
  color: white;
  font-family: "SansMedium", sans-serif;
}

.button-container{
  display: flex;
  justify-content: center;
  flex-direction: column;
  margin-top: 3rem;
  gap: 1.5rem;

  .login-button{
    margin:0;
    width: 15rem;
  }
}

.top-bar-yellow{
  width: 100%;
  height: 0.5rem;
  background-color: #fffa00;
  margin-bottom: 0.6rem;
}

.top-bar-black{
  width: 100%;
  height: 7.5rem;

  display: flex;
  align-items: center;
  justify-content: center;

  background-size: cover;
  background-position: center;
  background-image: url("../assets/header_bg.png");
}

.back-btn{
  position: absolute;
  margin-right: 30.5rem;
}

.close-btn{
  position: absolute;
  margin-left: 30.5rem;
}

.panel-content{
  position: relative;
  width: 100%;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.field-row{

  user-select: none;

  display: flex;
  margin-bottom: 1rem;
  width: 21rem;
  height: 2.5rem;
  align-items: center;
  padding-left: 15px;
  overflow: hidden;

  background-color: rgba(159, 159, 159, 0.24);

  font-family: "SansMedium", sans-serif;
  font-weight: 500;

  .field-label{
    width: 24%;
    text-align: left;
  }

  .field-value{
    display: flex;
    text-align: center;
    justify-content: center;
  }

  .line{
    height: 20rem;
    width: 6px;
    background-color: #fffa00;
    margin-right: 0.9rem;
  }

}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}


</style>