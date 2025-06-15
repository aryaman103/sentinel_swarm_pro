<template>
  <div>
    <table class="min-w-full table-auto">
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Source IP</th>
          <th>Severity</th>
          <th>Raw</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="event in filteredEvents" :key="event.id" :class="rowClass(event.severity)">
          <td>{{ event.ts }}</td>
          <td>{{ event.src_ip }}</td>
          <td>{{ event.severity.toFixed(2) }}</td>
          <td>
            <pre class="text-xs">{{ event.raw }}</pre>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useEventStore } from '../stores/eventStore'

const store = useEventStore()
const filteredEvents = computed(() => store.events)

function rowClass(severity: number) {
  if (severity > 0.8) return 'bg-red-200'
  if (severity > 0.5) return 'bg-amber-100'
  return 'bg-green-50'
}
</script>
