<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import api from '../../api'
import 'vue3-toastify/dist/index.css'

const router = useRouter()

const professional = ref({
    name: '',
    email: '',
    password: '',
    mobile: '',
    category_id: '',
    location_id: '',
    experience: null,
    image_url: '',
})

const categories = ref([])
const locations = ref([])
const loading = ref(false)

const fetchCategoriesAndLocations = async () => {
    try {
        loading.value = true
        const [categoryResponse, locationResponse] = await Promise.all([
            api.get('/api/professional/get-categories'),
            api.get('/api/professional/get-locations'),
        ])

        categories.value = categoryResponse.data
        locations.value = locationResponse.data
    } catch (error) {
        toast.error('Failed to load dropdown data.')
    } finally {
        loading.value = false
    }
}

const registerProfessional = async () => {
    if (!professional.value.category_id || !professional.value.location_id) {
        toast.error('Please select a category and location.')
        return
    }

    try {
        loading.value = true
        await api.post('/api/professional/register-professional', professional.value)

        toast.success('Registration Successful!', { autoClose: 2000 })

        // Redirect to dashboard after success
        setTimeout(() => {
            router.push('/professional/dashboard')
        }, 2000)
    } catch (error) {
        toast.error(error.response?.data?.message || 'Registration Failed.', { autoClose: 3000 })
    } finally {
        loading.value = false
    }
}

onMounted(fetchCategoriesAndLocations)
</script>

<style scoped>
.container {
    max-width: 500px;
}
</style>

<template>
    <div class="container mt-5">
        <h2 class="text-center mb-4">Register as a Professional</h2>

        <form @submit.prevent="registerProfessional">
            <!-- Name -->
            <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" class="form-control" v-model="professional.name" required />
            </div>

            <!-- Email -->
            <div class="mb-3">
                <label class="form-label">Email Address</label>
                <input type="email" class="form-control" v-model="professional.email" required />
            </div>

            <!-- Mobile -->
            <div class="mb-3">
                <label class="form-label">Mobile Number</label>
                <input
                    type="text"
                    class="form-control"
                    v-model="professional.mobile"
                    pattern="\d{10}"
                    required
                />
            </div>

            <!-- Password -->
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                    type="password"
                    class="form-control"
                    v-model="professional.password"
                    required
                />
            </div>

            <!-- Category Dropdown -->
            <div class="mb-3">
                <label class="form-label">Select Category</label>
                <select class="form-control" v-model="professional.category_id" required>
                    <option value="" disabled>Select a category</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                        {{ category.name }}
                    </option>
                </select>
            </div>

            <!-- Location Dropdown -->
            <div class="mb-3">
                <label class="form-label">Select Location</label>
                <select class="form-control" v-model="professional.location_id" required>
                    <option value="" disabled>Select a location</option>
                    <option v-for="location in locations" :key="location.id" :value="location.id">
                        {{ location.city }} ({{ location.state }})
                    </option>
                </select>
            </div>

            <!-- Experience -->
            <div class="mb-3">
                <label class="form-label">Experience (Years)</label>
                <input
                    type="number"
                    step="0.1"
                    class="form-control"
                    v-model="professional.experience"
                    required
                />
            </div>

            <!-- Profile Image URL -->
            <div class="mb-3">
                <label class="form-label">Profile Image URL</label>
                <input type="text" class="form-control" v-model="professional.image_url" required />
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Registering...' : 'Register' }}
            </button>
        </form>
    </div>
</template>
