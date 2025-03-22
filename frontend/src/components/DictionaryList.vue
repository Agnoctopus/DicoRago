<script setup lang="ts">
import DictionaryEntry from '@/components/DictionaryEntry.vue'
import type { LearnedWord } from '@/types'

defineProps<{ learnedVocab: LearnedWord[] }>()
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
        <DictionaryEntry v-for="(entry, index) in learnedVocab" :key="index" :vocab="entry" />
      </tbody>
    </table>
  </div>
</template>
