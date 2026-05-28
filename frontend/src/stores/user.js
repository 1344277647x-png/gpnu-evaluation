import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const TOKEN_KEY = 'gpnu_access_token'
const REFRESH_KEY = 'gpnu_refresh_token'
const USER_KEY = 'gpnu_user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const refreshToken = ref(localStorage.getItem(REFRESH_KEY) || '')
  const user = ref(JSON.parse(localStorage.getItem(USER_KEY) || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  function setAuth(access, refresh, u) {
    token.value = access
    refreshToken.value = refresh
    user.value = u
    localStorage.setItem(TOKEN_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
    localStorage.setItem(USER_KEY, JSON.stringify(u))
  }

  function updateUser(u) {
    user.value = u
    localStorage.setItem(USER_KEY, JSON.stringify(u))
  }

  function setAccessToken(t) {
    token.value = t
    localStorage.setItem(TOKEN_KEY, t)
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
  }

  return { token, refreshToken, user, isLoggedIn, isAdmin, setAuth, updateUser, setAccessToken, logout }
})
