<script setup lang="ts">
import NavigationBar from '@/components/NavigationBar.vue'
import { useVocabStore } from '@/stores/vocabulary'

// Retrieve vocabulary store
const vocabStore = useVocabStore()

// The learnedVocab variable is defined in the store as a readonly ref.
const learnedVocab = vocabStore.learnedVocab
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Bar at the top -->
    <NavigationBar />

    <!-- Main Content Container -->
    <div class="flex flex-col items-center p-4">
      <!-- Learned Vocabulary List -->
      <div v-if="learnedVocab.length" class="w-full max-w-3xl">
        <div
          v-for="(word, index) in learnedVocab"
          :key="index"
          class="mb-4 bg-white p-4 rounded shadow"
        >
          <!-- Header with the word and its "Appris" badge -->
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-semibold">{{ word.written }}</h3>
            <div>
              <span class="px-2 py-1 bg-green-200 text-green-800 rounded">Appris</span>
            </div>
          </div>
          <!-- Additional word details can be added here -->
        </div>
      </div>

      <!-- Message when no vocabulary is learned -->
      <div v-else class="text-gray-600">
        <p>Aucun vocabulaire appris pour le moment.</p>
      </div>
    </div>
  </div>
</template>
