<template>
  <div v-if="course">
    <div class="course-header">
      <div class="course-info">
        <el-tag size="small" type="primary">{{ course.category?.name }}</el-tag>
        <h2>{{ course.name }}</h2>
        <div class="course-meta">
          <span><el-icon><User /></el-icon> {{ course.teacher?.name }} · {{ course.teacher?.department }}</span>
          <span><el-icon><Calendar /></el-icon> {{ course.semester }}</span>
        </div>
        <p v-if="course.description" class="course-desc">{{ course.description }}</p>
      </div>
      <div class="course-score">
        <div class="overall">{{ course.ratings?.overall || '-' }}</div>
        <div class="overall-label">综合评分</div>
        <div class="review-count">{{ course.review_count }} 条评价</div>
      </div>
    </div>

    <el-card class="section-card">
      <template #header><span>评分雷达图</span></template>
      <div v-if="course.review_count">
        <RadarChart :ratings="course.ratings" :height="300" />
      </div>
      <EmptyState v-else>暂无评价，来做第一个评价的人吧</EmptyState>
    </el-card>

    <el-card v-if="userStore.isLoggedIn && myReview" class="section-card">
      <template #header><span>我的评价</span></template>
      <ReviewItem :review="myReview" />
    </el-card>

    <div class="action-bar">
      <el-button v-if="userStore.isLoggedIn && !myReview && course.status==='approved'" type="primary"
        @click="$router.push(`/course/${course.id}/review`)">
        <el-icon><Edit /></el-icon> 我要评价
      </el-button>
      <el-button v-if="myReview && myReview.user?.id===userStore.user?.id" type="danger" plain
        @click="deleteMyReview">
        <el-icon><Delete /></el-icon> 删除我的评价
      </el-button>
    </div>

    <el-card class="section-card">
      <template #header><span>全部评价 ({{ reviewTotal }})</span></template>
      <div v-if="reviews.length">
        <ReviewItem v-for="r in reviews" :key="r.id" :review="r" />
        <div v-if="reviewTotal > reviewPerPage" class="pagination-wrap">
          <el-pagination v-model:current-page="reviewPage" :total="reviewTotal"
            :page-size="reviewPerPage" layout="prev, pager, next" @current-change="fetchReviews" />
        </div>
      </div>
      <EmptyState v-else>暂无评价</EmptyState>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '../stores/user'
import RadarChart from '../components/RadarChart.vue'
import ReviewItem from '../components/ReviewItem.vue'
import EmptyState from '../components/illustrations/EmptyState.vue'
import api from '../api'

const route = useRoute()
const userStore = useUserStore()
const courseId = Number(route.params.id)
const course = ref(null)
const reviews = ref([])
const myReview = ref(null)
const reviewPage = ref(1)
const reviewPerPage = 10
const reviewTotal = ref(0)

async function fetchCourse() {
  const res = await api.get(`/api/courses/${courseId}`)
  course.value = res.data.data
}

async function fetchReviews() {
  const res = await api.get(`/api/courses/${courseId}/reviews`, {
    params: { page: reviewPage.value, per_page: reviewPerPage }
  })
  const d = res.data.data
  reviews.value = d.items; reviewTotal.value = d.total
  if (userStore.isLoggedIn) {
    myReview.value = d.items.find(r => r.user?.id === userStore.user?.id) || myReview.value
  }
}

async function deleteMyReview() {
  await ElMessageBox.confirm('确定删除你的评价吗？', '提示', { type: 'warning' })
  await api.delete(`/api/reviews/${myReview.value.id}`)
  myReview.value = null
  await fetchCourse()
  await fetchReviews()
}

onMounted(async () => { await fetchCourse(); await fetchReviews() })
</script>

<style scoped>
.course-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap; gap: 20px; }
.course-info h2 { font-size: 24px; margin: 8px 0; color: #1f2937; }
.course-meta { display: flex; gap: 16px; font-size: 14px; color: #374151; margin-bottom: 8px; }
.course-meta span { display: flex; align-items: center; gap: 4px; }
.course-desc { font-size: 14px; color: #374151; line-height: 1.7; max-width: 700px; }
.course-score { text-align: center; background: rgba(16,185,129,0.12); backdrop-filter: blur(8px); border-radius: 16px; padding: 20px 32px; min-width: 120px; border: 1px solid rgba(16,185,129,0.15); }
.overall { font-size: 40px; font-weight: 700; color: #10b981; }
.overall-label { font-size: 13px; color: #6b7280; margin-top: 4px; }
.review-count { font-size: 12px; color: #6b7280; margin-top: 4px; }
.section-card { margin-bottom: 16px; }
.action-bar { margin-bottom: 16px; display: flex; gap: 12px; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 16px; }
</style>
