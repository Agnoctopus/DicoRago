import { ref, readonly } from 'vue'
import { defineStore } from 'pinia'
import type { Word } from '@/types'
import { getWordsFromWritten } from '@/api' // Ensure this function exists

/**
 * Dictionary Store
 *
 * This store manages dictionary words using localStorage as a cache.
 * It stores words in a mapping from a written form (string) to an array of Word objects.
 */
export const useDictionaryStore = defineStore('dictionary', () => {
  // Reactive object holding dictionary words, keyed by the written form.
  const dictionary = ref<Record<string, Word[]>>({})

  /**
   * Loads the dictionary from localStorage.
   */
  function loadLocal() {
    const stored = localStorage.getItem('dictionaryWords')
    if (stored) {
      try {
        dictionary.value = JSON.parse(stored)
      } catch (error) {
        console.error('Error parsing dictionary from localStorage:', error)
        dictionary.value = {}
      }
    }
  }

  /**
   * Saves the dictionary to localStorage.
   */
  function saveLocal() {
    localStorage.setItem('dictionaryWords', JSON.stringify(dictionary.value))
  }

  /**
   * Loads the dictionary from the local cache.
   */
  async function loadDictionary() {
    loadLocal()
  }

  /**
   * Adds or updates the words for a given written form.
   *
   * @param written - The unique written form of the word.
   * @param words - An array of Word objects associated with the written form.
   */
  function addWritten(written: string, words: Word[]): void {
    dictionary.value[written] = words
    saveLocal()
  }

  /**
   * Retrieves the words for a given written form.
   *
   * @param written - The written form to search for.
   * @returns An array of Word objects if found, or undefined if the written form has not been added.
   */
  function getWords(written: string): Word[] | undefined {
    const ret = dictionary.value[written]
    return ret
  }

  /**
   * Fetches the words from the server for a given written form
   * and adds them to the dictionary.
   *
   * @param written - The word form to fetch from the server.
   */
  async function syncWritten(written: string): Promise<void> {
    try {
      const words = await getWordsFromWritten(written, true)
      addWritten(written, words)
    } catch (error) {
      console.error(`Failed to sync dictionary for "${written}":`, error)
    }
  }

  // Automatically load the dictionary from localStorage when the store is created.
  loadLocal()

  return {
    dictionary: readonly(dictionary),
    loadDictionary,
    loadLocal,
    saveLocal,
    addWritten,
    getWords,
    syncWritten,
  }
})
