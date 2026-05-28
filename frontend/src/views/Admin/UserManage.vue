<template>
  <div>
    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索用户名或昵称" clearable style="width:260px"
        @keyup.enter="doSearch" @clear="doSearch" />
    </div>
    <el-table :data="users" stripe v-loading="loading">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="student_id" label="学号" />
      <el-table-column prop="role" label="角色" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{row}">
          <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
            {{ row.is_active ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{row}">
          <el-button v-if="row.role!=='admin'" size="small"
            :type="row.is_active ? 'danger' : 'success'"
            @click="toggle(row.id)">
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-wrap">
      <el-pagination v-model:current-page="page" :total="total" :page-size="perPage"
        layout="prev, pager, next" @current-change="fetchUsers" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../../api'

const users = ref([])
const loading = ref(false)
const search = ref('')
const page = ref(1)
const perPage = 20
const total = ref(0)

function doSearch() { page.value = 1; fetchUsers() }

async function fetchUsers() {
  loading.value = true
  try {
    const res = await api.get('/api/admin/users', { params: { search: search.value || undefined, page: page.value, per_page: perPage } })
    users.value = res.data.data?.items || []
    total.value = res.data.data?.total || 0
  } finally { loading.value = false }
}

async function toggle(id) {
  await api.put(`/api/admin/users/${id}/toggle`)
  ElMessage.success('已更新')
  fetchUsers()
}

onMounted(fetchUsers)
</script>

<style scoped>
.search-bar { margin-bottom: 16px; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 16px; }
</style>
