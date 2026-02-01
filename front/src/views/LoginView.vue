<template>
  <div class="container">
    <div class="top-bar-black">
      <BackButton class="back-btn" v-if="currentView === 'register'" @click="switchView('login')">

      </BackButton>
    </div>
    <div class="top-bar-yellow">
    </div>

    <div class="panel-content">
      <transition :name="transitionName">
        <div class="panel-wrapper"  v-if="currentView === 'login'">
          <LoginPanel @toRegister="switchView('register')" ></LoginPanel>
        </div>
        <div class="panel-wrapper" v-else-if="currentView === 'register'">
          <RegisterPanel></RegisterPanel>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from 'vue';
import LoginPanel from "../components/LoginPanel.vue"
import RegisterPanel from '../components/RegisterPanel.vue';
import BackButton from "../components/BackButton.vue";

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

<style scoped>
.container{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 38rem;
  height: 38rem;

  box-shadow: rgba(0,0,0, 0.25) 0 0 0.75rem;

  overflow: hidden;
}

.top-bar-yellow{
  width: 100%;
  height: 1.2rem;
  background-color: #fffa00;
  margin-bottom: 0.6rem;
}

.top-bar-black{
  width: 100%;
  height: 7.5rem;
  background-color: #000000;

  display: flex;
  align-items: center;
  justify-content: left;
}

.back-btn{
  margin-left: 1.2rem;
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

.panel-wrapper{
  position: absolute;
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

</style>