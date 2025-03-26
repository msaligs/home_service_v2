<template>
    <div class="container mt-5">
        <h2 class="text-center mb-4 text-primary">Professional Profile</h2>

        <div
            v-if="isLoading"
            class="d-flex justify-content-center align-items-center"
            style="height: 200px"
        >
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else class="card shadow-sm p-4 border-0 rounded-3">
            <div class="d-flex align-items-center mb-4">
                <img
                    :src="'https://thispersondoesnotexist.com/' || profile.profile_img_url"
                    alt="Profile Image"
                    class="rounded-circle border border-primary img-thumbnail"
                    style="width: 120px; height: 120px; object-fit: cover"
                />
                <div class="ms-3">
                    <h4 class="fw-bold">{{ profile.name }}</h4>
                    <p class="text-muted">{{ profile.email }}</p>
                </div>
            </div>

            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label fw-semibold">Mobile</label>
                    <div v-if="editingField === 'mobile'">
                        <input v-model="editableValues.mobile" class="form-control" />
                        <button
                            class="btn btn-sm btn-success mt-2"
                            @click="saveField('mobile')"
                            :disabled="!editableValues.mobile"
                        >
                            Save
                        </button>
                        <button class="btn btn-sm btn-secondary mt-2 ms-2" @click="cancelEdit">
                            Cancel
                        </button>
                    </div>
                    <div v-else>
                        <p class="form-control-plaintext">{{ profile.mobile }}</p>
                        <button class="btn btn-sm btn-outline-primary" @click="startEdit('mobile')">
                            Edit
                        </button>
                    </div>
                </div>

                <div class="col-md-6">
                    <label class="form-label fw-semibold">Experience (years)</label>
                    <p class="form-control-plaintext">{{ profile.experience }}</p>
                </div>

                <div class="col-md-6">
                    <label class="form-label fw-semibold">Rating</label>
                    <p class="form-control-plaintext">{{ profile.rating }}</p>
                </div>

                <div class="col-md-6">
                    <label class="form-label fw-semibold">Category</label>
                    <div v-if="editingField === 'category_id'">
                        <select
                            v-model="editableValues.category_id"
                            class="form-control"
                            @focus="fetchCategories"
                        >
                            <option
                                v-for="category in categories"
                                :key="category.id"
                                :value="category.id"
                            >
                                {{ category.name }}
                            </option>
                        </select>
                        <button
                            class="btn btn-sm btn-success mt-2"
                            @click="saveField('category_id')"
                            :disabled="!editableValues.category_id"
                        >
                            Save
                        </button>
                        <button class="btn btn-sm btn-secondary mt-2 ms-2" @click="cancelEdit">
                            Cancel
                        </button>
                    </div>
                    <div v-else>
                        <p class="form-control-plaintext">{{ profile.category }}</p>
                        <button
                            class="btn btn-sm btn-outline-primary"
                            @click="startEdit('category_id')"
                        >
                            Edit
                        </button>
                    </div>
                </div>

                <div class="col-md-6">
                    <label class="form-label fw-semibold">Location</label>
                    <div v-if="editingField === 'location_id'">
                        <select
                            v-model="editableValues.location_id"
                            class="form-control"
                            @focus="fetchLocations"
                        >
                            <option
                                v-for="location in locations"
                                :key="location.id"
                                :value="location.id"
                            >
                                {{ location.city }} - {{ location.state }}
                            </option>
                        </select>
                        <button
                            class="btn btn-sm btn-success mt-2"
                            @click="saveField('location_id')"
                            :disabled="!editableValues.location_id"
                        >
                            Save
                        </button>
                        <button class="btn btn-sm btn-secondary mt-2 ms-2" @click="cancelEdit">
                            Cancel
                        </button>
                    </div>
                    <div v-else>
                        <p class="form-control-plaintext">
                            {{ profile.city }} - {{ profile.state }}
                        </p>
                        <button
                            class="btn btn-sm btn-outline-primary"
                            @click="startEdit('location_id')"
                        >
                            Edit
                        </button>
                    </div>
                </div>

                <div class="col-md-6">
                    <label class="form-label fw-semibold">Available</label>
                    <p class="form-control-plaintext">
                        <i
                            :class="
                                profile.available
                                    ? 'pi pi-check-circle text-success'
                                    : 'pi pi-times-circle text-danger'
                            "
                        ></i>
                    </p>
                    <button class="btn btn-sm btn-outline-primary" @click="toggleAvailability">
                        Toggle
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { toast } from 'vue3-toastify'
import api from '@/api'
import { h } from 'vue'

export default {
    data() {
        return {
            profile: {},
            isLoading: true,
            locations: [],
            categories: [],
            editingField: null,
            editableValues: {},
            editableFields: {
                mobile: 'Mobile',
                category: 'Category',
            },
        }
    },
    mounted() {
        this.fetchProfile()
    },
    methods: {
        async fetchProfile() {
            try {
                const token = localStorage.getItem('token')
                if (!token) throw new Error('Token missing!')

                const response = await api.get('/api/professional/profile', {
                    headers: { 'Authentication-Token': token },
                })
                this.profile = response.data
            } catch (error) {
                toast.error('Error fetching profile data!')
            } finally {
                this.isLoading = false
            }
        },
        async fetchCategories() {
            if (this.categories.length > 0) return // Prevent unnecessary API calls
            try {
                const response = await api.get('/api/professional/get-categories')
                this.categories = response.data
            } catch (error) {
                toast.error('Error fetching categories!')
            }
        },

        async fetchLocations() {
            if (this.locations.length > 0) return // Prevent unnecessary API calls
            try {
                const response = await api.get('/api/professional/get-locations')
                this.locations = response.data
            } catch (error) {
                toast.error('Error fetching locations!')
            }
        },

        startEdit(field) {
            this.editingField = field
            this.editableValues[field] = this.profile[field] // Set ID instead of name

            if (field === 'category_id') this.fetchCategories()
            if (field === 'location_id') this.fetchLocations()
        },

        cancelEdit() {
            this.editingField = null
            this.editableValues = {}
        },

        async saveField(field) {
            const token = localStorage.getItem('token')
            if (!token) {
                toast.error('Token missing!')
                return
            }

            const newValue = this.editableValues[field]
            if (!newValue || newValue === this.profile[field]) {
                toast.warning('No changes detected!')
                return
            }

            try {
                const payload = { [field]: newValue }
                const response = await api.put('/api/professional/update-profile', payload, {
                    headers: { 'Authentication-Token': token },
                })

                toast.success(response.data?.message || 'Profile updated successfully!')
                this.fetchProfile()
                this.cancelEdit()
            } catch (error) {
                toast.error(error.response?.data?.error || 'Error updating profile!')
            }
        },

        async toggleAvailability() {
            const token = localStorage.getItem('token')
            if (!token) {
                toast.error('Token missing!')
                return
            }

            if (!confirm('Are you sure you want to toggle availability?')) return

            const previousAvailability = this.profile.available
            this.profile.available = !previousAvailability

            try {
                const response = await api.put(
                    '/api/professional/update-availability',
                    {},
                    {
                        headers: { 'Authentication-Token': token },
                    }
                )
                if (response.status === 200) {
                    this.profile.available = response.data.available
                    toast.success('Availability updated successfully!')
                } else {
                    throw new Error('Unexpected response from server')
                }
            } catch (error) {
                this.profile.available = previousAvailability
                toast.error('Error updating availability!')
            }
        },
    },
}
</script>
