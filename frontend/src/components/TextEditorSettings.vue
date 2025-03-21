<script setup lang="ts">
import { computed, defineEmits, onMounted } from 'vue'
import ToggleSwitch from '@/components/ToggleSwitch.vue'
import { mdiLightbulb, mdiTranslate } from '@mdi/js'
import { useSettingsStore } from '@/stores/settings'
import { useUserStore } from '@/stores/user'

// Emit 'close' event to close the settings panel.
defineEmits<{ (e: 'close'): void }>()

// Access settings and user stores.
const settingsStore = useSettingsStore()
const userStore = useUserStore()

// Computed property for "onlyUnknownColoring" from the settings store.
const onlyUnknown = computed({
  get: () => settingsStore.onlyUnknownColoring,
  set: (value: boolean) => settingsStore.setOnlyUnknownColoring(value),
})

// Computed property for dictionary language. Default is "en_US" (English).
const dictionaryLanguage = computed({
  get: () => settingsStore.dictionaryLanguage,
  set: (value: string) => settingsStore.setDictionaryLanguage(value),
})

// Interface for Google Credential Response.
interface GoogleCredentialResponse {
  credential: string
}

// Handles the Google credential response by submitting a form to the API.
function handleGoogleCredentialResponse(response: GoogleCredentialResponse) {
  const form = document.createElement('form')
  form.method = 'POST'
  form.action = '/api/auth/google'

  const input = document.createElement('input')
  input.type = 'hidden'
  input.name = 'credential'
  input.value = response.credential

  form.appendChild(input)
  document.body.appendChild(form)
  form.submit()
}

// Interface for Google SDK.
interface GoogleSDK {
  accounts: {
    id: {
      prompt: () => void
      initialize: (options: Record<string, unknown>) => void
    }
  }
}

// Interface for Apple ID SDK.
interface AppleIDSDK {
  auth: {
    signIn: () => void
    init: (options: Record<string, unknown>) => void
  }
}

// Extend the global window object with Google and Apple ID SDKs.
declare global {
  interface Window {
    google: GoogleSDK
    AppleID: AppleIDSDK
  }
}

// Trigger Google sign-in prompt if the SDK is available.
function handleGoogleSignIn() {
  if (window.google && window.google.accounts) {
    window.google.accounts.id.prompt()
  }
}

// Trigger Apple sign-in if the SDK is available.
function handleAppleSignIn() {
  if (window.AppleID && window.AppleID.auth) {
    window.AppleID.auth.signIn()
  }
}

// Sign out by redirecting to the logout API endpoint.
function signOut() {
  window.location.href = '/api/auth/logout'
}

// On component mount, fetch the user and initialize the auth SDKs.
onMounted(async () => {
  await userStore.fetchUser()

  // Initialize Google SDK in redirect mode.
  if (window.google && window.google.accounts) {
    window.google.accounts.id.initialize({
      client_id: '738555358973-8t65bo2j79olfbr86l84m7fhr6ckob7v.apps.googleusercontent.com',
      context: 'signin',
      ux_mode: 'redirect',
      login_uri: 'https://dicorago.com/api/auth/google',
      callback: handleGoogleCredentialResponse,
    })
  }
  // Initialize Apple ID SDK.
  if (window.AppleID && window.AppleID.auth) {
    window.AppleID.auth.init({
      clientId: 'com.DicoRago.webapp',
      scope: 'name email',
      redirectURI: 'https://dicorago.com/api/auth/apple',
      usePopup: false,
    })
  }
})
</script>

<template>
  <!-- Fullscreen overlay with a blurred background -->
  <div
    class="fixed top-0 left-0 w-screen h-screen flex items-center justify-center backdrop-blur-sm z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white p-6 border border-gray-300 rounded-md shadow-lg w-11/12 max-w-md">
      <!-- Header: title and close button -->
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

      <!-- Option: Toggle for coloring only unknown words -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Lightbulb icon -->
            <svg class="w-6 h-6 mr-2" viewBox="0 0 24 24">
              <path :d="mdiLightbulb" fill="currentColor" />
            </svg>
            <span>Coloring only unknown</span>
          </div>
          <ToggleSwitch v-model="onlyUnknown" />
        </div>

        <!-- Dictionary language selector with icon -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Translate icon -->
            <svg class="w-6 h-6 mr-2" viewBox="0 0 24 24">
              <path :d="mdiTranslate" fill="currentColor" />
            </svg>
            <span>Dictionary Language</span>
          </div>
          <select
            id="dict-lang"
            v-model="dictionaryLanguage"
            class="p-2 border border-gray-300 rounded-md text-center font-semibold"
          >
            <option value="en_US">English</option>
            <option value="ko_KR">한국어</option>
            <option value="fr_FR">Français</option>
            <option value="es_ES">Español</option>
            <option value="ja_JP">日本語</option>
          </select>
        </div>
      </div>

      <!-- Authentication section -->
      <div v-if="userStore.isFetched" class="mt-6">
        <!-- If user is logged in -->
        <div v-if="userStore.user" class="space-y-2">
          <h4 class="text-lg font-bold mb-2">User</h4>
          <button
            class="w-full relative bg-white border border-gray-300 rounded-sm py-2 hover:bg-gray-50"
          >
            <span class="block text-center w-full">{{ userStore.user.name }}</span>
          </button>
          <button
            @click="signOut"
            class="w-full relative bg-black border border-black text-white rounded-sm py-2 hover:bg-gray-800"
          >
            <span class="block text-center w-full">Sign Out</span>
          </button>
        </div>
        <!-- Otherwise, display sign-in buttons -->
        <div v-else class="space-y-2">
          <h4 class="text-lg font-bold mb-2">Sign-in</h4>
          <button
            @click="handleGoogleSignIn"
            class="w-full relative bg-white border border-gray-300 rounded-sm py-2 hover:bg-gray-50"
          >
            <img
              src="@/assets/google-brand.svg"
              alt="Google Logo"
              class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2"
            />
            <span class="block text-center w-full">Sign in with Google</span>
          </button>
          <!-- Custom button for Apple sign-in -->
          <button
            @click="handleAppleSignIn"
            class="w-full relative bg-black border border-black text-white rounded-sm py-2 hover:bg-gray-800"
          >
            <img
              src="@/assets/apple-brand.svg"
              alt="Apple Logo"
              class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2"
            />
            <span class="block text-center w-full">Sign in with Apple</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
