<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const services = ref([])
const loading = ref(true)
const editingService = ref(null) // Track service being edited
const editedName = ref('')
const editedDescription = ref('')
const editedBasePrice = ref(0)
const searchQuery = ref('') // 🔍 Search input

const fetchServices = async () => {
    loading.value = true
    try {
        const response = await api.get('/api/admin/get-services')
        services.value = response.data
    } catch (error) {
        toast.error('Failed to load services')
    } finally {
        loading.value = false
    }
}

// Filter services based on category name
const filteredServices = computed(() => {
    return services.value.filter((service) =>
        service.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
})

// Delete Service
const deleteService = async (id) => {
    if (!confirm('Are you sure you want to delete this service?')) return

    try {
        await api.delete(`/api/admin/delete-service/${id}`)
        toast.success('Service deleted successfully')
        fetchServices()
    } catch (error) {
        toast.error('Failed to delete service')
    }
}

// Start Editing Service
const startEditing = (service) => {
    editingService.value = service.id
    editedName.value = service.name
    editedDescription.value = service.description
    editedBasePrice.value = service.base_price
}

// Save Updated Service
const saveEdit = async (id) => {
    try {
        await api.put(`/api/admin/update-service/${id}`, {
            name: editedName.value,
            description: editedDescription.value,
            base_price: editedBasePrice.value,
        })
        toast.success('Service updated successfully')
        editingService.value = null
        fetchServices()
    } catch (error) {
        toast.error('Failed to update service')
    }
}

// Cancel Editing
const cancelEdit = () => {
    editingService.value = null
}

onMounted(fetchServices)
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Services Management</h2>

        <!-- Search Bar -->
        <div class="mb-3">
            <input
                v-model="searchQuery"
                type="text"
                class="form-control"
                placeholder="Type here to search..."
            />
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center">
            <p>Loading services...</p>
        </div>

        <!-- No Services Found -->
        <div v-else-if="filteredServices.length === 0" class="text-center text-muted">
            <p>No services found for the given category.</p>
        </div>

        <!-- Services Table -->
        <div v-else class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Base Price</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in filteredServices" :key="service.id">
                        <td>
                            <img :src="service.image_url" alt="Service Image" class="service-img" />
                        </td>
                        <td v-if="editingService !== service.id">{{ service.name }}</td>
                        <td v-else>
                            <input v-model="editedName" class="form-control" />
                        </td>
                        <td v-if="editingService !== service.id">{{ service.description }}</td>
                        <td v-else>
                            <textarea v-model="editedDescription" class="form-control"></textarea>
                        </td>
                        <td>{{ service.category_name }}</td>
                        <td v-if="editingService !== service.id">₹{{ service.base_price }}</td>
                        <td v-else>
                            <input v-model="editedBasePrice" type="number" class="form-control" />
                        </td>
                        <td>{{ service.created_at }}</td>
                        <td>
                            <button
                                v-if="editingService !== service.id"
                                class="btn btn-sm btn-primary me-2"
                                @click="startEditing(service)"
                            >
                                Edit
                            </button>

                            <button
                                v-if="editingService === service.id"
                                class="btn btn-sm btn-success me-2"
                                @click="saveEdit(service.id)"
                            >
                                Save
                            </button>

                            <button
                                v-if="editingService === service.id"
                                class="btn btn-sm btn-secondary me-2"
                                @click="cancelEdit"
                            >
                                Cancel
                            </button>

                            <button
                                class="btn btn-sm btn-danger"
                                @click="deleteService(service.id)"
                            >
                                Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
.service-img {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 5px;
}
.btn {
    min-width: 90px;
}
</style>
