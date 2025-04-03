<script setup lang="ts">
import { computed } from 'vue'
import type { Unit, Word, Sense } from '@/types'
import SenseList from '@/components/SenseList.vue'
import { useVocabStore } from '@/stores/vocabulary'
import { tagMeanings } from '@/data/tag'
import { mdiHelpCircleOutline } from '@mdi/js'

/**
 * Props:
 * - unit: An analyzed text unit to display.
 * - vocab: Vocabulary words.
 */
const props = defineProps<{
  unit: Unit
  vocab: Word[]
}>()

// Access the vocabulary store.
const vocabStore = useVocabStore()

// Returns words matching the unit's vocabulary property.
const matchingWords = computed(() =>
  props.unit.vocabulary ? props.vocab.filter((word) => word.written === props.unit.vocabulary) : [],
)

// Aggregates senses from matching words into an array.
const aggregatedSenses = computed(() => {
  const senses: Sense[] = []
  matchingWords.value.forEach((word) => word.senses.forEach((sense) => senses.push(sense)))
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
  learned: 'bg-[#c0ffc0] text-green-800',
  seen: 'bg-[#ffe0a8] text-orange-900',
  unknown: 'bg-red-100 text-red-400 hover:bg-red-100',
  ignore: 'bg-gray-300 text-black',
}

// Colors for the unselected state (no borders, just colored text with subtle hover).
const unselectedColors: Record<string, string> = {
  learned: 'bg-white opacity-50 text-green-600 hover:bg-green-100',
  seen: 'bg-white opacity-50 text-orange-600 hover:bg-orange-100',
  unknown: 'bg-white opacity-50 text-red-400 hover:bg-red-100',
  ignore: 'bg-white opacity-50 text-gray-600 hover:bg-gray-100',
}

// Computed property for the vocabulary status.
const status = computed({
  get() {
    return props.unit.vocabulary ? vocabStore.getStatus(props.unit.vocabulary) : 'unknown'
  },
  set(value: string) {
    if (props.unit.vocabulary && value !== vocabStore.getStatus(props.unit.vocabulary)) {
      // Update the status in the store, passing the matching words if needed.
      vocabStore.setStatus(props.unit.vocabulary, value, matchingWords.value)
    }
  },
})
</script>

<template>
  <div v-if="unit.vocabulary" class="w-full max-w-2xl mx-auto mt-4 bg-white p-4 rounded shadow">
    <div class="flex items-center justify-between mb-4">
      <!-- Vocabulary word inside a styled container -->
      <div class="px-2 py-1 border border-gray-300 rounded-md bg-gray-50">
        <h2 class="text-2xl font-bold">{{ unit.vocabulary }}</h2>
      </div>
      <!-- Status buttons -->
      <div role="radiogroup" class="flex space-x-1">
        <button
          v-for="option in statusOptions"
          :key="option.value"
          @click="status = option.value"
          :class="[
            'cursor-pointer px-2 py-1 font-semibold rounded-md transition-colors duration-150 focus:outline-none',
            status === option.value ? selectedColors[option.value] : unselectedColors[option.value],
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

    <!-- Aggregated Senses Section -->
    <section>
      <div v-if="aggregatedSenses.length" class="px-2 py-2">
        <SenseList :senses="aggregatedSenses" />
      </div>
      <div v-else class="px-2 py-2 text-gray-600 text-sm">
        <p>
          The word <strong>{{ unit.vocabulary }}</strong> could not be found in the dictionary.
        </p>
      </div>
    </section>
  </div>

  <!-- Morphemes Section -->
  <div class="w-full max-w-2xl mx-auto bg-white p-4 rounded shadow mt-2">
    <h3 class="text-lg font-semibold mb-4">Morphemes</h3>
    <div class="flex flex-wrap gap-2 px-2 py-1">
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
</template>
