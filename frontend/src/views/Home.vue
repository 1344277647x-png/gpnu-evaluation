<template>
  <div>
    <div class="page-header">
      <h2>课程广场</h2>
      <p class="subtitle">浏览公选课评价，选课不踩坑</p>
    </div>

    <div class="search-bar">
      <el-input v-model="search" placeholder="搜索课程名或教师名" clearable :prefix-icon="Search"
        class="search-input" @keyup.enter="doSearch" @clear="doSearch" />
      <el-select v-model="categoryId" placeholder="全部分类" clearable class="filter-select" @change="doSearch">
        <el-option v-for="c in appStore.categories" :key="c.id" :label="c.name" :value="c.id" />
      </el-select>
      <el-select v-model="semester" placeholder="全部学期" clearable class="filter-select" @change="doSearch">
        <el-option v-for="s in semesters" :key="s" :label="s" :value="s" />
      </el-select>
      <el-select v-model="sort" class="sort-select" @change="doSearch">
        <el-option label="按评分排序" value="rating" />
        <el-option label="按最新排序" value="newest" />
      </el-select>
    </div>

    <div v-if="loading" class="loading-wrap"><el-skeleton :rows="3" animated /></div>
    <template v-else>
      <div v-if="courses.length" class="course-grid">
        <CourseCard v-for="c in courses" :key="c.id" :course="c" />
      </div>
      <EmptyState v-else>暂无课程，去提交一门新课吧</EmptyState>
    </template>

    <div v-if="total > perPage" class="pagination-wrap">
      <el-pagination v-model:current-page="page" :total="total" :page-size="perPage"
        layout="prev, pager, next" @current-change="fetchCourses" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import CourseCard from '../components/CourseCard.vue'
import EmptyState from '../components/illustrations/EmptyState.vue'
import api from '../api'

const appStore = useAppStore()
const search = ref('')
const categoryId = ref(null)
const semester = ref('')
const sort = ref('rating')
const page = ref(1)
const perPage = 12
const total = ref(0)
const courses = ref([])
const semesters = ref([])
const loading = ref(false)

function doSearch() { page.value = 1; fetchCourses() }

async function fetchCourses() {
  loading.value = true
  try {
    const res = await api.get('/api/courses', { params: {
      search: search.value || undefined, category_id: categoryId.value || undefined,
      semester: semester.value || undefined, sort: sort.value, page: page.value, per_page: perPage
    }})
    const d = res.data.data
    courses.value = d.items; total.value = d.total
  } finally { loading.value = false }
}

onMounted(async () => {
  await appStore.fetchCategories()
  await fetchCourses()
  try {
    const res = await api.get('/api/courses', { params: { per_page: 1000 } })
    semesters.value = [...new Set((res.data.data?.items||[]).map(c=>c.semester).filter(Boolean))].sort().reverse()
  } catch(e){}
})
</script>

<style scoped>
.subtitle { font-size: 14px; color: #9ca3af; margin-top: 4px; }
.search-bar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.search-input { flex: 1; min-width: 200px; }
.filter-select { width: 140px; }
.sort-select { width: 130px; }
.loading-wrap { background: rgba(255,255,255,0.18); backdrop-filter: blur(12px); padding: 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.22); }
.pagination-wrap { display: flex; justify-content: center; margin-top: 24px; }
</style>
