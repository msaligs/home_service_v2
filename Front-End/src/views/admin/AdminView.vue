<script setup>
import adminHeader from '../components/AdminHeader.vue'

// role = localStorage.getItem('role')
</script>

<template>
  <div>
    <adminHeader />
    <router-view />
  </div>
</template>

<style scoped>
div {
  padding-left: 20px;
  padding-right: 20px;
}
</style>
