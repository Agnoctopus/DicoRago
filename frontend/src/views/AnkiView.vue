<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useVocabStore } from '@/stores/vocabulary'
import AnkiLogin from '@/components/AnkiLogin.vue'

// Access the stores.
const userStore = useUserStore()
const vocabStore = useVocabStore()

// Fetch user and vocabulary data on mount.
onMounted(async () => {
  if (!userStore.isFetched) {
    await userStore.fetchUser()
    if (userStore.user) {
      await vocabStore.loadVocabulary()
    }
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-3xl mx-auto px-4 py-8">
      <!-- Show login view if user is not authenticated -->
      <AnkiLogin v-if="!userStore.user" />

      <!-- Main content when user is authenticated -->
      <div v-else>
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Your Vocabulary</h1>
          <div class="flex items-center space-x-4 mt-4 sm:mt-0">
            <span class="text-gray-700"
              >Hello, <strong>{{ userStore.user.name }}</strong></span
            >
          </div>
        </div>
        <!-- Additional content like vocabulary list can be added here -->
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles can be added here if necessary */
</style>
