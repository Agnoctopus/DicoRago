import { readonly, ref } from 'vue'
import { defineStore } from 'pinia'
import {
  updateUserVocs,
  updateUserVoc,
  getVocSince,
  getVoc,
  getStatusVoc,
  clearUserVoc,
} from '@/api'
import { useUserStore } from '@/stores/user'
import { useDictionaryStore } from '@/stores/dictionary'
import { useSettingsStore } from '@/stores/settings'
import type { VocabWord, VocStatus, Word } from '@/types'
import { VocabWordArraySchema } from '@/schemas'
import { ZodError } from 'zod'

export const useVocabStore = defineStore('learned', () => {
  // Reactive array holding vocabulary words with their statuses.
  const vocabWords = ref<VocabWord[]>([])

  // Access other stores.
  const userStore = useUserStore()
  const dictionaryStore = useDictionaryStore()
  const settingsStore = useSettingsStore()

  // For offline mode, store the last sync timestamp (initialized to epoch).
  const lastSynced = ref<Date>(new Date(0))

  /**
   * Loads vocabulary from localStorage (offline mode).
   */
  function loadLocal() {
    const stored = localStorage.getItem('vocabWords')
    if (stored) {
      try {
        const parsedData = JSON.parse(stored)
        const validatedData = VocabWordArraySchema.parse(parsedData)
        vocabWords.value = validatedData
      } catch (error) {
        // Reset vocabWords
        vocabWords.value = []
        saveLocal()

        if (error instanceof ZodError || error instanceof Error) {
          console.error('Error loading learned vocabulary from localStorage:', error.message)
        } else {
          console.error('Error loading learned vocabulary from localStorage.')
        }
      }
    }
  }

  /**
   * Saves vocabulary to localStorage (offline mode).
   */
  function saveLocal() {
    localStorage.setItem('vocabWords', JSON.stringify(vocabWords.value))
  }

  /**
   * Loads vocabulary from the server if connected,
   * otherwise loads from localStorage.
   */
  async function loadVocabulary() {
    if (userStore.user) {
      try {
        const words: VocabWord[] = await getVoc()
        vocabWords.value = words
        const status = await getStatusVoc()
        lastSynced.value = status.last_update
      } catch (error) {
        console.error('Error loading vocabulary from server:', error)
      }
    } else {
      loadLocal()
    }
  }

  /**
   * Retrieves the status of a vocabulary word.
   *
   * @param vocab - The vocabulary word to check.
   * @returns The status of the word ('learned', 'seen', or 'unknown').
   */
  function getStatus(vocab: string): string {
    const word = vocabWords.value.find((item) => item.written === vocab)
    return word ? word.status : 'unknown'
  }

  /**
   * Sets the status of a vocabulary word.
   *
   * @param vocab - The vocabulary word to update.
   * @param newStatus - The new status ('learned', 'seen', or 'unknown').
   * @param words - Associated dictionary words.
   */
  async function setStatus(vocab: string, newStatus: string, words: Word[]) {
    const updated_at = new Date()
    const previousLastSynced = lastSynced.value

    // Check if the word already exists in the learned vocabulary.
    const index = vocabWords.value.findIndex((item) => item.written === vocab)
    if (index === -1) {
      // If not found and new status is 'unknown', do nothing.
      if (newStatus === 'unknown') {
        return
      }
      // Add the new word with its status.
      vocabWords.value.push({ written: vocab, updated_at, status: newStatus })
      dictionaryStore.addWritten(vocab, settingsStore.dictionaryLanguage, words)
    } else {
      // Word exists; update only if the status has changed.
      if (vocabWords.value[index].status !== newStatus) {
        if (newStatus === 'unknown') {
          // Remove the word if the new status is 'unknown'.
          vocabWords.value.splice(index, 1)
        } else {
          // Update the status and timestamp.
          vocabWords.value[index].status = newStatus
          vocabWords.value[index].updated_at = updated_at
        }
      }
    }

    // If offline, save changes locally.
    if (!userStore.user) {
      saveLocal()
      return
    }

    // In online mode, update the server.
    try {
      const status: VocStatus = await updateUserVoc(vocab, newStatus, updated_at)

      // If the server's last update timestamp differs from our previous sync,
      // fetch recent changes.
      if (status.last_update.getTime() !== previousLastSynced.getTime()) {
        const words: VocabWord[] = await getVocSince(previousLastSynced)
        words.forEach((serverWord) => {
          const idx = vocabWords.value.findIndex(
            (localWord) => localWord.written === serverWord.written,
          )
          if (idx !== -1) {
            // Update the local word if the server version is more recent.
            if (serverWord.updated_at.getTime() > vocabWords.value[idx].updated_at.getTime()) {
              vocabWords.value[idx].updated_at = serverWord.updated_at
              vocabWords.value[idx].status = serverWord.status

              // Remove the word locally if its status is 'unknown' on the server.
              if (serverWord.status === 'unknown') {
                vocabWords.value.splice(idx, 1)
              }
            }
          } else {
            // Add the word from the server if its status is not 'unknown'.
            if (serverWord.status !== 'unknown') {
              vocabWords.value.push(serverWord)
            }
          }
        })
      }
      // Update the in-memory sync timestamp.
      lastSynced.value = updated_at
    } catch (error) {
      console.error('Failed to update vocabulary on the server:', error)
    }
  }

  /**
   * Imports vocabulary from an array of written words.
   *
   * @param writtens - An array of written word strings.
   */
  async function importVocab(writtens: string[]) {
    const uniqueWrittens = Array.from(new Set(writtens))
    const newWrittens = uniqueWrittens.filter(
      (written) => !vocabWords.value.some((word) => word.written === written),
    )
    if (newWrittens.length === 0) {
      return
    }
    const now = new Date()
    const newWords = newWrittens.map((written) => ({
      written,
      updated_at: now,
      status: 'learned', // Default new words to 'learned'
    }))
    vocabWords.value.push(...newWords)

    if (userStore.user) {
      try {
        await updateUserVocs(
          newWords.map((word) => ({
            written: word.written,
            status: word.status,
            updated_at: word.updated_at,
          })),
        )
      } catch (error) {
        console.error('Error updating vocabulary on the server:', error)
      }
    } else {
      saveLocal()
    }
  }

  /**
   * Clears the entire vocabulary list.
   */
  async function clearVocabulary() {
    vocabWords.value = []
    if (userStore.user) {
      try {
        await clearUserVoc()
        lastSynced.value = new Date()
      } catch (error) {
        console.error('Failed to clear vocabulary on the server:', error)
      }
    } else {
      saveLocal()
    }
  }

  // Load vocabulary on store initialization.
  loadVocabulary()

  return {
    vocabWords: readonly(vocabWords),
    lastSynced: readonly(lastSynced),
    importVocab,
    getStatus,
    setStatus,
    loadVocabulary,
    clearVocabulary,
  }
})
