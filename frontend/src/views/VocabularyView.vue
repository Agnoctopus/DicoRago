<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useVocabStore } from '@/stores/vocabulary'
import NavigationBar from '@/components/NavigationBar.vue'
import VocabularyTable from '@/components/VocabularyTable.vue'

// Access the vocab and user store.
const vocabStore = useVocabStore()
const userStore = useUserStore()

// Fetch user data when the component mounts.
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
  <div class="min-h-screen flex flex-col bg-gray-50">
    <NavigationBar />

    <!-- Main content area -->
    <div class="p-4 flex flex-col items-center">
      <VocabularyTable />
    </div>
  </div>
</template>
