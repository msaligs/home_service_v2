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
    <div class="container-fluid">
      <!-- Logo & Website Name -->
      <router-link
        class="navbar-brand d-flex align-items-center text-decoration-none"
        to="/pro/dashboard"
      >
        <img src="/tab-icon.webp" alt="Logo" class="logo me-2" />
        <span class="fw-bold">Service Professional</span>
      </router-link>

      <!-- Toggler for Mobile View -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#proNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar Links -->
      <div class="collapse navbar-collapse" id="proNavbar">
        <ul class="navbar-nav ms-auto">
          <!-- Dashboard -->
          <li class="nav-item">
            <router-link class="nav-link" to="/professional/dashboard">
              <i class="pi pi-home"></i>&nbsp; Dashboard
            </router-link>
          </li>

          <!-- Service Requests -->
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="requestsDropdown"
              role="button"
              data-bs-toggle="dropdown"
            >
              <i class="pi pi-list"></i>&nbsp; Service Requests
            </a>
            <ul class="dropdown-menu">
              <li>
                <router-link class="dropdown-item" to="/professional/requests">
                  <i class="pi pi-folder"></i>&nbsp; View All Requests
                </router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/professional/requests/pending">
                  <i class="pi pi-hourglass"></i>&nbsp; Accept/Reject Requests
                </router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/professional/requests/completed">
                  <i class="pi pi-check-circle"></i>&nbsp; Close Completed Requests
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
              <router-link class="dropdown-item" to="/professional/profile">
                <i class="pi pi-user"></i> &nbsp;&nbsp; Profile
              </router-link>
            </li>
            <li>
              <router-link class="dropdown-item" to="/professional/settings">
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
