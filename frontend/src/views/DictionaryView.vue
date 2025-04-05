<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import NavigationBar from '@/components/NavigationBar.vue'
import DictionaryList from '@/components/DictionaryList.vue'

import { searchWordsFromFragment } from '@/api'
import { useSettingsStore } from '@/stores/settings'
import { useVocabStore } from '@/stores/vocabulary'
import { useDictionaryStore } from '@/stores/dictionary'

import type { Word } from '@/types'

// Get the settings and vocabStore instance.
const settingsStore = useSettingsStore()
const vocabStore = useVocabStore()
const dictionaryStore = useDictionaryStore()

// Reactive variable to store the search query input by the user.
const searchQuery = ref('')

// Reactive array to store the search results returned from the API.
const searchResults = ref<Word[]>([])

// Reactive variable to indicate if the search is in progress.
const isLoading = ref(false)

// Debounce timeout reference.
let debounceTimeout: ReturnType<typeof setTimeout> | null = null

// Function to perform the search based on the input fragment.
const performSearch = async () => {
  if (searchQuery.value.trim()) {
    isLoading.value = true
    try {
      searchResults.value = await searchWordsFromFragment(
        searchQuery.value.trim(),
        true,
        settingsStore.dictionaryLanguage,
      )
    } catch (error) {
      console.error('Search error:', error)
      searchResults.value = []
    } finally {
      isLoading.value = false
    }
  } else {
    searchResults.value = []
  }
}

// Watch the searchQuery and perform the search with a debounce.
watch(searchQuery, () => {
  if (debounceTimeout) clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(() => {
    performSearch()
  }, 300) // 300ms debounce delay.
})

// Group searchResults into a record with key as the 'written' field.
const groupedSearchResults = computed<Record<string, Word[]>>(() => {
  return searchResults.value.reduce(
    (acc, word) => {
      if (!acc[word.written]) {
        acc[word.written] = []
      }
      acc[word.written].push(word)
      return acc
    },
    {} as Record<string, Word[]>,
  )
})

watch(groupedSearchResults, (grouped) => {
  Object.entries(grouped).forEach(([written, words]) => {
    dictionaryStore.addWritten(written, settingsStore.dictionaryLanguage, words)
  })
})

// Get unique written strings from the grouped search results.
const uniqueWrittens = computed(() => Object.keys(groupedSearchResults.value))

// Retrieve associated VocabWord objects using getAssociatedVocabWord from vocabStore.
const associatedVocabWords = computed(() => {
  const ret = vocabStore.getAssociatedVocabWords(uniqueWrittens.value)
  return ret
})

// Merge the grouped search results and associated VocabWord objects.
// Each entry contains the 'written' key, the array of Word objects, and the associated VocabWord.
//const vocabWordsData = computed(() => {})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <NavigationBar />
    <div class="container mx-auto py-4">
      <div class="w-full max-w-2xl mx-auto bg-white p-2 rounded shadow">
        <!-- Search Bar -->
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search words..."
            class="border border-gray-800 p-2 rounded w-full h-10"
          />
          <!-- Clear button appears when there's text in the search input -->
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-2 top-2 text-gray-500 hover:text-gray-700"
          >
            Clear
          </button>
        </div>
      </div>
      <div class="mt-2">
        <!-- Pass the computed vocabWordsData to DictionaryList -->
        <DictionaryList :vocabWords="associatedVocabWords" />
      </div>
    </div>
  </div>
</template>
