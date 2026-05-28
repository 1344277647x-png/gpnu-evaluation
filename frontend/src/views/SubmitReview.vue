<template>
  <div class="review-page" v-if="course">
    <div class="page-header">
      <h2>评价课程</h2>
      <p class="subtitle">{{ course.name }} · {{ course.teacher?.name }}</p>
    </div>

    <el-card>
      <el-form ref="formRef" :model="form" label-position="top">
        <el-row :gutter="20">
          <el-col :span="12" :xs="24">
            <el-form-item label="教学质量" prop="rating_teaching">
              <div class="rating-row">
                <el-rate v-model="form.rating_teaching" :max="5" :texts="rateTexts" show-text />
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="12" :xs="24">
            <el-form-item label="课程内容" prop="rating_content">
              <el-rate v-model="form.rating_content" :max="5" :texts="rateTexts" show-text />
            </el-form-item>
          </el-col>
          <el-col :span="12" :xs="24">
            <el-form-item label="考核方式" prop="rating_exam">
              <el-rate v-model="form.rating_exam" :max="5" :texts="rateTexts" show-text />
            </el-form-item>
          </el-col>
          <el-col :span="12" :xs="24">
            <el-form-item label="给分公平度" prop="rating_fairness">
              <el-rate v-model="form.rating_fairness" :max="5" :texts="rateTexts" show-text />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="评语（选填）">
          <el-input v-model="form.comment" type="textarea" :rows="4" maxlength="2000" show-word-limit
            placeholder="分享一下你的上课体验..." />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="submit">提交评价</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'

const route = useRoute()
const router = useRouter()
const courseId = Number(route.params.id)
const course = ref(null)
const submitting = ref(false)
const rateTexts = ['很差', '较差', '一般', '较好', '很好']
const form = reactive({ rating_teaching: 3, rating_content: 3, rating_exam: 3, rating_fairness: 3, comment: '' })

async function submit() {
  if (!form.rating_teaching || !form.rating_content || !form.rating_exam || !form.rating_fairness) {
    ElMessage.warning('请完成所有评分')
    return
  }
  submitting.value = true
  try {
    await api.post(`/api/courses/${courseId}/reviews`, {
      rating_teaching: form.rating_teaching,
      rating_content: form.rating_content,
      rating_exam: form.rating_exam,
      rating_fairness: form.rating_fairness,
      comment: form.comment
    })
    ElMessage.success('评价成功')
    router.push(`/course/${courseId}`)
  } finally { submitting.value = false }
}

onMounted(async () => {
  const res = await api.get(`/api/courses/${courseId}`)
  course.value = res.data.data
})
</script>

<style scoped>
.subtitle { font-size: 14px; color: #909399; margin-top: 4px; }
</style>
