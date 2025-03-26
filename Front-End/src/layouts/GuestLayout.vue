<script setup>
import { ref, onMounted } from 'vue'
import GuestHeader from '@/components/guest/GuestHeader.vue'
import UserHeader from '@/components/user/UserHeader.vue'

const token = ref(null)

onMounted(() => {
    token.value = localStorage.getItem('token') // Get the token on component mount
})
</script>

<template>
    <div>
        <UserHeader v-if="token" />
        <GuestHeader v-else />
        <router-view />
    </div>
</template>
