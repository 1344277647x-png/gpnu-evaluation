<template>
  <div class="chat-bubble-wrapper">
    <div class="chat-fab" @click="toggleChat" :class="{ active: isOpen }">
      <el-icon :size="24" v-if="!isOpen"><ChatDotRound /></el-icon>
      <el-icon :size="20" v-else><Close /></el-icon>
      <span v-if="unread" class="chat-badge"></span>
    </div>

    <transition name="chat-slide">
      <div v-if="isOpen" class="chat-panel">
        <div class="chat-header">
          <div class="chat-header-left">
            <div class="chat-avatar">AI</div>
            <div>
              <div class="chat-title">AI 管理员</div>
              <div class="chat-status"><span class="status-dot"></span>在线</div>
            </div>
          </div>
          <el-button text circle @click="isOpen = false">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>

        <div class="chat-messages" ref="msgContainer">
          <div v-for="(msg, i) in messages" :key="i" class="msg-row" :class="msg.role">
            <div class="msg-bubble" v-html="renderMsg(msg)"></div>
          </div>
          <div v-if="isLoading" class="msg-row assistant">
            <div class="msg-bubble typing">
              <span class="dot"></span><span class="dot"></span><span class="dot"></span>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <el-input v-model="input" placeholder="输入问题..." :disabled="isLoading"
            @keyup.enter="send" size="small">
            <template #suffix>
              <el-button text :disabled="!input.trim() || isLoading" @click="send">
                <el-icon><Promotion /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { marked } from 'marked'
import api from '../api'

const isOpen = ref(false)
const input = ref('')
const isLoading = ref(false)
const unread = ref(false)
const sessionId = crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36)
const messages = ref([{
  role: 'assistant',
  content: '你好！我是 AI 管理员小助，管理员不在时由我代班。关于课程评价有什么想问的吗？'
}])
const msgContainer = ref(null)

function toggleChat() {
  isOpen.value = !isOpen.value
  if (isOpen.value) { unread.value = false; nextTick(scrollBottom) }
}

function renderMsg(msg) {
  if (msg.role === 'assistant') return marked.parse(msg.content, { breaks: true })
  return msg.content
}

async function send() {
  const text = input.value.trim()
  if (!text || isLoading.value) return
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  isLoading.value = true
  await nextTick(scrollBottom)
  try {
    const history = messages.value.map(m => ({ role: m.role, content: m.content }))
    const res = await api.post('/api/chat', { messages: history, session_id: sessionId })
    const reply = res.data.data.reply || '抱歉，我暂时无法回答这个问题。'
    messages.value.push({ role: 'assistant', content: reply })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: '抱歉，AI 服务暂时不可用，请稍后再试。' })
  } finally {
    isLoading.value = false
    if (!isOpen.value) unread.value = true
    await nextTick(scrollBottom)
  }
}

function scrollBottom() {
  const el = msgContainer.value
  if (el) el.scrollTop = el.scrollHeight
}
</script>

<style scoped>
.chat-bubble-wrapper { position: fixed; bottom: 24px; right: 24px; z-index: 1000; }
.chat-fab {
  width: 56px; height: 56px; border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; display: flex; align-items: center; justify-content: center;
  cursor: pointer; box-shadow: 0 4px 16px rgba(16,185,129,0.35);
  transition: transform 0.2s, box-shadow 0.2s; position: relative;
}
.chat-fab:hover { transform: scale(1.08); box-shadow: 0 6px 24px rgba(16,185,129,0.45); }
.chat-fab.active { background: #6b7280; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.chat-badge {
  position: absolute; top: 4px; right: 4px; width: 12px; height: 12px;
  background: #ef4444; border-radius: 50%; border: 2px solid #fff;
}

.chat-panel {
  position: absolute; bottom: 68px; right: 0; width: 380px; height: 520px;
  background: rgba(255,255,255,0.20); backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(16,185,129,0.12); border-radius: 16px;
  box-shadow: 0 16px 48px rgba(0,0,0,0.1);
  display: flex; flex-direction: column; overflow: hidden;
}
.chat-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px; background: rgba(16,185,129,0.10);
  border-bottom: 1px solid rgba(16,185,129,0.1); backdrop-filter: blur(8px);
}
.chat-header-left { display: flex; align-items: center; gap: 10px; }
.chat-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700;
}
.chat-title { font-size: 15px; font-weight: 600; color: #1f2937; }
.chat-status { font-size: 12px; color: #059669; display: flex; align-items: center; gap: 4px; }
.status-dot { width: 7px; height: 7px; background: #10b981; border-radius: 50%; }

.chat-messages {
  flex: 1; overflow-y: auto; padding: 12px 14px;
  display: flex; flex-direction: column; gap: 10px; background: transparent;
}
.msg-row { display: flex; }
.msg-row.user { justify-content: flex-end; }
.msg-bubble {
  max-width: 82%; padding: 10px 14px; border-radius: 14px;
  font-size: 13px; line-height: 1.6; word-break: break-word;
}
.msg-row.user .msg-bubble { background: #10b981; color: #fff; border-bottom-right-radius: 4px; }
.msg-row.assistant .msg-bubble {
  background: rgba(255,255,255,0.22); backdrop-filter: blur(6px);
  color: #1f2937; border: 1px solid rgba(16,185,129,0.08); border-bottom-left-radius: 4px;
}
.msg-row.assistant .msg-bubble :deep(p) { margin: 0 0 6px; }
.msg-row.assistant .msg-bubble :deep(p:last-child) { margin: 0; }

.typing { display: flex; gap: 4px; padding: 14px 18px; }
.dot { width: 7px; height: 7px; background: #9ca3af; border-radius: 50%; animation: bounce 1.4s infinite; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }

.chat-input {
  padding: 10px 14px; border-top: 1px solid rgba(16,185,129,0.08);
  background: rgba(255,255,255,0.18); backdrop-filter: blur(8px);
}
.chat-slide-enter-active { transition: all 0.25s ease-out; }
.chat-slide-leave-active { transition: all 0.2s ease-in; }
.chat-slide-enter-from, .chat-slide-leave-to { opacity: 0; transform: translateY(16px) scale(0.95); }
</style>
