import GuestLayout from '@/layouts/GuestLayout.vue'
import AuthView from '@/views/guest/AuthView.vue'
import Login from '@/components/guest/Login.vue'
import Register from '@/components/guest/UserRegister.vue'
import ForgotPassword from '@/components/guest/ForgotPassword.vue'
import Services from '../components/common/Services.vue'
import ProfessionalRegister from '../components/guest/ProfessionalRegister.vue'
import LocationCategory from '../components/common/LocationCategory.vue'

export default [
    {
        path: '/',
        component: GuestLayout,
        children: [
            { path: '', component: LocationCategory, name: 'location-category' },
            {
                path: '/services',
                component: Services,
                name: 'services',
            },
        ],
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
            {
                path: 'professional-register',
                component: ProfessionalRegister,
                name: 'professional-register',
            },
        ],
        meta: { requiresGuest: true },
    },

    // 🔹 Lazy-loaded Unauthorized Page
    {
        path: '/unauthorized',
        component: () => import('@/views/guest/Unauthorized.vue'),
        name: 'unauthorized',
    },
]
