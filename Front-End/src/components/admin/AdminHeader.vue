<script setup>
import { useRouter } from 'vue-router'
import api from '../../api'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css' // Import styles

const router = useRouter()

const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('email')
    localStorage.removeItem('role')
    toast.success('Logged out successfully!')
    router.push('/')
}

const fetchProfessionalData = async () => {
    try {
        const token = localStorage.getItem('token')
        if (!token) {
            toast.error('Authentication token missing!')
            return
        }

        // Notify user that the task has started
        // toast.info('Processing request... Please wait.', { autoClose: 1000 })

        // Step 1: Start the Celery Task
        const response = await api.get('/api/celery/create_prof', {
            headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
        })

        if (response.status !== 200) throw new Error('Failed to start task')

        const taskId = response.data.prof_task_id
        toast.success('Task started successfully! Fetching file...', { autoClose: 2000 })

        // Step 2: Poll for file readiness
        await checkTaskStatus(taskId)

        // Step 3: Download file when ready
        await downloadFile(taskId)
    } catch (error) {
        console.error('Error fetching professional data:', error)
        toast.error('Failed to download CSV.')
    }
}

const checkTaskStatus = (taskId) => {
    let retries = 0
    const maxRetries = 10 // Poll for max ~50 seconds

    return new Promise((resolve, reject) => {
        const interval = setInterval(async () => {
            try {
                const token = localStorage.getItem('token')
                if (!token) {
                    clearInterval(interval)
                    toast.error('Authentication token missing!')
                    reject('No token')
                    return
                }

                const response = await api.get(`/api/celery/send_prof/${taskId}`, {
                    headers: { 'Content-Type': 'application/json', 'Authentication-Token': token },
                })

                if (response.status === 200) {
                    clearInterval(interval)
                    resolve()
                } else {
                    console.log('File not ready yet... retrying')
                    retries++
                    if (retries >= maxRetries) {
                        clearInterval(interval)
                        toast.warning('File processing is taking longer than expected.', {
                            autoClose: 5000,
                        })
                        reject('Timeout')
                    }
                }
            } catch (error) {
                clearInterval(interval)
                console.error('Error checking task status:', error)
                toast.error('An error occurred while checking file status.')
                reject(error)
            }
        }, 5000) // Check every 5 seconds
    })
}

