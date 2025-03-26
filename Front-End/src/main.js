import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import 'primeicons/primeicons.css'
// import 'vue3-toast-notification/dist/theme-default.css'
import 'vue3-toastify/dist/index.css'

const app = createApp(App)

// app.use(Toast, { position: POSITION.TOP_RIGHT })

app.use(Vue3Toastify, {
    autoClose: 3000, // Toast disappears after 3 seconds
    position: 'top-right',
})
app.use(router)
app.mount('#app')
