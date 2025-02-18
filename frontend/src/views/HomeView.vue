<script setup lang="ts">
import { ref } from 'vue'
import TextEditor from '@/components/TextEditor.vue'
import UnitDetails from '@/components/UnitDetails.vue'
import VocabularyList from '@/components/VocabularyList.vue'
import type { Unit, Word, Analysis } from '@/types'

// Reactive state variables
const selectedUnit = ref<Unit | null>(null) // Currently selected unit (word)
const vocab = ref<Word[]>([]) // Extracted vocabulary list
const filterVocabulary = ref(false) // State of the vocabulary filter toggle

/**
 * Handles the 'word-selected' event from TextEditor.
 * @param unit - Selected unit or null if deselected.
 */
const handleWordSelected = async (unit: Unit | null) => {
  selectedUnit.value = unit
}

/**
 * Handles the 'analysis-complete' event from TextEditor.
 * @param analysis - Analysis result.
 */
const handleAnalysisComplete = (analysis: Analysis) => {
  vocab.value = analysis.vocab
}

/**
 * Handles the 'vocabulary-toggle' event from TextEditor.
 * @param filter - New state of the vocabulary filter.
 */
const handleVocabularyToggle = (filter: boolean) => {
  filterVocabulary.value = filter
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center p-4">
    <!-- Title -->
    <h1 class="text-4xl font-bold mt-2 mb-8 text-blue-600">DicoRago</h1>

    <!-- Text editing and analysis area -->
    <TextEditor
      @word-selected="handleWordSelected"
      @analysis-complete="handleAnalysisComplete"
      @vocabulary-toggle="handleVocabularyToggle"
    />

    <!-- Display details of the selected unit -->
    <UnitDetails v-if="selectedUnit" :unit="selectedUnit" :vocab="vocab" />

    <!-- Display the extracted vocabulary list with boolean filter applied -->
    <VocabularyList v-if="vocab.length" :vocab="vocab" :filter="filterVocabulary" />
  </div>
</template>
