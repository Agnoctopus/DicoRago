<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useDictionaryStore } from '@/stores/dictionary'
import { useSettingsStore } from '@/stores/settings'
import type { LearnedWord, Word, Sense } from '@/types'
import SenseList from '@/components/SenseList.vue'
import { mdiTrashCan } from '@mdi/js'

/**
 * Component props:
 * - vocab: A LearnedWord object containing the written word and its update timestamp.
 */
const props = defineProps<{ vocab: LearnedWord }>()

// Define emits to notify parent for removal of a vocabulary word.
const emit = defineEmits<{ (e: 'remove', written: string): void }>()

// Get the dictionary and settings store instance.
const dictionaryStore = useDictionaryStore()
const settingsStore = useSettingsStore()

// On component mount, if the words for the given written form are not loaded, sync them from the server.
onMounted(async () => {
  if (!dictionaryStore.getWords(props.vocab.written, settingsStore.dictionaryLanguage)) {
    await dictionaryStore.syncWritten(props.vocab.written, settingsStore.dictionaryLanguage)
  }
})

// Watch for changes in props.vocab; if its words are not loaded, sync from the server.
watch(
  () => props.vocab,
  async (newVocab) => {
    if (newVocab && !dictionaryStore.getWords(newVocab.written, settingsStore.dictionaryLanguage)) {
      await dictionaryStore.syncWritten(newVocab.written, settingsStore.dictionaryLanguage)
    }
    isExpanded.value = false
  },
)

/**
 * Computed property to get the associated Word objects from the dictionary store
 * that match the learned word's written form. If none are found, returns an empty array.
 */
const associatedWords = computed<Word[]>(() => {
  console.log(settingsStore.dictionaryLanguage);
  return dictionaryStore.getWords(props.vocab.written, settingsStore.dictionaryLanguage) || []
})

/**
 * Computes a comma-separated string of unique translations
 * from all senses of the associated words.
 */
const translatedSensesText = computed(() => {
  const translations = new Set<string>()
  associatedWords.value.forEach((word: Word) => {
    word.senses.forEach((sense: Sense) => {
      translations.add(sense.translation)
    })
  })
  return Array.from(translations).join(', ')
})

/**
 * Aggregates all senses from the associated words into an array.
 */
const aggregatedSenses = computed(() => {
  const senses: Sense[] = []
  associatedWords.value.forEach((word: Word) => {
    word.senses.forEach((sense: Sense) => senses.push(sense))
  })
  return senses
})

// Toggle state for expanding/collapsing the word senses.
const isExpanded = ref(false)
const toggle = () => {
  isExpanded.value = !isExpanded.value
}

// Remove function: emits the remove event for this learned word.
function removeWord(e: Event) {
  e.stopPropagation()
  emit('remove', props.vocab.written)
}
</script>

<template>
  <!-- Main row: displays the word and a summary of its senses translations -->
  <tr
    @click="toggle"
    class="transition-all duration-300 hover:bg-gray-50 cursor-pointer select-none"
  >
    <td class="px-4 py-1 font-extrabold whitespace-nowrap">
      <span class="select-text font-extrabold">{{ vocab.written }}</span>
    </td>
    <td class="px-4 py-1 truncate">{{ translatedSensesText }}</td>
    <td class="px-4 py-1 text-right">
      <svg
        :class="{ 'transform rotate-180': isExpanded }"
        class="w-5 h-5 text-blue-500 transition-transform duration-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M19 9l-7 7-7-7" />
      </svg>
    </td>
  </tr>

  <!-- Expanded row: shows the learned date, remove button, and detailed list of senses -->
  <tr v-if="isExpanded">
    <td></td>
    <td colspan="2" class="px-4 py-2 border-t">
      <div class="flex items-center justify-start mb-2">
        <!-- Trashcan button to remove the word -->
        <button @click.stop="removeWord" class="cursor-pointer">
          <svg class="w-5 h-5 text-red-500" viewBox="0 0 24 24">
            <path :d="mdiTrashCan" />
          </svg>
        </button>
        <span class="ml-2 text-sm text-gray-600">
          Learned on:
          {{
            new Date(props.vocab.updated_at).toLocaleString(undefined, {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            })
          }}
        </span>
      </div>
      <SenseList :senses="aggregatedSenses" />
    </td>
  </tr>
</template>
