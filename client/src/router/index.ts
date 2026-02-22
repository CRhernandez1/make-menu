import { createRouter, createWebHistory } from 'vue-router'
import EstablishmentList from '@/views/EstablishmentList.vue'
import TableList from '@/views/TableList.vue'
import LandingView from '@/views/LandingView.vue'
import AuthView from '@/views/AuthView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path:'',name:"Home", component: LandingView},
    {path:"/login",name:"Login",component:AuthView},
    {
      path: '/establishments',
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
