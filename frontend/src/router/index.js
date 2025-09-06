import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/coach',
      name: 'coaching',
      component: () => import('../views/CoachView.vue'),
    },
    {
      path: '/refiner',
      name: 'refiner',
      component: () => import('../views/RefinerView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/DocsView.vue'),
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
  ],
})

export default router