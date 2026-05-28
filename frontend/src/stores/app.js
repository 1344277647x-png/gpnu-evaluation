import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useAppStore = defineStore('app', () => {
  const categories = ref([])
  const teachers = ref([])

  async function fetchCategories() {
    if (categories.value.length) return
    const res = await api.get('/api/categories')
    categories.value = res.data.data || []
  }

  async function fetchTeachers(search = '') {
    const res = await api.get('/api/teachers', { params: { search, per_page: 50 } })
    teachers.value = res.data.data?.items || []
    return teachers.value
  }

  return { categories, teachers, fetchCategories, fetchTeachers }
})
