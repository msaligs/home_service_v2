<script setup>
import { ref } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const city = ref('')
const state = ref('')
const loading = ref(false)

const addLocation = async () => {
    if (!city.value.trim() || !state.value.trim()) {
        toast.error('City and State are required!')
        return
    }

    loading.value = true
    try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('Token missing!')

        await api.post(
            '/api/admin/add-location',
            {
                city: city.value,
                state: state.value,
            },
            {
                headers: { 'Authentication-Token': token },
            }
        )
        toast.success('Location added successfully')
        city.value = ''
        state.value = ''
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
            </div>

            <div class="mb-3">
                <label class="form-label"><strong>State Name:</strong></label>
                <input
                    v-model="state"
                    type="text"
                    class="form-control"
                    placeholder="Enter state name"
                />
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
