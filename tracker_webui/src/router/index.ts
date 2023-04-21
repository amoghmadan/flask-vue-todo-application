import { createRouter, createWebHistory } from 'vue-router'

import { URLs } from "@/constants";
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: URLs.ROOT,
      name: 'home',
      component: HomeView
    },
    {
      path: URLs.TODO,
      name: 'todo',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/TodoView.vue')
    }
  ]
})

export default router
