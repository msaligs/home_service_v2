<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../../api'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css' // ✅ Import Vue3 Toastify CSS

// 🔹 Reactive State
const locations = ref([]) // List of locations from backend
const categories = ref([]) // Categories based on selected location
const selectedLocation = ref(localStorage.getItem('location_id') || null) // Get stored location
const selectedCategory = ref(null)
const loadingCategories = ref(false) // ✅ Loading state

const router = useRouter() // Vue Router for navigation

// 🔹 Fetch Locations from Backend
const fetchLocations = async () => {
    try {
        const response = await api.get('/api/common/get-locations')
        locations.value = response.data || []
    } catch (error) {
        console.error('Error fetching locations:', error)
        toast.error('Failed to load locations.', { autoClose: 3000 }) // ✅ Corrected toast syntax
    }
}

// 🔹 Fetch Categories Based on Selected Location
const fetchCategories = async () => {
    if (!selectedLocation.value) return

    loadingCategories.value = true // ✅ Start loading

    try {
        const response = await api.get(`/api/common/service-location/${selectedLocation.value}`)
        categories.value = response.data || []

        if (categories.value.length === 0) {
            toast.warn('No services available for this location.', { autoClose: 3000 }) // ✅ Corrected toast
        }
    } catch (error) {
        console.error('Error fetching categories:', error)
        toast.error('Failed to load categories.', { autoClose: 3000 }) // ✅ Corrected toast
    } finally {
        loadingCategories.value = false // ✅ Stop loading
    }
}

// 🔹 Redirect to Services Page
const goToServices = () => {
    if (!selectedCategory.value) {
        toast.warn('Please select a service category first.', { autoClose: 3000 }) // ✅ Corrected toast
        return
    }
    toast.success('Redirecting to services...', { autoClose: 2000 }) // ✅ Success message before navigation
    router.push(`/services?category=${selectedCategory.value}`)
}

// 🔹 Fetch Locations on Component Mount
onMounted(() => {
    fetchLocations()
    if (selectedLocation.value) {
        fetchCategories() // Fetch categories if location exists in localStorage
    }
})

// 🔹 Watch for Location Change & Fetch Categories
watch(selectedLocation, (newLocation) => {
    if (newLocation) {
        localStorage.setItem('location_id', newLocation) // Store location in localStorage
        fetchCategories()
    } else {
        localStorage.removeItem('location_id') // Remove from storage if null
    }
    selectedCategory.value = null // Reset category on location change
})
</script>

<template>
    <div class="container text-center mt-5">
        <h2 class="mb-4">Find the Best Home Services</h2>

        <!-- Location Dropdown -->
        <div class="mb-3">
            <label class="form-label">Select Your Location</label>
            <select v-model="selectedLocation" class="form-select">
                <option value="" disabled>Select Location</option>
                <option v-for="location in locations" :key="location.id" :value="location.id">
                    {{ location.city }} ({{ location.state }})
                </option>
            </select>
        </div>

        <!-- Category Dropdown (Dependent on Location) -->
        <div class="mb-3">
            <label class="form-label">Select Service Category</label>
            <select
                v-model="selectedCategory"
                class="form-select"
                :disabled="!selectedLocation || loadingCategories"
            >
                <option value="" disabled>Select Category</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                </option>
            </select>
            <div v-if="loadingCategories" class="text-primary mt-2">Loading categories...</div>
        </div>

        <!-- Search Button -->
        <button class="btn btn-primary" @click="goToServices" :disabled="!selectedCategory">
            Find Services
        </button>
    </div>
</template>

<style scoped>
.container {
    max-width: 500px;
    margin: auto;
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
