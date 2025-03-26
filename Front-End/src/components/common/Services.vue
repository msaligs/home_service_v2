<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

// Reactive State
const services = ref([])
const categoryId = ref(null)
const isLoading = ref(true)
const searchQuery = ref('')
const selectedService = ref(null)
const isBookingConfirmed = ref(false)
const bookingDetails = ref(null)
const showModal = ref(false)
const isProcessingBooking = ref(false) // Added loading state
const isBookingLoading = ref(false) // New state for loading animation

const route = useRoute()
const router = useRouter()

const isAuthenticated = () => {
    return localStorage.getItem('token') !== null
}

const bookService = async (serviceId, price) => {
    if (!isAuthenticated()) {
        localStorage.setItem('redirectAfterLogin', route.fullPath)
        router.push('/auth')
        return
    }

    const token = localStorage.getItem('token')
    if (!token) {
        console.error('Token not found!')
        toast.warn('⚠️ Authentication token missing. Please log in.', { autoClose: 3000 })
        return
    }

    // Close service details modal & show loader
    closeModal()
    isProcessingBooking.value = true
    isBookingLoading.value = true // Start loading animation

    try {
        const response = await api.post(
            `/api/user/book_service/${serviceId}`,
            { price },
            {
                headers: {
                    'Authentication-Token': token,
                },
            }
        )

        const { message, status, data } = response.data

        if (status.toLowerCase() === 'success') {
            // Store booking details & open confirmation modal
            bookingDetails.value = {
                message: message,
                service_name: data?.service_name || 'Unknown Service',
                price: data?.price || price,
                remarks: data?.remarks || 'No remarks',
            }

            isBookingConfirmed.value = true
            toast.success(`🎉 ${message}`, { autoClose: 3000 })
        } else {
            toast.warn(`⚠️ ${message}`, { autoClose: 3000 })
            throw new Error('Failed to book service.')
        }
    } catch (error) {
        console.error('Error booking service:', error.response?.data || error.message)

        if (error.response) {
            const { status, data } = error.response
            const errorMessage = data?.message || 'Failed to book service.'

            // Handle Unauthorized (Session Expired)
            if (status === 401) {
                toast.warn('⚠️ Session expired. Please log in again.', { autoClose: 3000 })
                localStorage.setItem('redirectAfterLogin', route.fullPath)
                localStorage.removeItem('token')
                router.push('/auth')
                return
            }

            // Handle Bad Request (Validation Errors)
            if (status === 400) {
                toast.warn(`⚠️ ${errorMessage}`, { autoClose: 4000 })
            }
            // Handle Conflict (Existing Request)
            else if (status === 409) {
                if (data?.existing_request) {
                    const existingRequest = data.existing_request
                    toast.warn(
                        `⚠️ ${errorMessage}\n📌 Request ID: ${existingRequest.id}\n📅 Date: ${existingRequest.requested_at}\n📍 Status: ${existingRequest.status}`,
                        { autoClose: 5000 }
                    )
                } else {
                    toast.warn(`⚠️ ${errorMessage}`, { autoClose: 3000 })
                }
            }
            // Handle Server Errors
            else if (status === 500) {
                toast.error(`❌ Server error: ${data?.details || 'Please try again later.'}`, {
                    autoClose: 4000,
                })
            }
            // Handle Other Errors
            else {
                toast.error(`❌ ${errorMessage}`, { autoClose: 3000 })
            }
        } else {
            toast.error(`❌ Network error. Please check your connection.`, { autoClose: 3000 })
        }
    } finally {
        isProcessingBooking.value = false
        isBookingLoading.value = false // Stop loading animation
    }
}

// Close the modal
const closeBookingModal = () => {
    isBookingConfirmed.value = false
    bookingDetails.value = null
}

// Navigate to Bookings Page
const goToBookings = () => {
    closeBookingModal()
    router.push('/user/bookings')
}

// Navigate to Home Page
const goToHome = () => {
    closeBookingModal()
    router.push('/')
}

// Open Modal with Service Details
const openModal = (service) => {
    selectedService.value = service
    showModal.value = true
}

// Close Modal
const closeModal = () => {
    showModal.value = false
    selectedService.value = null
}

// Fetch Services
const fetchServices = async () => {
    if (!categoryId.value) return
    isLoading.value = true

    try {
        const response = await api.get(`/api/common/services/${categoryId.value}`)
        services.value =
            response.data.map((service) => ({
                ...service,
                rating: (Math.random() * 5).toFixed(1), // Generate random rating between 0-5
            })) || []
    } catch (error) {
        console.error('Error fetching services:', error)
        toast.error(`❌ Failed to load services. Please try again later.`, { autoClose: 3000 })
    } finally {
        isLoading.value = false
    }
}

