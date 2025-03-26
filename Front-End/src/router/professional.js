import ProfessionalLayout from '@/layouts/ProfessionalLayout.vue'
import Dashboard from '@/views/professional/Dashboard.vue'
import ProfessionalRequestCheck from '../components/professional/professionalRequestCheck.vue'

export default [
    {
        path: '/professional',
        component: ProfessionalLayout,
        meta: { requiresAuth: true, role: 'professional' },
        children: [
            { path: '', component: ProfessionalRequestCheck, name: 'professional-request-check' },
            { path: 'dashboard', component: Dashboard, name: 'professional-dashboard' },
            { path: 'profile', component: () => import('@/views/professional/Profile.vue') },
        ],
    },
]
