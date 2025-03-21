<script setup lang="ts">
import { ref, computed } from 'vue'
import { analyzeText } from '@/api'
import type { Unit, Analysis } from '@/types'
import TextEditorSettings from '@/components/TextEditorSettings.vue'
import TextEditorControls from '@/components/TextEditorControls.vue'
import TextEditorText from '@/components/TextEditorText.vue'
import { useSettingsStore } from '@/stores/settings'

// Reference to state for analyzed units.
const units = ref<Unit[]>([])
const text = ref('')

// Access settings store.
const settingsStore = useSettingsStore()

// Controls the display of the settings panel.
const showSettings = ref(false)
const handleSettingsClose = async () => {
  showSettings.value = false
}

// Define events to emit to the parent component.
const emit = defineEmits<{
  (e: 'word-selected', unit: Unit | null): void
  (e: 'analysis-complete', analysis: Analysis): void
}>()

// Text length state and limit.
const textLength = ref(0)
const maxLength = 1000
const isTextTooLong = computed(() => textLength.value > maxLength)

/**
 * Analyzes the current text via the API and emits the analysis result.
 * Will not analyze if the text exceeds the maximum allowed length.
 */
const analyzeCurrentText = async () => {
  if (!text.value || isTextTooLong.value) {
    return
  }
  try {
    const analysis: Analysis = await analyzeText(text.value, settingsStore.dictionaryLanguage)
    units.value = analysis.units
    emit('analysis-complete', analysis)
  } catch (error) {
    console.error('Error analyzing text:', error)
  }
}

// Mise à jour du texte
const updateText = (updated_text: string) => {
  text.value = updated_text
  if (updated_text) textLength.value = updated_text.length
  else textLength.value = 0
}

/**
 * Updates the selected unit from TextEditor.
 * @param unit - The chosen unit or null.
 */
const handleWordSelected = async (unit: Unit | null) => {
  emit('word-selected', unit)
}
</script>

<template>
  <div class="w-full max-w-2xl">
    <TextEditorText
      :maxLength="maxLength"
      @word-selected="handleWordSelected"
      @text-updated="updateText"
      :units="units"
    />

    <TextEditorControls
      :isTextTooLong="isTextTooLong"
      @analyze="analyzeCurrentText"
      @toggle-settings="showSettings = !showSettings"
    />

    <!-- Toolbar with toggles and analysis button -->
    <TextEditorSettings v-if="showSettings" @close="handleSettingsClose" />
  </div>
</template>
