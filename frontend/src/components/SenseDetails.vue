<script setup lang="ts">
import type { Sense, Example } from '@/types'
import ExampleDetails from '@/components/ExampleDetails.vue'

/**
 * Props:
 * - sense: Sense to display.
 * - examples: Examples for the sense.
 */
defineProps<{
  sense: Sense
  examples: Example[]
}>()
</script>

<template>
  <div class="mt-3 p-4 bg-gray-100 rounded shadow-sm">
    <h4 class="text-sm font-semibold border-b pb-1 mb-2">Definition</h4>
    <p class="text-sm text-gray-700 mb-3">{{ sense.english_definition }}</p>
    <div v-if="examples.length">
      <ExampleDetails :examples="examples" />
    </div>
  </div>
</template>
