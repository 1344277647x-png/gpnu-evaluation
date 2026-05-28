<template>
  <div class="course-card" @click="$router.push(`/course/${course.id}`)">
    <span class="card-category">{{ course.category?.name }}</span>
    <div class="card-title">{{ course.name }}</div>
    <div class="card-teacher">
      <el-icon :size="14"><User /></el-icon>
      {{ course.teacher?.name }}
    </div>
    <div class="card-meta">{{ course.semester }} · {{ course.teacher?.department }}</div>
    <div class="card-footer">
      <div class="card-rating" v-if="course.review_count">
        <span class="rating-num">{{ course.ratings?.overall }}</span>
        <span class="rating-label">综合评分</span>
      </div>
      <div class="card-rating" v-else>
        <span class="rating-label">暂无评价</span>
      </div>
      <span class="card-count">{{ course.review_count || 0 }} 条评价</span>
    </div>
  </div>
</template>

<script setup>
defineProps({ course: Object })
</script>

<style scoped>
.course-card {
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  padding: 20px;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s;
  display: flex;
  flex-direction: column;
}
.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 40px rgba(16, 185, 129, 0.12), 0 2px 8px rgba(0, 0, 0, 0.06);
}
.card-category {
  font-size: 12px; color: #059669;
  background: rgba(16,185,129,0.12); backdrop-filter: blur(4px);
  display: inline-block; padding: 2px 8px; border-radius: 6px;
  align-self: flex-start; margin-bottom: 10px;
}
.card-title { font-size: 16px; font-weight: 600; margin-bottom: 8px; line-height: 1.4; color: #111827; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-teacher { font-size: 13px; color: #374151; display: flex; align-items: center; gap: 4px; margin-bottom: 4px; }
.card-meta { font-size: 12px; color: #6b7280; margin-bottom: 14px; }
.card-footer { display: flex; align-items: flex-end; justify-content: space-between; margin-top: auto; }
.card-rating { display: flex; align-items: baseline; gap: 4px; }
.rating-num { font-size: 24px; font-weight: 700; color: #10b981; }
.rating-label { font-size: 12px; color: #6b7280; }
.card-count { font-size: 12px; color: #6b7280; }
</style>
