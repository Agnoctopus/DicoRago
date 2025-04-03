<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Unit } from '@/types'

const props = defineProps<{
  units: Unit[]
  text: string
  vocabWords: Record<string, string>
}>()

// Événement à émettre au parent.
const emit = defineEmits<{
  (e: 'word-selected', unit: Unit | null): void
}>()

// Référence à la zone annotée.
const editor = ref<HTMLElement | null>(null)

// États de coloration et styles.
const coloringEnabled = true
const onlyUnknownColoring = false
const annotationStyle = 'zen'
const wordStyle = `word-${annotationStyle}`
const editorStyle = `editor-${annotationStyle}`

/**
 * Transforme le texte original en ajoutant des balises <span>
 * autour de chaque mot (défini dans les unités).
 * La classe supplémentaire est ajoutée selon que le mot est connu
 * (vocabulary figure dans props.vocabWords), inconnu, ou indéfini.
 * Les retours à la ligne sont remplacés par des <br>.
 */
function annotateText(original: string, units: Unit[]): string {
  let result = ''
  let startIndex = 0
  units.forEach((unit, i) => {
    const pos = original.indexOf(unit.word, startIndex)
    if (pos === -1) return
    result += original.slice(startIndex, pos)
    let extraClass = ''
    if (coloringEnabled) {
      if (unit.vocabulary) {
        const status = props.vocabWords[unit.vocabulary] ?? 'unknown'

        if (onlyUnknownColoring) {
          if (status === 'unknown') extraClass = ' unknown'
        } else {
          if (status === 'learned') {
            extraClass = ' known'
          } else if (status === 'seen') {
            extraClass = ' seen'
          } else if (status === 'unknown') {
            extraClass = ' unknown'
          }
        }
      } else if (!onlyUnknownColoring) {
        extraClass = ' undefined'
      }
    }
    result += `<span data-index="${i}" class="${wordStyle}${extraClass}">${unit.word}</span>`
    startIndex = pos + unit.word.length
  })
  result += original.slice(startIndex)
  return result.replace(/\n/g, '<br>')
}

/**
 * Affiche le texte annoté dans l'éditeur.
 * Utilise props.text pour le texte original, ou un texte par défaut si vide.
 */
const renderAnnotatedText = () => {
  if (editor.value) {
    const originalText = props.text.trim()
    editor.value.innerHTML = annotateText(originalText, props.units)
  }
}

/**
 * Gère les clics sur les mots annotés pour activer/désactiver leur sélection.
 */
const handleClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (target && target.classList.contains(wordStyle)) {
    const currentlySelected = editor.value?.querySelector(`.${wordStyle}.selected`)
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

onMounted(() => {
  renderAnnotatedText()
  if (editor.value) {
    editor.value.addEventListener('click', handleClick)
  }
})
</script>

<template>
  <!-- Zone d'affichage annotée (lecture seule) -->
  <div class="relative">
    <div
      ref="editor"
      :contenteditable="false"
      :class="[
        editorStyle,
        'w-full max-w-2xl p-2 bg-transparent border-none focus:outline-none lg:text-2xl text-2xl overflow-y-auto focus:ring-blue-400',
      ]"
      style="cursor: default"
    ></div>
  </div>
</template>

<!-- Import des styles spécifiques pour l'éditeur -->
<style src="@/assets/editor.css"></style>
