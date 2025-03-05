<script setup lang="ts">
import { computed } from 'vue'
import type { Word } from '@/types'
import VocabularyEntry from './VocabularyEntry.vue'
import { useVocabStore } from '@/stores/vocabulary'
import { useSettingsStore } from '@/stores/settings'

/**
 * Component props:
 * - vocab: Array of Word to display.
 */
const props = defineProps<{ vocab: Word[] }>()

// Access the vocabulary store.
const vocabStore = useVocabStore()
const settingsStore = useSettingsStore()

// Use the settings store
const filterVocabulary = computed({
  get: () => settingsStore.vocabularyEnabled,
  set: () => {},
})

/**
 * Compute filtered vocabulary:
 * If filter is enable, return only words that are not learned.
 * Otherwise, return all words.
 */
const filteredVocab = computed(() => {
  return filterVocabulary.value
    ? props.vocab.filter((word) => !vocabStore.isLearned(word.written))
    : props.vocab
})

/**
 * Group words by their "written" property.
 * Returns an array of objects with:
 * - written: the word string.
 * - words: a set of Word objects sharing the same written form.
 */
const groupedVocab = computed(() => {
  const groups: Record<string, Set<Word>> = {}
  filteredVocab.value.forEach((word) => {
    if (!groups[word.written]) {
      groups[word.written] = new Set<Word>()
    }
    groups[word.written].add(word)
  })
  return Object.entries(groups).map(([written, words]) => ({
    written,
    words,
  }))
})
</script>

<template>
  <div class="w-full max-w-2xl mx-auto mt-6 bg-white p-4 rounded shadow">
    <h3 class="text-xl font-semibold mb-4">Vocabulary List</h3>
    <table class="w-full table-fixed border-collapse">
      <thead>
        <tr>
          <th class="px-4 py-1 text-left w-25">Word</th>
          <th class="px-4 py-1 text-left">English Translations</th>
          <th class="px-4 py-1 w-10"></th>
        </tr>
      </thead>
      <tbody>
        <!-- Iterate over grouped vocabulary entries -->
        <VocabularyEntry
          v-for="group in groupedVocab"
          :key="group.written"
          :written="group.written"
          :words="group.words"
        />
      </tbody>
    </table>
  </div>
</template>
