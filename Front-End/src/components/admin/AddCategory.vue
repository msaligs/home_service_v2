<script setup>
import { ref } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'

const newCategory = ref({
    name: '',
    description: '',
    image_url: '',
})

const loading = ref(false)

const addCategory = async () => {
    if (!newCategory.value.name || !newCategory.value.description) {
        toast.error('Name and description are required!')
        return
    }

    loading.value = true
    try {
        await api.post('/api/admin/add-category', newCategory.value)
        toast.success('Category added successfully!')
        newCategory.value = { name: '', description: '', image_url: '' } // Reset form
    } catch (error) {
        toast.error('Failed to add category')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Add New Category</h2>

        <div class="card p-4 shadow">
            <form @submit.prevent="addCategory">
                <div class="mb-3">
                    <label class="form-label">Category Name</label>
                    <input type="text" class="form-control" v-model="newCategory.name" required />
                </div>

                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea
                        class="form-control"
                        v-model="newCategory.description"
                        required
                    ></textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label">Image URL (optional)</label>
                    <input type="text" class="form-control" v-model="newCategory.image_url" />
                </div>

                <button type="submit" class="btn btn-primary" :disabled="loading">
                    {{ loading ? 'Adding...' : 'Add Category' }}
                </button>
            </form>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 500px;
    margin: auto;
}
.card {
    border-radius: 8px;
}
.btn {
    width: 100%;
}
</style>
