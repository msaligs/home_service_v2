<template>
    <div class="container py-5">
        <h2 class="text-center mb-4">Assigned Service Requests</h2>

        <!-- Loader -->
        <div v-if="isLoading" class="d-flex justify-content-center my-5">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <!-- No Requests Message -->
        <div v-else-if="requests.length === 0" class="text-center text-muted">
            <img src="" alt="No Requests" class="img-fluid w-50 mb-3" />
            <p>No service requests assigned to you.</p>
        </div>

        <!-- Request List -->
        <div v-else class="row g-4">
            <div v-for="request in requests" :key="request.id" class="col-md-6 col-lg-4">
                <div class="card shadow-sm">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">{{ request.service_name }}</h5>
                        <span class="badge" :class="statusClass(request.status)">
                            <i :class="statusIcon(request.status)"></i> {{ request.status }}
                        </span>
                    </div>

                    <div class="card-body">
                        <p class="text-muted">{{ request.Service_description }}</p>

                        <!-- <p><strong>Request ID:</strong> #{{ request.service_request_id }}</p> -->
                        <p><strong>Assigned On:</strong> {{ formatDate(request.assign_date) }}</p>

                        <p v-if="request.accept_reject_date">
                            <strong v-if="request.status !== 'REJECTED'">Accepted On:</strong>
                            <strong v-else-if="request.status == 'REJECTED'">Rejected On:</strong>
                            {{ formatDate(request.accept_reject_date) }}
                        </p>
                        <p v-if="request.completition_date">
                            <strong>Completed On:</strong>
                            {{ formatDate(request.completition_date) }}
                        </p>

                        <hr />

                        <h6 class="text-muted">Customer Details</h6>
                        <p class="mb-1"><strong>Mobile:</strong> {{ request.customer_mobile }}</p>
                        <p class="mb-1">
                            <strong>Address:</strong> {{ request.customer_address }},
                            {{ request.customer_city }}, {{ request.customer_state }} -
                            {{ request.customer_pincode }}
                        </p>
                    </div>

                    <!-- Action Buttons -->
                    <div
                        class="card-footer d-flex justify-content-between"
                        v-if="request.status === 'ASSIGNED' || request.status === 'ACCEPTED'"
                    >
                        <button
                            v-if="request.status === 'ASSIGNED'"
                            @click="confirmAction('ACCEPTED', request)"
                            class="btn btn-success btn-sm w-50"
                        >
                            ✅ Accept
                        </button>

                        <button
                            v-if="request.status === 'ASSIGNED'"
                            @click="confirmAction('REJECTED', request)"
                            class="btn btn-danger btn-sm w-50"
                        >
                            ❌ Reject
                        </button>

                        <button
                            v-if="request.status === 'ACCEPTED'"
                            @click="confirmAction('COMPLETED', request)"
                            class="btn btn-primary btn-sm w-100"
                        >
                            🎯 Mark as Completed
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { toast } from 'vue3-toastify'
import api from '@/api'

export default {
    data() {
        return {
            requests: [],
            isLoading: true,
        }
    },
    mounted() {
        this.fetchRequests()
    },
    methods: {
        async fetchRequests() {
            try {
                const token = localStorage.getItem('token')
                if (!token) throw new Error('Token missing!')

                const response = await api.get('/api/professional/get-requests', {
                    headers: { 'Authentication-Token': token },
                })
                this.requests = response.data || []
            } catch (error) {
                toast.error('Error fetching assigned requests!')
            } finally {
                this.isLoading = false
            }
        },
        formatDate(date) {
            return date ? new Date(date).toLocaleString() : 'N/A'
        },
        statusClass(status) {
            return {
                'bg-secondary text-white': status === 'ASSIGNED',
                'bg-success text-white': status === 'ACCEPTED',
                'bg-danger text-white': status === 'REJECTED',
                'bg-info text-white': status === 'COMPLETED',
            }
        },
        statusIcon(status) {
            return {
                'fas fa-tasks': status === 'ASSIGNED',
                'fas fa-check-circle': status === 'ACCEPTED',
                'fas fa-times-circle': status === 'REJECTED',
                'fas fa-flag-checkered': status === 'COMPLETED',
            }
        },
        async confirmAction(status, request) {
            try {
                const token = localStorage.getItem('token')
                if (!token) throw new Error('Token missing!')

                await api.post(
                    `/api/professional/update-request-status/${request.id}`,
                    { status },
                    {
                        headers: { 'Authentication-Token': token },
                    }
                )
                toast.success(`Request ${status.toLowerCase()} successfully!`)
                this.fetchRequests() // Refresh the list after updating
            } catch (error) {
                toast.error('Error updating request status!')
            }
        },
    },
}
</script>

<style scoped>
.card {
    border-radius: 10px;
    overflow: hidden;
}

.card-header {
    font-size: 1.1rem;
    font-weight: bold;
    background-color: #007bff;
    color: white;
}

.card-footer {
    display: flex;
    gap: 5px;
}

.badge {
    padding: 5px 10px;
    border-radius: 8px;
    font-size: 0.9rem;
}
</style>
