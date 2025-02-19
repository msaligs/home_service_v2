<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const professionals = ref([])
const loading = ref(true)
const processing = ref(null) // Stores the ID of the professional being processed
const waiting = ref(false) // Indicates whether the forced wait is active

const fetchNewProfessionals = async () => {
    try {
        const response = await api.get('/api/admin/professionals?filter=pending')
        professionals.value = response.data
    } catch (error) {
        toast.error('Failed to load professionals')
    } finally {
        loading.value = false
    }
}

const confirmAction = (id, status) => {
    processing.value = id
    waiting.value = true
    toast.info('Please wait 3 seconds before confirming...')

    setTimeout(async () => {
        waiting.value = false
        const confirmation = confirm(
            `Are you sure you want to ${status} this professional? This action cannot be undone.`
        )

        if (confirmation) {
            updateProfessionalStatus(id, status)
        } else {
            processing.value = null
        }
    }, 3000) // Force admin to wait 3 seconds
}

const updateProfessionalStatus = async (id, status) => {
    try {
        const response = await api.post(`/api/admin/update_professional_status/${id}`, { status })
        professionals.value = professionals.value.filter((pro) => pro.id !== id)
        toast.success(response.data.message)
    } catch (error) {
        toast.error(`Error ${status} professional`)
    } finally {
        processing.value = null
    }
}

onMounted(fetchNewProfessionals)
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Newly Registered Professionals</h2>

        <div v-if="loading" class="text-center">
            <p>Loading professionals...</p>
        </div>

        <div v-else-if="professionals.length === 0" class="text-center text-muted">
            <p>No new professionals found.</p>
        </div>

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
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="professional in professionals" :key="professional.id">
                        <td>{{ professional.name }}</td>
                        <td>{{ professional.email }}</td>
                        <td>{{ professional.mobile }}</td>
                        <td>{{ professional.category }}</td>
                        <td>{{ professional.location }}</td>
                        <td>{{ professional.experience }} years</td>
                        <td>
                            <button
                                class="btn btn-sm btn-success me-2"
                                @click="confirmAction(professional.id, 'verified')"
                                :disabled="processing === professional.id"
                            >
                                <i class="pi pi-check"></i>
                                {{
                                    processing === professional.id && waiting
                                        ? 'Waiting...'
                                        : 'Approve'
                                }}
                            </button>
                            <button
                                class="btn btn-sm btn-danger"
                                @click="confirmAction(professional.id, 'rejected')"
                                :disabled="processing === professional.id"
                            >
                                <i class="pi pi-times"></i>
                                {{
                                    processing === professional.id && waiting
                                        ? 'Waiting...'
                                        : 'Reject'
                                }}
                            </button>
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
button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}
</style>
