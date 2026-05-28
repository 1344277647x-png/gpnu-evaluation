<template>
  <div>
    <div class="page-header"><h2>个人中心</h2></div>

    <el-row :gutter="20">
      <el-col :span="8" :xs="24">
        <el-card class="mb-16">
          <template #header><span>个人信息</span></template>
          <el-form label-position="top">
            <el-form-item label="昵称">
              <el-input v-model="profile.nickname" />
            </el-form-item>
            <el-form-item label="学号">
              <el-input v-model="profile.student_id" />
            </el-form-item>
            <el-button type="primary" :loading="saving" @click="saveProfile">保存</el-button>
          </el-form>
        </el-card>
        <el-card>
          <template #header><span>修改密码</span></template>
          <el-form label-position="top">
            <el-form-item label="原密码">
              <el-input v-model="pwForm.old_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="pwForm.new_password" type="password" show-password placeholder="至少8位，含大小写字母和数字" />
            </el-form-item>
            <el-button type="primary" :loading="changingPw" @click="changePassword">修改密码</el-button>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="16" :xs="24">
        <el-card class="mb-16">
          <template #header><span>我的评价 ({{ myReviewsTotal }})</span></template>
          <el-table :data="myReviews" stripe v-loading="loadingReviews" empty-text="暂无评价">
            <el-table-column prop="course_name" label="课程" />
            <el-table-column label="综合评分" width="100">
              <template #default="{row}">{{ avgRating(row) }}</template>
            </el-table-column>
            <el-table-column label="评语" min-width="160">
              <template #default="{row}">{{ row.comment || '-' }}</template>
            </el-table-column>
            <el-table-column label="时间" width="110">
              <template #default="{row}">{{ fmt(row.created_at) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="{row}">
                <el-button text type="primary" @click="$router.push(`/course/${row.course_id}`)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="myReviewsTotal > 10" class="pagination-wrap">
            <el-pagination small layout="prev, pager, next" :total="myReviewsTotal" :page-size="10"
              v-model:current-page="reviewPg" @current-change="fetchMyReviews" />
          </div>
        </el-card>

        <el-card>
          <template #header><span>我提交的课程</span></template>
          <el-table :data="myCourses" stripe v-loading="loadingCourses" empty-text="暂无提交">
            <el-table-column prop="name" label="课程名称" />
            <el-table-column label="状态" width="100">
              <template #default="{row}">
                <el-tag v-if="row.status==='approved'" type="success" size="small">已通过</el-tag>
                <el-tag v-else-if="row.status==='pending'" type="warning" size="small">审核中</el-tag>
                <el-tag v-else-if="row.status==='rejected'" type="danger" size="small">已驳回</el-tag>
                <el-tag v-else type="info" size="small">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="驳回理由" min-width="120">
              <template #default="{row}">{{ row.reject_reason || '-' }}</template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import api from '../api'

const userStore = useUserStore()

const profile = reactive({ nickname: userStore.user?.nickname || '', student_id: userStore.user?.student_id || '' })
const pwForm = reactive({ old_password: '', new_password: '' })
const saving = ref(false)
const changingPw = ref(false)

const myReviews = ref([])
const myReviewsTotal = ref(0)
const reviewPg = ref(1)
const loadingReviews = ref(false)
const myCourses = ref([])
const loadingCourses = ref(false)

function avgRating(r) {
  const s = (r.rating_teaching + r.rating_content + r.rating_exam + r.rating_fairness) / 4
  return s.toFixed(1)
}
function fmt(t) { return t ? new Date(t).toLocaleDateString('zh-CN') : '' }

async function saveProfile() {
  saving.value = true
  try {
    await api.put('/api/auth/profile', profile)
    userStore.updateUser({ ...userStore.user, nickname: profile.nickname, student_id: profile.student_id })
    ElMessage.success('已更新')
  } finally { saving.value = false }
}

async function changePassword() {
  if (!pwForm.old_password || !pwForm.new_password) { ElMessage.warning('请填写完整'); return }
  changingPw.value = true
  try {
    await api.put('/api/auth/password', pwForm)
    ElMessage.success('密码修改成功')
    pwForm.old_password = ''; pwForm.new_password = ''
  } finally { changingPw.value = false }
}

async function fetchMyReviews() {
  loadingReviews.value = true
  try {
    const res = await api.get('/api/my/reviews', { params: { page: reviewPg.value } })
    myReviews.value = res.data.data?.items || []
    myReviewsTotal.value = res.data.data?.total || 0
  } finally { loadingReviews.value = false }
}

async function fetchMyCourses() {
  loadingCourses.value = true
  try {
    const res = await api.get('/api/my/courses')
    myCourses.value = res.data.data?.items || []
  } finally { loadingCourses.value = false }
}

onMounted(() => { fetchMyReviews(); fetchMyCourses() })
</script>

<style scoped>
.mb-16 { margin-bottom: 16px; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 12px; }
</style>
