<script setup lang="ts">
import { ref, onMounted, watch, nextTick, computed } from 'vue'
import { analyzeText } from '@/api'
import type { Unit, Analysis } from '@/types'
import { mdiPalette, mdiFilter, mdiCog } from '@mdi/js'
import { useVocabStore } from '@/stores/vocabulary'
import TextEditorSettings from '@/components/TextEditorSettings.vue'
import { useSettingsStore } from '@/stores/settings'

// Reference to the editable area and state for analyzed units.
const editor = ref<HTMLElement | null>(null)
const units = ref<Unit[]>([])

// Use the settings store for the "only unknown" toggle.
const settingsStore = useSettingsStore()

// Toggle states for coloring and vocabulary filtering.
const coloringEnabled = computed({
  get: () => settingsStore.coloringEnabled,
  set: (value: boolean) => settingsStore.setColoringEnabled(value),
})
const vocabularyEnabled = computed({
  get: () => settingsStore.vocabularyEnabled,
  set: (value: boolean) => settingsStore.setVocabularyEnabled(value),
})
const onlyUnknownColoring = computed({
  get: () => settingsStore.onlyUnknownColoring,
  set: (value: boolean) => settingsStore.setOnlyUnknownColoring(value),
})

// Controls the display of the settings panel.
const showSettings = ref(false)
const handleSettingsClose = async () => {
  showSettings.value = false
}

const isEditable = ref(true)
const isMobile = /Mobi|Android/i.test(navigator.userAgent)

// Access the vocabulary store.
const vocabStore = useVocabStore()

// Define events to emit to the parent component.
const emit = defineEmits<{
  (e: 'word-selected', unit: Unit | null): void
  (e: 'analysis-complete', analysis: Analysis): void
}>()

// Text length state and limit.
const textLength = ref(0)
const maxLength = 1000
const isTextTooLong = computed(() => textLength.value > maxLength)

// Update the text length based on the editor content.
function updateTextLength() {
  if (editor.value) {
    textLength.value = editor.value.innerText.length
  }
}

/**
 * Annotates the original text by wrapping each unit word with a <span>.
 * Applies classes based on the unit's status:
 * - 'known' if the word is learned.
 * - 'unknown' if not learned.
 * - 'undefined' if no vocabulary is defined.
 * In "only unknown" mode, only unknown words get colored.
 * Newlines are replaced with <br>.
 */
function annotateText(original: string, units: Unit[]): string {
  let result = ''
  let startIndex = 0
  units.forEach((unit, i) => {
    const pos = original.indexOf(unit.word, startIndex)
    if (pos === -1) {
      return
    }
    result += original.slice(startIndex, pos)
    let extraClass = ''
    if (coloringEnabled.value) {
      if (unit.vocabulary) {
        const known = vocabStore.isLearned(unit.vocabulary)
        if (onlyUnknownColoring.value) {
          if (!known) {
            extraClass = ' unknown'
          }
        } else {
          extraClass = known ? ' known' : ' unknown'
        }
      } else if (!onlyUnknownColoring.value) {
        extraClass = ' undefined'
      }
    }
    result += `<span data-index="${i}" class="word${extraClass}">${unit.word}</span>`
    startIndex = pos + unit.word.length
  })
  result += original.slice(startIndex)
  return result.replace(/\n/g, '<br>')
}

/**
 * Updates the coloring classes of annotated words.
 */
function updateColorize() {
  if (!editor.value) {
    return
  }
  const wordElements = editor.value.querySelectorAll('.word')
  wordElements.forEach((wordElement) => {
    const indexStr = wordElement.getAttribute('data-index')
    if (!indexStr) {
      return
    }
    const index = parseInt(indexStr, 10)
    const unit = units.value[index]
    wordElement.classList.remove('known', 'unknown', 'undefined')
    if (!coloringEnabled.value) {
      return
    }
    if (unit && unit.vocabulary) {
      const known = vocabStore.isLearned(unit.vocabulary)
      if (known) {
        if (!onlyUnknownColoring.value) {
          wordElement.classList.add('known')
        }
      } else {
        wordElement.classList.add('unknown')
      }
    } else if (!onlyUnknownColoring.value) {
      wordElement.classList.add('undefined')
    }
  })
}

/**
 * Renders the annotated text in the editor.
 */
const renderAnnotatedText = () => {
  if (editor.value) {
    const originalText = editor.value.innerText
    editor.value.innerHTML = annotateText(originalText, units.value)
  }
}

/**
 * Analyzes the current text via the API and emits the analysis result.
 * Will not analyze if the text exceeds the maximum allowed length.
 */
const analyzeCurrentText = async () => {
  if (!editor.value || !editor.value.innerText) {
    return
  }
  updateTextLength()
  if (isTextTooLong.value) {
    return
  }
  try {
    const analysis: Analysis = await analyzeText(editor.value.innerText)
    units.value = analysis.units
    renderAnnotatedText()
    emit('analysis-complete', analysis)
    if (isMobile) {
      isEditable.value = false
    }
  } catch (error) {
    console.error('Error analyzing text:', error)
  }
}

/**
 * Handles clicks on annotated words to toggle their selection.
 */
const handleClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (target && target.classList.contains('word')) {
    const currentlySelected = editor.value?.querySelector('.word.selected')
    if (currentlySelected && currentlySelected !== target) {
      currentlySelected.classList.remove('selected')
    }
    if (target.classList.contains('selected')) {
      target.classList.remove('selected')
      emit('word-selected', null)
    } else {
      target.classList.add('selected')
      const indexStr = target.getAttribute('data-index')
      if (indexStr) {
        const index = parseInt(indexStr, 10)
        const unit = units.value[index]
        emit('word-selected', unit)
      }
    }
  }
}

