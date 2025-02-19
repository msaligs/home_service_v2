<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import { toast } from 'vue3-toastify'
import dayjs from 'dayjs'

const users = ref([])
const loading = ref(false)
const filterRole = ref('user')
const filterStatus = ref('true')
const currentPage = ref(1)
const totalPages = ref(1)
const perPage = 20

const fetchUsers = async () => {
    loading.value = true
    try {
        const response = await api.get('/api/admin/users', {
            params: {
                page: currentPage.value,
                per_page: perPage,
                role: filterRole.value,
                status: filterStatus.value,
            },
        })
        users.value = response.data.users
        totalPages.value = response.data.total_pages
    } catch (error) {
        toast.error('Failed to load users')
    } finally {
        loading.value = false
    }
}

const toggleUserStatus = async (id, isActive) => {
    try {
        await api.get(`/api/admin/toggle_user/${id}`)
        toast.success(isActive ? 'User blocked successfully' : 'User unblocked successfully')
        fetchUsers()
    } catch (error) {
        toast.error('Action failed')
    }
}

const changePage = (newPage) => {
    if (newPage > 0 && newPage <= totalPages.value) {
        currentPage.value = newPage
        fetchUsers()
    }
}

onMounted(fetchUsers)
</script>

<template>
    <div class="container mt-5">
        <h2 class="text-center mb-4">User Management</h2>

        <!-- Filters -->
        <div class="row mb-3">
            <div class="col-md-4">
                <select class="form-select" v-model="filterRole" @change="fetchUsers">
                    <option value="user">User</option>
                    <option value="professional">Professional</option>
                </select>
            </div>
            <div class="col-md-4">
                <select class="form-select" v-model="filterStatus" @change="fetchUsers">
                    <option value="true">Active</option>
                    <option value="false">Blocked</option>
                </select>
            </div>
        </div>

        <!-- User Table -->
        <div class="table-responsive">
            <table class="table table-hover table-bordered align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Mobile</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody v-if="users.length">
                    <tr v-for="(user, index) in users" :key="user.id">
                        <td>{{ (currentPage - 1) * perPage + index + 1 }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.mobile }}</td>
                        <td>{{ user.role }}</td>
                        <td>
                            <span class="badge" :class="user.active ? 'bg-success' : 'bg-danger'">
                                {{ user.active ? 'Active' : 'Blocked' }}
                            </span>
                        </td>
                        <td>{{ dayjs(user.created_at).format('DD-MM-YYYY HH:mm') }}</td>
                        <td class="text-center">
                            <button
                                class="btn btn-sm d-flex align-items-center gap-1"
                                title="Toggle User Status"
                                :class="user.active ? 'btn-outline-danger' : 'btn-outline-success'"
                                @click="toggleUserStatus(user.id, user.active)"
                            >
                                <i :class="user.active ? 'pi pi-lock' : 'pi pi-unlock'"></i>
                                <span>{{ user.active ? 'Block' : 'Unblock' }}</span>
                            </button>
                        </td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="8" class="text-center">No users found</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Pagination -->
        <div class="d-flex justify-content-center mt-3">
            <button
                class="btn btn-outline-primary mx-2"
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
            >
                <i class="pi pi-angle-left"></i> Previous
            </button>
            <span class="align-self-center">Page {{ currentPage }} of {{ totalPages }}</span>
            <button
                class="btn btn-outline-primary mx-2"
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
            >
                Next <i class="pi pi-angle-right"></i>
            </button>
        </div>
    </div>
</template>

<style scoped>
.user-link {
    text-decoration: none;
    color: #007bff;
    font-weight: 500;
}

.user-link:hover {
    color: #0056b3;
    text-decoration: underline;
}
</style>
