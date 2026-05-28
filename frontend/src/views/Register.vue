<template>
  <div class="auth-page">
    <div class="auth-wrapper">
      <LoginIllust class="auth-illust" />
      <el-card class="auth-card glass-card">
        <h2 class="auth-title">加入我们</h2>
        <p class="auth-sub">注册账号，开始评价课程</p>
        <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleRegister">
          <el-form-item label="昵称" prop="nickname">
            <el-input v-model="form.nickname" placeholder="怎么称呼你" />
          </el-form-item>
          <el-form-item label="学号" prop="student_id">
            <el-input v-model="form.student_id" placeholder="请输入学号" />
          </el-form-item>
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="3-20位字母、数字或下划线" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" type="password" placeholder="至少8位，含大小写字母和数字" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="password2">
            <el-input v-model="form.password2" type="password" placeholder="再次输入密码" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">注册</el-button>
          </el-form-item>
        </el-form>
        <p class="auth-link">已有账号？<router-link to="/login">去登录</router-link></p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import LoginIllust from '../components/illustrations/LoginIllust.vue'
import api from '../api'

const router = useRouter()
const loading = ref(false)
const formRef = ref(null)
const form = reactive({ nickname: '', student_id: '', username: '', password: '', password2: '' })

const validatePassword2 = (rule, value, callback) => {
  if (value !== form.password) callback(new Error('两次密码不一致'))
  else callback()
}

const rules = {
  nickname: [{ required: true, message: '请输入昵称' }],
  student_id: [{ required: true, message: '请输入学号' }],
  username: [
    { required: true, message: '请输入用户名' },
    { pattern: /^[a-zA-Z0-9_]{3,20}$/, message: '3-20位字母、数字或下划线' }
  ],
  password: [
    { required: true, message: '请输入密码' },
    { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/, message: '至少8位，含大小写字母和数字' }
  ],
  password2: [
    { required: true, message: '请确认密码' },
    { validator: validatePassword2 }
  ]
}

async function handleRegister() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await api.post('/api/auth/register', {
      nickname: form.nickname, student_id: form.student_id,
      username: form.username, password: form.password
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
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
