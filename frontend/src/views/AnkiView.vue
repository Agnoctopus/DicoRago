<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useVocabStore } from '@/stores/vocabulary'
import { useRouter } from 'vue-router'

// Access the stores.
const userStore = useUserStore()
const vocabStore = useVocabStore()
const router = useRouter()

// Sign-out function: redirect to your logout endpoint.
function signOut() {
  window.location.href = '/api/auth/logout/anki'
}

// Fetch user and vocabulary data on mount.
onMounted(async () => {
  if (!userStore.isFetched) {
    await userStore.fetchUser()
    if (!userStore.user) {
      // Redirect to the separate login view if not authenticated.
      router.push({ name: 'AnkiLoginView' })
      return
    }
    await vocabStore.loadVocabulary()
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-3xl mx-auto px-4 py-8">
      <!-- Main content when data is fetched and user is authenticated -->
      <div v-if="userStore.user">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Your Vocabulary</h1>
          <div class="flex items-center space-x-4 mt-4 sm:mt-0">
            <span class="text-gray-700">
              Hello, <strong>{{ userStore.user.name }}</strong>
            </span>
            <button
              @click="signOut"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors duration-200"
            >
              Sign Out
            </button>
          </div>
        </div>
        <!-- Additional content (e.g., vocabulary list) goes here -->
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles can be added here if necessary */
</style>
