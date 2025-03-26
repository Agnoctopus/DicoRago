<template>
    <div class="container">
      <h2>Dicorago Login</h2>
      <div v-if="!online" class="offline">
        No internet connection. Please check your connection.
      </div>
      <div v-else>
        <p>Click the button below to sign in with Google.</p>
        <button @click="startGoogleSignIn">Sign in with Google</button>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'App',
    data() {
      return {
        online: navigator.onLine,
        message: ""
      }
    },
    mounted() {
      window.addEventListener('online', () => this.online = true)
      window.addEventListener('offline', () => this.online = false)
  
      // Initialisation du QWebChannel pour récupérer l'objet Python exposé
      new QWebChannel(qt.webChannelTransport, (channel) => {
        window.authHandler = channel.objects.authHandler;
      });
    },
    methods: {
      startGoogleSignIn() {
        if (!this.online) {
          this.message = "No internet connection. Please try again later.";
          return;
        }
        this.message = "Starting Google sign-in...";
  
        // Ici, déclenchez votre flux d'authentification en ligne.
        // Pour cet exemple, on simule une récupération de token après 2 secondes.
        setTimeout(() => {
          // Dans une implémentation réelle, le backend redirigerait vers une URL avec le token.
          const token = "demo_token_123"; // Remplacez par le token réel
          if (window.authHandler && window.authHandler.sendToken) {
            window.authHandler.sendToken(token);
          }
        }, 2000);
      }
    }
  }
  </script>
  
  <style>
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
  