<script setup lang="ts">
import {ref} from "vue";

import {Message,Lock} from "@element-plus/icons-vue";

import type {FormInstance, FormRules} from "element-plus";
import {analyzeObject} from "../utils/utils.ts";

import {useAuthStore} from "../stores/auth.ts";
import type {UserModel} from "../types/User.ts";
import {useMessagesStore} from "../stores/messages.ts";

const formData = ref({
  "email": "",
  "password": "",
})
const formRef = ref<FormInstance>();

const formRules: FormRules = {
  email:[
    {required: true, message: '请输入邮箱地址', trigger: 'submit'},
    {type: 'email', message: '请输入正确的邮箱格式', trigger: ['submit']}
  ],
  password:[
    {required:true,message:'请输入密码', trigger: 'submit'},
  ]
}

const authStore = useAuthStore();

const messagesStore = useMessagesStore();


const onSubmit = async (formElement: FormInstance | undefined) => {
  try{
    const valid = await formElement?.validate()
    if(!valid) return
  }catch(error){
    console.log(error)
    messagesStore.addMessage(analyzeObject(error))
    return
  }

  try{
    const userForLogin:Pick<UserModel, 'email' | 'password'> = {
      email:formData.value.email,
      password:formData.value.password,
    };


    const result = await authStore.loginUser(userForLogin)

    console.log(result)

    if(result.type === "success"){
      emit('loginSuccess')
    }

  }catch(error){
    console.log(error)
  }
}

const emit = defineEmits<{
  toRegister:[],
  loginSuccess:[]
}>();

const toRegister = () =>{
  emit("toRegister")
}
</script>

<template>
    <el-form
        class="form-login"
        ref="formRef"
        :model="formData"
        :rules="formRules"
        :show-message="false"
        style="width: 28rem;"
        @submit.prevent="onSubmit(formRef)"
    >
      <el-form-item prop="email">
        <el-input placeholder="请输入邮箱" v-model="formData.email">
          <template #prefix>
            <el-icon class="icon" size="23">
              <Message/>
            </el-icon>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input placeholder="请输入密码" type="password" show-password v-model="formData.password">
          <template #prefix>
            <el-icon class="icon" size="23">
              <Lock/>
            </el-icon>
          </template>
        </el-input>
      </el-form-item>

      <div class="button-container">
        <el-button
            data-icon
            class="login-button"
            @click="onSubmit(formRef)"
            native-type="submit"
        >
          登录
        </el-button>
        <el-button data-icon class="login-button" @click="toRegister">
          注册
        </el-button>
      </div>
    </el-form>
</template>

<style scoped>

@import "../css/form-login.css";
@import "../css/login-button.css";

.form-login :deep(.el-input__wrapper) {
  margin-bottom: 1.3rem;
}

.login-button{
  margin-top: 1.8rem;
}

.button-container{
  display: flex;
  justify-content: center;
  gap: 3rem;
}
</style>