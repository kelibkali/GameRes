<script setup lang="ts">
import LoginView from "./views/LoginView.vue";
import {computed, onMounted, ref} from "vue";
import {checkLogin} from "./services/UserApi.ts";

import {UserFilled,Lock} from "@element-plus/icons-vue"
import UserInfoView from "./views/UserInfoView.vue";
import GlobalMessageContainer from "./components/GlobalMessageContainer.vue";

const showLoginView = ref(false);

const showUserInfoView = ref(false);

const selectOption = ref("homePage")

const selectIndex = ref(0)

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
  }else{
    user.value = {
      userID:"",
      email: "",
      username: "",
      steamID:"",
      steamLogin:false
    }
  }
}

const asideHover = ref(false);

const panelMenuRadius = computed(() => ({
  borderRadius:`${asideHover.value ? 0.2 : 1.5 }rem`,
  marginLeft: `${asideHover.value ? 1 : 1.3 }rem`,
  marginRight: `${asideHover.value ? 1: 1.3 }rem`
}))

const showTextStyle = computed(() => ({
  'show-text': asideHover.value
}))

const handleLoginSuccess = () =>{
  showLoginView.value = false;
  getUserLogin()
}

const handleRefreshPanel = async () =>{
  console.log("refreshPanel");
  await getUserLogin()
}

const handlePageChange = (page:string) => {
  if(page === "homePage"){
    selectIndex.value = 0;
  }else if(page === "gameList"){
    selectIndex.value = 1;
  }else if(page === "personalPage"){
    selectIndex.value = 2;
  }

  selectOption.value = page;
}

const overlayY = computed(() => ({
  transform:`translateY(${selectIndex.value * 3.4 }rem)`
}))


onMounted(() => {
  getUserLogin()
})

</script>

<template>

  <GlobalMessageContainer />

  <LoginView
      class="login-view"
      :show="showLoginView"
      @close-panel="showLoginView = false"
      @loginSuccess="handleLoginSuccess"
  ></LoginView>

  <UserInfoView
      class="login-view"
      :user="user"
      :show="showUserInfoView"
      @close-panel="showUserInfoView = false"
      @refreshPanel="handleRefreshPanel"
  ></UserInfoView>

  <el-container style="height: 100vh">
    <el-aside
        class="page-aside"
        style="user-select: none;z-index: 1000;overflow: hidden;"
        @mouseenter="asideHover = true"
        @mouseleave="asideHover = false"
    >
      <div class="menu-header">
        Logo
      </div>
      <div class="panel-main">

        <div class="page-change-group">

          <div class="option-overlay" :style="overlayY">
            <div class="header-overlay"></div>
            <div class="bg-overlay" :class="{active: asideHover}"></div>
          </div>

          <div class="p-option" :class="{active: selectOption == 'homePage'}" @click="handlePageChange('homePage')">
            <div class="p-icon">
            </div>
            <span class="p-option-font" :class="showTextStyle">
              主页
            </span>
          </div>
          <div class="p-option" :class="{active: selectOption == 'gameList'}" @click="handlePageChange('gameList')">
            <div class="p-icon">
            </div>
            <span class="p-option-font" :class="showTextStyle">
              游戏列表
            </span>
          </div>
          <div class="p-option" :class="{active: selectOption == 'personalPage'}" @click="handlePageChange('personalPage')">
            <div class="p-icon">
            </div>
            <span class="p-option-font" :class="showTextStyle">
              个人资料
            </span>
          </div>
        </div>


        <div class="option-group" :style="panelMenuRadius">
          <div class="option" @click="openUserPanel">
            <el-icon class="option-icon" size="18px">
              <UserFilled />
            </el-icon>
            <div class="panel-font" :class="showTextStyle">
              用户
            </div>
          </div>

          <div class="line" :class="{active: asideHover}"></div>

          <div class="option">
            <el-icon class="option-icon" size="18px">
              <Lock />
            </el-icon>
            <div class="panel-font" :class="showTextStyle">
              用户用户有
            </div>
          </div>

          <div class="line" :class="{active: asideHover}" ></div>

          <div class="option">
            <el-icon class="option-icon" size="18px">
              <Lock />
            </el-icon>
            <div class="panel-font" :class="showTextStyle" >
              hello
            </div>
          </div>
        </div>
      </div>
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
  width: 5rem;
  background: white;
  box-shadow: 0 0 0.3rem rgba(0,0,0,.2);
  transition: width 0.25s ease-out;

  overflow: hidden;
}

