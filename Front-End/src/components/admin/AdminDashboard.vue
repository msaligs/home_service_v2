<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { Bar, Pie, Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    ArcElement,
    LineElement,
    CategoryScale,
    LinearScale,
} from 'chart.js'
import api from '../../api'
import { toast } from 'vue3-toastify'

// Register Chart.js components
ChartJS.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    ArcElement,
    LineElement,
    CategoryScale,
    LinearScale
)

// ✅ Define all state variables
const loading = ref(true)
const stats = ref({}) // ✅ FIXED: Make sure it's declared
const usersByLocation = ref([])
const professionalsByCategory = ref([])
const servicesByCategory = ref([])
const userGrowth = ref([])

// Fetch data with debugging logs
const fetchDashboardData = async () => {
    console.log('fetchDashboardData() started')

    try {
        const response = await api.get('/api/admin/dashboard')
        console.log('API Response:', response.data)

        if (!response || !response.data) {
            throw new Error('Invalid API response')
        }

        // ✅ Assign values to reactive refs
        stats.value = response.data.stats || {}
        usersByLocation.value = response.data.users_by_location || []
        professionalsByCategory.value = response.data.users_by_category || []
        servicesByCategory.value = response.data.services_by_category || []
        userGrowth.value = response.data.user_growth || []

        console.log('Updated stats:', stats.value)

        await nextTick() // ✅ Ensures UI updates
    } catch (error) {
        console.error('Error fetching dashboard data:', error.message)
        toast.error('Failed to load dashboard data')
    } finally {
        setTimeout(() => {
            loading.value = false
            console.log('Setting loading to false')
        }, 300)
    }
}

// ✅ Run function when component mounts
onMounted(() => {
    setTimeout(fetchDashboardData, 300)
})
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Admin Dashboard</h2>

        <!-- Loading Indicator -->
        <div v-if="loading" class="text-center">
            <p>Loading dashboard...</p>
        </div>

        <template v-else>
            <div class="row">
                <div class="col-md-3" v-for="(value, key) in stats" :key="key">
                    <div class="card stat-card">
                        <h5>{{ key.replace(/_/g, ' ').toUpperCase() }}</h5>
                        <p>{{ value }}</p>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<style scoped>
.stat-card {
    text-align: center;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
