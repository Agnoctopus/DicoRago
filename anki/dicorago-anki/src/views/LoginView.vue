<script setup lang="ts">
import { onMounted, ref, nextTick } from 'vue'

// Declare the global types for window properties.
declare global {
  interface Window {
    anki: {
      syncVocabulary: (vocabJson: string) => void
    }
    qt?: any
    QWebChannel?: any
  }
}

const loading = ref(false)
const message = ref('')
const inAnki = ref(false)

// Starts the login process by redirecting to the login URL.
function startLogin() {
  loading.value = true
  // Use the current URL (without query) as the redirect_uri.
  const currentUrl = window.location.href.split('?')[0]
  const redirectUrl = encodeURIComponent(currentUrl)
  // Replace with your actual login URL if needed.
  const loginUrl = `https://agno.re/anki`
  window.location.href = loginUrl
}

onMounted(() => {
  window.anki.syncVocabulary("test")
  inAnki.value = !!window.anki;
})
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-indigo-600"
  >
    <div class="max-w-md w-full p-8 bg-white rounded-lg shadow-lg">
      <h2 class="text-3xl font-bold text-center mb-4">Dicorago Login</h2>
      <p v-if="message" class="mb-4 text-center text-gray-700">{{ message }}</p>
      <button
        v-if="!loading"
        @click="startLogin"
        class="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
      >
        Sign in with Google
      </button>
      <p v-if="loading" class="mt-4 text-center text-gray-600">Logging in, please wait...</p>
      <p v-if="inAnki" class="mt-4 text-center text-green-600">Running in Anki</p>
      <p v-if="!inAnki" class="mt-4 text-center text-red-600">Not running in Anki</p>
    </div>
  </div>
</template>

<style scoped>
/* Tailwind CSS handles all styling */
</style>
