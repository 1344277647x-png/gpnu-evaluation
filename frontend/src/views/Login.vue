<template>
  <div class="auth-page">
    <div class="auth-wrapper">
      <LoginIllust class="auth-illust" />
      <el-card class="auth-card glass-card">
        <h2 class="auth-title">欢迎回来</h2>
        <p class="auth-sub">登录 GPnu 公选课评价系统</p>
        <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleLogin">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">登录</el-button>
          </el-form-item>
        </el-form>
        <p class="auth-link">还没有账号？<router-link to="/register">立即注册</router-link></p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import LoginIllust from '../components/illustrations/LoginIllust.vue'
import api from '../api'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const formRef = ref(null)
const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const res = await api.post('/api/auth/login', form)
    const { access_token, refresh_token, user } = res.data.data
    userStore.setAuth(access_token, refresh_token, user)
    router.push('/')
  } finally { loading.value = false }
}
</script>

<style scoped>
.auth-page { display: flex; justify-content: center; padding-top: 40px; }
.auth-wrapper { display: flex; align-items: center; gap: 40px; flex-wrap: wrap; justify-content: center; }
.auth-illust { width: 280px; flex-shrink: 0; }
.auth-card { width: 380px; max-width: 90vw; background: rgba(255,255,255,0.18) !important; backdrop-filter: blur(14px) !important; -webkit-backdrop-filter: blur(14px) !important; border: 1px solid rgba(255,255,255,0.25) !important; box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important; border-radius: 18px !important; }
.auth-title { text-align: center; margin-bottom: 4px; font-size: 22px; }
.auth-sub { text-align: center; font-size: 13px; color: #9ca3af; margin-bottom: 20px; }
.auth-link { text-align: center; font-size: 14px; color: #9ca3af; }
.auth-link a { color: #10b981; font-weight: 500; }
@media (max-width: 720px) { .auth-illust { display: none; } }
</style>
