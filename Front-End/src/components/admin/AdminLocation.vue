<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const locations = ref([])
const loading = ref(true)
const editingLocation = ref(null)
const showEditModal = ref(false)

// Fetch Locations
const fetchLocations = async () => {
    loading.value = true
    try {
        const response = await api.get('/api/admin/get-locations')
        locations.value = response.data
    } catch (error) {
        toast.error('Failed to load locations')
    } finally {
        loading.value = false
    }
}

// Open Edit Modal
const openEditModal = (location) => {
    editingLocation.value = { ...location }
    showEditModal.value = true
}

// Update Location
const updateLocation = async () => {
    try {
        await api.put(
            `/api/admin/update-location/${editingLocation.value.id}`,
            editingLocation.value
        )
        toast.success('Location updated successfully')
        showEditModal.value = false
        fetchLocations()
    } catch (error) {
        toast.error('Failed to update location')
    }
}

onMounted(fetchLocations)
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Manage Locations</h2>

        <!-- Loading Indicator -->
        <div v-if="loading" class="text-center">
            <p>Loading locations...</p>
        </div>

        <!-- No Locations Found -->
        <div v-else-if="locations.length === 0" class="text-center text-muted">
            <p>No locations found.</p>
        </div>

        <!-- Locations Table -->
        <div v-else class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>City</th>
                        <th>State</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="location in locations" :key="location.id">
                        <td>{{ location.city }}</td>
                        <td>{{ location.state }}</td>
                        <td>
                            <button @click="openEditModal(location)" class="btn btn-warning btn-sm">
                                Update
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Edit Location Modal -->
        <div v-if="showEditModal" class="modal-overlay">
            <div class="modal-content">
                <h4>Edit Location</h4>
                <form @submit.prevent="updateLocation">
                    <div class="mb-2">
                        <label>City:</label>
                        <input
                            v-model="editingLocation.city"
                            type="text"
                            class="form-control"
                            required
                        />
                    </div>
                    <div class="mb-2">
                        <label>State:</label>
                        <input
                            v-model="editingLocation.state"
                            type="text"
                            class="form-control"
                            required
                        />
                    </div>
                    <div class="d-flex justify-content-end">
                        <button
                            type="button"
                            class="btn btn-secondary me-2"
                            @click="showEditModal = false"
                        >
                            Cancel
                        </button>
                        <button type="submit" class="btn btn-success">Save</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 400px;
}
</style>
