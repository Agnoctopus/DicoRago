import { readonly, ref } from 'vue'
import { defineStore } from 'pinia'

/**
 * Pinia store for managing learned vocabulary.
 */
export const useVocabStore = defineStore('learned', () => {
  // Reactive array holding learned vocabulary words.
  const learnedVocab = ref<string[]>([])

  /**
   * Loads learned vocabulary from localStorage.
   */
  function loadLearned() {
    const stored = localStorage.getItem('learnedVocabulary')
    if (stored) {
      try {
        learnedVocab.value = JSON.parse(stored)
      } catch (error) {
        // Reset if parsing fails.
        learnedVocab.value = []
        console.error('Error loading learned vocabulary:', error)
      }
    }
  }

  /**
   * Toggles the learned status of a vocabulary word.
   * @param vocab - Vocabulary word to toggle.
   */
  function toggleLearned(vocab: string) {
    if (learnedVocab.value.includes(vocab)) {
      learnedVocab.value = learnedVocab.value.filter((v) => v !== vocab)
    } else {
      learnedVocab.value.push(vocab)
    }
    localStorage.setItem('learnedVocabulary', JSON.stringify(learnedVocab.value))
  }

  /**
   * Checks if a vocabulary word is marked as learned.
   * @param vocab - Vocabulary word to check.
   * @returns True if the word is learned.
   */
  function isLearned(vocab: string): boolean {
    return learnedVocab.value.includes(vocab)
  }

  // Load learned vocabulary on store initialization.
  loadLearned()

  return { learnedVocab: readonly(learnedVocab), toggleLearned, isLearned }
})
