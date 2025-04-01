import './assets/style.css'
import { createApp } from 'vue'
import App from './App.vue'

// Déclarez les variables globales pour éviter les erreurs TypeScript
declare global {
  interface Window {
    bridge: any;
  }
}
declare var QWebChannel: any;
declare var qt: { webChannelTransport: any };

window.onload = () => {
  new QWebChannel(qt.webChannelTransport, function(channel: any) {
    console.log(2)

    window.anki = channel.objects.anki;
    // Démarrage de l'application Vue une fois le bridge initialisé
    createApp(App).mount('#app');
  });
};
