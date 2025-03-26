import UserLayout from '@/layouts/UserLayout.vue'
import DashboardView from '@/views/user/DashboardView.vue'
import ProfileView from '@/views/user/ProfileView.vue'
import NotFound from '@/components/common/NotFound.vue'
import UserBooking from '../components/user/UserBooking.vue'
import UserAddress from '../components/user/UserAddress.vue'
import Services from '../components/common/Services.vue'
import LocationCategory from '../components/common/LocationCategory.vue'
import UserProfile from '../components/user/UserProfile.vue'

export default [
    {
        path: '/user',
        component: UserLayout,
        meta: { requiresAuth: true, role: 'user' },
        children: [
            { path: '', component: LocationCategory, name: 'user-services' },
            { path: 'bookings', component: UserBooking, name: 'user-booking' },
            { path: 'dashboard', component: DashboardView, name: 'user-dashboard' },
            { path: 'address', component: UserAddress, name: 'user-address' },
            { path: 'profile', name: 'user-profile', component: UserProfile },
            { path: ':pathMatch(.*)*', component: NotFound },
        ],
    },
]
