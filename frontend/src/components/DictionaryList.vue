<script setup lang="ts">
import { onMounted } from 'vue'
import DictionaryEntry from '@/components/DictionaryEntry.vue'
import { useVocabStore } from '@/stores/vocabulary'
import { useDictionaryStore } from '@/stores/dictionary'
import { useSettingsStore } from '@/stores/settings'
import type { VocabWord } from '@/types'

// Receive the vocab words as a prop.
const props = defineProps<{ vocabWords: VocabWord[] }>()

// Get the vocabulary, dictionary, and settings store instances.
const vocabStore = useVocabStore()
const dictionaryStore = useDictionaryStore()
const settingsStore = useSettingsStore()

// On component mount, retrieve vocab words that are not yet in the dictionary and sync them.
onMounted(async () => {
  const missingWrittens: string[] = []
  props.vocabWords.forEach((vocab) => {
    const words = dictionaryStore.getWords(vocab.written, settingsStore.dictionaryLanguage)
    if (!words) {
      missingWrittens.push(vocab.written)
    }
  })
  if (missingWrittens.length > 0) {
    await dictionaryStore.syncWrittens(missingWrittens, settingsStore.dictionaryLanguage)
  }
})

// Handle the removal of a vocabulary word.
function handleRemove(written: string) {
  vocabStore.setStatus(written, 'unknown', [])
}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto bg-white p-2 rounded shadow">
    <table class="w-full table-fixed border-collapse">
      <thead>
        <tr>
          <th class="px-4 py-1 text-left w-25">Word</th>
          <th class="px-4 py-1 text-left">Translations</th>
          <th class="px-4 py-1 w-10"></th>
        </tr>
      </thead>
      <tbody>
        <template v-if="props.vocabWords.length > 0">
          <DictionaryEntry
            v-for="(entry, index) in props.vocabWords"
            :key="index"
            :vocab="entry"
            @remove="handleRemove"
          />
        </template>
        <tr v-else>
          <td colspan="3" class="px-4 py-2 text-center text-gray-600">No matching word entry.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