.page-aside:hover{
  width: 15rem;
}

.menu-header{
  height: 5rem;
  display: flex;
  justify-content: space-between;
  padding: 0;
}

.line{
  background-color: #cccccc;
  height: 0.05rem;
  width: 1rem;
  transform: translate3d(0,0,0) scaleX(1);

  transition: transform 0.25s ease-out;

  &.active{
    transform: translate3d(0.1rem,0,0) scaleX(11.5);
  }

}

.option-group{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;

  height: 7rem;
  font-size: 1rem;

  transition: all 0.25s ease-out;

  overflow: hidden;

  background-color: #f0f0f0;
  gap: 0.2rem;

  padding-top: 0.25rem;

  padding-bottom: 0.25rem;

  .option{
    display: flex;
    align-items: center;
    justify-content: flex-start;

    background-color: #f0f0f0;
    color: #191919;
    width: 93%;
    border-radius: 3px;
    height: 2rem;
    transition: all .3s ease;

    white-space: nowrap;

    overflow: hidden;

    .el-icon{
      margin-left: 0.55rem;
    }
  }
  .option:hover{
    background-color: #d9d9d9;
    color: #191919;
  }
}

.panel-font{
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  font-size: 12px;
  width: 40%;
  transform: translateX(2rem);
  transition: all .3s ease;

  font-family: "SansMedium", sans-serif;

}

.panel-font.show-text{
  opacity: 1;
  visibility: visible;
  transform: translateX(3rem);

}


.login-view{
  scale: 90%;
  position: absolute;
  top: 43%;
  left: 50%;
  z-index: 1000;
  transform: translate(-50%, -50%);
}

.panel-main{
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  .page-change-group{
    display: flex;
    flex-direction: column;
    gap: 0.2rem;

    .p-option{
      display: flex;
      align-items: center;
      background-color: white;
      height: 3.2rem;
      margin-left: 1rem;
      margin-right: 1rem;

      border-radius: 3px;

      transition: all .25s ease-out;

      &.active{
        background-color: #e6e6e6;
      }
    }

    .p-option:hover{
      background-color: #e6e6e6;
      .p-icon{
        color: #858585;
      }
    }
  }
}

.p-option-font{
  white-space: nowrap;
  font-size: 14px;
  font-family: "SansMedium", sans-serif;
  opacity: 0;
  transform: translateX(0rem);
  transition: all .2s ease;
  z-index: 15;
}

.p-option-font.show-text{
  opacity: 1;
  transform: translateX(0.5rem);
}

.p-icon{
  padding-left: .3rem;
  position: relative;
  width: 40px;
  height: 40px;
  color: #d9d9d9;
  transition: all .25s ease-out;
  scale: 70%;
}

.option-overlay{
  transition: all 0.2s ease;

  .header-overlay{
    position: absolute;
    width: 8px;
    height: 3.2rem;
    margin-top: 0.2rem;
    background-color: #1a1a1a;
    z-index: 15;
  }

  .bg-overlay{
    position: absolute;
    width: 4rem;
    height: 3.2rem;
    margin-top: 0.2rem;
    z-index: 5;
    background-color: #e6e6e6;
    transition: all 0.25s ease-out;

    &.active{
      width: 14rem;
    }
  }
}

</style>