const downloadFile = async (taskId) => {
    try {
        const token = localStorage.getItem('token')
        if (!token) {
            toast.error('Authentication token missing!')
            return
        }

        const response = await api.get(`/api/celery/send_prof/${taskId}`, {
            headers: { 'Authentication-Token': token },
            responseType: 'blob', // Important for file download
        })

        if (response.status === 200) {
            const blob = new Blob([response.data], { type: 'text/csv' })
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = 'professionals.csv'
            document.body.appendChild(a)
            a.click()
            window.URL.revokeObjectURL(url)
            toast.success('Download started successfully!')
        } else {
            toast.error('Failed to fetch file.')
        }
    } catch (error) {
        console.error('Error downloading file:', error)
        toast.error('An error occurred while downloading the file.')
    }
}
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-danger shadow-sm">
        <div class="container-fluid">
            <!-- Logo & Website Name -->
            <router-link
                class="navbar-brand d-flex align-items-center text-decoration-none"
                to="/admin"
            >
                <img src="/tab-icon.webp" alt="Logo" class="logo me-2" />
                <span class="fw-bold">Home Service Admin</span>
            </router-link>

            <!-- Toggler for Mobile View -->
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#adminNavbar"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Navbar Links -->
            <div class="collapse navbar-collapse" id="adminNavbar">
                <ul class="navbar-nav ms-auto">
                    <!-- User Management -->
                    <li class="nav-item dropdown">
                        <a
                            class="nav-link dropdown-toggle"
                            href="#"
                            id="userDropdown"
                            role="button"
                            data-bs-toggle="dropdown"
                        >
                            <i class="pi pi-users"></i>&nbsp; Users
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <router-link class="dropdown-item" to="/admin/users">
                                    <i class="pi pi-list"></i>&nbsp; Manage Users
                                </router-link>
                            </li>
                            <li>
                                <router-link
                                    class="dropdown-item text-info"
                                    to="/admin/onboard-professional"
                                >
                                    <i class="pi pi-verified"></i>&nbsp; Approve Professionals
                                </router-link>
                            </li>
                            <li>
                                <router-link class="dropdown-item" to="/admin/professionals">
                                    <i class="pi pi-briefcase"></i>&nbsp; Professionals
                                </router-link>
                            </li>
                            <li>
                                <button class="dropdown-item" @click="fetchProfessionalData">
                                    <i class="pi pi-download"></i>&nbsp; Download Professionals Data
                                </button>
                            </li>
                        </ul>
                    </li>

                    <!-- Location -->
                    <li class="nav-item dropdown">
                        <a
                            class="nav-link dropdown-toggle"
                            href="#"
                            id="userDropdown"
                            role="button"
                            data-bs-toggle="dropdown"
                        >
                            <i class="pi pi-map"></i>&nbsp; Locations
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <router-link class="dropdown-item" to="/admin/locations">
                                    <i class="pi pi-list"></i>&nbsp; Manage Locations
                                </router-link>
                            </li>
                            <li>
                                <router-link
                                    class="dropdown-item text-info"
                                    to="/admin/add-location"
                                >
                                    <i class="pi pi-plus"></i>&nbsp; Create New Location
                                </router-link>
                            </li>
                        </ul>
                    </li>

                    <!-- Categories -->
                    <li class="nav-item dropdown">
                        <a
                            class="nav-link dropdown-toggle"
                            href="#"
                            id="userDropdown"
                            role="button"
                            data-bs-toggle="dropdown"
                        >
                            <i class="pi pi-bars"></i>&nbsp; Categories
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <router-link class="dropdown-item" to="/admin/categories">
                                    <i class="pi pi-list"></i>&nbsp; Manage Categories
                                </router-link>
                            </li>
                            <li>
                                <router-link
                                    class="dropdown-item text-info"
                                    to="/admin/add-category"
                                >
                                    <i class="pi pi-plus"></i>&nbsp; Create New Categories
                                </router-link>
                            </li>
                        </ul>
                    </li>

                    <!-- Service Management -->
                    <li class="nav-item dropdown">
                        <a
                            class="nav-link dropdown-toggle"
                            href="#"
                            id="serviceDropdown"
                            role="button"
                            data-bs-toggle="dropdown"
                        >
                            <i class="pi pi-briefcase"></i>&nbsp; Services
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <router-link class="dropdown-item" to="/admin/services">
                                    <i class="pi pi-list"></i>&nbsp; Manage Services
                                </router-link>
                            </li>
                            <li>
                                <router-link class="dropdown-item" to="/admin/add-service">
                                    <i class="pi pi-plus"></i>&nbsp; Create New Service
                                </router-link>
                            </li>
                        </ul>
                    </li>
                </ul>

                <!-- Profile Dropdown -->
                <div class="dropdown ms-3">
                    <button
                        class="btn btn-light dropdown-toggle"
                        type="button"
                        id="profileDropdown"
                        data-bs-toggle="dropdown"
                    >
                        <i class="pi pi-user" style="font-size: 1.5rem"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <router-link class="dropdown-item" to="/admin/profile">
                                <i class="pi pi-user"></i> &nbsp;&nbsp; Profile
                            </router-link>
                        </li>
                        <li>
                            <router-link class="dropdown-item" to="/admin/settings">
                                <i class="pi pi-cog"></i> &nbsp;&nbsp; Settings
                            </router-link>
                        </li>
                        <li><hr class="dropdown-divider" /></li>
                        <li>
                            <a class="dropdown-item text-danger" href="#" @click="logout">
                                <i class="pi pi-sign-out"></i>&nbsp;&nbsp; Logout
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</template>

<style scoped>
/* Logo Styling */
.logo {
    height: 40px;
}

/* Navbar Styling */
.navbar-nav .nav-link {
    font-size: 1rem;
    font-weight: 500;
    color: #333;
    transition: 0.3s;
}

.navbar-nav .nav-link:hover {
    color: #007bff;
}

/* Profile Icon Styling */
.profile-icon {
    height: 40px;
    width: 40px;
    border-radius: 50%;
    object-fit: cover;
}

/* Dropdown Menu */
.dropdown-menu {
    min-width: 220px;
}

.dropdown-item {
    font-size: 0.95rem;
    padding: 10px 15px;
}

.dropdown-item:hover {
    background-color: #f8f9fa;
}
</style>
