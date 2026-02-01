<script setup lang="ts">
import {computed, ref} from 'vue';
import LoginPanel from "../components/LoginPanel.vue"
import RegisterPanel from '../components/RegisterPanel.vue';
import BackButton from "../components/BackButton.vue";
import CloseButton from "../components/CloseButton.vue";

const props = defineProps({
  show:{
    type: Boolean,
    required:true,
    default: false
  }
})

const emit = defineEmits<{
  closePanel:[],
}>()

const handleClosePanel = ()=> {
  emit("closePanel");
}

const currentView = ref<'login' | 'register'>('login');

const switchView = (view: 'login' | 'register') => {
  currentView.value = view;
};

const transitionName = computed(()=>{
  if(currentView.value === 'register'){
    return 'slide-right'
  }
  return 'slide-left'
})


</script>

<template>
  <transition name="fade">
    <div class="container" v-if="props.show">
      <div class="top-bar-black">
        <BackButton class="back-btn" v-if="currentView === 'register'" @click="switchView('login')">
        </BackButton>
        <img src="../assets/logo.png" style="margin-top: 0.2rem" alt=""/>
        <CloseButton class="close-btn" v-if="currentView === 'login'" @click="handleClosePanel">
        </CloseButton>
      </div>
      <div class="top-bar-yellow">
      </div>

      <div class="panel-content">
        <transition :name="transitionName">
          <div class="panel-wrapper-login"  v-if="currentView === 'login'">
            <LoginPanel @toRegister="switchView('register')" ></LoginPanel>
          </div>
          <div class="panel-wrapper-register" v-else-if="currentView === 'register'">
            <RegisterPanel></RegisterPanel>
          </div>
        </transition>
      </div>
    </div>
  </transition>
</template>

<style scoped>
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
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.panel-wrapper-login{
  position: absolute;
  margin-bottom: 2.5rem;
}

.panel-wrapper-register{
  position: absolute;
  margin-bottom: 0;
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.3s ease-in-out;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(-100%);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

/* 向右滑动的过渡效果 */
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease-in-out;
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(100%); /* 从右侧进入 */
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(-100%); /* 向左侧离开 */
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