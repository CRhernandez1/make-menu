import NotFound404 from '@/components/NotFound404.vue'
import LandingLayout from '@/modules/landing/layouts/LandingLayout.vue'
import HomeView from '@/modules/landing/views/HomeView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
      ],
    },
    {
      path: '/auth',
      redirect: '/login',
      component: () => import('@/modules/auth/layouts/AuthLayout.vue'),
      children: [
        {
          path: '/login',
          name: 'login',
          component: () => import('@/modules/auth/views/LoginView.vue'),
        },
        {
          path: '/register',
          name: 'register',
          component: () => import('@/modules/auth/views/RegisterView.vue'),
          beforeEnter: (to) => {
            const code = to.query.code as string

            // Esta fórmula matemática comprueba que el formato sea 8-4-4-4-12 caracteres hexadecimales
            const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

            // Si no hay código o no pasa la prueba del formato UUID, lo echamos
            if (!code || !uuidRegex.test(code)) {
              console.warn('Intento de acceso con enlace inválido o corrupto.')
              return { name: 'login' }
            }

            return true // Formato correcto, le dejamos ver la pantalla
          },
        },
      ],
    },
    {
      path: '/manager',
      name: 'manager',
      component: () => import('@/modules/manager/layouts/ManagerLayout.vue'),
      children: [
        {
          path: 'invite',
          name: 'manager-invite',
          component: () => import('@/modules/manager/views/StaffInviteView.vue'),
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound404,
    },
  ],
})

export default router
