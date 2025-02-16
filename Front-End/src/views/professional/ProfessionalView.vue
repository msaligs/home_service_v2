<script setup>
import ProfessionalHeader from '../components/ProfessionalHeader.vue'
</script>

<template>
  <div>
    <ProfessionalHeader />
    <router-view />
  </div>
</template>

<style scoped>
div {
  padding-left: 20px;
  padding-right: 20px;
}
</style>