/**
 * Intercepts paste events to insert plain text only.
 */
const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault()
  const text = event.clipboardData?.getData('text/plain') || ''
  document.execCommand('insertText', false, text)
}

/**
 * Enables editing and focuses on the editable area.
 */
function enableEditing() {
  isEditable.value = true
  nextTick(() => {
    editor.value?.focus()
  })
}

// Set up event listeners when the component is mounted.
onMounted(() => {
  if (editor.value) {
    editor.value.addEventListener('click', handleClick)
    editor.value.addEventListener('paste', handlePaste)
    editor.value.addEventListener('input', updateTextLength)
  }
})

// Watch toggles and learned vocabulary to update word coloring.
watch(coloringEnabled, updateColorize)
watch(onlyUnknownColoring, updateColorize)
watch(
  () => vocabStore.learnedVocab,
  () => {
    if (coloringEnabled.value) {
      updateColorize()
    }
  },
  { deep: true },
)
</script>

<template>
  <div class="w-full max-w-2xl">
    <!-- Editable text area -->
    <div class="relative">
      <div
        ref="editor"
        :contenteditable="isEditable"
        :class="[
          'editor w-full max-w-2xl p-4 bg-white border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-2 text-xl overflow-y-auto',
          isTextTooLong
            ? 'ring-2 focus:ring-3 ring-red-400 focus:ring-red-400'
            : 'focus:ring-blue-400',
        ]"
        style="min-height: 250px; max-height: 400px"
      ></div>
      <!-- Mobile edit button -->
      <button
        v-if="isMobile && !isEditable"
        @click="enableEditing"
        class="absolute bottom-2 right-2 text-gray-600 cursor-pointer hover:bg-gray-200 font-medium py-1 px-2 rounded border border-gray-300 shadow text-sm"
      >
        Edit
      </button>
      <!-- Display text length if limit is exceeded -->
      <div
        v-if="isTextTooLong"
        class="absolute top-2 right-2 bg-white px-2 py-1 text-red-600 font-semibold border-3 border-red-600 rounded"
      >
        {{ textLength }}/{{ maxLength }}
      </div>
    </div>

    <!-- Toolbar with toggles and analysis button -->
    <div class="mt-2 bg-white flex items-center justify-between p-2 pl-4 rounded shadow">
      <!-- Left: Toggles for Coloring and Vocabulary -->
      <div class="flex sm:flex-row flex-col items-start gap-2 sm:gap-6">
        <!-- Coloring toggle -->
        <label for="toggle-coloring" class="flex items-center cursor-pointer">
          <input
            type="checkbox"
            id="toggle-coloring"
            v-model="coloringEnabled"
            class="form-checkbox h-5 w-5"
          />
          <svg class="ml-2" style="width: 1.25em; height: 1.25em" viewBox="0 0 24 24">
            <path :d="mdiPalette" fill="currentColor" />
          </svg>
          <span class="ml-1">Coloring</span>
        </label>
        <!-- Vocabulary filtering toggle -->
        <label for="toggle-vocabulary" class="flex items-center cursor-pointer">
          <input
            type="checkbox"
            id="toggle-vocabulary"
            v-model="vocabularyEnabled"
            class="form-checkbox h-5 w-5 text-blue-600"
          />
          <svg class="ml-2" style="width: 1.25em; height: 1.25em" viewBox="0 0 24 24">
            <path :d="mdiFilter" fill="currentColor" />
          </svg>
          <span class="ml-1">Vocabulary</span>
        </label>
      </div>
      <!-- Right: Gear icon and Analyze button -->
      <div class="flex items-center gap-4">
        <!-- Gear icon button -->
        <button
          @click="showSettings = !showSettings"
          class="flex items-center cursor-pointer focus:outline-none"
        >
          <svg style="width: 1.25em; height: 1.25em" viewBox="0 0 24 24">
            <path :d="mdiCog" fill="currentColor" />
          </svg>
        </button>
        <!-- Analyze text button -->
        <button
          @click="analyzeCurrentText"
          class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded shadow transition duration-200"
        >
          Analyze Text
        </button>
      </div>
      <!-- Settings panel -->
      <TextEditorSettings v-if="showSettings" @close="handleSettingsClose" />
    </div>
  </div>
</template>

<style>
.word {
  display: inline;
  box-shadow: 0 0 0 1px gray;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
  border-radius: 0.1rem;
  cursor: pointer;
  outline: 2px solid black;
  outline-offset: 3px;
  animation: borderFadeIn 0.5s;
  transition:
    background-color 0.25s ease,
    box-shadow 0.25s ease;
}

@keyframes borderFadeIn {
  from {
    box-shadow: 0 0 0 1px transparent;
    outline: 2px solid transparent;
  }
  to {
    box-shadow: 0 0 0 1px gray;
    outline: 2px solid black;
  }
}

.word:hover {
  background-color: #d0e0f0;
  box-shadow: 0 0 0 4px #50a0d0;
}

.word::selection {
  background: #70b0f0;
}

.word.selected {
  background-color: #ffd54f;
  box-shadow: 0 0 0 4px #ffa726;
}

.word.known {
  background-color: #c0ffc0;
}

.word.unknown {
  background-color: #ffc0c0;
}

.word.undefined {
  background-color: #e8e8e8;
}

.editor {
  word-spacing: 0.5em;
  line-height: 1.8em;
  text-align: justify;
  text-justify: inter-character;
  white-space: collapse;
}

.editor::selection {
  background: #a0c0d0;
}
</style>
