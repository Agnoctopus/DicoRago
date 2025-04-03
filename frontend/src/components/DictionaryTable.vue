<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import DictionaryList from '@/components/DictionaryList.vue'
import DictionaryExportImport from '@/components/DictionaryExportImport.vue'
import { useVocabStore } from '@/stores/vocabulary'
import { mdiChevronLeft, mdiChevronRight, mdiExportVariant } from '@mdi/js'

// Get the vocabulary store instance.
const vocabStore = useVocabStore()

// State for search text and sort order.
const searchText = ref('')
const sortOrder = ref<'alphabetical' | 'date'>('date')

// Pagination settings.
const pageSize = 20
const currentPage = ref(1)

// Reactive state to filter vocabulary by status.
// By default, all three statuses are selected.
const selectedStatuses = ref<string[]>(['learned', 'seen', 'ignore'])

// Toggle a status filter: add it if not selected, remove it if already selected.
function toggleStatus(statusOption: string) {
  const index = selectedStatuses.value.indexOf(statusOption)
  if (index > -1) {
    selectedStatuses.value.splice(index, 1)
  } else {
    selectedStatuses.value.push(statusOption)
  }
}

// Define the status options.
const statusOptions = [
  { value: 'ignore', label: 'Ignore' },
  { value: 'seen', label: 'Seen' },
  { value: 'learned', label: 'Learned' },
]

// Colors for the selected state.
const selectedColors: Record<string, string> = {
  learned: 'bg-[#c0ffc0] text-green-800', // Pale green background for learned.
  seen: 'bg-[#ffe0a8] text-orange-900',
  ignore: 'bg-gray-300 text-black',
}

// Colors for the unselected state.
const unselectedColors: Record<string, string> = {
  learned: 'bg-white opacity-50 text-green-600 hover:bg-green-100',
  seen: 'bg-white opacity-50 text-orange-600 hover:bg-orange-100',
  ignore: 'bg-white opacity-50 text-gray-600 hover:bg-gray-100',
}

// Computed property that filters and sorts the vocabulary words.
const filteredVocabWords = computed(() => {
  let filtered = vocabStore.vocabWords.filter((word) =>
    word.written.toLowerCase().includes(searchText.value.toLowerCase()),
  )
  // Filter by selected statuses.
  filtered = filtered.filter((word) => selectedStatuses.value.includes(word.status))

  if (sortOrder.value === 'alphabetical') {
    filtered.sort((a, b) => a.written.localeCompare(b.written))
  } else if (sortOrder.value === 'date') {
    filtered.sort((a, b) => b.updated_at.getTime() - a.updated_at.getTime())
  }
  return filtered
})

// Compute total pages based on the filtered list.
const totalPages = computed(() => Math.ceil(filteredVocabWords.value.length / pageSize))

// Compute the paginated list of vocabulary items.
const paginatedVocabWords = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredVocabWords.value.slice(start, start + pageSize)
})

// When search text or sort order changes, reset current page to 1.
watch([searchText, sortOrder], () => {
  currentPage.value = 1
})

// State for showing modal overlay for export/import vocabulary.
const showExportImport = ref(false)
</script>

<template>
  <div>
    <!-- Top Control Bar: Always 2 rows -->
    <div class="w-full max-w-2xl mx-auto mb-2 p-2 bg-white rounded shadow space-y-2">
      <!-- Row 1: Search Input & Export Button -->
      <div class="w-full flex items-center justify-between space-x-2">
        <input
          v-model="searchText"
          type="text"
          placeholder="Search words..."
          class="border border-gray-800 p-2 rounded w-full h-10"
        />
        <button
          @click="showExportImport = true"
          class="flex items-center justify-center px-2 h-10 w-10 bg-gray-200 rounded hover:bg-gray-300"
        >
          <svg class="w-6 h-6" viewBox="0 0 24 24">
            <path :d="mdiExportVariant" fill="currentColor" />
          </svg>
        </button>
      </div>
      <!-- Row 2: Status Filters & Sort Order Select -->
      <div class="w-full flex items-center justify-between space-x-2">
        <!-- Status Filter Buttons -->
        <div class="flex space-x-1">
          <button
            v-for="option in statusOptions"
            :key="option.value"
            @click="toggleStatus(option.value)"
            :class="[
              'cursor-pointer p-2 font-semibold rounded-md transition-colors duration-150 focus:outline-none',
              selectedStatuses.includes(option.value)
                ? selectedColors[option.value]
                : unselectedColors[option.value],
            ]"
            role="checkbox"
            :aria-checked="selectedStatuses.includes(option.value)"
          >
            {{ option.label }}
          </button>
        </div>
        <!-- Sort Order Select -->
        <div class="w-full">
          <select v-model="sortOrder" class="border border-gray-800 p-2 rounded h-10 w-full">
            <option value="date">By Date</option>
            <option value="alphabetical">Alphabetical</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Dictionary List Component -->
    <DictionaryList :vocabWords="paginatedVocabWords" />

    <!-- Pagination Controls -->
    <div v-if="totalPages > 1" class="flex items-center mt-2 bg-white p-2 rounded shadow">
      <button
        @click="currentPage = Math.max(currentPage - 1, 1)"
        :disabled="currentPage === 1"
        class="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
      >
        <svg class="w-6 h-6" viewBox="0 0 24 24">
          <path :d="mdiChevronLeft" fill="currentColor" />
        </svg>
      </button>
      <span class="flex-grow text-center"> Page {{ currentPage }} of {{ totalPages }} </span>
      <button
        @click="currentPage = Math.min(currentPage + 1, totalPages)"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
      >
        <svg class="w-6 h-6" viewBox="0 0 24 24">
          <path :d="mdiChevronRight" fill="currentColor" />
        </svg>
      </button>
    </div>

    <!-- Modal Overlay for Export/Import Vocabulary -->
    <DictionaryExportImport v-if="showExportImport" @close="showExportImport = false" />
  </div>
</template>
