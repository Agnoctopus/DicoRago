// stores/settings.ts
import { readonly, ref, watch } from 'vue'
import { defineStore } from 'pinia'

/**
 * Pinia store for managing app settings.
 * Settings are persisted to localStorage.
 */
export const useSettingsStore = defineStore('settings', () => {
  // Reactive state variables.
  const onlyUnknownColoring = ref(false)
  const coloringEnabled = ref(false)
  const vocabularyEnabled = ref(false)
  const dictionaryLanguage = ref('en_US')
  const annotationStyle = ref('box')

  /**
   * Loads settings from localStorage.
   */
  function loadSettings() {
    const stored = localStorage.getItem('settings')
    if (stored) {
      try {
        const data = JSON.parse(stored)
        onlyUnknownColoring.value = data.onlyUnknownColoring ?? false
        coloringEnabled.value = data.coloringEnabled ?? false
        vocabularyEnabled.value = data.vocabularyEnabled ?? false
        dictionaryLanguage.value = data.dictionaryLanguage ?? 'en_US'
        annotationStyle.value = data.annotationStyle ?? 'box'
      } catch (error) {
        console.error('Error loading settings:', error)
      }
    }
  }

  /**
   * Saves current settings to localStorage.
   */
  function saveSettings() {
    const data = {
      onlyUnknownColoring: onlyUnknownColoring.value,
      coloringEnabled: coloringEnabled.value,
      vocabularyEnabled: vocabularyEnabled.value,
      dictionaryLanguage: dictionaryLanguage.value,
      annotationStyle: annotationStyle.value,
    }
    localStorage.setItem('settings', JSON.stringify(data))
  }

  // Auto-save settings on change.
  watch(
    [onlyUnknownColoring, coloringEnabled, vocabularyEnabled, dictionaryLanguage],
    saveSettings,
    { deep: true },
  )

  // Initialize by loading saved settings.
  loadSettings()

  return {
    // Expose read-only state.
    onlyUnknownColoring: readonly(onlyUnknownColoring),
    coloringEnabled: readonly(coloringEnabled),
    vocabularyEnabled: readonly(vocabularyEnabled),
    dictionaryLanguage: readonly(dictionaryLanguage),
    annotationStyle: readonly(annotationStyle),
    // Setters to update settings.
    setOnlyUnknownColoring(value: boolean) {
      onlyUnknownColoring.value = value
    },
    setColoringEnabled(value: boolean) {
      coloringEnabled.value = value
    },
    setVocabularyEnabled(value: boolean) {
      vocabularyEnabled.value = value
    },
    setDictionaryLanguage(value: string) {
      dictionaryLanguage.value = value
    },
    setAnnotationStyle(value: string) {
      annotationStyle.value = value
    },
  }
})
