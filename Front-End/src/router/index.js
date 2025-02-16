import { createRouter, createWebHistory } from 'vue-router'
import guestRoutes from './guest'
import adminRoutes from './admin'
import professionalRoutes from './professional'
import userRoutes from './user'
import { toast } from 'vue3-toastify'
import NotFound from '../components/common/NotFound.vue'

const routes = [
  ...guestRoutes,
  ...adminRoutes,
  ...professionalRoutes,
  ...userRoutes,
  { path: '/:pathMatch(.*)*', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  // ✅ Redirect '/' to respective dashboard
  if (token) {
    if (role === 'admin' && to.path === '/') return next('/admin')
    if (role === 'professional' && to.path === '/') return next('/professional')
    if (role === 'user' && to.path === '/') return next('/user')
  }

  // ✅ Prevent unauthenticated access to protected routes
  if (to.meta.requiresAuth && !token) {
    toast.warn('You need to log in to access this page!', { autoClose: 3000 })
    setTimeout(() => next('/auth'), 1500) // ✅ Now it correctly redirects
    return
  }

  // ✅ Prevent logged-in users from accessing guest routes
  if (to.meta.requiresGuest && token) {
    toast.info('You are already logged in.', { autoClose: 3000 })
    setTimeout(() => {
      if (role === 'admin') next('/admin')
      else if (role === 'professional') next('/professional')
      else next('/user')
    }, 1500)
    return
  }

  // ✅ **Unauthorized Access Handling**
  if (token) {
    if (role === 'admin' && to.path.startsWith('/professional')) {
      toast.error('Access Denied! Redirecting to Admin Dashboard.', { autoClose: 3000 })
      setTimeout(() => next('/admin'), 1500)
      return
    }
    if (role === 'admin' && to.path.startsWith('/user')) {
      toast.error('Access Denied! Redirecting to Admin Dashboard.', { autoClose: 3000 })
      setTimeout(() => next('/admin'), 1500)
      return
    }

    if (role === 'professional' && to.path.startsWith('/admin')) {
      toast.error('Access Denied! Redirecting to Professional Dashboard.', { autoClose: 3000 })
      setTimeout(() => next('/professional'), 1500)
      return
    }
    if (role === 'professional' && to.path.startsWith('/user')) {
      toast.error('Access Denied! Redirecting to Professional Dashboard.', { autoClose: 3000 })
      setTimeout(() => next('/professional'), 1500)
      return
    }

    if (role === 'user' && to.path.startsWith('/admin')) {
      toast.error('Access Denied! Redirecting to User Dashboard.', { autoClose: 3000 })
      setTimeout(() => next('/user'), 1500)
      return
    }
    if (role === 'user' && to.path.startsWith('/professional')) {
      toast.error('Access Denied! Redirecting to User Dashboard.', { autoClose: 3000 })
      setTimeout(() => next('/user'), 1500)
      return
    }
  }

  next()
})

export default router
