<template>
  <div>
    <h2 class="text-center mb-3">Create an Account</h2>

    <form @submit.prevent="registerUser">
      <div class="mb-3">
        <label for="name" class="form-label">Full Name</label>
        <input type="text" id="name" class="form-control" v-model="user.name" required />
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Email Address</label>
        <input type="email" id="email" class="form-control" v-model="user.email" required />
      </div>

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

      <button type="submit" class="btn btn-primary w-100" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>

      <div class="text-center mt-3">
        Already have an account?
        <router-link to="/auth">Login</router-link>
      </div>

      <!-- Success / Error Messages -->
      <div v-if="message" :class="`alert mt-3 ${messageType}`">
        {{ message }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const user = ref({
  name: '',
  email: '',
  mobile: '',
  password: '',
  role: 'user',
})

const loading = ref(false)
const message = ref('')
const messageType = ref('') // 'alert-success' or 'alert-danger'

const registerUser = async () => {
  if (!/^\d{10}$/.test(user.value.mobile)) {
    message.value = 'Mobile number must be exactly 10 digits.'
    messageType.value = 'alert-danger'
    return
  }

  loading.value = true
  message.value = ''

  try {
    const response = await fetch('http://127.0.0.1:5000/register_user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user.value),
    })

    const data = await response.json()

    if (response.ok) {
      message.value = data.message || 'Registration successful!'
      messageType.value = 'alert-success'
      user.value = { name: '', email: '', mobile: '', password: '' } // Reset form
      routerKey.push('/auth') // Redirect
    } else {
      message.value = data.error || 'Registration failed. Try again.'
      messageType.value = 'alert-danger'
    }
  } catch (error) {
    message.value = 'Server error. Please try again later.'
    messageType.value = 'alert-danger'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.alert {
  padding: 10px;
  border-radius: 5px;
  text-align: center;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
