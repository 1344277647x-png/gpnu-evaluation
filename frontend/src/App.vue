<template>
  <div id="app-container">
    <el-container>
      <el-header class="app-header" height="56px">
        <div class="header-left">
          <router-link to="/" class="logo">
            <el-icon :size="20"><School /></el-icon>
            <span>GPnu 公选课评价</span>
          </router-link>
        </div>
        <div class="header-right">
          <template v-if="userStore.isLoggedIn">
            <el-button text @click="$router.push('/course/add')">
              <el-icon><Plus /></el-icon> 提交新课
            </el-button>
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                <el-icon><User /></el-icon>
                {{ userStore.user?.nickname }}
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="my">
                    <el-icon><User /></el-icon> 个人中心
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.isAdmin" command="admin">
                    <el-icon><Setting /></el-icon> 管理面板
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon> 退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button text @click="$router.push('/login')">登录</el-button>
            <el-button type="primary" size="small" @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </el-header>

      <el-main class="app-main">
        <router-view />
      </el-main>

      <el-footer class="app-footer" height="40px">
        <span>GPnu 公选课教师评价系统 &copy; 2026</span>
      </el-footer>
    </el-container>

    <ChatBubble />
  </div>
</template>

<script setup>
import { useUserStore } from './stores/user'
import { useRouter } from 'vue-router'
import ChatBubble from './components/ChatBubble.vue'

const userStore = useUserStore()
const router = useRouter()

function handleCommand(cmd) {
  if (cmd === 'logout') {
    userStore.logout()
    router.push('/')
  } else {
    router.push(`/${cmd}`)
  }
}
</script>
