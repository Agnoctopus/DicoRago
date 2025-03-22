<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import DictionaryList from '@/components/DictionaryList.vue'
import { useVocabStore } from '@/stores/vocabulary'
import type { LearnedWord } from '@/types'
import { mdiChevronLeft, mdiChevronRight } from '@mdi/js'

// Get the vocabulary store instance and cast learnedVocab.
const vocabStore = useVocabStore()
const learnedVocab = vocabStore.learnedVocab as LearnedWord[]

// State for search text and sort order.
const searchText = ref('')
const sortOrder = ref<'alphabetical' | 'date'>('date')

// Pagination settings.
const pageSize = 2
const currentPage = ref(1)

// Computed property that filters and sorts the learned vocabulary.
const filteredLearnedVocab = computed(() => {
  const filtered = learnedVocab.filter((word) =>
    word.written.toLowerCase().includes(searchText.value.toLowerCase()),
  )

  if (sortOrder.value === 'alphabetical') {
    filtered.sort((a, b) => a.written.localeCompare(b.written))
  } else if (sortOrder.value === 'date') {
    filtered.sort((a, b) => b.updated_at.getTime() - a.updated_at.getTime())
  }
  return filtered
})

// Compute total pages based on the filtered list.
const totalPages = computed(() => Math.ceil(filteredLearnedVocab.value.length / pageSize))

// Compute the paginated list of vocabulary items.
const paginatedLearnedVocab = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredLearnedVocab.value.slice(start, start + pageSize)
})

// When search text or sort order changes, reset current page to 1.
watch([searchText, sortOrder], () => {
  currentPage.value = 1
})
</script>

<template>
  <div>
    <!-- Search & Sort Bar -->
    <div class="flex items-center justify-between mb-2 p-2 bg-white rounded shadow">
      <input
        v-model="searchText"
        type="text"
        placeholder="Search words..."
        class="border border-gray-800 p-2 rounded w-full mr-2 h-10"
      />
      <select v-model="sortOrder" class="border border-gray-800 p-2 rounded h-10">
        <option value="date">By Date</option>
        <option value="alphabetical">Alphabetical</option>
      </select>
    </div>

    <!-- Dictionary List Component -->
    <DictionaryList :learnedVocab="paginatedLearnedVocab" />

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
  </div>
</template>
