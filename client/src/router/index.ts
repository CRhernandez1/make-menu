import { createRouter, createWebHistory } from 'vue-router'
import EstablishmentList from '@/views/EstablishmentList.vue'
import TableList from '@/views/TableList.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'establishments',
      component: EstablishmentList
    },
    {
      path: '/establishments/:cif/tables',
      name: 'tables',
      component: TableList,
      props: true
    }
  ]
})

export default router
