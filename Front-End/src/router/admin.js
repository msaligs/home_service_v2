import AdminLayout from '@/layouts/AdminLayout.vue'
import AdminDashboard from '../components/admin/AdminDashboard.vue'
import AdminUsers from '../components/admin/AdminUsers.vue'
import ProfessionalDetails from '../components/admin/ProfessionalDetails.vue'
import ApproveProfessional from '../components/admin/ApproveProfessional.vue'
import AllProfessional from '../components/admin/AllProfessional.vue'
import AdminLocation from '../components/admin/AdminLocation.vue'
import AddLocation from '../components/admin/AddLocation.vue'
import AdminCategories from '../components/admin/AdminCategories.vue'
import AddCategory from '../components/admin/AddCategory.vue'
import AdminServices from '../components/admin/AdminServices.vue'
import AddService from '../components/admin/AddService.vue'
import Profile from '../components/admin/AdminProfile.vue'

export default [
    {
        path: '/admin',
        component: AdminLayout,
        meta: { requiresAuth: true, role: 'admin' },
        redirect: '/admin/dashboard',
        children: [
            { path: 'dashboard', component: AdminDashboard, name: 'admin-dashboard' },
            { path: 'profile', component: Profile, name: 'admin-profile' },
            { path: 'users', component: AdminUsers, name: 'admin-users' },
            {
                path: 'professional/:id',
                component: ProfessionalDetails,
                name: 'professional-details',
            },
            {
                path: 'onboard-professional',
                component: ApproveProfessional,
                name: 'approve-professional',
            },
            { path: 'professionals', component: AllProfessional, name: 'all-professional' },
            {
                path: 'locations',
                component: AdminLocation,
                name: 'admin-location',
            },

            { path: 'add-location', component: AddLocation, name: 'add-location' },
            {
                path: 'categories',
                component: AdminCategories,
                name: 'admin-categories',
            },
            { path: 'add-category', component: AddCategory, name: 'add-category' },
            {
                path: 'services',
                component: AdminServices,
                name: 'admin-services',
            },
            { path: 'add-service', component: AddService, name: 'add-service' },
        ],
    },
]
