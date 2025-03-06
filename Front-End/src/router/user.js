import UserLayout from '@/layouts/UserLayout.vue'
import DashboardView from '@/views/user/DashboardView.vue'
import ProfileView from '@/views/user/ProfileView.vue'
import NotFound from '@/components/common/NotFound.vue'
import UserBooking from '../components/user/UserBooking.vue'

export default [
    {
        path: '/user',
        component: UserLayout,
        meta: { requiresAuth: true, role: 'user' },
        children: [
            { path: 'bookings', component: UserBooking, name: 'user-booking' },
            { path: 'dashboard', component: DashboardView, name: 'user-dashboard' },
            { path: 'profile', component: ProfileView, name: 'user-profile' },
            { path: ':pathMatch(.*)*', component: NotFound },
        ],
    },
]
