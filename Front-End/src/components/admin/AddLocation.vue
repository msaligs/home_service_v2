<script setup>
import { ref } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const city = ref('')
const state = ref('')
const loading = ref(false)
const errors = ref({ city: '', state: '' }) // Track validation errors

// Validate form fields
const validateForm = () => {
    errors.value.city = city.value.trim() ? '' : 'City name is required.'
    errors.value.state = state.value.trim() ? '' : 'State name is required.'
    return !errors.value.city && !errors.value.state // Return true if no errors
}

const addLocation = async () => {
    // Perform validation before submission
    if (!validateForm()) {
        toast.error('Please fix the errors before submitting!')
        return
    }

    loading.value = true
    try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('Token missing!')

        await api.post(
            '/api/admin/add-location',
            { city: city.value, state: state.value },
            { headers: { 'Authentication-Token': token } }
        )
        toast.success('Location added successfully')
        city.value = ''
        state.value = ''
        errors.value = { city: '', state: '' } // Clear errors after successful submission
    } catch (error) {
        toast.error('Failed to add location')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Add New Location</h2>

        <div class="card p-4 shadow-sm">
            <div class="mb-3">
                <label class="form-label"><strong>City Name:</strong></label>
                <input
                    v-model="city"
                    type="text"
                    class="form-control"
                    placeholder="Enter city name"
                />
                <small v-if="errors.city" class="text-danger">{{ errors.city }}</small>
            </div>

            <div class="mb-3">
                <label class="form-label"><strong>State Name:</strong></label>
                <input
                    v-model="state"
                    type="text"
                    class="form-control"
                    placeholder="Enter state name"
                />
                <small v-if="errors.state" class="text-danger">{{ errors.state }}</small>
            </div>

            <button class="btn btn-primary" @click="addLocation" :disabled="loading">
                {{ loading ? 'Adding...' : 'Add Location' }}
            </button>
        </div>
    </div>
</template>

<style scoped>
.card {
    max-width: 500px;
    margin: auto;
    border-radius: 10px;
}

.btn {
    width: 100%;
}
</style>
