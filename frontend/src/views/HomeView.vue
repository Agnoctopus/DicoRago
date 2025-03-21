<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TextEditor from '@/components/TextEditor.vue'
import UnitDetails from '@/components/UnitDetails.vue'
import VocabularyList from '@/components/VocabularyList.vue'
import NavigationBar from '@/components/NavigationBar.vue'
import { useUserStore } from '@/stores/user'
import { useVocabStore } from '@/stores/vocabulary'

import type { Unit, Word, Analysis } from '@/types'

// Reactive state: currently selected unit and vocabulary list.
const selectedUnit = ref<Unit | null>(null)
const vocab = ref<Word[]>([])

// Access the vocab and user store.
const vocabStore = useVocabStore()
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
  if (!userStore.isFetched) {
    await userStore.fetchUser()
  }
  if (userStore.user) {
    await vocabStore.loadVocabulary()
  }
})
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Navigation Bar -->
    <NavigationBar />

    <!-- Main content area -->
    <div class="p-4 flex flex-col items-center">
      <!-- Text editing and analysis area -->
      <TextEditor @word-selected="handleWordSelected" @analysis-complete="handleAnalysisComplete" />

      <!-- Display details of the selected unit -->
      <UnitDetails v-if="selectedUnit" :unit="selectedUnit" :vocab="vocab" />

      <!-- Show vocabulary list if available -->
      <VocabularyList v-if="vocab.length" :vocab="vocab" />
    </div>
  </div>
</template>
