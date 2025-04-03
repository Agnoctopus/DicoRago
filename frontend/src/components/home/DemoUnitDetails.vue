<script setup lang="ts">
import { computed } from 'vue'
import type { Unit, Word, Sense } from '@/types'
import SenseList from '@/components/SenseList.vue'
import { tagMeanings } from '@/data/tag'
import { mdiHelpCircleOutline } from '@mdi/js'

/**
 * Props:
 * - unit: Analyzed text unit to display.
 * - vocab: Vocabulary words.
 */
const props = defineProps<{
  unit: Unit
  vocab: Word[]
  status: string
}>()

// Returns words matching the unit's vocabulary property.
const matchingWords = computed(() => {
  if (props.unit.vocabulary) {
    return props.vocab.filter((word) => word.written === props.unit.vocabulary)
  }
  return []
})

// Aggregates senses from matching words into an array.
const aggregatedSenses = computed(() => {
  const senses: Sense[] = []
  matchingWords.value.forEach((word) => {
    word.senses.forEach((sense) => senses.push(sense))
  })
  return senses
})

// Define the status options.
// For "unknown," the label is removed so that an icon is used instead.
const statusOptions = [
  { value: 'ignore', label: 'Ignore' },
  { value: 'seen', label: 'Seen' },
  { value: 'learned', label: 'Learned' },
  { value: 'unknown', label: '' },
]

// Colors for the selected state.
const selectedColors: Record<string, string> = {
  learned: 'bg-[#c0ffc0] text-green-800', // Pale green background for learned.
  seen: 'bg-[#ffe0a8] text-orange-900',
  unknown: 'bg-red-100 text-red-400 hover:bg-red-100', // For unknown, the background is light.
  ignore: 'bg-gray-300 text-black',
}

// Colors for the unselected state (no borders, just colored text with subtle hover).
const unselectedColors: Record<string, string> = {
  learned: 'bg-white opacity-50 text-green-600 hover:bg-green-100',
  seen: 'bg-white opacity-50 text-orange-600 hover:bg-orange-100',
  unknown: 'bg-white opacity-50 text-red-400 hover:bg-red-100',
  ignore: 'bg-white opacity-50 text-gray-600 hover:bg-gray-100',
}
</script>

<template>
  <!-- Disposition en deux colonnes -->
  <div class="flex flex-col-reverse lg:flex-row items-scretch lg:gap-0 gap-4">
    <!-- Colonne premiere (40% sur desktop) -->
    <div class="lg:w-2/5 lg:pr-8 lg:border-r-2 border-gray-200">
      <!-- Morphemes Section -->
      <div class="w-full overflow-auto bg-white p-4 rounded shadow">
        <h3 class="text-xl font-semibold mb-4">Morphemes</h3>
        <div class="flex flex-wrap gap-2 px-4 py-1">
          <!-- Iterate through each morpheme in the unit -->
          <div
            v-for="(morph, index) in unit.morphs"
            :key="index"
            class="flex flex-col items-center px-2 py-1 bg-gray-100 rounded-2xl border border-gray-300"
          >
            <span class="font-bold">{{ morph.lex }}</span>
            <span class="text-[0.5rem] leading-tight text-gray-500">
              {{ tagMeanings[morph.tag] || morph.tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="lg:w-3/5 lg:pl-8 flex items-center justify-center">
      <!-- Vocabulary Section -->
      <div class="w-full h-full bg-white p-4 rounded shadow">
        <!-- Header with title and status selection -->
        <div class="flex items-center justify-between mb-4">
          <!-- Vocabulary word inside a styled container -->
          <div class="px-2 py-1 border border-gray-300 rounded-md bg-gray-50">
            <h2 class="text-2xl font-bold">{{ unit.vocabulary ?? unit.word }}</h2>
          </div>
          <!-- Status buttons -->
          <div role="radiogroup" class="flex space-x-1">
            <button
              v-for="option in statusOptions"
              :key="option.value"
              :class="[
                'cursor-pointer px-2 py-1 font-semibold rounded-md transition-colors duration-150 focus:outline-none',
                status === option.value
                  ? selectedColors[option.value]
                  : unselectedColors[option.value],
              ]"
              role="radio"
              :aria-checked="status === option.value"
            >
              <template v-if="option.value === 'unknown'">
                <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                  <path :d="mdiHelpCircleOutline" />
                </svg>
              </template>
              <template v-else>
                {{ option.label }}
              </template>
            </button>
          </div>
        </div>

        <!-- Display aggregated senses if available, otherwise show a message -->
        <div v-if="aggregatedSenses.length" class="px-4 py-1">
          <SenseList :senses="aggregatedSenses" />
        </div>
        <div v-else class="px-4 py-1 text-gray-600 text-sm">
          <p>
            The word <strong>{{ unit.vocabulary ?? unit.word }}</strong> could not be found in the
            dictionary.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
