<script setup lang="ts">
import DictionaryEntry from '@/components/DictionaryEntry.vue'
import { useVocabStore } from '@/stores/vocabulary'
import type { LearnedWord } from '@/types'

// Receive the learned vocabulary as a prop.
defineProps<{ learnedVocab: LearnedWord[] }>()
// Get the vocabulary store instance.
const vocabStore = useVocabStore()

// Handle the removal of a vocabulary word.
function handleRemove(written: string) {
  vocabStore.toggleLearned(written, [])
}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto bg-white p-2 rounded shadow">
    <table class="w-full table-fixed border-collapse">
      <thead>
        <tr>
          <th class="px-4 py-1 text-left w-25">Word</th>
          <th class="px-4 py-1 text-left">Translations</th>
          <th class="px-4 py-1 w-10"></th>
        </tr>
      </thead>
      <tbody>
        <template v-if="learnedVocab.length > 0">
          <DictionaryEntry
            v-for="(entry, index) in learnedVocab"
            :key="index"
            :vocab="entry"
            @remove="handleRemove"
          />
        </template>
        <tr v-else>
          <td colspan="3" class="px-4 py-2 text-center text-gray-600">
            No learned vocabulary yet.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
