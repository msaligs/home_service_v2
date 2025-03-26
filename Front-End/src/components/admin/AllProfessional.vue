<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const professionals = ref([])
const categories = ref([])
const locations = ref([])
const loading = ref(true)

// Filters
const selectedFilter = ref('all')
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedLocation = ref('')

// Fetch professionals with applied filters
const fetchProfessionals = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('Token missing!')

        const response = await api.get('/api/admin/professionals', {
            params: {
                filter: selectedFilter.value,
                search: searchQuery.value,
                category: selectedCategory.value,
                location: selectedLocation.value,
            },
            headers: { 'Authentication-Token': token },
        })
        professionals.value = response.data
    } catch (error) {
        toast.error('Failed to load professionals')
    } finally {
        loading.value = false
    }
}

// Fetch categories and locations
const fetchFilters = async () => {
    try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('Token missing!')

        const [catRes, locRes] = await Promise.all([
            api.get('/api/admin/get-categories', {
                headers: { 'Authentication-Token': token },
            }),
            api.get('/api/admin/get-locations', {
                headers: { 'Authentication-Token': token },
            }),
        ])
        categories.value = catRes.data
        locations.value = locRes.data
    } catch (error) {
        toast.error('Failed to load filters')
    }
}

// Watch for filter changes and fetch professionals dynamically
watch([selectedFilter, searchQuery, selectedCategory, selectedLocation], fetchProfessionals)

onMounted(() => {
    fetchProfessionals()
    fetchFilters()
})
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Professionals List</h2>

        <!-- Filters & Search -->
        <div class="row mb-3">
            <div class="col-md-3">
                <label class="form-label"><strong>Filter by Status:</strong></label>
                <select v-model="selectedFilter" class="form-select">
                    <option value="all">All</option>
                    <option value="pending">Pending</option>
                    <option value="verified">Verified</option>
                    <option value="rejected">Rejected</option>
                </select>
            </div>
            <div class="col-md-3">
                <label class="form-label"><strong>Search by Name or Email:</strong></label>
                <input
                    v-model="searchQuery"
                    type="text"
                    class="form-control"
                    placeholder="Enter name or email"
                />
            </div>
            <div class="col-md-3">
                <label class="form-label"><strong>Filter by Category:</strong></label>
                <select v-model="selectedCategory" class="form-select">
                    <option value="">All Categories</option>
                    <option
                        v-for="category in categories"
                        :key="category.id"
                        :value="category.name"
                    >
                        {{ category.name }}
                    </option>
                </select>
            </div>
            <div class="col-md-3">
                <label class="form-label"><strong>Filter by Location:</strong></label>
                <select v-model="selectedLocation" class="form-select">
                    <option value="">All Locations</option>
                    <option v-for="location in locations" :key="location.id" :value="location.city">
                        {{ location.city }}
                    </option>
                </select>
            </div>
        </div>

        <!-- Loading Message -->
        <div v-if="loading" class="text-center">
            <p>Loading professionals...</p>
        </div>

        <!-- No Professionals Found -->
        <div v-else-if="professionals.length === 0" class="text-center text-muted">
            <p>No professionals found.</p>
        </div>

        <!-- Professionals Table -->
        <div v-else class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Mobile</th>
                        <th>Category</th>
                        <th>Location</th>
                        <th>Experience</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="professional in professionals" :key="professional.id">
                        <td>
                            <router-link
                                :to="'/admin/professional/' + professional.id"
                                class="user-link"
                            >
                                {{ professional.name }}
                            </router-link>
                        </td>
                        <td>{{ professional.email }}</td>
                        <td>{{ professional.mobile }}</td>
                        <td>{{ professional.category || 'N/A' }}</td>
                        <td>{{ professional.location || 'N/A' }}</td>
                        <td>{{ professional.experience }} years</td>
                        <td>
                            <span
                                :class="{
                                    'badge bg-secondary': professional.status === 'pending',
                                    'badge bg-success': professional.status === 'verified',
                                    'badge bg-danger': professional.status === 'rejected',
                                }"
                            >
                                {{ professional.status }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
.table {
    width: 100%;
    margin-top: 20px;
}

.badge {
    font-size: 0.9rem;
    padding: 5px 10px;
}

.user-link {
    text-decoration: none;
    color: #007bff;
    font-weight: 500;
}

.user-link:hover {
    color: #0056b3;
    text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .table-responsive {
        overflow-x: auto;
    }
    .form-select,
    .form-control {
        font-size: 0.9rem;
    }
}
</style>
