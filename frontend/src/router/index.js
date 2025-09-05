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
      path: '/coaching',
      name: 'coaching',
      component: () => import('../views/CoachingView.vue'),
    },
    {
      path: '/refiner',
      name: 'refiner',
      component: () => import('../views/RefinerView.vue'),
    },
  ],
})

export default router