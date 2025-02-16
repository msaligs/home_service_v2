import AdminLayout from '@/layouts/AdminLayout.vue'
import Dashboard from '@/views/admin/Dashboard.vue'

export default [
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', component: Dashboard, name: 'admin-dashboard' },
      { path: 'profile', component: () => import('@/views/admin/Profile.vue') },
    ],
  },
]
