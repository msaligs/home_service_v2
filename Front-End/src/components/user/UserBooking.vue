<script>
import { ref, onMounted } from 'vue'
import api from '@/api' // Ensure your API module is correctly set up
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export default {
    setup() {
        const serviceRequests = ref([])

        const fetchServiceRequests = async () => {
            try {
                const token = localStorage.getItem('token')
                if (!token) throw new Error('Token missing!')

                const response = await api.get('api/user/get_bookings', {
                    headers: { 'Authentication-Token': token },
                })
                serviceRequests.value = response.data.data
                // console.log('Service requests:', serviceRequests.value) // Debugging
            } catch (error) {
                console.error('Failed to fetch service requests:', error)
                toast.error('❌ Unable to fetch service requests. Try again later.', {
                    autoClose: 3000,
                })
            }
        }

        const cancelRequest = async (requestId) => {
            try {
                const token = localStorage.getItem('token')
                if (!token) throw new Error('Token missing!')

                const response = await api.delete(`/api/user/cancel_request/${requestId}`, {
                    headers: { 'Authentication-Token': token },
                })

                console.log('Cancel response:', response.data) // Debugging

                const index = serviceRequests.value.findIndex((req) => req.id === requestId)
                if (index !== -1) {
                    serviceRequests.value[index] = {
                        ...serviceRequests.value[index],
                        status: 'CANCELLED',
                        remarks: response.data.data?.remarks || 'No remarks',
                    }

                    // Force Vue to update the UI
                    serviceRequests.value = [...serviceRequests.value]
                }

                toast.success('✅ Service request canceled successfully.', { autoClose: 3000 })
            } catch (error) {
                console.error('Error canceling request:', error)
                toast.error('❌ Failed to cancel request.', { autoClose: 3000 })
            }
        }

        const confirmCancel = (requestId) => {
            if (confirm('Are you sure you want to cancel this request?')) {
                cancelRequest(requestId)
            }
        }

        const formatDate = (date) => {
            return new Date(date).toLocaleString()
        }

        const statusClass = (status) => {
            return {
                'status-pending': status === 'PENDING',
                'status-assigned': status === 'ASSIGNED',
                'status-accepted': status === 'ACCEPTED',
                'status-completed': status === 'COMPLETED',
                'status-cancelled': status === 'CANCELLED',
            }
        }

        onMounted(fetchServiceRequests)

        return {
            serviceRequests,
            confirmCancel,
            formatDate,
            statusClass,
        }
    },
}
</script>

<template>
    <div class="service-requests">
        <h2 class="title">Your Service Requests</h2>
        <div v-if="serviceRequests.length > 0">
            <div v-for="request in serviceRequests" :key="request.id" class="request-card">
                <div class="request-header">
                    <h3>{{ request.service_name }}</h3>
                    <span :class="statusClass(request.status)">{{ request.status }}</span>
                </div>
                <p><strong>Price:</strong> ₹{{ request.total_price.toFixed(2) }}</p>
                <p><strong>Remarks:</strong> {{ request.remarks || 'No remarks' }}</p>
                <p><strong>Request Date:</strong> {{ formatDate(request.requested_at) }}</p>
                <p v-if="request.professional">
                    <strong>Professional:</strong> {{ request.professional }}
                </p>
                <p v-if="request.completition_date">
                    <strong>Completion Date:</strong> {{ formatDate(request.completition_date) }}
                </p>

                <button
                    v-if="request.status === 'PENDING'"
                    class="cancel-btn"
                    @click="confirmCancel(request.id)"
                >
                    Cancel Request
                </button>
            </div>
        </div>
        <p v-else class="no-requests">No service requests found.</p>
    </div>
</template>

<style scoped>
.service-requests {
    max-width: 600px;
    margin: auto;
    padding: 20px;
}

.title {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.request-card {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.request-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.status-pending {
    background-color: #ffcc00;
    color: black;
    padding: 5px 10px;
    border-radius: 5px;
}

.status-assigned {
    background-color: #17a2b8;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
}
.status-accepted {
    background-color: #007bff;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
}

.status-completed {
    background-color: #28a745;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
}

.status-cancelled {
    background-color: #dc3545;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
}

.cancel-btn {
    background-color: #dc3545;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
}

.cancel-btn:hover {
    background-color: #c82333;
}

.restore-btn {
    background-color: #007bff;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
}

.restore-btn:hover {
    background-color: #0056b3;
}

.no-requests {
    text-align: center;
    font-size: 1.2rem;
    color: #666;
}
</style>
