<template>
  <div v-loading="loading">
    <el-row :gutter="20">
      <el-col :span="6" :xs="12" v-for="s in statCards" :key="s.label">
        <el-card class="stat-card">
          <div class="stat-num">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const loading = ref(false)
const stats = ref({})

const statCards = computed(() => [
  { label: '课程总数', value: stats.value.course_count || 0 },
  { label: '已审核', value: stats.value.approved_count || 0 },
  { label: '待审核', value: stats.value.pending_count || 0 },
  { label: '评价总数', value: stats.value.review_count || 0 },
  { label: '用户数', value: stats.value.user_count || 0 }
])

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/api/admin/stats')
    stats.value = res.data.data || {}
  } finally { loading.value = false }
})
</script>

<style scoped>
.stat-card { text-align: center; padding: 8px 0; }
.stat-num { font-size: 36px; font-weight: 700; color: #10b981; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
</style>
