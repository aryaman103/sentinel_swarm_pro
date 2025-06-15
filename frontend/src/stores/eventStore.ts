import { defineStore } from 'pinia'

export interface Event {
  id: number
  ts: number
  src_ip: string
  severity: number
  raw: string
}

export const useEventStore = defineStore('eventStore', {
  state: () => ({
    events: [] as Event[]
  }),
  actions: {
    addEvent(event: Event) {
      this.events.unshift(event)
      if (this.events.length > 500) {
        this.events.pop()
      }
    }
  }
})
