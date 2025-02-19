import AdminLayout from '@/layouts/AdminLayout.vue'
import Dashboard from '@/views/admin/Dashboard.vue'
import AdminUsers from '../components/admin/AdminUsers.vue'
import ProfessionalDetails from '../components/admin/ProfessionalDetails.vue'
import ApproveProfessional from '../components/admin/ApproveProfessional.vue'
import AllProfessional from '../components/admin/AllProfessional.vue'

export default [
    {
        path: '/admin',
        component: AdminLayout,
        meta: { requiresAuth: true, role: 'admin' },
        children: [
            { path: '', component: Dashboard, name: 'admin-dashboard' },
            { path: 'profile', component: () => import('@/views/admin/Profile.vue') },
            { path: 'users', component: AdminUsers, name: 'admin-users' },
            { path: 'users/:id', component: ProfessionalDetails, name: 'professional-details' },
            {
                path: 'onboard-professional',
                component: ApproveProfessional,
                name: 'approve-professional',
            },
            { path: 'professional', component: AllProfessional, name: 'all-professional' },
        ],
    },
]
