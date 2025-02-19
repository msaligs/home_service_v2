<script setup>
import { ref, computed, onMounted } from 'vue'
import dayjs from 'dayjs'
import api from '../../api'
import { useRoute } from 'vue-router'
import { toast } from 'vue3-toastify'

const route = useRoute()
const professional = ref(null)
const loading = ref(true)
const blocking = ref(false)

const fetchProfessionalDetails = async () => {
    loading.value = true
    try {
        const response = await api.get(`/api/admin/user_detail/${route.params.id}`)
        console.log('API Response:', response.data)
        professional.value = response.data
    } catch (error) {
        console.error('Error fetching details:', error)
        toast.error('Failed to load professional details.')
    } finally {
        loading.value = false
    }
}

const toggleBlockStatus = async () => {
    if (!professional.value) return

    blocking.value = true
    try {
        await api.get(`/api/admin/toggle_user/${professional.value.user_id}`)
        professional.value.available = !professional.value.available
        toast.success(
            professional.value.available
                ? 'User unblocked successfully'
                : 'User blocked successfully'
        )
    } catch (error) {
        console.error('Error toggling block status:', error)
        toast.error('Failed to update status.')
    } finally {
        blocking.value = false
    }
}

const formatDate = (date) => dayjs(date).format('DD MMM YYYY, HH:mm')

onMounted(fetchProfessionalDetails)
</script>

<template>
    <div class="container mt-4">
        <button class="btn btn-outline-primary mb-3" @click="$router.go(-1)">
            <i class="bi bi-arrow-left"></i> Back
        </button>

        <!-- Loading State -->
        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- Error State -->
        <div v-else-if="!professional" class="text-center text-danger">
            <p>Failed to load details.</p>
        </div>

        <!-- Professional Details -->
        <div v-else class="card profile-card shadow-lg p-4">
            <div class="row g-5">
                <!-- Increased spacing between columns -->

                <!-- Profile Image & Basic Info -->
                <div class="col-md-4 text-center">
                    <img
                        :src="'https://placehold.co/300x300.png' || professional.profile_img_url"
                        alt="Profile Image"
                        class="profile-image rounded-circle img-fluid"
                    />
                    <h4 class="mt-3">{{ professional.name }}</h4>
                    <span class="badge bg-primary px-3 py-2">{{ professional.category }}</span>

                    <!-- Block/Unblock Button -->
                    <button
                        class="btn mt-3 btn-lg"
                        :class="professional.available ? 'btn-danger' : 'btn-success'"
                        @click="toggleBlockStatus"
                        :disabled="blocking"
                    >
                        <i
                            class="bi"
                            :class="professional.available ? 'bi-x-circle' : 'bi-check-circle'"
                        ></i>
                        {{ professional.available ? 'Block User' : 'Unblock User' }}
                    </button>
                </div>

                <!-- Professional Details -->
                <div class="col-md-8 details-section">
                    <h5 class="text-muted mb-3">Professional Details</h5>
                    <div class="info-grid">
                        <div class="info-item">
                            <strong>Location:</strong>
                            <span>{{ professional.location }}</span>
                        </div>
                        <div class="info-item">
                            <strong>Rating:</strong>
                            <span class="badge bg-warning text-dark">{{
                                professional.rating || 'N/A'
                            }}</span>
                        </div>
                        <div class="info-item">
                            <strong>Experience:</strong>
                            <span>{{ professional.experience }} years</span>
                        </div>
                        <div class="info-item">
                            <strong>Status:</strong>
                            <span
                                class="badge"
                                :class="{
                                    'bg-success': professional.verified === 'verified',
                                    'bg-danger': professional.verified === 'rejected',
                                    'bg-secondary': professional.verified === 'pending',
                                }"
                            >
                                {{ professional.verified }}
                            </span>
                        </div>
                        <div class="info-item">
                            <strong>Joined:</strong>
                            <span>{{ formatDate(professional.created_at) }}</span>
                        </div>
                        <div class="info-item">
                            <strong>Email:</strong>
                            <span>{{ professional.email }}</span>
                        </div>
                        <div class="info-item">
                            <strong>Mobile:</strong>
                            <span>{{ professional.mobile }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Profile Card */
.profile-card {
    max-width: 900px;
    margin: auto;
    border-radius: 12px;
    overflow: hidden;
    background: #ffffff;
}

/* Add extra spacing between columns */
.details-section {
    padding-left: 40px; /* Increased left padding */
}

/* Profile Image */
.profile-image {
    width: 140px;
    height: 140px;
    object-fit: cover;
    border: 3px solid #007bff;
    padding: 5px;
    transition: transform 0.3s ease-in-out;
}
.profile-image:hover {
    transform: scale(1.08);
}

/* Info Grid */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px; /* Increased spacing between rows */
    padding: 10px 0;
}
.info-item {
    background: #f8f9fa;
    padding: 12px 18px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Badge Styles */
.badge {
    font-size: 0.9rem;
    padding: 6px 12px;
    border-radius: 5px;
}

/* Button */
.btn-lg {
    width: 180px;
}
</style>
