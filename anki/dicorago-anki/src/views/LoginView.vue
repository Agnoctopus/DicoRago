<template>
  <div class="container">
    <h2>Dicorago Login</h2>
    <div v-if="!online" class="offline">No internet connection. Please check your connection.</div>
    <div v-else>
      <p>Click the button below to sign in with Google.</p>
      <button @click="startGoogleSignIn">Sign in with Google</button>
    </div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
console.log(1);
// Declare QWebChannel and qt if types are not available
declare const QWebChannel: any
declare const qt: any

import { ref, onMounted } from 'vue'

const online = ref<boolean>(navigator.onLine)
const message = ref<string>('')

function updateOnlineStatus(): void {
  online.value = navigator.onLine
}

onMounted(() => {
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)

  // Initialize QWebChannel to expose the Python authHandler
  if (typeof qt !== 'undefined' && qt.webChannelTransport) {
    new QWebChannel(qt.webChannelTransport, (channel: any) => {
      ;(window as any).authHandler = channel.objects.authHandler
    })
  } else {
    console.error('qt is not defined. QWebChannel cannot be initialized.')
  }
})

function startGoogleSignIn(): void {
  if (!navigator.onLine) {
    message.value = 'No internet connection. Please try again later.'
    return
  }
  message.value = 'Starting Google sign-in...'

  // Simulate an asynchronous authentication process (replace with your real flow)
  setTimeout(() => {
    const token: string = 'demo_token_123' // Replace with the actual token from your backend
    if (
      (window as any).authHandler &&
      typeof (window as any).authHandler.sendToken === 'function'
    ) {
      ;(window as any).authHandler.sendToken(token)
    }
  }, 2000)
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  font-family: Arial, sans-serif;
  padding: 20px;
}
.offline {
  color: red;
  font-weight: bold;
  margin-bottom: 20px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
