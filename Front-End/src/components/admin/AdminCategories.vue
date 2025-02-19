<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const categories = ref([])
const loading = ref(true)

// State for the category being updated
const editingCategory = ref(null)
const showModal = ref(false)

// Fetch categories from API
const fetchCategories = async () => {
    loading.value = true
    try {
        const response = await api.get('/api/admin/get-categories')
        categories.value = response.data
    } catch (error) {
        toast.error('Failed to load categories')
    } finally {
        loading.value = false
    }
}

// Open the update modal and set category data
const openUpdateModal = (category) => {
    editingCategory.value = { ...category } // Clone object to avoid direct mutation
    showModal.value = true
}

// Close the modal
const closeModal = () => {
    showModal.value = false
    editingCategory.value = null
}

// Update category API call
const updateCategory = async () => {
    try {
        await api.put(`/api/admin/update-category/${editingCategory.value.id}`, {
            name: editingCategory.value.name,
            description: editingCategory.value.description,
            image_url: editingCategory.value.image_url,
        })
        toast.success('Category updated successfully')
        closeModal()
        fetchCategories() // Refresh list
    } catch (error) {
        toast.error('Failed to update category')
    }
}

onMounted(fetchCategories)
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Categories</h2>

        <!-- Loading State -->
        <div v-if="loading" class="text-center">
            <p>Loading categories...</p>
        </div>

        <!-- No Categories Found -->
        <div v-else-if="categories.length === 0" class="text-center text-muted">
            <p>No categories available.</p>
        </div>

        <!-- Categories Table -->
        <div v-else class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="category in categories" :key="category.id">
                        <td>
                            <img
                                :src="category.image_url || 'https://placehold.co/100x100'"
                                alt="Category Image"
                                class="category-img"
                            />
                        </td>
                        <td>{{ category.name }}</td>
                        <td>{{ category.description }}</td>
                        <td>
                            <button
                                class="btn btn-sm btn-warning me-2"
                                @click="openUpdateModal(category)"
                            >
                                Update
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Update Category Modal -->
        <div v-if="showModal" class="modal d-block">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Update Category</h5>
                        <button type="button" class="btn-close" @click="closeModal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input
                                type="text"
                                class="form-control"
                                v-model="editingCategory.name"
                            />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            <textarea
                                class="form-control"
                                v-model="editingCategory.description"
                            ></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Image URL</label>
                            <input
                                type="text"
                                class="form-control"
                                v-model="editingCategory.image_url"
                            />
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeModal">
                            Cancel
                        </button>
                        <button type="button" class="btn btn-primary" @click="updateCategory">
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.category-img {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 5px;
}
.btn {
    min-width: 90px;
}
.modal {
    background: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.modal-dialog {
    max-width: 500px;
    background: white;
    padding: 20px;
    border-radius: 8px;
}
</style>
