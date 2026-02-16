import { createRouter, createWebHistory } from 'vue-router'
import AuthView from '@/views/AuthView.vue'
import LandingView from '@/views/LandingView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path:"",name:"Home",component:LandingView},
    {path:"/login",
      name:"Login",
      component: AuthView
    }
  ],
})

export default router
