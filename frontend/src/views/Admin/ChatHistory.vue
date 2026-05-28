<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8" :xs="24">
        <el-card class="session-list">
          <template #header><span>对话会话</span></template>
          <div v-loading="loadingSessions" style="min-height:100px">
            <div v-if="sessions.length === 0 && !loadingSessions" style="color:#9ca3af;text-align:center;padding:20px">
              暂无对话记录
            </div>
            <div
              v-for="s in sessions" :key="s.session_id"
              class="session-item"
              :class="{ active: selectedId === s.session_id }"
              @click="selectSession(s.session_id)"
            >
              <div class="session-user">{{ s.nickname || s.username || 'Anonymous' }}</div>
              <div class="session-meta">{{ s.msg_count }} 条消息 · {{ fmt(s.last_msg) }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16" :xs="24">
        <el-card>
          <template #header><span>对话详情</span></template>
          <div v-if="!selectedId" style="color:#9ca3af;text-align:center;padding:40px">
            请从左侧选择一个会话
          </div>
          <div v-else v-loading="loadingMsgs" class="msg-list">
            <div v-for="m in messages" :key="m.id" class="admin-msg-row" :class="m.role">
              <div class="admin-msg-role">{{ m.role === 'user' ? '用户' : 'AI' }}</div>
              <div class="admin-msg-content">{{ m.content }}</div>
              <div class="admin-msg-time">{{ fmt(m.created_at) }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const sessions = ref([])
const loadingSessions = ref(false)
const selectedId = ref('')
const messages = ref([])
const loadingMsgs = ref(false)

function fmt(t) {
  return t ? new Date(t).toLocaleString('zh-CN') : ''
}

async function fetchSessions() {
  loadingSessions.value = true
  try {
    const res = await api.get('/api/admin/chat/sessions')
    sessions.value = res.data.data?.items || []
  } finally {
    loadingSessions.value = false
  }
}

async function selectSession(sid) {
  selectedId.value = sid
  loadingMsgs.value = true
  try {
    const res = await api.get(`/api/admin/chat/sessions/${sid}`)
    messages.value = res.data.data?.items || []
  } finally {
    loadingMsgs.value = false
  }
}

onMounted(fetchSessions)
</script>

<style scoped>
.session-list { max-height: 600px; overflow-y: auto; }
.session-item {
  padding: 10px 12px; cursor: pointer; border-radius: 8px;
  margin-bottom: 4px; transition: background 0.15s;
}
.session-item:hover { background: rgba(16,185,129,0.06); }
.session-item.active { background: rgba(16,185,129,0.12); }
.session-user { font-size: 14px; font-weight: 600; color: #1f2937; }
.session-meta { font-size: 12px; color: #9ca3af; margin-top: 2px; }

.msg-list { display: flex; flex-direction: column; gap: 12px; max-height: 500px; overflow-y: auto; }
.admin-msg-row { padding: 12px 16px; border-radius: 12px; background: rgba(255,255,255,0.5); }
.admin-msg-row.user { border-left: 3px solid #10b981; }
.admin-msg-row.assistant { border-left: 3px solid #6366f1; }
.admin-msg-role { font-size: 12px; font-weight: 600; margin-bottom: 4px; color: #6b7280; }
.admin-msg-content { font-size: 14px; color: #1f2937; line-height: 1.6; white-space: pre-wrap; }
.admin-msg-time { font-size: 11px; color: #9ca3af; margin-top: 6px; }
</style>
