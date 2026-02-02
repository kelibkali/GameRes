<script setup lang="ts">
import LoginView from "./views/LoginView.vue";
import {computed, onMounted, ref} from "vue";
import {checkLogin} from "./services/UserApi.ts";

import {UserFilled,Lock} from "@element-plus/icons-vue"
import UserInfoView from "./views/UserInfoView.vue";

const showLoginView = ref(false);

const showUserInfoView = ref(false);

const user = ref({
  userID:"",
  email: "",
  username: "",
  steamID:"",
  steamLogin:false
})

const openUserPanel = async () =>{
  const data  = user.value.userID;
  if(data === ""){
    showLoginView.value = true;
  }else{
    showUserInfoView.value = true;
  }
}

const getUserLogin = async () =>{
  const data  = await checkLogin();
  if(data.login){
    user.value = {...data.user_info};
    if(user.value.steamID == null){
      user.value.steamID = ""
    }else{
      user.value.steamLogin = true
    }
    console.log(user.value);
  }
}

const asideHover = ref(true);

const panelMenuRadius = computed(() => ({
  borderRadius:`${asideHover.value ? 0.4 : 2.3 }rem`
}))

const showTextStyle = computed(() => ({
  'show-text': asideHover.value
}))

const lineStyle = computed(() => ({
  'line-style': asideHover.value
}))

onMounted(() => {
  getUserLogin()
})

</script>

<template>
  <LoginView class="login-view" :show="showLoginView" @close-panel="showLoginView = false"></LoginView>
  <UserInfoView class="login-view" :user="user" :show="showUserInfoView" @close-panel="showUserInfoView = false"></UserInfoView>
  <el-container style="height: 100vh">
    <el-aside
        class="page-aside"
        style="user-select: none"
        @mouseenter="asideHover = true"
        @mouseleave="asideHover = false"
    >
      <el-container>
        <el-header class="menu-header">
          Logo
        </el-header>
        <el-main style="padding: 0">
          <el-menu class="page-change">
<!--            <el-menu-item>-->
<!--              hello-->
<!--            </el-menu-item>-->
<!--            <el-menu-item>-->
<!--              hello-->
<!--            </el-menu-item>-->
<!--            <el-menu-item>-->
<!--              hello-->
<!--            </el-menu-item>-->
          </el-menu>
        </el-main>
        <el-footer style="padding: 0">
          <div class="option-group" :style="panelMenuRadius">
            <div class="option" @click="openUserPanel">
              <el-icon size="20px">
                <UserFilled />
              </el-icon>
              <div class="panel-font" :class="showTextStyle">
                用户
              </div>
            </div>
            <div class="line" :class="lineStyle"></div>
            <div class="option">
              <el-icon size="20px">
                <Lock />
              </el-icon>
              <div class="panel-font" :class="showTextStyle">
                hello
              </div>
            </div>
          </div>
        </el-footer>
      </el-container>
    </el-aside>
    <el-main style="padding: 0;margin-left: 5.5rem">
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<style scoped>
.page-aside{
  position: absolute;
  height: 100vh;
  width: 5.5rem;
  background: white;
  box-shadow: 0 0 0.5rem rgba(0,0,0,.3);
  transition: width 0.3s ease;

  overflow: hidden;
}

.page-aside:hover{
  width: 12.5rem;
}

.menu-header{
  height: 6rem;
  display: flex;
  justify-content: space-between;
  padding: 0;
}

.page-change{
  height: 65vh;
}

.line{
  position: absolute;
  background-color: #cccccc;
  height: .1rem;
  width: 25%;
  padding: 0;
  transition: width 0.3s ease;
}

.line-style{
  width: 75%;
}

.option-group{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;

  height: 8rem;
  margin-left: .5rem;
  margin-right: .5rem;
  border-radius: 2.3rem;
  font-size: 1rem;

  transition: all .3s ease;

  overflow: hidden;

  background-color: #f0f0f0;

  .option{
    display: flex;
    align-items: center;
    justify-content: flex-start;

    background-color: #f0f0f0;
    color: #191919;
    width: 93%;
    border-radius: 3px;
    height: 3rem;
    transition: all .3s ease;

    white-space: nowrap;

    overflow: hidden;

    .el-icon{
      margin-left: 1.5rem;
    }


  }
  .option:hover{
    background-color: #d9d9d9;
    color: #191919;
  }
}

.panel-font{
  position: relative;
  opacity: 0;
  visibility: hidden;
  width: 0;
  transform: translateX(2rem);
  transition: all .3s ease;
}

.panel-font.show-text{
  position: relative;
  opacity: 1;
  visibility: visible;
  width: auto;
  transform: translateX(3rem);
}


.login-view{
  position: absolute;
  top: 43%;
  left: 50%;
  z-index: 1000;
  transform: translate(-50%, -50%);
}


</style>