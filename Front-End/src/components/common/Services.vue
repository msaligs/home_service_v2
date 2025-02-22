<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'

// 🔹 Reactive State
const services = ref([]) // Stores fetched services
const categoryId = ref(null) // Stores the selected category ID
const isLoading = ref(true) // Loading state

const route = useRoute() // Get category_id from URL
const router = useRouter() // Vue Router for navigation

const isAuthenticated = () => {
    return localStorage.getItem('token') !== null // Assumes token is stored on login
}

const bookService = (serviceId) => {
    if (!isAuthenticated()) {
        localStorage.setItem('redirectAfterLogin', route.fullPath)
        router.push('/auth')
        return
    }

    router.push(`/services/${serviceId}/book`)
}

// 🔹 Fetch Services Based on Category ID
const fetchServices = async () => {
    if (!categoryId.value) return
    isLoading.value = true

    try {
        const response = await api.get(`/api/common/services/${categoryId.value}`)
        services.value = response.data || []
    } catch (error) {
        console.error('Error fetching services:', error)
    } finally {
        isLoading.value = false
    }
}

// 🔹 On Component Mount
onMounted(() => {
    categoryId.value = route.query.category || null // Get category_id from URL query params
    fetchServices()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4 text-center text-primary">Explore Our Home Services</h2>

        <!-- Loader -->
        <div v-if="isLoading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3">Fetching available services...</p>
        </div>

        <!-- No Services Message -->
        <div v-else-if="services.length === 0" class="text-center no-services">
            <img src="" alt="No services" class="no-services-img" />
            <p class="mt-3 text-muted">No services available for this category.</p>
        </div>

        <!-- Service List -->
        <div class="row g-4">
            <div v-for="service in services" :key="service.id" class="col-md-4">
                <div class="card service-card">
                    <img
                        :src="service.image_url || '/default-image.jpg'"
                        class="card-img-top"
                        alt="Service Image"
                    />
                    <div class="card-body">
                        <h5 class="card-title text-primary">{{ service.name }}</h5>
                        <p class="card-text text-muted">
                            {{
                                service.description.length > 60
                                    ? service.description.substring(0, 60) + '...'
                                    : service.description
                            }}
                        </p>
                        <p class="card-text price">
                            <strong>₹{{ service.base_price }}</strong>
                        </p>
                        <button
                            class="btn btn-outline-primary w-100"
                            @click="bookService(service.id)"
                        >
                            Book Now
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* 📌 Service Card Styling */
.service-card {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card-img-top {
    height: 200px;
    object-fit: cover;
    border-bottom: 3px solid #007bff;
}

.card-title {
    font-weight: 600;
}

.price {
    font-size: 18px;
    color: #28a745;
    font-weight: bold;
}

/* 📌 Loader Styling */
.spinner-border {
    width: 3rem;
    height: 3rem;
}

/* 📌 No Services Message */
.no-services {
    margin-top: 50px;
}

.no-services-img {
    width: 150px;
    opacity: 0.8;
}
</style>
