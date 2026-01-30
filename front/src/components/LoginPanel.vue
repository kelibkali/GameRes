<script setup lang="ts">

import {onMounted, ref} from "vue";

import {getCaptchaImage} from "../services/api.ts";

import { Message,Lock } from "@element-plus/icons-vue"
import Close from "./Close.vue";

const formData = ref({
  "username":"",
  "password":"",
  "re-password":"",
  "email":"",
  "captcha":""
})

const imageSrc = ref()

async function fetchCaptchaImage() {
  try{
    imageSrc.value = await getCaptchaImage()
  }catch(error){
    console.log(error)
  }
}

function clearText(){
  formData.value.username = "";
}

function refreshCaptchaImage() {
  fetchCaptchaImage();
}

onMounted(() => {
  refreshCaptchaImage()
})

</script>

<template>
  <el-form class="form-login" v-model="formData" label-width="auto" label-position="left" size="large" style="width: 28rem">
    <div class="top-bar-black"/>
    <div class="top-bar-y"/>
    <el-form-item>
      <el-input v-model="formData.username" >
        <template #prefix>
          <el-icon class="user-icon" size="23">
            <Message />
          </el-icon>
        </template>
        <template #suffix>
          <el-icon @click="clearText">
            <Close></Close>
          </el-icon>
          <el-divider direction="vertical" />
          <el-link underline="never">
            发送验证码
          </el-link>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-input v-model="formData.password" type="password" show-password>
        <template #prefix>
          <el-icon class="user-icon" size="23">
            <Lock />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-input v-model="formData['re-password']" type="password" show-password>
        <template #prefix>
          <el-icon class="user-icon" size="23">
            <Lock />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-input placeholder="验证码" v-model="formData.captcha" style="width: 42%;margin-right: 1rem"></el-input>
      <el-image class="form-image" :src="imageSrc" fit="cover" @click="refreshCaptchaImage"></el-image>
    </el-form-item>
    <el-button class="login-button" color="#333333">注册</el-button>
  </el-form>
</template>

<style scoped>

.login-button{
  transition: all 0.2s ease;
  width: 10rem;
  height: 3rem;
  font-size: 1.3rem;
  font-family: "SansMedium",sans-serif;
  border-radius: 2px;
  border:none;
  margin-top: 2rem;
}

.login-button:hover{
  border-radius: 6px ;
}

.login-button:focus{
  outline: none;
}

.form-image{
  width: 240px;
  height: 80px;
}

.form-login :deep(.el-input__inner) {
  font-size: 1.2rem;
}

.form-login :deep(.el-input__wrapper) {
  transition: box-shadow 0.5s ease;
  box-shadow: rgba(0, 0, 0, 0.08) 0 0 0 1px;
  border-radius: 1.5rem;
  height: 3rem;
}

.form-login :deep(.el-input__wrapper):hover {
 box-shadow: #1a1a1a 0 0 0 1px;

  .el-icon.user-icon{
    color: #1a1a1a;
  }

}

.form-login :deep(.el-input__wrapper.is-focus) {
  box-shadow: #1a1a1a 0 0 0 1px;

  .el-icon.user-icon{
    color: #1a1a1a;
  }

}

.form-login :deep(.el-icon.user-icon) {
  transition: color 0.5s ease;
}
</style>