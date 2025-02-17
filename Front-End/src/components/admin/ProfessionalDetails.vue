<script>
import axios from 'axios'
import dayjs from 'dayjs'
import api from '../../api'

export default {
    data() {
        return {
            professional: null,
        }
    },
    mounted() {
        this.fetchProfessionalDetails()
    },
    methods: {
        async fetchProfessionalDetails() {
            try {
                const response = await api.get(`/api/admin/user_details/${this.$route.params.id}`)
                console.log('API Response:', response.data) // Check the response data
                this.professional = response.data
            } catch (error) {
                console.error('Error fetching details:', error)
            }
        },
        formatDate(date) {
            return dayjs(date).format('DD-MM-YYYY HH:mm')
        },
    },
}
</script>

<template>
    <div class="container mt-4">
        <button class="btn btn-outline-secondary mb-3" @click="$router.go(-1)">
            <i class="bi bi-arrow-left"></i> Back
        </button>

        <div v-if="professional" class="card shadow-lg p-4">
            <div class="row">
                <div class="col-md-4 text-center">
                    <img
                        v-if="professional.image_url"
                        :src="professional.image_url"
                        alt="Profile Image"
                        class="profile-image rounded-circle img-fluid"
                    />
                    <h4 class="mt-3">{{ professional.name }}</h4>
                    <span class="badge bg-primary">{{ professional.category }}</span>
                </div>

                <div class="col-md-8">
                    <h5 class="text-muted">Professional Details</h5>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            <strong>Location:</strong> {{ professional.location }}
                        </li>
                        <li class="list-group-item">
                            <strong>Rating:</strong>
                            <span class="badge bg-warning text-dark">{{
                                professional.rating
                            }}</span>
                        </li>
                        <li class="list-group-item">
                            <strong>Experience:</strong> {{ professional.experience }} years
                        </li>
                        <li class="list-group-item">
                            <strong>Available:</strong>
                            <span
                                class="badge"
                                :class="professional.available ? 'bg-success' : 'bg-danger'"
                            >
                                {{ professional.available ? 'Available' : 'Not Available' }}
                            </span>
                        </li>
                        <li class="list-group-item">
                            <strong>Verified:</strong>
                            <span
                                class="badge"
                                :class="professional.verified ? 'bg-success' : 'bg-danger'"
                            >
                                {{ professional.verified ? '✅ Verified' : '❌ Not Verified' }}
                            </span>
                        </li>
                        <li class="list-group-item">
                            <strong>Joined:</strong> {{ formatDate(professional.created_at) }}
                        </li>
                        <li class="list-group-item">
                            <strong>Email:</strong> {{ professional.email }}
                        </li>
                        <li class="list-group-item">
                            <strong>Mobile:</strong> {{ professional.mobile }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <p v-else class="text-center text-muted">Loading professional details...</p>
    </div>
</template>

<style scoped>
.profile-image {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border: 3px solid #007bff;
    padding: 5px;
}
</style>
