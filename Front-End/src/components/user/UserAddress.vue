<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import AddressForm from './AddressForm.vue'

const address = ref(null)
const loading = ref(true)
const showForm = ref(false)
const token = localStorage.getItem('token')

const fetchAddress = async () => {
    loading.value = true
    try {
        const response = await api.get('/api/user/user_address', {
            headers: { 'Authentication-Token': token },
        })
        address.value = response.data.data
    } catch (error) {
        console.error('Error fetching address:', error)
        address.value = null
    } finally {
        loading.value = false
    }
}

const addAddress = () => {
    address.value = null
    showForm.value = true
}

const editAddress = () => {
    showForm.value = true
}

onMounted(fetchAddress)
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">User Address</h2>

        <div v-if="loading" class="alert alert-info">Loading...</div>

        <div v-else-if="address" class="card">
            <div class="card-body">
                <h5 class="card-title">Saved Address</h5>
                <p class="card-text"><strong>Address:</strong> {{ address.address }}</p>
                <p class="card-text"><strong>City:</strong> {{ address.city }}</p>
                <p class="card-text"><strong>State:</strong> {{ address.state }}</p>
                <p class="card-text"><strong>Pincode:</strong> {{ address.pincode }}</p>
                <button class="btn btn-primary" @click="editAddress">Update Address</button>
            </div>
        </div>

        <div v-else class="alert alert-warning">
            No address found.
            <button class="btn btn-success mt-2" @click="addAddress">Add Address</button>
        </div>

        <AddressForm
            v-if="showForm"
            :address="address"
            @close="showForm = false"
            @save="fetchAddress"
        />
    </div>
</template>
