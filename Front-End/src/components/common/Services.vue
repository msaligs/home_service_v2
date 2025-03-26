<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const services = ref([])
const categoryId = ref(null)
const isLoading = ref(true)
const searchQuery = ref('')

const route = useRoute()
const router = useRouter()

const fetchServices = async () => {
    if (!categoryId.value) return
    isLoading.value = true

    try {
        const response = await api.get(`/api/common/services/${categoryId.value}`)
        services.value = response.data || []
    } catch (error) {
        console.error('Error fetching services:', error)
        toast.error('❌ Failed to load services. Please try again later.', { autoClose: 3000 })
    } finally {
        isLoading.value = false
    }
}

const filteredServices = computed(() => {
    return services.value.filter((service) =>
        service.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
})

onMounted(() => {
    categoryId.value = route.query.category || null
    fetchServices()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4 text-center text-primary fw-bold">Explore Our Home Services</h2>

        <!-- Search Bar -->
        <div class="mb-4 text-center">
            <input
                type="text"
                v-model="searchQuery"
                class="form-control w-50 mx-auto"
                placeholder="Search services by name..."
            />
        </div>

        <div v-if="isLoading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3">Fetching available services...</p>
        </div>

        <div v-else-if="filteredServices.length === 0" class="text-center no-services">
            <p class="mt-3 text-muted">No matching services found.</p>
        </div>

        <div class="row g-4">
            <div v-for="service in filteredServices" :key="service.id" class="col-md-4">
                <div class="card service-card">
                    <img
                        :src="service.image_url || 'https://via.placeholder.com/150'"
                        class="card-img-top service-img"
                        alt="Service Image"
                    />
                    <div class="card-body text-center">
                        <h5 class="card-title text-primary fw-bold">{{ service.name }}</h5>
                        <p class="card-text text-muted">{{ service.description }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.service-card {
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
    background: white;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

.service-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
</style>
