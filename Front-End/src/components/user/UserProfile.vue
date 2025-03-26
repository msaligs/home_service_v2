<template>
    <div class="container mt-5">
        <div class="card shadow-lg p-3 mb-5 bg-white rounded">
            <div class="card-body text-center">
                <img
                    :src="user.profile_img_url || 'https://via.placeholder.com/150'"
                    alt="Profile Image"
                    class="rounded-circle mb-3"
                    width="150"
                    height="150"
                />
                <h3 class="card-title">{{ user.name }}</h3>
                <p class="text-muted">{{ user.email }}</p>
                <p class="text-muted">Mobile: {{ user.mobile }}</p>
                <p class="text-muted">Member Since: {{ formatDate(user.created_at) }}</p>
                <button class="btn btn-primary mt-3" @click="editProfile">Edit Profile</button>
            </div>
        </div>
    </div>
</template>

<script>
import api from '../../api'

export default {
    data() {
        return {
            user: {},
        }
    },
    mounted() {
        this.fetchUserProfile()
    },
    methods: {
        async fetchUserProfile() {
            try {
                const token = localStorage.getItem('token')
                if (!token) throw new Error('Token missing!')

                const response = await api.get(
                    '/api/user/profile',

                    {
                        headers: { 'Authentication-Token': token },
                    }
                )
                this.user = response.data
            } catch (error) {
                console.error('Error fetching user profile:', error)
            }
        },
        formatDate(dateString) {
            const date = new Date(dateString)
            return date.toLocaleDateString()
        },
        editProfile() {
            alert('Edit Profile clicked!')
        },
    },
}
</script>

<style scoped>
.card {
    max-width: 400px;
    margin: auto;
}
</style>
