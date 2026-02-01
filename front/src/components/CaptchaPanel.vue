<script setup lang="ts">

import {onMounted, ref} from "vue";
import {getCaptchaImage,verifyCaptcha} from "../services/CaptchaApi.ts";
import MessagePanel from "./MessagePanel.vue";

const messages = ref<string[]>([]);

const captcha = ref("");

const imageSrc = ref();

const emit = defineEmits<{
  captchaVerified:[success:boolean]
}>();

async function fetchCaptchaImage() {
  try{
    imageSrc.value = await getCaptchaImage()
  }catch(error){
    console.log(error)
  }
}

async function verifyCaptchaCode(){
  if(!captcha.value.trim()){
    messages.value.push("验证码不能为空")
    return
  }

  try{
    const result = await verifyCaptcha(captcha.value)
    if(result["type"] === "success"){
      messages.value.push("发送成功")
      await refreshCaptchaImage()
      captcha.value = "";
      emit("captchaVerified", true);
      return
    }
    if(result["type"] === "error"){
      await refreshCaptchaImage()
      messages.value.push("验证码错误")
      captcha.value = "";
      emit("captchaVerified", false);
      return
    }

    if(result["type"] === "message"){
      await refreshCaptchaImage()
      messages.value.push(result["message"])
      captcha.value = "";
      emit("captchaVerified", false);
      return
    }

  }catch(error){
    console.log(error)
  }
}

async function refreshCaptchaImage() {
  await fetchCaptchaImage();
}

onMounted(() => {
  refreshCaptchaImage()
})


defineExpose({
  messages,
})
</script>

<template>

  <MessagePanel
    v-for="msg in messages"
    :text="msg"
    :top="30"
  ></MessagePanel>

  <el-form class="form-login" label-position="left">
    <el-form-item >
      <el-input placeholder="验证码" v-model="captcha"></el-input>
    </el-form-item>
  </el-form>
  <el-image class="form-image" :src="imageSrc" fit="cover" @click="refreshCaptchaImage"></el-image>
  <br/>
  <el-button data-icon class="login-button" @click="verifyCaptchaCode">
    确认
  </el-button>

</template>

<style scoped>
@import "../css/login-button.css";
@import "../css/form-login.css";

.form-image{
  width: 240px;
  height: 80px;
  cursor: pointer;
  border: rgba(0,0,0,0.08) 1px solid;
  transition: border 0.4s ease;
}

.form-image:hover{
  border: #1a1a1a 1px solid;
}
</style>