<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
// import { useToast } from 'vue-toastification'
import { toast } from 'vue3-toastify'

const email = ref('')
const password = ref('')

const router = useRouter()
// const toast = useToast()

const login = () => {
  axios
    .post('http://127.0.0.1:5000/user_login', {
      email: email.value,
      password: password.value,
    })
    .then((response) => {
      if (response.data.success) {
        const userData = response.data.data

        // Store token, email, and role
        localStorage.setItem('token', userData.token)
        localStorage.setItem('email', userData.email)
        localStorage.setItem('role', userData.role)

        // Show success message
        toast.success(response.data.message, { timeout: 3000 })

        // Redirect based on user role
        if (userData.role === 'admin') {
          router.push('/admin')
        } else if (userData.role === 'professional') {
          router.push('/professional')
        } else {
          router.push('/')
        }
      }
    })
    .catch((error) => {
      if (error.response) {
        // Extract error message from API response
        const errorMessage = error.response.data.message || 'An error occurred.'
        toast.error(errorMessage, { timeout: 3000 })
      } else {
        // Handle network or unknown errors
        toast.error('Network error. Please try again.', { timeout: 3000 })
      }
      console.error('Login failed:', error)
    })
}
</script>
<template>
  <div>
    <h3 class="text-center mb-3">Login</h3>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input type="email" v-model="email" class="form-control" id="email" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" v-model="password" class="form-control" id="password" required />
      </div>

      <button type="submit" class="btn btn-primary w-100">Login</button>

      <div class="text-center mt-3">
        <router-link to="/auth/register">Register</router-link> |
        <router-link to="/auth/forgot-password">Forgot Password?</router-link>
      </div>
    </form>
  </div>
</template>
