<script setup>
import { useRouter, useRoute } from 'vue-router'
import { ref, computed, onMounted } from 'vue'

const router = useRouter()
const route = useRoute()

const isAuthenticated = ref(false)

// ✅ Use `computed` to ensure reactivity
const hideLoginButton = computed(() => route.path === '/auth')
const hideProButton = computed(() => route.path === '/auth/professional-register')

onMounted(() => {
    isAuthenticated.value = !!localStorage.getItem('token') // Check if token exists
})

const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('email')
    isAuthenticated.value = false
    router.push('/auth') // Redirect to login after logout
}
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-light shadow-sm border-bottom">
        <div class="container d-flex justify-content-between align-items-center">
            <!-- Logo & Brand Name -->
            <router-link class="navbar-brand d-flex align-items-center text-decoration-none" to="/">
                <img src="/tab-icon.webp" alt="Logo" class="logo" />
                <span class="fw-bold fs-3 ms-2 text-primary">Home Service</span>
            </router-link>

            <!-- Right-side Links -->
            <div class="d-flex align-items-center">
                <!-- Register as Pro Button (Hidden on Professional Register Page) -->
                <router-link
                    v-if="!hideProButton"
                    to="/auth/professional-register"
                    class="pro-link ms-3"
                >
                    <i class="pi pi-briefcase me-2"></i> Become a Pro
                </router-link>

                <!-- If User is Authenticated, Show Dropdown -->
                <div v-if="isAuthenticated" class="dropdown ms-3">
                    <button
                        class="btn btn-light dropdown-toggle profile-btn"
                        type="button"
                        id="profileDropdown"
                        data-bs-toggle="dropdown"
                    >
                        <i class="pi pi-user" style="font-size: 1.5rem"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <router-link class="dropdown-item" to="/profile">
                                <i class="pi pi-user"></i> &nbsp;&nbsp; Profile
                            </router-link>
                        </li>
                        <li>
                            <router-link class="dropdown-item" to="/settings">
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

                <!-- If User is NOT Authenticated, Show Login Button (Hidden on Login Page) -->
                <button
                    v-if="!isAuthenticated && !hideLoginButton"
                    class="profile-btn ms-3"
                    @click="router.push('/auth')"
                >
                    <i class="pi pi-user fs-3"></i>
                    <span class="ms-2">Login</span>
                </button>
            </div>
        </div>
    </nav>
</template>

<style scoped>
/* Logo */
.logo {
    height: 60px;
    margin-right: 15px;
}

/* Navbar Background */
.navbar {
    background-color: #ffffff !important;
}

/* Brand Name */
.navbar-brand span {
    font-size: 1.8rem;
    font-weight: bold;
}

/* Register as Pro Button (Highlighted) */
.pro-link {
    font-size: 1rem;
    font-weight: 600;
    color: white !important;
    background-color: #ff7f0e; /* Bright orange to stand out */
    padding: 10px 18px;
    border-radius: 25px;
    text-decoration: none;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-in-out;
}

.pro-link:hover {
    background-color: #e66b00;
    box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.15);
}

/* Profile Button */
.profile-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #333;
    transition: 0.3s;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
}

.profile-btn:hover {
    color: #007bff;
}

/* Dropdown Menu */
.dropdown-menu {
    min-width: 180px;
}

.dropdown-item {
    display: flex;
    align-items: center;
}

.dropdown-item i {
    font-size: 1.2rem;
}
</style>
