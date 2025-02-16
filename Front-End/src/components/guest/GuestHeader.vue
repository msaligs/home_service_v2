<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()
const isAuthenticated = ref(false)

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
  <nav class="navbar navbar-expand-lg bg-primary shadow-sm">
    <div class="container d-flex justify-content-between align-items-center">
      <!-- Logo & Brand Name -->
      <router-link class="navbar-brand d-flex align-items-center text-decoration-none" to="/">
        <img src="/tab-icon.webp" alt="Logo" class="logo" />
        <span class="fw-bold fs-3 ms-2">Home Service</span>
      </router-link>

      <!-- Right-side Links -->
      <div class="d-flex align-items-center">
        <!-- Register as Pro Button -->
        <router-link to="/auth/register-pro" class="pro-link"> Register as Pro </router-link>

        <!-- If User is Authenticated, Show Dropdown -->
        <div v-if="isAuthenticated" class="dropdown ms-3">
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

        <!-- If User is NOT Authenticated, Show Login Button -->
        <button v-else class="profile-btn ms-3" @click="router.push('/auth')">
          <i class="pi pi-user fs-3"></i>
          <span class="ms-2">Login</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.logo {
  height: 60px;
  margin-right: 15px;
}

.navbar-brand span {
  font-size: 1.8rem;
}

/* Register as Pro Button */
.pro-link {
  font-size: 1.1rem;
  font-weight: 500;
  color: #007bff;
  padding: 8px 15px;
  border: 2px solid #007bff;
  border-radius: 20px; /* Rounded corners */
  text-decoration: none;
  transition: 0.3s ease-in-out;
}

.pro-link:hover {
  background-color: #007bff;
  color: white;
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
