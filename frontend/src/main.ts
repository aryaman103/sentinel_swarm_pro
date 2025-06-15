import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './index.css'
import { useEventStore } from './stores/eventStore'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')

// WebSocket for real-time events
const store = useEventStore()
const ws = new WebSocket('ws://localhost:8000/ws/events')
ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  store.addEvent(data)
}
