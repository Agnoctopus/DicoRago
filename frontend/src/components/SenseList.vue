<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Sense, Example } from '@/types'
import { getExamples } from '@/api'
import SenseDetails from '@/components/SenseDetails.vue'

/**
 * Props:
 * - senses: All Sense to display.
 */
const props = defineProps<{ senses: Sense[] }>()

// Local state: currently selected sense and its examples.
const selectedSense = ref<Sense | null>(null)
const selectedExamples = ref<Example[]>([])

/**
 * Selects a sense and fetches its examples.
 * @param sense - Selected sense.
 * @param e - Click event.
 */
const selectSense = async (sense: Sense, e: Event) => {
  e.stopPropagation() // Prevent event propagation.
  selectedSense.value = sense
  try {
    const examples = await getExamples(sense.id)
    selectedExamples.value = examples
  } catch (error) {
    console.error('Error loading examples:', error)
  }
}

// Reset selection when the senses prop changes.
watch(
  () => props.senses,
  () => {
    selectedSense.value = null
    selectedExamples.value = []
  },
  { deep: true },
)
</script>

<template>
  <div>
    <!-- Sense selection list -->
    <div class="flex flex-wrap gap-2">
      <span
        v-for="sense in senses"
        :key="sense.id"
        @click="selectSense(sense, $event)"
        class="text-sm text-gray-600 cursor-pointer border border-gray-300 rounded px-1 hover:bg-gray-200"
        :class="{
          'font-bold': selectedSense && selectedSense.id === sense.id,
        }"
      >
        {{ sense.english_word }}
      </span>
    </div>
    <!-- Display selected sense details -->
    <div v-if="selectedSense">
      <SenseDetails :sense="selectedSense" :examples="selectedExamples" />
    </div>
  </div>
</template>
