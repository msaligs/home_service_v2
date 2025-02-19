<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
    // Perform logout logic (clear session, redirect)
    localStorage.removeItem('token')
    localStorage.removeItem('email')
    localStorage.removeItem('role')
    // alert('Logging out...')
    router.push('/')
}
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-danger shadow-sm">
        <div class="container-fluid">
            <!-- Logo & Website Name -->
            <router-link
                class="navbar-brand d-flex align-items-center text-decoration-none"
                to="/admin/dashboard"
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
                    <!-- Admin Dashboard -->
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/dashboard">
                            <i class="pi pi-chart-line"></i>&nbsp; Dashboard
                        </router-link>
                    </li>

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
                                    <i class="pi pi-check"></i>&nbsp; Approve Professionals
                                </router-link>
                            </li>
                            <li>
                                <router-link class="dropdown-item" to="/admin/professional">
                                    <i class="pi pi-briefcase"></i>&nbsp; Professionals
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
                                <router-link class="dropdown-item" to="/admin/services/create">
                                    <i class="pi pi-plus"></i>&nbsp; Create New Service
                                </router-link>
                            </li>
                            <li>
                                <router-link class="dropdown-item" to="/admin/services/update">
                                    <i class="pi pi-pencil"></i>&nbsp; Update Service
                                </router-link>
                            </li>
                            <li>
                                <router-link
                                    class="dropdown-item text-danger"
                                    to="/admin/services/delete"
                                >
                                    <i class="pi pi-trash"></i>&nbsp; Delete Service
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
