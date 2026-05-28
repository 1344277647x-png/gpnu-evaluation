<template>
  <div>
    <el-table :data="courses" stripe v-loading="loading" empty-text="暂无待审核课程">
      <el-table-column prop="name" label="课程名称" />
      <el-table-column label="教师" width="120">
        <template #default="{row}">{{ row.teacher?.name }}</template>
      </el-table-column>
      <el-table-column label="分类" width="100">
        <template #default="{row}">{{ row.category?.name }}</template>
      </el-table-column>
      <el-table-column prop="semester" label="学期" width="120" />
      <el-table-column prop="created_by" label="提交者" width="100" />
      <el-table-column label="操作" width="180">
        <template #default="{row}">
          <el-button size="small" type="success" @click="approve(row.id)">通过</el-button>
          <el-button size="small" type="danger" @click="reject(row)">驳回</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../../api'

const courses = ref([])
const loading = ref(false)

async function fetchPending() {
  loading.value = true
  try {
    const res = await api.get('/api/courses/pending')
    courses.value = res.data.data?.items || []
  } finally { loading.value = false }
}

async function approve(id) {
  await api.put(`/api/courses/${id}/approve`)
  ElMessage.success('已通过')
  fetchPending()
}

async function reject(row) {
  try {
    const { value } = await ElMessageBox.prompt('请填写驳回理由', '驳回课程', { type: 'warning' })
    await api.put(`/api/courses/${row.id}/reject`, { reason: value })
    ElMessage.success('已驳回')
    fetchPending()
  } catch (e) { /* cancelled */ }
}

onMounted(fetchPending)
</script>
