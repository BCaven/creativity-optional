/**
 * outputscene.js
 *
 * Bootstraps Vuetify and other plugins then mounts the OutputScene
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './OutputScene.vue'

// Composables
import { createApp } from 'vue'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
