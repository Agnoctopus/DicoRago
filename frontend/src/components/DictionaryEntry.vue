<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useDictionaryStore } from '@/stores/dictionary'
import type { LearnedWord, Word, Sense } from '@/types'
import SenseList from '@/components/SenseList.vue'

/**
 * Component props:
 * - vocab: A LearnedWord object containing the written word and its update timestamp.
 */
const props = defineProps<{ vocab: LearnedWord }>()

// Get the dictionary store instance.
const dictionaryStore = useDictionaryStore()

// On component mount, if the words for the given written form are not loaded,
// sync them from the server.
onMounted(async () => {
  if (!dictionaryStore.getWords(props.vocab.written)) {
    await dictionaryStore.syncWritten(props.vocab.written)
  }
})

/**
 * Computed property to get the associated Word objects from the dictionary store
 * that match the learned word's written form. If none are found, returns an empty array.
 */
const associatedWords = computed<Word[]>(() => {
  return dictionaryStore.getWords(props.vocab.written) || []
})

/**
 * Computes a comma-separated string of unique translations
 * from all senses of the associated words.
 */
const translatedSensesText = computed(() => {
  const translations = new Set<string>()
  associatedWords.value.forEach((word: Word) => {
    word.senses.forEach((sense: Sense) => {
      translations.add(sense.translation)
    })
  })
  return Array.from(translations).join(', ')
})

/**
 * Aggregates all senses from the associated words into an array.
 */
const aggregatedSenses = computed(() => {
  const senses: Sense[] = []
  associatedWords.value.forEach((word: Word) => {
    word.senses.forEach((sense: Sense) => senses.push(sense))
  })
  return senses
})

// Toggle state for expanding/collapsing the word senses.
const isExpanded = ref(false)
const toggle = () => {
  isExpanded.value = !isExpanded.value
}
</script>

<template>
  <!-- Main row: displays the word and a summary of its senses translations -->
  <tr
    @click="toggle"
    class="transition-all duration-300 hover:bg-gray-50 cursor-pointer select-none"
  >
    <td class="px-4 py-1 font-extrabold whitespace-nowrap">
      <span class="select-text font-extrabold">{{ vocab.written }}</span>
    </td>
    <td class="px-4 py-1 truncate">{{ translatedSensesText }}</td>
    <td class="px-4 py-1 text-right">
      <svg
        :class="{ 'transform rotate-180': isExpanded }"
        class="w-5 h-5 text-blue-500 transition-transform duration-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M19 9l-7 7-7-7" />
      </svg>
    </td>
  </tr>

  <!-- Expanded row: shows detailed list of senses when expanded -->
  <tr v-if="isExpanded">
    <td></td>
    <td colspan="2" class="px-4 py-2 border-t">
      <SenseList :senses="aggregatedSenses" />
    </td>
  </tr>
</template>
