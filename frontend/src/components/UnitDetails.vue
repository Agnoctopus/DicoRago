<script setup lang="ts">
import { computed } from 'vue'
import type { Unit, Word, Sense } from '@/types'
import SenseList from '@/components/SenseList.vue'
import { useVocabStore } from '@/stores/vocabulary'
import { tagMeanings } from '@/data/tag'

/**
 * Props:
 * - unit: Analyzed text unit to display.
 * - vocab: Vocabulary words.
 */
const props = defineProps<{
  unit: Unit
  vocab: Word[]
}>()

// Access the learned vocabulary store.
const learnedStore = useVocabStore()

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

// Computed property for the "Learned" checkbox.
const learned = computed({
  get() {
    return props.unit.vocabulary ? learnedStore.isLearned(props.unit.vocabulary) : false
  },
  set(value: boolean) {
    if (props.unit.vocabulary && value !== learnedStore.isLearned(props.unit.vocabulary)) {
      learnedStore.toggleLearned(props.unit.vocabulary, matchingWords.value)
    }
  },
})
</script>

<template>
  <!-- Vocabulary Section -->
  <div v-if="unit.vocabulary" class="w-full max-w-2xl mx-auto mt-6 bg-white p-4 rounded shadow">
    <!-- Header with title and learned checkbox -->
    <div class="flex items-center justify-between mb-4">
      <!-- Left: Vocabulary label -->
      <div class="flex-1 text-left">
        <h3 class="text-xl font-semibold">Vocabulary</h3>
      </div>
      <!-- Center: Display vocabulary word -->
      <div class="flex-1 text-center">
        <span class="text-2xl font-extrabold">{{ unit.vocabulary }}</span>
      </div>
      <!-- Right: "Learned" checkbox -->
      <div class="flex-1 text-right">
        <label class="flex items-center justify-end space-x-2 cursor-pointer">
          <input type="checkbox" v-model="learned" class="form-checkbox h-4 w-4" />
          <span class="text-sm">Learned</span>
        </label>
      </div>
    </div>

    <!-- Display aggregated senses if available, otherwise show a message -->
    <div v-if="aggregatedSenses.length" class="px-4 py-1">
      <SenseList :senses="aggregatedSenses" />
    </div>
    <div v-else class="px-4 py-1 text-gray-600 text-sm">
      <p>
        The word <strong>{{ unit.vocabulary }}</strong> could not be found in the dictionary.
      </p>
    </div>
  </div>

  <!-- Morphemes Section -->
  <div
    class="w-full max-w-2xl mx-auto bg-white p-4 rounded shadow"
    :class="unit.vocabulary && aggregatedSenses.length ? 'mt-2' : 'mt-6'"
  >
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
</template>
