<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const categories = ref([])
const serviceName = ref('')
const serviceDescription = ref('')
const serviceCategory = ref('')
const serviceBasePrice = ref('')
const serviceImageUrl = ref('')
const loading = ref(false)
const errors = ref({ name: '', description: '', category: '', price: '' }) // Track validation errors

// Fetch categories from backend
const fetchCategories = async () => {
    try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('Token missing!')

        const response = await api.get('/api/admin/get-categories', {
            headers: { 'Authentication-Token': token },
        })
        categories.value = response.data
    } catch (error) {
        toast.error('Failed to load categories')
    }
}

// Validate form fields
const validateForm = () => {
    errors.value.name = serviceName.value.trim() ? '' : 'Service name is required.'
    errors.value.description = serviceDescription.value.trim() ? '' : 'Description is required.'
    errors.value.category = serviceCategory.value ? '' : 'Category is required.'
    errors.value.price =
        serviceBasePrice.value && serviceBasePrice.value > 0 ? '' : 'Valid base price is required.'
    return (
        !errors.value.name &&
        !errors.value.description &&
        !errors.value.category &&
        !errors.value.price
    ) // Return true if no errors
}

// Submit new service
const addService = async () => {
    if (!validateForm()) {
        toast.error('Please fix the errors before submitting!')
        return
    }

    loading.value = true
    try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('Token missing!')

        await api.post(
            '/api/admin/add-service',
            {
                name: serviceName.value,
                description: serviceDescription.value,
                category_id: serviceCategory.value,
                base_price: serviceBasePrice.value,
                image_url: serviceImageUrl.value || null,
            },
            {
                headers: { 'Authentication-Token': token },
            }
        )
        toast.success('Service added successfully!')

        // Reset form
        serviceName.value = ''
        serviceDescription.value = ''
        serviceCategory.value = ''
        serviceBasePrice.value = ''
        serviceImageUrl.value = ''
        errors.value = { name: '', description: '', category: '', price: '' } // Clear errors after successful submission

        // Refresh categories
        fetchCategories()
    } catch (error) {
        toast.error('Failed to add service')
    } finally {
        loading.value = false
    }
}

onMounted(fetchCategories)
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Add New Service</h2>

        <div class="card p-4 shadow">
            <div class="mb-3">
                <label class="form-label">Service Name <span class="text-danger">*</span></label>
                <input
                    v-model="serviceName"
                    type="text"
                    class="form-control"
                    placeholder="Enter service name"
                />
                <small v-if="errors.name" class="text-danger">{{ errors.name }}</small>
            </div>

            <div class="mb-3">
                <label class="form-label">Description <span class="text-danger">*</span></label>
                <textarea
                    v-model="serviceDescription"
                    class="form-control"
                    placeholder="Enter service description"
                    rows="3"
                ></textarea>
                <small v-if="errors.description" class="text-danger">{{
                    errors.description
                }}</small>
            </div>

            <div class="mb-3">
                <label class="form-label">Category <span class="text-danger">*</span></label>
                <select v-model="serviceCategory" class="form-select">
                    <option value="" disabled>Select category</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                        {{ category.name }}
                    </option>
                </select>
                <small v-if="errors.category" class="text-danger">{{ errors.category }}</small>
            </div>

            <div class="mb-3">
                <label class="form-label">Base Price (₹) <span class="text-danger">*</span></label>
                <input
                    v-model="serviceBasePrice"
                    type="number"
                    class="form-control"
                    placeholder="Enter base price"
                />
                <small v-if="errors.price" class="text-danger">{{ errors.price }}</small>
            </div>

            <div class="mb-3">
                <label class="form-label">Image URL (Optional)</label>
                <input
                    v-model="serviceImageUrl"
                    type="text"
                    class="form-control"
                    placeholder="Enter image URL"
                />
            </div>

            <button @click="addService" class="btn btn-primary" :disabled="loading">
                <span v-if="loading">Adding...</span>
                <span v-else>Add Service</span>
            </button>
        </div>
    </div>
</template>

<style scoped>
.card {
    max-width: 600px;
    margin: auto;
    border-radius: 10px;
}
</style>
