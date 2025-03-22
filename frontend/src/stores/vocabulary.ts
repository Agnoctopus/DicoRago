import { readonly, ref } from 'vue'
import { defineStore } from 'pinia'
import { updateUserVoc, getVocSince, getVoc, getStatusVoc, clearUserVoc } from '@/api'
import { useUserStore } from '@/stores/user'
import type { LearnedWord, VocStatus } from '@/types'

export const useVocabStore = defineStore('learned', () => {
  // Reactive array holding the learned vocabulary words.
  const learnedVocab = ref<LearnedWord[]>([])
  // Access the user store to check if the user is logged in.
  const userStore = useUserStore()

  // In offline mode, lastSynced is kept in memory (initialized to epoch).
  const lastSynced = ref<Date>(new Date(0))

  /**
   * Loads vocabulary from localStorage (used in offline mode).
   */
  function loadLocal() {
    const stored = localStorage.getItem('learnedVocabulary')
    if (stored) {
      try {
        learnedVocab.value = JSON.parse(stored)
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
        const words: LearnedWord[] = await getVoc()
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
  async function toggleLearned(vocab: string) {
    const updated_at = new Date()
    const previousLastSynced = lastSynced.value

    // Check if the word already exists; if it does, remove it (mark as not learned), otherwise add it.
    const index = learnedVocab.value.findIndex((item) => item.written === vocab)
    if (index === -1) {
      learnedVocab.value.push({ written: vocab, learned: true, updated_at })
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
          const words: LearnedWord[] = await getVocSince(previousLastSynced)
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
                learnedVocab.value.push(serverWord)
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
    isLearned,
    loadVocabulary,
    clearVocabulary,
  }
})
