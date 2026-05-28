<template>
  <div class="review-item">
    <div class="review-header">
      <span class="review-user">{{ review.user?.nickname || review.user?.username }}</span>
      <span class="review-time">{{ fmt(review.created_at) }}</span>
    </div>
    <div class="review-scores">
      <div class="score-item" v-for="s in scoreItems" :key="s.key">
        <span class="score-label">{{ s.label }}</span>
        <span class="score-stars">{{ stars(review[s.key]) }}</span>
      </div>
    </div>
    <div v-if="review.comment" class="review-comment">{{ review.comment }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ review: Object })

const scoreItems = [
  { key: 'rating_teaching', label: '教学质量' },
  { key: 'rating_content', label: '课程内容' },
  { key: 'rating_exam', label: '考核方式' },
  { key: 'rating_fairness', label: '给分公平' }
]

function stars(n) {
  return '★'.repeat(n || 0) + '☆'.repeat(5 - (n || 0))
}
function fmt(t) {
  return t ? new Date(t).toLocaleDateString('zh-CN') : ''
}
</script>

<style scoped>
.review-item {
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  padding: 16px 20px; margin-bottom: 12px;
}
.review-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.review-user { font-weight: 600; color: #111827; }
.review-time { font-size: 12px; color: #9ca3af; }
.review-scores { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 10px; }
.score-item { display: flex; align-items: center; gap: 4px; font-size: 13px; }
.score-label { color: #374151; }
.score-stars { color: #f59e0b; }
.review-comment { font-size: 14px; color: #111827; line-height: 1.7; white-space: pre-wrap; }
</style>
