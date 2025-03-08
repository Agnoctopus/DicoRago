<script setup lang="ts">
import { computed, defineEmits, onMounted } from 'vue'
import ToggleSwitch from '@/components/ToggleSwitch.vue'
import { mdiPalette } from '@mdi/js'
import { useSettingsStore } from '@/stores/settings'
import { loginWithGoogle, loginWithApple } from '@/api'

// Émission de l'événement 'close' pour fermer le panneau de paramètres.
defineEmits<{ (e: 'close'): void }>()

const settingsStore = useSettingsStore()

// Proxy computé pour onlyUnknownColoring depuis le store.
const onlyUnknown = computed({
  get: () => settingsStore.onlyUnknownColoring,
  set: (value: boolean) => settingsStore.setOnlyUnknownColoring(value),
})

// Fonction déclenchée lors du clic sur le bouton Google personnalisé.
// En mode redirect, appeler prompt() déclenchera une redirection complète.
function handleGoogleSignIn() {
  if (window.google && window.google.accounts) {
    window.google.accounts.id.prompt()
  }
}

// Fonction déclenchée lors du clic sur le bouton Apple personnalisé.
// En mode redirect (usePopup: false), l'appel à signIn() redirige l'utilisateur.
function handleAppleSignIn() {
  if (window.AppleID && window.AppleID.auth) {
    AppleID.auth.signIn()
  }
}

onMounted(() => {
  // Initialisation du SDK Google en mode redirect.
  if (window.google && window.google.accounts) {
    window.google.accounts.id.initialize({
      client_id: '738555358973-8t65bo2j79olfbr86l84m7fhr6ckob7v.apps.googleusercontent.com',
      ux_mode: 'redirect', // Utilisation du mode redirect (sans popup)
      redirect_uri: 'https://dicorago.com/auth/google', // Votre URI de redirection pour Google
    })
  }
  // Initialisation du SDK Apple pour le flux en mode redirect.
  if (window.AppleID && window.AppleID.auth) {
    AppleID.auth.init({
      clientId: 'com.DicoRago.webapp',
      scope: 'name email',
      redirectURI: 'https://dicorago.com/auth/apple', // Votre URI de redirection pour Apple
      usePopup: false, // Désactive la popup ; redirection complète
    })
  }
})
</script>

<template>
  <!-- Overlay plein écran avec fond flouté -->
  <div
    class="fixed top-0 left-0 w-screen h-screen flex items-center justify-center backdrop-blur-sm z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white p-6 border border-gray-300 rounded-md shadow-lg w-11/12 max-w-md">
      <!-- En-tête avec titre et bouton de fermeture -->
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-xl font-bold m-0">Settings</h3>
        <button
          class="bg-transparent border-0 text-2xl leading-none cursor-pointer focus:outline-none"
          @click="$emit('close')"
        >
          ×
        </button>
      </div>
      <hr class="border-t border-gray-300 mb-4" />

      <!-- Option : Toggle pour colorer uniquement les mots inconnus -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Icône palette -->
            <svg class="w-6 h-6 mr-2" viewBox="0 0 24 24">
              <path :d="mdiPalette" fill="currentColor" />
            </svg>
            <span>Coloring only unknown</span>
          </div>
          <ToggleSwitch v-model="onlyUnknown" />
        </div>
      </div>

      <!-- Section pour les boutons de connexion -->
      <div class="mt-6 space-y-4">
        <h4 class="text-lg font-bold mb-2">Sign In</h4>
        <!-- Bouton personnalisé pour Google -->
        <button
          @click="handleGoogleSignIn"
          class="w-full relative bg-white border border-gray-300 rounded-sm py-2 hover:bg-gray-50"
        >
          <img
            src="@/assets/google-logo.svg"
            alt="Google Logo"
            class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2"
          />
          <span class="block text-center w-full">Sign in with Google</span>
        </button>
        <!-- Bouton personnalisé pour Apple -->
        <button
          @click="handleAppleSignIn"
          class="w-full relative bg-black border border-black text-white rounded-sm py-2 hover:bg-gray-800"
        >
          <img
            src="@/assets/apple-logo.svg"
            alt="Apple Logo"
            class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2"
          />
          <span class="block text-center w-full">Sign in with Apple</span>
        </button>
      </div>
    </div>
  </div>
</template>
