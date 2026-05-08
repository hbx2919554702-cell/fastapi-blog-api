<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';
import { loginApi, getUserInfoApi } from '../api/user';

const router = useRouter();
const userStore = useUserStore();

const username = ref('');
const password = ref('');
const loading = ref(false);
const errorMsg = ref('');

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMsg.value = '用户名和密码不能为空';
    return;
  }

  loading.value = true;
  errorMsg.value = '';

  try {
    // 1. 组装 OAuth2 要求的表单数据
    const formData = new URLSearchParams();
    formData.append('username', username.value);
    formData.append('password', password.value);

    // 2. 发起登录请求
    const res = await loginApi(formData);

    // 3. 登录成功，保存 Token 到 Pinia
    if (res.access_token) {
      userStore.setToken(res.access_token);

      // 4. 趁热打铁，用刚拿到的 Token 去拉取个人信息
      const infoRes = await getUserInfoApi();
      if (infoRes.code === 200) {
        userStore.setUserInfo(infoRes.data);
        // 5. 一切就绪，跳转回首页
        router.push('/');
      }
    }
  } catch (error: any) {
    errorMsg.value = error.response?.data?.detail || '登录失败，请检查账号密码';
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};

</script>

<template>
  <div class="min-h-screen bg-brand-gray flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-brand-white p-8 rounded-xl shadow-md border border-gray-100">
      <div>
        <h2 class="mt-2 text-center text-3xl font-extrabold text-gray-900">登录系统</h2>
        <p class="mt-2 text-center text-sm text-gray-600">现代化博客系统</p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="username" class="sr-only">用户名</label>
            <input id="username" v-model="username" type="text" required class="appearance-none rounded-lg relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-brand-blue focus:border-brand-blue focus:z-10 sm:text-sm" placeholder="请输入用户名" />
          </div>
          <div>
            <label for="password" class="sr-only">密码</label>
            <input id="password" v-model="password" type="password" required class="appearance-none rounded-lg relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-brand-blue focus:border-brand-blue focus:z-10 sm:text-sm" placeholder="请输入密码" />
          </div>
        </div>

        <div v-if="errorMsg" class="text-red-500 text-sm text-center">{{ errorMsg }}</div>

       <div class="flex gap-4">
          <button type="button" @click="goBack" class="w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-brand-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-blue transition">
            取 消
          </button>
          <button type="submit" :disabled="loading" class="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-brand-white bg-brand-blue hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-blue transition disabled:opacity-50">
            {{ loading ? '登录中...' : '登 录' }}
          </button>
        </div>

        <div class="mt-4 text-center text-sm text-gray-600">
            还没有账号？ <button type="button" @click="router.push('/register')" class="text-brand-blue hover:underline">立即注册</button>
        </div>
        </form>
    </div>
  </div>
</template>