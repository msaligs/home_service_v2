<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
// import { useToast } from 'vue-toastification'
import { toast } from 'vue3-toastify'
import api from '../../api'

const email = ref('')
const password = ref('')
const router = useRouter()
// const toast = useToast()

// Function to validate email format
const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

const login = () => {
    // Frontend validation before making API call
    if (!email.value || !password.value) {
        toast.error('Email and Password are required!', { timeout: 3000 })
        return
    }
    if (!isValidEmail(email.value)) {
        toast.error('Invalid email format!', { timeout: 3000 })
        return
    }

    api.post('/user_login', {
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

                const redirectAfterLogin = localStorage.getItem('redirectAfterLogin')
                // Redirect based on user role
                setTimeout(() => {
                    if (redirectAfterLogin) {
                        router.push(redirectAfterLogin)
                        localStorage.removeItem('redirectAfterLogin')
                    }
                    // router.push('/auth')
                    else if (userData.role === 'admin') {
                        router.push('/admin')
                    } else if (userData.role === 'professional') {
                        router.push('/professional')
                    } else {
                        router.push('/')
                    }
                }, 1000)
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
                <input
                    type="password"
                    v-model="password"
                    class="form-control"
                    id="password"
                    required
                />
            </div>

            <button type="submit" class="btn btn-primary w-100">Login</button>

            <div class="text-center mt-3">
                <router-link to="/auth/register">Register</router-link> |
                <router-link to="/auth/forgot-password">Forgot Password?</router-link>
            </div>
        </form>
    </div>
</template>
