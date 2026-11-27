
import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import PublicationsCountByUniversity from '../views/PublicationsCountByUniversity/PublicationsCountByUniversity.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/cs_statistics',
      name: 'home',
      component: Home,
    },
    {
      path: '/cs_statistics/publications-count-by-university',
      name: 'publications-count-by-university',
      component: PublicationsCountByUniversity,
    },
  ],

  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
