<template>
    <div class="modal fade show d-block" tabindex="-1" aria-modal="true" role="dialog">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ address ? 'Update Address' : 'Add Address' }}</h5>
                    <button type="button" class="btn-close" @click="$emit('close')"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="saveAddress">
                        <div class="mb-3">
                            <label class="form-label">Address</label>
                            <input
                                v-model="form.address"
                                type="text"
                                required
                                class="form-control"
                            />
                            <!-- Added validation message for address length -->
                            <small v-if="form.address.trim().length < 5" class="text-danger">
                                Address must be at least 5 characters long.
                            </small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">State</label>
                            <select v-model="selectedState" class="form-select" required>
                                <option value="" disabled>Select a state</option>
                                <option v-for="state in uniqueStates" :key="state" :value="state">
                                    {{ state }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">City</label>
                            <select
                                v-model="form.location_id"
                                class="form-select"
                                :disabled="!selectedState"
                                required
                            >
                                <option value="" disabled>Select a city</option>
                                <option v-for="loc in filteredCities" :key="loc.id" :value="loc.id">
                                    {{ loc.city }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Pincode</label>
                            <input
                                v-model="form.pincode"
                                type="text"
                                required
                                class="form-control"
                                @input="validatePincode"
                            />
                            <!-- Added validation message for pincode -->
                            <small v-if="form.pincode && !isValidPincode" class="text-danger">
                                Invalid Pincode
                            </small>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="$emit('close')">
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-primary">Save</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import api from '@/api'

const props = defineProps({
    address: Object,
})
const emit = defineEmits(['close', 'save'])

const form = ref({ address: '', location_id: '', pincode: '' })
const locations = ref([])
const selectedState = ref('')
const token = localStorage.getItem('token')
const isValidPincode = ref(true)

const fetchLocations = async () => {
    try {
        const response = await api.get('/api/common/get-locations')
        locations.value = response.data
    } catch (error) {
        console.error('Error fetching locations:', error)
    }
}

const uniqueStates = computed(() => {
    return [...new Set(locations.value.map((loc) => loc.state))]
})

const filteredCities = computed(() => {
    return locations.value.filter((loc) => loc.state === selectedState.value)
})

const validatePincode = async () => {
    if (!form.value.pincode || form.value.pincode.length !== 6) {
        isValidPincode.value = false
        return
    }
    try {
        const response = await api.get(`https://api.postalpincode.in/pincode/${form.value.pincode}`)
        isValidPincode.value = response.data[0].Status === 'Success'
    } catch (error) {
        isValidPincode.value = false
        console.error('Error validating pincode:', error)
    }
}

watch(() => form.value.pincode, validatePincode)

watch(
    () => props.address,
    (newAddress) => {
        if (newAddress) {
            selectedState.value =
                locations.value.find((loc) => loc._id === newAddress.location_id)?.state || ''
            form.value = { ...newAddress }
        } else {
            selectedState.value = ''
            form.value = { address: '', location_id: '', pincode: '' }
        }
    },
    { immediate: true }
)

const saveAddress = async () => {
    validatePincode()
    // Added validation check for address length before saving
    if (!isValidPincode.value || form.value.address.trim().length < 5) {
        alert('Please enter a valid address and pincode before submitting.')
        return
    }
    try {
        if (props.address) {
            await api.put(`/api/user/update_address`, form.value, {
                headers: { 'Authentication-Token': token },
            })
        } else {
            await api.post('/api/user/add_address', form.value, {
                headers: { 'Authentication-Token': token },
            })
        }
        emit('save')
        emit('close')
    } catch (error) {
        console.error('Error saving address:', error)
    }
}

onMounted(fetchLocations)
</script>
