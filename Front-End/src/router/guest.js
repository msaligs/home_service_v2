import GuestLayout from '@/layouts/GuestLayout.vue'
import AuthView from '@/views/guest/AuthView.vue'
import Login from '@/components/guest/Login.vue'
import Register from '@/components/guest/UserRegister.vue'
import ForgotPassword from '@/components/guest/ForgotPassword.vue'
import Services from '../components/common/Services.vue'

export default [
  {
    path: '/',
    component: GuestLayout,
    children: [{ path: '', component: Services, name: 'services' }],
  },

  {
    path: '/auth',
    component: AuthView,
    name: 'auth',
    redirect: '/auth/login',
    children: [
      { path: 'login', component: Login, name: 'login' },
      { path: 'register', component: Register, name: 'register' },
      { path: 'forgot-password', component: ForgotPassword, name: 'forgot-password' },
    ],
    meta: { requiresGuest: true },
  },
  { path: '/unauthorized', component: () => import('@/views/guest/Unauthorized.vue') },
]