const filteredServices = computed(() => {
    return services.value.filter((service) =>
        service.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
})
// On Component Mount
onMounted(() => {
    categoryId.value = route.query.category || null
    fetchServices()
})
</script>

<template>
    <div class="container mt-5">
        <h2 class="mb-4 text-center text-primary fw-bold">Explore Our Home Services</h2>

        <!-- Search Bar -->
        <div class="mb-4 text-center">
            <input
                type="text"
                v-model="searchQuery"
                class="form-control w-50 mx-auto"
                placeholder="Search services by name..."
            />
        </div>

        <!-- Loader -->
        <div v-if="isLoading" class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3">Fetching available services...</p>
        </div>

        <!-- No Services Message -->
        <div v-else-if="services.length === 0" class="text-center no-services">
            <p class="mt-3 text-muted">No services available for this category.</p>
        </div>

        <!-- Service List -->
        <div class="row g-4">
            <div v-for="service in filteredServices" :key="service.id" class="col-md-4">
                <div class="card service-card">
                    <img
                        :src="service.image_url || 'https://thispersondoesnotexist.com/'"
                        class="card-img-top"
                        alt="Service Image"
                    />
                    <div class="card-body text-center">
                        <h5 class="card-title text-primary fw-bold">{{ service.name }}</h5>

                        <!-- ⭐ Star Rating -->
                        <div class="rating-container">
                            <span class="rating-title">Rating:</span>
                            <div class="rating">
                                <span
                                    v-for="n in 5"
                                    :key="n"
                                    :class="[
                                        'pi',
                                        n <= Math.round(service.rating)
                                            ? 'pi-star-fill'
                                            : 'pi-star',
                                    ]"
                                ></span>
                                <span class="rating-value">({{ service.rating }})</span>
                            </div>
                        </div>

                        <p class="card-text text-muted">
                            {{
                                service.description.length > 60
                                    ? service.description.substring(0, 60) + '...'
                                    : service.description
                            }}
                        </p>
                        <button class="btn btn-link show-more" @click="openModal(service)">
                            Show More <i class="pi pi-arrow-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Service Details Modal -->
        <div v-if="showModal" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title text-primary fw-bold">
                            {{ selectedService?.name }}
                        </h5>
                        <button type="button" class="btn-close" @click="closeModal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <p class="modal-description text-muted mt-3">
                            {{ selectedService?.description || 'No description available.' }}
                        </p>

                        <p class="modal-price text-success fw-bold">
                            💰 Base Price: ₹{{ selectedService?.base_price || 'N/A' }}
                        </p>

                        <p class="modal-duration text-info fw-bold">
                            ⏳ Estimated Time: {{ selectedService?.time_required || 'N/A' }} min
                        </p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="closeModal">Close</button>
                        <button
                            class="btn btn-primary"
                            @click="bookService(selectedService.id, selectedService.base_price)"
                        >
                            Book Now
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Booking Processing Animation -->
        <div v-if="isBookingLoading" class="loading-overlay">
            <i class="pi pi-spin pi-spinner loading-icon"></i>
            <p class="mt-3 text-white">Processing your booking...</p>
        </div>

        <!-- Booking Confirmation Modal -->
        <div v-if="isBookingConfirmed" class="modal fade show d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title">🎉 Booking Successful!</h5>
                    </div>
                    <div class="modal-body text-center">
                        <p class="text-muted">{{ bookingDetails.message }}</p>
                        <p><strong> Service Name:</strong> {{ bookingDetails.service_name }}</p>
                        <p><strong>💰 Price:</strong> ₹{{ bookingDetails.price }}</p>
                        <p><strong>📌 Remarks:</strong> {{ bookingDetails.remarks }}</p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-primary" @click="goToBookings">
                            📋 View My Bookings
                        </button>
                        <button class="btn btn-secondary" @click="goToHome">🏠 Go to Home</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* 📌 Service Card Styling */
.service-card {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
    background: white;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

.service-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
.card-img-top {
    height: 220px;
    object-fit: cover;
    border-bottom: 3px solid #007bff;
}

/* ⭐ Rating */
.rating-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-top: 5px;
    font-weight: bold;
}

.rating {
    display: flex;
    align-items: center;
    gap: 3px;
    font-size: 18px;
    color: #f5c518;
}

.rating-title {
    font-size: 14px;
    color: #333;
    font-weight: bold;
}

.rating .pi-star {
    color: #ccc;
}

/* Full-width Image */
.modal-img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    border-radius: 5px;
}

/* Description Styling */
.modal-description {
    font-size: 16px;
    line-height: 1.5;
}

/* Base Price Styling */
.modal-price {
    font-size: 18px;
}

/* Rating Styling */

.rating .pi-star {
    color: #ccc;
}

.rating-value {
    font-size: 14px;
    color: #555;
    font-weight: bold;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.6); /* Dark transparent background */
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    z-index: 1050;
    pointer-events: all; /* Prevents interactions */
}

/* PrimeIcons Spinner */
.loading-icon {
    font-size: 3rem;
    color: white;
}
</style>
