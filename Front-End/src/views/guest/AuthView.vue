<script setup>
import { RouterView } from 'vue-router'
import GuestHeader from '../../components/guest/GuestHeader.vue'
</script>

<template>
  <GuestHeader />
  <div class="auth-container d-flex justify-content-center align-items-center vh-100">
    <div class="auth-card">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
}

.auth-card {
  width: 400px;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
