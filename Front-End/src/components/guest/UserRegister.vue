<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'
import { toast } from 'vue3-toastify'

const router = useRouter()

const user = ref({
    name: '',
    email: '',
    mobile: '',
    password: '',
    role: 'user',
})

const loading = ref(false)

// Validation function
const validateUserData = () => {
    // Validate name
    if (!user.value.name.trim()) {
        toast.error('Name is required.', { timeout: 3000 })
        return false
    }

    // Validate email format using regex
    if (!/^\S+@\S+\.\S+$/.test(user.value.email)) {
        toast.error('Invalid email format.', { timeout: 3000 })
        return false
    }

    // Validate mobile number (must be exactly 10 digits)
    if (!/^\d{10}$/.test(user.value.mobile)) {
        toast.error('Mobile number must be exactly 10 digits.', { timeout: 3000 })
        return false
    }

    // Validate password length (must be at least 6 characters long)
    if (user.value.password.length < 6) {
        toast.error('Password must be at least 6 characters long.', { timeout: 3000 })
        return false
    }

    return true // Validation passed
}

const registerUser = async () => {
    if (!validateUserData()) return // Stop if validation fails

    loading.value = true

    try {
        const response = await api.post('/api/user/register_user', user.value)

        if (response.status === 201) {
            // Reset form after successful registration
            user.value = { name: '', email: '', mobile: '', password: '', role: 'user' }
            toast.success(response.data.message, { timeout: 3000 })

            setTimeout(() => {
                router.push('/auth')
            }, 2500)
        } else {
            toast.error('Registration failed. Try again.', { timeout: 3000 })
        }
    } catch (error) {
        toast.error(error.response?.data?.error || 'An error occurred.', { timeout: 3000 })
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div>
        <h2 class="text-center mb-3">Create an Account</h2>

        <form @submit.prevent="registerUser">
            <!-- Name Field -->
            <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" id="name" class="form-control" v-model="user.name" required />
            </div>

            <!-- Email Field -->
            <div class="mb-3">
                <label for="email" class="form-label">Email Address</label>
                <input type="email" id="email" class="form-control" v-model="user.email" required />
            </div>

            <!-- Mobile Field -->
            <div class="mb-3">
                <label for="mobile" class="form-label">Mobile Number</label>
                <input
                    type="text"
                    id="mobile"
                    class="form-control"
                    v-model="user.mobile"
                    pattern="\d{10}"
                    required
                />
            </div>

            <!-- Password Field -->
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                    type="password"
                    id="password"
                    class="form-control"
                    v-model="user.password"
                    required
                />
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Registering...' : 'Register' }}
            </button>

            <div class="text-center mt-3">
                Already have an account?
                <router-link to="/auth">Login</router-link>
            </div>
        </form>
    </div>
</template>
