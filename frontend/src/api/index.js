import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '',
  timeout: 15000
})

// 请求拦截：附带 token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('gpnu_access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：统一解包 + 401 刷新
let isRefreshing = false
let refreshQueue = []

function processQueue(token) {
  refreshQueue.forEach(cb => cb(token))
  refreshQueue = []
}

api.interceptors.response.use(
  res => res,
  async error => {
    const msg = error.response?.data?.message || '网络错误'
    const code = error.response?.data?.code

    // 401 尝试刷新
    if (error.response?.status === 401 && code !== 401) {
      // code 不是 401 说明不是刷新失败，尝试刷新
    }

    if (code === 401 && error.config && !error.config._retry) {
      const refreshToken = localStorage.getItem('gpnu_refresh_token')
      if (!refreshToken) {
        localStorage.removeItem('gpnu_access_token')
        localStorage.removeItem('gpnu_user')
        ElMessage.error('登录已过期，请重新登录')
        window.location.href = '/login'
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise(resolve => {
          refreshQueue.push(newToken => {
            error.config.headers.Authorization = `Bearer ${newToken}`
            error.config._retry = true
            resolve(api(error.config))
          })
        })
      }

      isRefreshing = true
      error.config._retry = true

      try {
        const res = await axios.post('/api/auth/refresh', { refresh_token: refreshToken })
        const newToken = res.data.data.access_token
        const newRefresh = res.data.data.refresh_token
        localStorage.setItem('gpnu_access_token', newToken)
        localStorage.setItem('gpnu_refresh_token', newRefresh)
        processQueue(newToken)
        error.config.headers.Authorization = `Bearer ${newToken}`
        return api(error.config)
      } catch (e) {
        processQueue(null)
        localStorage.removeItem('gpnu_access_token')
        localStorage.removeItem('gpnu_refresh_token')
        localStorage.removeItem('gpnu_user')
        ElMessage.error('登录已过期，请重新登录')
        window.location.href = '/login'
        return Promise.reject(error)
      } finally {
        isRefreshing = false
      }
    }

    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

export default api
