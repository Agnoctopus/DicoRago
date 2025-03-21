<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Word, Sense } from '@/types'
import SenseList from '@/components/SenseList.vue'

/**
 * Component props:
 * - written: Written form.
 * - words: Words sharing the same written form.
 */
const props = defineProps<{
  written: string
  words: Set<Word>
}>()

/**
 * Computes a comma-separated string of unique translations
 * from all senses of the displayed words.
 */
const translatedSensesText = computed(() => {
  const translations = new Set<string>()
  props.words.forEach((word) => {
    word.senses.forEach((sense) => {
      translations.add(sense.translation)
    })
  })
  return Array.from(translations).join(', ')
})

/**
 * Aggregates all senses from the displayed word into an array.
 */
const aggregatedSenses = computed(() => {
  const senses: Sense[] = []
  props.words.forEach((word) => {
    word.senses.forEach((sense) => {
      senses.push(sense)
    })
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
      <span class="select-text font-extrabold">{{ written }}</span>
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
