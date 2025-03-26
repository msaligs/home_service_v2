<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('email')
    router.push('/')
}
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light-subtle shadow-sm">
        <div class="container-fluid d-flex justify-content-between align-items-center">
            <!-- Logo & Website Name -->
            <router-link
                class="navbar-brand d-flex align-items-center text-decoration-none"
                to="/professional"
            >
                <img src="/tab-icon.webp" alt="Logo" class="logo me-2" />
                <span class="fw-bold">Service Professional</span>
            </router-link>

            <!-- Profile Dropdown -->
            <div class="dropdown">
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
                        <router-link class="dropdown-item" to="/professional/profile">
                            <i class="pi pi-user"></i> &nbsp;&nbsp; Profile
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
    </nav>
</template>

<style scoped>
/* Logo Styling */
.logo {
    height: 40px;
}

/* Navbar Styling */
.navbar {
    padding: 10px 20px;
    background: #f8f9fa;
}

/* Profile Dropdown */
.dropdown-menu {
    min-width: 180px;
}

.dropdown-item {
    font-size: 0.95rem;
    padding: 10px 15px;
}

.dropdown-item:hover {
    background-color: #f0f0f0;
}
</style>
