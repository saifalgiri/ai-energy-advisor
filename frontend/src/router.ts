import type { RouteRecordRaw } from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from './views/Dashboard.vue'
import House  from './views/House.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/',
    name: 'House',
    component: House,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
