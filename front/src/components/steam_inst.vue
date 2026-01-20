<!-- src/App.vue -->
<template>
  <div id="app">
    <header>
      <h1>Steam 登录 Demo</h1>
      <!-- 登录按钮 -->
      <button v-if="!user" @click="handleLogin">登录 Steam</button>
      <!-- 用户信息和登出按钮 -->
      <div v-else class="user-info">
        <p>欢迎, Steam ID: {{ user.steam_id }}</p>
        <button @click="handleLogout">登出</button>
      </div>
    </header>

    <main>
      <p v-if="loading">加载中...</p>
      <p v-else-if="error">{{ error }}</p>
      <p v-else-if="user">已登录，可以访问受保护的内容。</p>
      <p v-else>请先登录。</p>
    </main>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import {fetchUser, logout} from '../services/api';

interface User {
  steam_id: string;
}

const user = ref<User | null>(null);
const loading = ref<boolean>(true);
const error = ref<string | null>(null);

// 检查用户是否已登录
const checkAuthStatus = async () => {
  try {
    const userData = await fetchUser();
    if (userData.error) {
      // 后端返回了错误，说明未登录
      console.log('未登录:', userData.error);
      user.value = null;
    } else {
      // 登录成功
      user.value = userData;
    }
  } catch (err) {
    console.error('检查登录状态失败:', err);
    error.value = '无法连接到服务器或发生错误。';
    user.value = null;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  checkAuthStatus();
});

// 处理登录点击事件
const handleLogin = () => {
  // 直接重定向到后端的 /login 路由
  // 后端会处理重定向到 Steam 并最终回调到 http://localhost:5173/callback
  window.location.href = 'http://localhost:5000/login';
};

// 处理登出点击事件
const handleLogout = async () => {
  await logout();
  // logout 函数内部会执行重定向，这里无需再次设置 user.value = null;
  // 但如果你想在UI上立即反映变化（虽然很快会被刷新），也可以设置：
  // user.value = null;
};
</script>

<style scoped>
/* 简单样式 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.user-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>