<script setup lang="ts">

import {ref} from "vue";

import {Message, Lock, Key, User} from "@element-plus/icons-vue"
import Close from "./Close.vue";
import CaptchaPanel from "./CaptchaPanel.vue";
import MessagePanel from "./MessagePanel.vue";
import {generateEmailCode, verifyCode} from "../services/EmailApi.ts";
import { type FormInstance, type FormRules} from "element-plus";

const PASSWORD_REGEX =  /^(?:(?=.*[A-Za-z])(?=.*\d)|(?=.*[A-Za-z])(?=.*[^A-Za-z0-9\s])|(?=.*\d)(?=.*[^A-Za-z0-9\s]))[A-Za-z\d\S]+$/

const messages = ref<string[]>([]);

const formData = ref({
  "email": "",
  "code": "",
  "username": "",
  "password": "",
  "re_password": ""
})

const formRef = ref<FormInstance>();

const formRules: FormRules = {
  email: [
    {required: true, message: '请输入邮箱地址', trigger: 'submit'},
    {type: 'email', message: '请输入正确的邮箱格式', trigger: ['submit']}
  ],
  code: [
    {required:true,message:'请输入邮箱验证码',trigger:['submit']},
    // {
    //   asyncValidator: async (_rule, value, callback) => {
    //     const data = await verifyCode(formData.value.email,value)
    //     if(!data["type"] || data["type"]!="success") {
    //       callback(new Error(data["message"]))
    //     }
    //     callback()
    //   },
    //   trigger:['submit']
    // }
  ],
  username: [
    {required:true,message:'请输入用户名',trigger:['submit']},
    { max: 15, message: '用户名过长', trigger: 'submit' },
    { pattern: /^[a-zA-Z0-9_\u4e00-\u9fa5]+$/, message: '用户名包含非法字符', trigger: 'submit' }
  ],
  password: [
    {required:true,message:'请输入密码', trigger: 'submit'},
    {min:6,max: 20, message: '密码必须为6-20位', trigger: 'submit' },
    {pattern:PASSWORD_REGEX,message: "密码包含数字、字母、字母中的两种", trigger:['submit']},
  ],
  re_password: [
    {required:true,message:'请再次输入密码', trigger: 'submit'},
    {
      validator: (_rule, value, callback) => {
        if(value !== formData.value.password){
          callback(new Error('两次输入的密码不一致'))
        }else {
          callback()
        }
      },
      trigger:['submit']
    }
  ],
}

const dialog = ref(false)

const countdownActive = ref(false)

const countdownSeconds = ref(60)

const canBeEdit = ref(true);

const startCountdown = async () => {
  if (countdownActive.value) return
  countdownActive.value = true

  let remaining = countdownSeconds.value

  const tick = () => {
    if (remaining > 0) {
      countdownSeconds.value = remaining;
      remaining--;
      setTimeout(tick, 1000)
    } else {
      countdownActive.value = false
      countdownSeconds.value = 60
    }
  }

  tick()
}

function clearText() {
  formData.value.email = "";
}

const analyzeObject = (object: any) => {
  if (typeof object === "object" && object) {
    let fieldName = Object.keys(object)[0]
    if(fieldName){
      if (Object.prototype.hasOwnProperty.call(object, fieldName)) {
        const fieldErrors = (object as Record<string, any[]>)[fieldName]
        if (Array.isArray(fieldErrors)) {
          fieldErrors.forEach(errorObject => {
            if (errorObject && typeof errorObject === "object" && "message" in errorObject) {
              const message = errorObject.message as string
              if (message && message.length > 0) {
                messages.value.push(message)
              }
            }
          })
        }
      }
    }
  }
}

const openDialog = async () => {
  try {
    await formRef.value?.validateField("email")
  } catch (error) {
    analyzeObject(error)
    return
  }
  dialog.value = true
}

const handleCaptchaVerified = async (success: boolean) => {
  if (success) {
    dialog.value = false;
    canBeEdit.value = false
    //发送邮件
    await generateEmailCode(formData.value.email);
    //按钮进入倒计时
    await startCountdown()
  }
}

const onSubmit = async (formElement: FormInstance | undefined) => {
  await formElement?.validate((valid,fields)=>{
    if (!valid) {
      console.log("error",fields)
      analyzeObject(fields)
      return
    }
  })

  try{
    const data = await verifyCode(formData.value.email,formData.value.code)
    if(!data["type"] || data["type"] != "success"){
      if(data["message"]){
        messages.value.push(data["message"])
      }else {
        messages.value.push("未知错误")
      }
      return
    }
    //验证成功


  }catch(e){
    messages.value.push("未知错误")
    console.log("error",e);
  }



}
</script>

<template>

  <MessagePanel
      v-for="msg in messages"
      :text="msg"
      :top="50"
  ></MessagePanel>

  <el-dialog destroy-on-close title="请输入验证码" v-model="dialog" width="24rem">
    <CaptchaPanel @captchaVerified="handleCaptchaVerified"></CaptchaPanel>
  </el-dialog>
  <el-form
      class="form-login"
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="auto"
      label-position="left"
      style="width: 28rem"
      :show-message="false"
  >
    <div class="top-bar-black"/>
    <div class="top-bar-y"/>
    <el-form-item prop="email">
      <el-input :disabled="!canBeEdit" v-model="formData.email" placeholder="请输入邮箱">
        <template #prefix>
          <el-icon class="icon" size="23">
            <Message/>
          </el-icon>
        </template>
        <template #suffix>
          <el-icon @click="clearText">
            <Close></Close>
          </el-icon>
          <el-divider direction="vertical"/>
          <el-link
              class="login-link"
              underline="never"
              style="user-select: none"
              :disabled="countdownActive || !canBeEdit"
              @click="openDialog"
          >
            {{ countdownActive ? `${countdownSeconds}s后重发` : '发送验证码' }}
          </el-link>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="code">
      <el-input placeholder="邮箱验证码" v-model="formData.code">
        <template #prefix>
          <el-icon class="icon" size="23">
            <Key/>
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="username">
      <el-input v-model="formData.username" placeholder="请输入用户名">
        <template #prefix>
          <el-icon class="icon" size="23">
            <User/>
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input v-model="formData.password" type="password" show-password placeholder="请输入密码">
        <template #prefix>
          <el-icon class="icon" size="23">
            <Lock/>
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="re_password">
      <el-input v-model="formData.re_password" type="password" show-password placeholder="请再次输入密码">
        <template #prefix>
          <el-icon class="icon" size="23">
            <Lock/>
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-button @click="onSubmit(formRef)" data-icon class="login-button">
      注册
    </el-button>
  </el-form>
</template>

<style scoped>

@import "../css/login-button.css";
@import "../css/form-login.css";

.login-link {
  color: #0080ff;
  transition: color 0.3s ease;
  min-width: 5rem;
}

.login-link:hover:not(.is-disabled) {
  color: #49a2ff;
}
</style>