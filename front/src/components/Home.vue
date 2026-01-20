<script setup lang="ts">

import {onMounted, ref} from "vue";

import {getCaptchaImage} from "../services/api.ts";

const formData = ref({
  "username":"",
  "password":"",
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

function refreshCaptchaImage() {
  fetchCaptchaImage();
}

onMounted(() => {
  refreshCaptchaImage()
})

</script>

<template>
  <el-form class="form-login" v-model="formData" label-width="auto" label-position="left" size="large" style="width: 28rem">
    <el-form-item label="用户名">
      <el-input>
      </el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input>
      </el-input>
    </el-form-item>
    <el-form-item label="确认密码">
      <el-input>
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

.form-login /deep/ .el-form-item__label{
  font-size: 1.1rem;
}

</style>