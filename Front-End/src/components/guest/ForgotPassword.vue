<template>
  <div>
    <h2 class="text-center mb-3">Forgot Password</h2>
    <p class="text-muted text-center">
      Enter your email address below, and we'll send you a link to reset your password.
    </p>

    <form @submit.prevent="submitForgotPassword">
      <div class="mb-3">
        <label for="email" class="form-label">Email Address</label>
        <input type="email" id="email" class="form-control" v-model="email" required />
      </div>

      <button type="submit" class="btn btn-primary w-100">Send Reset Link</button>

      <div class="text-center mt-3">
        <router-link to="/auth">Back to Login</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')

const submitForgotPassword = () => {
  alert(`A password reset link has been sent to ${email.value}`)
}
</script>
