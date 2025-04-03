<script setup lang="ts">
import { ref } from 'vue'
import DemoAnalyzedText from './DemoAnalyzedText.vue'
import DemoUnitDetails from './DemoUnitDetails.vue'
import type { Unit } from '@/types'
import { sampleData } from '@/data/sample'

/* Sample data */
const units: Unit[] = sampleData.units
const text: string = sampleData.text
const vocabWords: Record<string, string> = sampleData.vocabWords
const vocab = sampleData.vocab

// Reactive state: currently selected unit and vocabulary list.
const selectedUnit = ref<Unit | null>(null)
const selectedStatus = ref<string>('undefined')

/**
 * Updates the selected unit from TextEditor.
 * @param unit - The chosen unit or null.
 */
const handleWordSelected = async (unit: Unit | null) => {
  selectedUnit.value = unit
  if (!unit || !unit.vocabulary) {
    selectedStatus.value = 'undefined'
  } else {
    selectedStatus.value = vocabWords[unit.vocabulary] ?? 'unknown'
  }
}
</script>

<template>
  <section class="bg-gray-50 overflow-hidden py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section principale compacte au-dessus -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">
          <span class="block">Learn Korean Through </span>
          <span class="block text-blue-600">Your Own Content</span>
        </h2>
        <p class="mt-3 max-w-xl mx-auto text-base text-gray-600">
          Quickly analyze any Korean text, discover new vocabulary, and boost your comprehension.
        </p>
      </div>

      <!-- Disposition en deux colonnes -->
      <div class="flex flex-col lg:flex-row items-center">
        <!-- Colonne explicative (40% sur desktop) -->
        <div class="lg:w-2/5 lg:pr-8 lg:border-r-2 border-gray-200">
          <h3 class="text-xl font-bold text-gray-800 mb-3">Start exploring!</h3>

          <!-- Répartition en deux colonnes en mode "sm" -->
          <div
            class="flex flex-col lg:flex-col sm:flex-row sm:justify-center sm:items-start lg:gap-0 sm:gap-6"
          >
            <!-- Première sous-colonne -->
            <div class="lg:w-full sm:w-1/2 text-center sm:text-left mb-2">
              <p class="text-base text-gray-600" style="text-align: justify">
                Dive into a Korean text with smart color-coding:
              </p>
              <ul
                class="mt-1 text-base text-gray-600 list-disc list-inside"
                style="text-align: justify"
              >
                <li><span class="word-zen known">Green</span>: Already known</li>
                <li><span class="word-zen unknown">Red</span>: Still to learn</li>
                <li><span class="word-zen seen">Orange</span>: Marked as seen</li>
                <li><span class="word-zen undefined">Gray</span>: Unrecognized</li>
              </ul>
            </div>
            <!-- Deuxième sous-colonne -->
            <div class="lg:w-full sm:w-1/2 text-center sm:text-left">
              <p class="text-base text-gray-600" style="text-align: justify">
                Click any word to see its <strong>meaning</strong>, <strong>grammar</strong> and
                <strong>examples</strong>. Easily add it to your own <strong>vocabulary</strong>.
              </p>
              <div class="mt-3">
                <router-link
                  to="/analyze"
                  class="w-full text-center inline-block px-6 py-3 text-lg font-semibold text-blue-600 border-blue-600 rounded border-2 hover:bg-blue-600 hover:text-white transition-colors duration-200"
                >
                  Try It Now
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Colonne de démo (60% sur desktop) -->
        <div class="lg:w-3/5 lg:pr-6 lg:pl-12 lg:mt-0 mt-4 flex items-center justify-center">
          <DemoAnalyzedText
            :units="units"
            :text="text"
            :vocabWords="vocabWords"
            @word-selected="handleWordSelected"
          />
        </div>
      </div>
      <!-- Display details of the selected unit -->
      <DemoUnitDetails
        v-if="selectedUnit"
        :unit="selectedUnit"
        :vocab="vocab"
        :status="selectedStatus"
        class="mt-4"
      />
    </div>
  </section>
</template>

<style src="@/assets/editor.css"></style>
<style scoped>
/* Affinez ici les styles spécifiques si besoin */
</style>
