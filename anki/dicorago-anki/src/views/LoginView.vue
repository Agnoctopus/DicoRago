<template>
  <div class="container">
    <h2>Connexion Dicorago</h2>
    <p v-if="message">{{ message }}</p>
    <button v-if="!loading && !token" @click="startLogin">
      Se connecter avec Google
    </button>
    <p v-if="loading">Connexion en cours, veuillez patienter...</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'

export default defineComponent({
  name: "LoginPage",
  setup() {
    const token = ref<string | null>(null)
    const loading = ref(false)
    const message = ref("")

    // Envoie le token vers l'extension via QWebChannel
    function sendTokenToAnki(token: string) {
      if ((window as any).authHandler && typeof (window as any).authHandler.sendToken === 'function') {
        (window as any).authHandler.sendToken(token)
      } else {
        console.error("authHandler indisponible")
      }
    }

    // Extrait le token des paramètres d'URL (exemple : ?token=abc123)
    function extractTokenFromUrl(): string | null {
      const params = new URLSearchParams(window.location.search)
      return params.get("token")
    }

    // Lance le processus de connexion en redirigeant vers dicorago.com/google
    function startLogin() {
      loading.value = true
      // On utilise l'URL actuelle (sans query) comme redirect_uri
      const currentUrl = window.location.href.split('?')[0]
      const redirectUrl = encodeURIComponent(currentUrl)
      const loginUrl = `https://agno.re/anki`
      window.location.href = loginUrl
    }

    onMounted(() => {
      // Initialisation du QWebChannel pour exposer authHandler
      if (typeof (window as any).qt !== 'undefined' && (window as any).qt.webChannelTransport) {
        new (window as any).QWebChannel((window as any).qt.webChannelTransport, (channel: any) => {
          (window as any).authHandler = channel.objects.authHandler
        })
      } else {
        console.error("qt ou webChannelTransport n'est pas défini")
      }

      // Si la page est rechargée avec un token dans l'URL, on le récupère
      const urlToken = extractTokenFromUrl()
      if (urlToken) {
        token.value = urlToken
        message.value = "Authentification réussie, transmission du token..."
        sendTokenToAnki(urlToken)
      }
    })

    return {
      token,
      loading,
      message,
      startLogin
    }
  }
})
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  font-family: Arial, sans-serif;
}

button {
  padding: 1rem 2rem;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}
</style>
