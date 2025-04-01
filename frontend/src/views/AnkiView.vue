<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useVocabStore } from '@/stores/vocabulary'
import { useRouter } from 'vue-router'

// Déclaration globale pour typer window.anki
declare global {
  interface Window {
    anki?: {
      syncVocabulary: (vocabJson: string) => void
    }
  }
}

// Accès aux stores.
const userStore = useUserStore()
const vocabStore = useVocabStore()
const router = useRouter()

// Vérifie si la vue est exécutée depuis l'add-on Anki.
const inAnki = ref(false)
onMounted(() => {
  inAnki.value = !!window.anki
})

// Fonction de déconnexion : redirige vers l'endpoint de logout.
function signOut() {
  window.location.href = '/api/auth/logout/anki'
}

// Fonction de synchronisation du vocabulaire.
function syncVocabulary() {
  if (!inAnki.value) {
    alert(
      'Sync is only available when running from the Anki add-on. Please use the Anki sync feature.',
    )
    return
  }
  const words = vocabStore.learnedVocab.map((word) => word.written)
  if (window.anki && typeof window.anki.syncVocabulary === 'function') {
    // Envoie la liste des mots sous forme de chaîne JSON.
    window.anki.syncVocabulary(JSON.stringify(words))
  } else {
    console.error('anki.syncVocabulary is not available.')
  }
}

// Récupère les données utilisateur et vocabulaire au montage.
onMounted(async () => {
  if (!userStore.isFetched) {
    await userStore.fetchUser()
    if (!userStore.user) {
      // Si l'utilisateur n'est pas authentifié et que nous sommes dans Anki, redirige vers la vue de login.
      if (inAnki.value) {
        router.push({ name: 'AnkiLoginView' })
      }
      return
    }
    await vocabStore.loadVocabulary()
  }
})
</script>

<template>
  <!-- Outer container sans padding externe afin que le bg s'étende sur toute la fenêtre -->
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-indigo-600 p-4"
  >
    <div class="max-w-3xl mx-auto px-4 py-8">
      <!-- Avertissement si l'add-on n'est pas détecté -->
      <div v-if="!inAnki" class="mb-8">
        <div class="bg-white rounded-lg shadow-lg p-8 max-w-md mx-auto">
          <div class="flex flex-col items-center mb-6">
            <img
              src="@/assets/icon.png"
              alt="App Logo"
              class="w-48 h-48 rounded-full border-2 shadow-lg mb-4"
            />
            <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">Welcome to Dicorago</h2>
            <p class="text-gray-600 text-center">
              This view is not running from within the Anki add-on.
              <br />
              Login and sync features are available only when accessed from Anki.
            </p>
          </div>
        </div>
      </div>

      <!-- Contenu principal lorsque l'utilisateur est authentifié et l'add-on est détecté -->
      <div v-if="userStore.user && inAnki">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Your Vocabulary</h1>
          <div class="flex items-center space-x-4 mt-4 sm:mt-0">
            <span class="text-gray-700">
              Hello, <strong>{{ userStore.user.name }}</strong>
            </span>
            <button
              @click="signOut"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors duration-200"
            >
              Sign Out
            </button>
          </div>
        </div>
        <!-- Section affichant le nombre de mots appris et le bouton de synchronisation -->
        <div class="mb-8">
          <p class="text-lg text-gray-700 mb-4">
            You have <strong>{{ vocabStore.learnedVocab.length }}</strong> learned word<span
              v-if="vocabStore.learnedVocab.length !== 1"
              >s</span
            >.
          </p>
          <button
            @click="syncVocabulary"
            class="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            Sync Vocabulary
          </button>
        </div>
        <!-- D'autres contenus, comme la liste détaillée du vocabulaire, peuvent être ajoutés ici -->
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Ajoutez ici des styles personnalisés supplémentaires si nécessaire */
</style>
