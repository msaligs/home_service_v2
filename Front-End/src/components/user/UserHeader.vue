<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('email')
  router.push('/') // Redirect to login after logout
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

      <!-- User Profile Dropdown -->
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
            <router-link class="dropdown-item" to="/user/profile">
              <i class="pi pi-user"></i> &nbsp;&nbsp; Profile
            </router-link>
          </li>
          <li>
            <router-link class="dropdown-item" to="/user/settings">
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
