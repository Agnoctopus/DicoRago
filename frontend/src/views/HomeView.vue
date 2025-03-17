<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TextEditor from '@/components/TextEditor.vue'
import UnitDetails from '@/components/UnitDetails.vue'
import VocabularyList from '@/components/VocabularyList.vue'
import { useUserStore } from '@/stores/user'
import type { Unit, Word, Analysis } from '@/types'

// Reactive state: currently selected unit and vocabulary list.
const selectedUnit = ref<Unit | null>(null)
const vocab = ref<Word[]>([])

// Access the user store.
const userStore = useUserStore()

/**
 * Updates the selected unit from TextEditor.
 * @param unit - The chosen unit or null.
 */
const handleWordSelected = async (unit: Unit | null) => {
  selectedUnit.value = unit
}

/**
 * Updates the vocabulary list after analysis.
 * @param analysis - Analysis result containing vocabulary.
 */
const handleAnalysisComplete = (analysis: Analysis) => {
  vocab.value = analysis.vocab
}

// Fetch user data when the component mounts.
onMounted(async () => {
  await userStore.fetchUser()
})
</script>

<template>
  <div class="min-h-screen flex flex-col items-center p-4 bg-gray-50">
    <!-- App title -->
    <h1 class="text-4xl font-bold mt-2 mb-8 text-blue-600">DicoRago</h1>

    <!-- Text editing and analysis area -->
    <TextEditor @word-selected="handleWordSelected" @analysis-complete="handleAnalysisComplete" />

    <!-- Display details of the selected unit -->
    <UnitDetails v-if="selectedUnit" :unit="selectedUnit" :vocab="vocab" />

    <!-- Show vocabulary list if available -->
    <VocabularyList v-if="vocab.length" :vocab="vocab" />
  </div>
</template>
