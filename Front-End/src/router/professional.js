import ProfessionalLayout from '@/layouts/ProfessionalLayout.vue'
import Dashboard from '@/views/professional/Dashboard.vue'

export default [
  {
    path: '/professional',
    component: ProfessionalLayout,
    meta: { requiresAuth: true, role: 'professional' },
    children: [
      { path: 'dashboard', component: Dashboard, name: 'professional-dashboard' },
      { path: 'profile', component: () => import('@/views/professional/Profile.vue') },
    ],
  },
]
