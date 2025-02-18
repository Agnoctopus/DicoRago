<script setup lang="ts">
import { computed } from 'vue'
import type { Example } from '@/types'

/**
 * Props:
 * - examples: All Example to display.
 */
const props = defineProps<{ examples: Example[] }>()

// Filter examples by category.
const fragmentExamples = computed(() => props.examples.filter((ex) => ex.category === 'fragment'))
const sentenceExamples = computed(() => props.examples.filter((ex) => ex.category === 'sentence'))
const conversationExamples = computed(() =>
  props.examples.filter((ex) => ex.category === 'conversation'),
)
</script>

<template>
  <div>
    <!-- Fragments Section -->
    <div v-if="fragmentExamples.length">
      <h4 class="text-sm font-semibold border-b pb-1 mb-2">Fragments</h4>
      <div class="grid grid-cols-2 sm:grid-cols-2 gap-1">
        <div
          v-for="(example, index) in fragmentExamples"
          :key="'frag-' + index"
          class="p-1 bg-white border rounded shadow-sm"
          :class="{
            'col-span-2':
              fragmentExamples.length % 2 !== 0 && index === fragmentExamples.length - 1,
          }"
        >
          <span class="text-gray-800">{{ example.example }}</span>
        </div>
      </div>
    </div>

    <!-- Sentences Section -->
    <div v-if="sentenceExamples.length" class="mt-4">
      <h4 class="text-sm font-semibold border-b pb-1 mb-2">Sentences</h4>
      <ul class="space-y-1">
        <li v-for="(example, index) in sentenceExamples" :key="'sentence-' + index">
          <div class="p-1 bg-white border rounded shadow-sm">
            <span class="text-gray-800">{{ example.example }}</span>
          </div>
        </li>
      </ul>
    </div>

    <!-- Conversations Section -->
    <div v-if="conversationExamples.length" class="mt-4">
      <h4 class="text-sm font-semibold border-b pb-1 mb-2">Conversations</h4>
      <ul class="space-y-1">
        <li v-for="(example, index) in conversationExamples" :key="'conv-' + index">
          <div class="p-1 bg-white border rounded shadow-sm border-l-4 border-gray-800">
            <!-- Split conversation lines on newline -->
            <div
              v-for="(line, lineIndex) in example.example.split('\n')"
              :key="lineIndex"
              class="whitespace-pre-line"
            >
              <!-- Alternate speaker labels -->
              <span class="font-bold text-gray-800 pr-2">
                {{ lineIndex % 2 === 0 ? '나' : '가' }}
              </span>
              <span class="ml-1 text-gray-800">{{ line }}</span>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
