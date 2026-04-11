import NotFound404 from '@/components/NotFound404.vue'
import LandingLayout from '@/modules/landing/layouts/LandingLayout.vue'
import HomeView from '@/modules/landing/views/HomeView.vue'
import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router'

// 🛡️ FÁBRICA DE GUARDS: Reutilizamos esta lógica para los 3 roles
const requireRoleGuard = (expectedRole: string) => {
  return async (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
    // Importación dinámica para evitar problemas de carga inicial con Pinia
    const { useAuthStore } = await import('@/modules/auth/stores/auth.store')
    const authStore = useAuthStore()

    if (authStore.isChecking) {
      await authStore.checkAuthStatus()
    }

    if (!authStore.isAuthenticated || authStore.user?.role !== expectedRole) {
      console.warn(`Acceso denegado: Área exclusiva para el rol '${expectedRole}'.`)
      return { name: 'login' }
    }

    return true // Pase VIP concedido
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // --- ZONA PÚBLICA ---
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
    
    // --- ZONA DE AUTENTICACIÓN ---
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
            const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

            if (!code || !uuidRegex.test(code)) {
              console.warn('Intento de acceso con enlace inválido o corrupto.')
              return { name: 'login' }
            }
            return true
          },
        },
      ],
    },

    // --- 👔 ZONA MANAGER ---
    {
      path: '/manager',
      component: () => import('@/modules/manager/layouts/ManagerLayout.vue'),
      beforeEnter: requireRoleGuard('manager'), // 👈 Usamos nuestra fábrica
      children: [
        {
          path: '', 
          name: 'manager', 
          component: () => import('@/modules/manager/views/ManagerHome.vue'),
        },{
      path: 'orders',
      name: 'manager-orders',
      component: () => import('@/modules/manager/views/ManagerOrders.vue'),
    },
        
        {
          path: 'invite',
          name: 'manager-invite',
          component: () => import('@/modules/manager/views/StaffInviteView.vue'),
        },
        {
          path: 'products',
          name: 'products',
          component: () => import('@/modules/manager/views/Products.vue')
        },
        {
          path: 'ingredients',
          name: 'ingredients',
          component: () => import('@/modules/manager/views/Ingredients.vue')
        }
      ],
    },

    // --- 👨‍🍳 ZONA KITCHEN ---
    {
      path: '/kitchen',
      component: () => import('@/modules/kitchen/layouts/KitchenLayout.vue'),
      beforeEnter: requireRoleGuard('kitchen'), // 👈 Usamos nuestra fábrica
      children: [
        {
          path: '', 
          name: 'kitchen', 
          component: () => import('@/modules/kitchen/views/KitchenHome.vue'),
        },
      ],
    },

    // --- 🏃‍♂️ ZONA WAITER ---
    {
      path: '/waiter',
      component: () => import('@/modules/waiter/layouts/WaiterLayout.vue'),
      beforeEnter: requireRoleGuard('waiter'), // 👈 Usamos nuestra fábrica
      children: [
        {
          path: '', 
          name: 'waiter', 
          component: () => import('@/modules/waiter/views/WaiterHome.vue'),
        },
      ],
    },

    // --- 404 NOT FOUND ---
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound404,
    },
  ],
})

export default router