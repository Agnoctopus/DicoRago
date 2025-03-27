<script setup lang="ts">
import { computed } from 'vue'
import type { Unit, Word, Sense } from '@/types'
import SenseList from '@/components/SenseList.vue'
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
        <!-- Header with title and learned checkbox -->
        <div class="flex items-center justify-between mb-4">
          <!-- Left: Vocabulary label -->
          <div class="flex-1 text-left">
            <h3 class="text-xl font-semibold">Vocabulary</h3>
          </div>
          <!-- Center: Display vocabulary word -->
          <div class="flex-1 text-center">
            <span class="text-2xl font-extrabold">{{ unit.vocabulary ?? unit.word }}</span>
          </div>
          <!-- Right: "Learned" checkbox -->
          <div class="flex-1 text-right">
            <label class="flex items-center justify-end space-x-2 cursor-pointer opacity-80">
              <input type="checkbox" disabled="true" class="form-checkbox h-4 w-4" />
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
            The word <strong>{{ unit.vocabulary ?? unit.word }}</strong> could not be found in the
            dictionary.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
