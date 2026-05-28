import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/course/:id',
    name: 'CourseDetail',
    component: () => import('../views/CourseDetail.vue')
  },
  {
    path: '/course/:id/review',
    name: 'SubmitReview',
    component: () => import('../views/SubmitReview.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/course/add',
    name: 'AddCourse',
    component: () => import('../views/AddCourse.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my',
    name: 'MyPage',
    component: () => import('../views/MyPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin/Index.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('gpnu_access_token')
  const user = JSON.parse(localStorage.getItem('gpnu_user') || 'null')

  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }
  if (to.meta.requiresAdmin && user?.role !== 'admin') {
    return next('/')
  }
  next()
})

export default router
