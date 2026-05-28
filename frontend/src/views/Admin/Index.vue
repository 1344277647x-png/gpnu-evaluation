<template>
  <div>
    <div class="page-header"><h2>管理面板</h2></div>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="课程审核" name="courses" />
      <el-tab-pane label="用户管理" name="users" />
      <el-tab-pane label="数据统计" name="stats" />
      <el-tab-pane label="AI对话" name="chat" />
    </el-tabs>
    <CourseReview v-if="activeTab==='courses'" />
    <UserManage v-if="activeTab==='users'" />
    <StatsView v-if="activeTab==='stats'" />
    <ChatHistory v-if="activeTab==='chat'" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CourseReview from './CourseReview.vue'
import UserManage from './UserManage.vue'
import StatsView from './Stats.vue'
import ChatHistory from './ChatHistory.vue'

const activeTab = ref('courses')
</script>
