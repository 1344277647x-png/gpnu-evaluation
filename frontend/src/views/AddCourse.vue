<template>
  <div>
    <div class="page-header"><h2>提交新课</h2></div>
    <el-card>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="课程名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入课程全称" maxlength="200" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12" :xs="24">
            <el-form-item label="授课教师" prop="teacher_id">
              <div class="teacher-row">
                <el-select v-model="form.teacher_id" filterable placeholder="搜索或选择教师" style="flex:1"
                  @focus="fetchTeacherOptions()" @visible-change="(v)=>v&&fetchTeacherOptions()">
                  <el-option v-for="t in teacherOptions" :key="t.id" :label="`${t.name} (${t.department})`" :value="t.id" />
                </el-select>
                <el-button @click="showAddTeacher = true" :icon="Plus" circle />
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="12" :xs="24">
            <el-form-item label="课程分类" prop="category_id">
              <el-select v-model="form.category_id" placeholder="选择分类" style="width:100%">
                <el-option v-for="c in appStore.categories" :key="c.id" :label="c.name" :value="c.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="学期" prop="semester">
          <el-input v-model="form.semester" placeholder="如：2025-2026-2" maxlength="20" />
        </el-form-item>
        <el-form-item label="课程简介（选填）">
          <el-input v-model="form.description" type="textarea" :rows="3" maxlength="2000" show-word-limit
            placeholder="简单介绍一下这门课..." />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="submit">提交审核</el-button>
          <el-button @click="$router.push('/')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Add Teacher Dialog -->
    <el-dialog v-model="showAddTeacher" title="添加新教师" width="400px" :close-on-click-modal="false">
      <el-form label-position="top" @submit.prevent="addTeacher">
        <el-form-item label="教师姓名" required>
          <el-input v-model="newTeacher.name" placeholder="如：王建国" maxlength="100" />
        </el-form-item>
        <el-form-item label="所属学院">
          <el-input v-model="newTeacher.department" placeholder="如：计算机学院" maxlength="100" />
        </el-form-item>
        <el-button type="primary" :loading="addingTeacher" @click="addTeacher" style="width:100%">确认添加</el-button>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useAppStore } from '../stores/app'
import api from '../api'

const router = useRouter()
const appStore = useAppStore()
const submitting = ref(false)
const teacherOptions = ref([])

const form = reactive({ name: '', teacher_id: null, category_id: null, semester: '', description: '' })
const rules = {
  name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  semester: [{ required: true, message: '请输入学期', trigger: 'blur' }]
}

const showAddTeacher = ref(false)
const addingTeacher = ref(false)
const newTeacher = reactive({ name: '', department: '' })

async function fetchTeacherOptions(search='') {
  const res = await api.get('/api/teachers', { params: { search, per_page: 50 } })
  teacherOptions.value = res.data.data?.items || []
}

async function addTeacher() {
  const name = newTeacher.name.trim()
  if (!name) { ElMessage.warning('请输入教师姓名'); return }
  addingTeacher.value = true
  try {
    const res = await api.post('/api/teachers', { name, department: newTeacher.department.trim() })
    const tid = res.data.data.id
    ElMessage.success(`已添加教师：${name}`)
    showAddTeacher.value = false
    newTeacher.name = ''
    newTeacher.department = ''
    await fetchTeacherOptions()
    form.teacher_id = tid
  } catch (e) {
    // handled by interceptor
  } finally {
    addingTeacher.value = false
  }
}

async function submit() {
  submitting.value = true
  try {
    await api.post('/api/courses', form)
    ElMessage.success('提交成功，等待管理员审核')
    router.push('/my')
  } finally { submitting.value = false }
}

onMounted(() => appStore.fetchCategories())
</script>

<style scoped>
.teacher-row { display: flex; gap: 8px; align-items: center; }
</style>
