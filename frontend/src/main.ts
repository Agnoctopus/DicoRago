import './assets/style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

/** Create the Vue app instance */
const app = createApp(App)

/** Register the Pinia store for state management */
app.use(createPinia())

/** Register the router for navigation */
app.use(router)

/** Mount the app to the DOM element with id 'app' */
app.mount('#app')
