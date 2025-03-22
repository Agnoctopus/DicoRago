<script setup lang="ts">
import { ref, watch, nextTick, onMounted, computed } from 'vue'
import type { Unit } from '@/types'
import { useVocabStore } from '@/stores/vocabulary'
import { useSettingsStore } from '@/stores/settings'

// Define properties for the current component.
const props = defineProps<{ units: Unit[]; maxLength: number }>()

// Define events to emit to the parent component.
const emit = defineEmits<{
  (e: 'word-selected', unit: Unit | null): void
  (e: 'text-updated', text: string): void
}>()

// Reference to the editable area
const editor = ref<HTMLElement | null>(null)

// Access the vocabulary store.
const vocabStore = useVocabStore()

// Reactive variables
const isEditable = ref(true)
const isMobile = /Mobi|Android/i.test(navigator.userAgent)
const textLength = ref(0)
const isTextTooLong = computed(() => textLength.value > props.maxLength)

// Use the settings store for the "only unknown" toggle.
const settingsStore = useSettingsStore()

// Toggle states for coloring, vocabulary filtering and word style.
const coloringEnabled = computed({
  get: () => settingsStore.coloringEnabled,
  set: (value: boolean) => settingsStore.setColoringEnabled(value),
})
const onlyUnknownColoring = computed({
  get: () => settingsStore.onlyUnknownColoring,
  set: (value: boolean) => settingsStore.setOnlyUnknownColoring(value),
})
const annotationStyle = computed({
  get: () => settingsStore.annotationStyle,
  set: (value: string) => settingsStore.setAnnotationStyle(value),
})
const wordStyle = computed(() => `word-${annotationStyle.value}`)
const editorStyle = computed(() => `editor-${annotationStyle.value}`)

// Updated toward parent
const updateText = () => {
  if (editor.value) {
    emit('text-updated', editor.value.innerText)
    textLength.value = editor.value.innerText.length
  } else {
    textLength.value = 0
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

    result += `<span data-index="${i}" class="${wordStyle.value}${extraClass}">${unit.word}</span>`
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
  const wordElements = editor.value.querySelectorAll(`.${wordStyle.value}`)
  wordElements.forEach((wordElement) => {
    const indexStr = wordElement.getAttribute('data-index')
    if (!indexStr) {
      return
    }
    const index = parseInt(indexStr, 10)
    const unit = props.units[index]
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
    editor.value.innerHTML = annotateText(originalText, props.units)
    if (isMobile) {
      isEditable.value = false
    }
  }
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

onMounted(() => {
  editor.value?.addEventListener('input', updateText)
})

/**
 * Handles clicks on annotated words to toggle their selection.
 */
const handleClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (target && target.classList.contains(wordStyle.value)) {
    const currentlySelected = editor.value?.querySelector(`.${wordStyle.value}.selected`)
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
        const unit = props.units[index]
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

// Set up event listeners when the component is mounted.
onMounted(() => {
  if (editor.value) {
    editor.value.addEventListener('click', handleClick)
    editor.value.addEventListener('paste', handlePaste)
    editor.value.addEventListener('input', updateText)
  }
})

watch(() => props.units, renderAnnotatedText)
watch(coloringEnabled, updateColorize)
watch(onlyUnknownColoring, updateColorize)
watch(() => annotationStyle.value, renderAnnotatedText)

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
  <!-- Editable text area -->
  <div class="relative">
    <div
      ref="editor"
      :contenteditable="isEditable"
      :class="[
        editorStyle,
        'w-full max-w-2xl p-4 bg-white border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-2 text-xl overflow-y-auto',
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
</template>

<style src="@/assets/editor.css"></style>
