<script setup lang="ts">
import LoginView from "./views/LoginView.vue";
import {computed, onMounted, ref} from "vue";
import {checkLogin} from "./services/UserApi.ts";

import {UserFilled,Lock} from "@element-plus/icons-vue"
import UserInfoView from "./views/UserInfoView.vue";
import GlobalMessageContainer from "./components/GlobalMessageContainer.vue";
import {useRouter} from "vue-router";

const router = useRouter()

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
    router.push("/")
  }else if(page === "gameList"){
    selectIndex.value = 1;
    router.push("/gameList")
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
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 256 256">
                <path d="M176,112H152a8,8,0,0,1,0-16h24a8,8,0,0,1,0,16ZM104,96H96V88a8,8,0,0,0-16,0v8H72a8,8,0,0,0,0,16h8v8a8,8,0,0,0,16,0v-8h8a8,8,0,0,0,0-16ZM241.48,200.65a36,36,0,0,1-54.94,4.81c-.12-.12-.24-.24-.35-.37L146.48,160h-37L69.81,205.09l-.35.37A36.08,36.08,0,0,1,44,216,36,36,0,0,1,8.56,173.75a.68.68,0,0,1,0-.14L24.93,89.52A59.88,59.88,0,0,1,83.89,40H172a60.08,60.08,0,0,1,59,49.25c0,.06,0,.12,0,.18l16.37,84.17a.68.68,0,0,1,0,.14A35.74,35.74,0,0,1,241.48,200.65ZM172,144a44,44,0,0,0,0-88H83.89A43.9,43.9,0,0,0,40.68,92.37l0,.13L24.3,176.59A20,20,0,0,0,58,194.3l41.92-47.59a8,8,0,0,1,6-2.71Zm59.7,32.59-8.74-45A60,60,0,0,1,172,160h-4.2L198,194.31a20.09,20.09,0,0,0,17.46,5.39,20,20,0,0,0,16.23-23.11Z">
                </path>
              </svg>
            </div>
            <span class="p-option-font" :class="showTextStyle">
              主页
            </span>
          </div>
          <div class="p-option" :class="{active: selectOption == 'gameList'}" @click="handlePageChange('gameList')">
            <div class="p-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 256 256">
                <path d="M230.91,172A8,8,0,0,1,228,182.91l-96,56a8,8,0,0,1-8.06,0l-96-56A8,8,0,0,1,36,169.09l92,53.65,92-53.65A8,8,0,0,1,230.91,172ZM220,121.09l-92,53.65L36,121.09A8,8,0,0,0,28,134.91l96,56a8,8,0,0,0,8.06,0l96-56A8,8,0,1,0,220,121.09ZM24,80a8,8,0,0,1,4-6.91l96-56a8,8,0,0,1,8.06,0l96,56a8,8,0,0,1,0,13.82l-96,56a8,8,0,0,1-8.06,0l-96-56A8,8,0,0,1,24,80Zm23.88,0L128,126.74,208.12,80,128,33.26Z">
                </path>
              </svg>
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
              敬请期待
            </div>
          </div>

          <div class="line" :class="{active: asideHover}" ></div>

          <div class="option">
            <el-icon class="option-icon" size="18px">
              <Lock />
            </el-icon>
            <div class="panel-font" :class="showTextStyle" >
              敬请期待
            </div>
          </div>
        </div>
      </div>
    </el-aside>
    <el-main style="padding: 0;margin-left: 5.5rem;overflow: hidden">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive>
            <component :is="Component" class="page-view"></component>
          </keep-alive>
        </transition>
      </router-view>
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


      .p-icon{
        padding-left: .3rem;
        position: relative;
        width: 28px;
        height: 28px;
        color: #d9d9d9;
        transition: all .25s ease-out;
        svg{
          fill: #d9d9d9;
          transition: all .25s ease-out;
        }
      }

      &.active{
        background-color: #e6e6e6;
        .p-icon{
          svg{
            fill: #191919;
          }
        }
      }

    }

    .p-option:hover{
      background-color: #e6e6e6;
      .p-icon{
        svg{
          fill:#858585
        }
      }
    }

    .p-option.active:hover{
      .p-icon{
        svg{
          fill: #191919;
        }
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
/* ================= 前进动画 (slide-up) ================= */
/* 新页面从底部向上滑入，旧页面向上滑出消失 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
  position: absolute; /* 关键：绝对定位以实现重叠过渡 */
  width: 100%;
  top: 0;
  left: 0;
}

.slide-up-enter-from {
  transform: translateY(100%); /* 初始位置：屏幕下方 */
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(-100%); /* 离开位置：稍微向上推一点，增加层次感 */
  opacity: 0;
}

/* ================= 后退动画 (slide-down) ================= */
/* 新页面从顶部向下滑入，旧页面向下滑出消失 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease;
  position: absolute;
  width: 100%;
  top: 0;
  left: 0;
}

.slide-down-enter-from {
  transform: translateY(-100%); /* 初始位置：屏幕上方 */
  opacity: 0;
}

.slide-down-leave-to {
  transform: translateY(100%); /* 离开位置：稍微向下推一点 */
  opacity: 0;
}

/* ================= 默认淡入 ================= */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.page-view{
  width: 100%;
  height: 100%;
}

</style>