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
import type { ServerLearnedWord, LearnedWord, VocStatus, Word } from '@/types'
import { learnedWordArraySchema } from '@/schemas'

export function convertServerLearnedWord(serverWord: ServerLearnedWord): LearnedWord {
  return {
    written: serverWord.written,
    updated_at: serverWord.updated_at,
  }
}

export function convertServerLearnedWords(serverWords: ServerLearnedWord[]): LearnedWord[] {
  return serverWords.map(convertServerLearnedWord)
}

export const useVocabStore = defineStore('learned', () => {
  // Reactive array holding the learned vocabulary words.
  const learnedVocab = ref<LearnedWord[]>([])
  // Access the user, dictionary and settings store
  const userStore = useUserStore()
  const dictionaryStore = useDictionaryStore()
  const settingsStore = useSettingsStore()

  // In offline mode, lastSynced is kept in memory (initialized to epoch).
  const lastSynced = ref<Date>(new Date(0))

  /**
   * Loads vocabulary from localStorage (used in offline mode).
   */
  function loadLocal() {
    const stored = localStorage.getItem('learnedVocabulary')
    if (stored) {
      try {
        const parsedData = JSON.parse(stored)
        const validatedData = learnedWordArraySchema.parse(parsedData)
        learnedVocab.value = validatedData
      } catch (error) {
        learnedVocab.value = []
        console.error('Error loading learned vocabulary from localStorage:', error)
      }
    }
  }

  /**
   * Saves vocabulary to localStorage (used in offline mode).
   */
  function saveLocal() {
    localStorage.setItem('learnedVocabulary', JSON.stringify(learnedVocab.value))
  }

  /**
   * Loads vocabulary:
   * - If the user is connected, it is loaded via the API (getVoc()) and lastSynced is updated from the server status.
   * - Otherwise, the vocabulary is loaded from localStorage.
   */
  async function loadVocabulary() {
    if (userStore.user) {
      try {
        const words: LearnedWord[] = convertServerLearnedWords(await getVoc())
        learnedVocab.value = words
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
   * Toggles the learned status of a vocabulary word.
   * In connected mode, the update is sent via the API and recent changes are synchronized with getVocSince().
   * In offline mode, the change is saved to localStorage.
   *
   * @param vocab - The vocabulary word to toggle.
   */
  async function toggleLearned(vocab: string, words: Word[]) {
    const updated_at = new Date()
    const previousLastSynced = lastSynced.value

    // Check if the word already exists; if it does, remove it (mark as not learned), otherwise add it.
    const index = learnedVocab.value.findIndex((item) => item.written === vocab)
    if (index === -1) {
      learnedVocab.value.push({ written: vocab, updated_at })
      dictionaryStore.addWritten(vocab, settingsStore.dictionaryLanguage, words)
    } else {
      learnedVocab.value.splice(index, 1)
    }

    if (userStore.user) {
      // Connected mode: update the server.
      try {
        const newStatus = index === -1
        const status: VocStatus = await updateUserVoc(vocab, newStatus, updated_at)
        // If the server's last update timestamp differs from our previous sync, fetch recent changes.
        if (status.last_update.getTime() !== previousLastSynced.getTime()) {
          const words: ServerLearnedWord[] = await getVocSince(previousLastSynced)
          words.forEach((serverWord) => {
            const idx = learnedVocab.value.findIndex(
              (localWord) => localWord.written === serverWord.written,
            )
            if (idx !== -1) {
              // Update the local word if the server version is more recent.
              if (serverWord.updated_at.getTime() > learnedVocab.value[idx].updated_at.getTime()) {
                learnedVocab.value[idx].updated_at = serverWord.updated_at
                // Remove the word locally if it is no longer learned on the server.
                if (!serverWord.learned) {
                  learnedVocab.value.splice(idx, 1)
                }
              }
            } else {
              // If the word is not in the local list and is learned on the server, add it.
              if (serverWord.learned) {
                learnedVocab.value.push(convertServerLearnedWord(serverWord))
              }
            }
          })
        }
        // Update the in-memory sync timestamp.
        lastSynced.value = updated_at
      } catch (error) {
        console.error('Failed to update vocabulary on the server:', error)
      }
    } else {
      // Offline mode: save the updated vocabulary to localStorage.
      saveLocal()
    }
  }

  /**
   * Imports vocabulary from an array of written words.
   * Filters the provided list to retain unique writtens, then adds them
   * to the learned vocabulary if they do not already exist.
   * Finally, calls updateUserVocs with the newly imported words.
   *
   * @param writtens - An array of written word strings.
   */
  async function importVocab(writtens: string[]) {
    // Filter for unique written values.
    const uniqueWrittens = Array.from(new Set(writtens))
    // Filter out those that already exist in the learned vocabulary.
    const newWrittens = uniqueWrittens.filter(
      (written) => !learnedVocab.value.some((word) => word.written === written),
    )
    if (newWrittens.length === 0) {
      return
    }
    const now = new Date()
    // Create new LearnedWord objects.
    const newWords = newWrittens.map((written) => ({
      written,
      updated_at: now,
    }))
    // Append new words to the learned vocabulary.
    learnedVocab.value.push(...newWords)

    // Update the server with the new vocabulary.
    if (userStore.user) {
      try {
        await updateUserVocs(
          newWords.map((word) => ({
            written: word.written,
            learned: true,
            updated_at: word.updated_at,
          })),
        )
      } catch (error) {
        console.error('Error updating vocabulary on the server:', error)
      }
    } else {
      // Persist the changes locally.
      saveLocal()
    }
  }

  /**
   * Checks if a vocabulary word is learned.
   *
   * @param vocab - The vocabulary word to check.
   * @returns True if the word is present in the learned vocabulary.
   */
  function isLearned(vocab: string): boolean {
    return learnedVocab.value.some((item) => item.written === vocab)
  }

  /**
   * Clears the vocabulary list.
   */
  async function clearVocabulary() {
    learnedVocab.value = []
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

  // Initial load of the vocabulary.
  loadVocabulary()

  return {
    learnedVocab: readonly(learnedVocab),
    lastSynced: readonly(lastSynced),
    toggleLearned,
    importVocab,
    isLearned,
    loadVocabulary,
    clearVocabulary,
  }
})
