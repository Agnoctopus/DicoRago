<script setup lang="ts">
import { ref } from 'vue'
defineEmits<{ (e: 'close'): void }>()
import { mdiFileOutline } from '@mdi/js'
import { useVocabStore } from '@/stores/vocabulary'

// Access the vocabulary store.
const vocabStore = useVocabStore()

function exportAsJSON() {
  const vocabWords = vocabStore.vocabWords
  if (!vocabWords || vocabWords.length === 0) return

  // Build an object where each key is a 'written' value and its value is 1.
  const exportData = vocabWords.reduce<Record<string, number>>((acc, word) => {
    acc[word.written] = 1
    return acc
  }, {})

  const jsonString = JSON.stringify(exportData, null, 2)
  const blob = new Blob([jsonString], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'vocabulary.json'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function exportAsCSV() {
  const vocabWords = vocabStore.vocabWords

  // For each vocab word, output its written form and a constant "1"
  const rows = vocabWords.map((word) => `${word.written},1`).join('\n')
  const csvData = rows

  const blob = new Blob([csvData], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'vocabulary.csv'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// State to hold the imported file.
const importFile = ref<File | null>(null)

// Handle file selection.
function handleFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    importFile.value = target.files[0]
  }
}

function importVocabulary() {
  if (!importFile.value) return
  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target?.result
    let writtenArray: string[] = []

    if (importFile.value?.name.endsWith('.json')) {
      try {
        // Expect JSON format: { "written1": 1, "written2": 1, ... }
        const data = JSON.parse(text as string)
        if (data && typeof data === 'object') {
          writtenArray = Object.keys(data)
        } else {
          alert('Invalid JSON format.')
          return
        }
      } catch (error) {
        alert('Error importing JSON file.')
        console.error('Error importing JSON file:', error)
        return
      }
    } else if (importFile.value?.name.endsWith('.csv')) {
      try {
        // Expect CSV format with no header: each row is "written,1"
        const rows = (text as string).split('\n').filter((row) => row.trim() !== '')
        writtenArray = rows.map((row) => row.split(',')[0].trim()).filter((w) => w !== '')
      } catch (error) {
        alert('Error importing CSV file.')
        console.error('Error importing CSV file:', error)
        return
      }
    } else {
      alert('Unsupported file type. Please import a .json or .csv file.')
      return
    }

    // Call the store's importVocab function with the array of written words.
    vocabStore.importVocab(writtenArray)
    alert('Vocabulary imported successfully!')
    importFile.value = null
  }
  reader.readAsText(importFile.value)
}
</script>

<template>
  <!-- Fullscreen overlay with a blurred background -->
  <div
    class="fixed top-0 left-0 w-screen h-screen flex items-center justify-center backdrop-blur-sm z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white p-6 border border-gray-300 rounded-md shadow-lg w-11/12 max-w-md">
      <!-- Header: title and close button -->
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-xl font-bold m-0">Vocabulary Export / Import</h3>
        <button
          class="bg-transparent border-0 text-2xl leading-none cursor-pointer focus:outline-none"
          @click="$emit('close')"
        >
          ×
        </button>
      </div>
      <hr class="border-t border-gray-300 mb-4" />
      <div class="space-y-4">
        <!-- Export Section -->
        <div>
          <h4 class="text-lg font-semibold underline underline-offset-2">Export</h4>
          <div class="flex space-x-2 mt-1">
            <button
              @click="exportAsJSON"
              class="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors duration-200"
            >
              Export as JSON
            </button>
            <button
              @click="exportAsCSV"
              class="flex-1 px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700 transition-colors duration-200"
            >
              Export as CSV
            </button>
          </div>
        </div>
        <!-- Import Section -->
        <div>
          <div class="flex items-center justify-between">
            <h4 class="text-lg font-semibold underline underline-offset-2">Import</h4>
            <span v-if="importFile" class="text-sm text-gray-600">
              {{ importFile.name }}
            </span>
          </div>
          <div class="flex items-center mt-1 space-x-2">
            <label
              class="flex items-center justify-center px-2 h-10 w-10 bg-gray-200 rounded hover:bg-gray-300 transition-colors duration-200"
            >
              <svg class="w-6 h-6" viewBox="0 0 24 24">
                <path :d="mdiFileOutline" fill="currentColor" />
              </svg>
              <input type="file" @change="handleFileChange" accept=".json,.csv" class="hidden" />
            </label>
            <button
              @click="importVocabulary"
              :disabled="!importFile"
              class="flex-1 px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Import Vocabulary
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
