<script setup>
import AdminHeader from '@/components/admin/AdminHeader.vue'
</script>
<template>
    <div class="admin-layout">
        <AdminHeader />
        <div class="admin-content">
            <router-view />
        </div>
    </div>
</template>
