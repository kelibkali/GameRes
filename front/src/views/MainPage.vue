<script setup lang="ts">

import {checkLogin, userLogout} from "../services/UserApi.ts";
import {ref} from "vue";
import LoginView from "./LoginView.vue";

const loginView = ref(false)

const check = async () =>{
  const data  = await checkLogin();
  console.log(data);
  if(!data.login){
    loginView.value = true;
  }
}

const logout = async () => {
  await userLogout()
}

</script>

<template>
  <LoginView class="login-view" :show="loginView" @close-panel="loginView = false"></LoginView>
<el-button class="btn" @click="check">
  login in
</el-button>

  <el-button class="btn" @click="logout">
    login out
  </el-button>
</template>

<style scoped>
.btn{
  outline: none;
}

.login-view{
  position: absolute;
  top: 50%;
  left: 50%;
  z-index: 1000;
  transform: translate(-50%, -50%);
}
</style>