import NotFound404 from '@/components/NotFound404.vue'
import LandingLayout from '@/modules/landing/layouts/LandingLayout.vue'
import HomeView from '@/modules/landing/views/HomeView.vue'
import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router'

const requireRoleGuard = (expectedRole: string) => {
  return async (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
    const { useAuthStore } = await import('@/modules/auth/stores/auth.store')
    const authStore = useAuthStore()

    if (authStore.isChecking) {
      await authStore.checkAuthStatus()
    }

    if (!authStore.isAuthenticated || authStore.user?.role !== expectedRole) {
      console.warn(`Acceso denegado: Área exclusiva para el rol '${expectedRole}'.`)
      return { name: 'login' }
    }

    return true
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
      beforeEnter: requireRoleGuard('manager'),
      children: [
        {
          path: '',
          name: 'manager',
          redirect: { name: 'establishments' },
        },
        {
          path: 'establishments',
          name: 'establishments',
          component: () => import('@/modules/manager/views/EstablishmentsView.vue'),
        },
        {
          path: 'establishments/:cif/tables',
          name: 'tables',
          component: () => import('@/modules/manager/views/TablesView.vue'),
        },
        {
          path: 'establishments/:cif/staff',
          name: 'staff',
          component: () => import('@/modules/manager/views/StaffView.vue'),
        },
        {
          path: 'invite',
          name: 'manager-invite',
          component: () => import('@/modules/manager/views/StaffInviteView.vue'),
        },
        {
          path: 'orders',
          name: 'manager-orders',
          component: () => import('@/modules/manager/views/ManagerOrders.vue'),
        },
        {
          path: 'products',
          name: 'products',
          component: () => import('@/modules/manager/views/Products.vue'),
        },
        {
          path: 'products/:productId',
          name: 'product-detail',
          component: () => import('@/modules/manager/views/ProductDetailView.vue'),
        },
        {
          path: 'ingredients',
          name: 'ingredients',
          component: () => import('@/modules/manager/views/Ingredients.vue'),
        },
      ],
    },

    // --- 👨‍🍳 ZONA KITCHEN ---
    {
      path: '/kitchen',
      component: () => import('@/modules/kitchen/layouts/KitchenLayout.vue'),
      beforeEnter: requireRoleGuard('kitchen'),
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
      beforeEnter: requireRoleGuard('waiter'),
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