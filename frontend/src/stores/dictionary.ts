import { ref, readonly } from 'vue'
import { defineStore } from 'pinia'
import type { Word } from '@/types'
import { getWordsFromWritten } from '@/api' // Ensure this function accepts language as an argument
import { z } from 'zod'
import { wordSchema } from '@/schemas'

/**
 * Dictionary Schema: an object where each key is a written form,
 * and each value is an object mapping language (string) to an array of Word objects.
 */
const dictionarySchema = z.record(z.record(z.array(wordSchema)))

/**
 * Dictionary Store
 *
 * This store manages dictionary words using localStorage as a cache.
 * Words are stored in an object where the key is the written form, and for each form,
 * an object associates a language with an array of Word objects.
 */
export const useDictionaryStore = defineStore('dictionary', () => {
  // Dictionary: key = written form, value = an object { language: Word[] }
  const dictionary = ref<Record<string, Record<string, Word[]>>>({})

  /**
   * Loads the dictionary from localStorage.
   * Validates the format using Zod and resets the dictionary if invalid.
   */
  function loadLocal() {
    const stored = localStorage.getItem('dictionaryWords')
    if (stored) {
      try {
        const parsed = JSON.parse(stored)
        const validation = dictionarySchema.safeParse(parsed)
        if (!validation.success) {
          throw new Error('Invalid dictionary format')
        }
        dictionary.value = validation.data
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
   * Adds or updates words for a given written form and language.
   *
   * @param written - The unique written form.
   * @param language - The associated language.
   * @param words - An array of Word objects corresponding to the written form and language.
   */
  function addWritten(written: string, language: string, words: Word[]): void {
    if (!dictionary.value[written]) {
      dictionary.value[written] = {}
    }
    dictionary.value[written][language] = words
    saveLocal()
  }

  /**
   * Retrieves words for a given written form and language.
   *
   * @param written - The written form to search for.
   * @param language - The desired language.
   * @returns An array of Word objects if found, otherwise undefined.
   */
  function getWords(written: string, language: string): Word[] | undefined {
    return dictionary.value[written] ? dictionary.value[written][language] : undefined
  }

  /**
   * Fetches words from the server for a given written form and language,
   * then adds them to the dictionary.
   *
   * @param written - The written form to synchronize.
   * @param language - The language to use for fetching.
   */
  async function syncWritten(written: string, language: string): Promise<void> {
    try {
      const words = await getWordsFromWritten(written, true, language)
      addWritten(written, language, words)
    } catch (error) {
      console.error(`Failed to sync dictionary for "${written}" in ${language}:`, error)
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
