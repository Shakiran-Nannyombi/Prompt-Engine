import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/coach',
    name: 'coaching',
    component: () => import('../views/CoachView.vue'),
    meta: { requiresAuth: true } // Protected route
  },
  {
    path: '/refiner',
    name: 'refiner',
    component: () => import('../views/RefinerView.vue'),
    meta: { requiresAuth: true } // Protected route
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/tutorials',
    name: 'tutorials',
    component: () => import('../views/TutorialsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  // Import auth store dynamically to avoid circular dependency
  import('../stores/useAuthStore').then(({ useAuthStore }) => {
    const authStore = useAuthStore()

    // Check if route requires authentication
    if (to.meta.requiresAuth && !authStore.checkAuth()) {
      // Redirect to login with return URL
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  })
})

export default router