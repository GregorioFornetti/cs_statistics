
<script setup lang="ts">
import { onMounted, ref } from 'vue'

const repositoryUrl =
  'https://github.com/GregorioFornetti/cs_statistics'

const metadataUrl =
  'https://raw.githubusercontent.com/GregorioFornetti/cs_statistics/main/data/processed/metadata.json'

const lastUpdated = ref<string | null>(null)
const loading = ref(true)

const dateFields = [
  'last_updated',
  'last_update',
  'updated_at',
  'last_modified',
  'generated_at',
  'date',
]

function findDate(data: unknown): string | null {
  if (!data || typeof data !== 'object') return null

  const object = data as Record<string, unknown>

  for (const field of dateFields) {
    const value = object[field]

    if (
      typeof value === 'string' ||
      typeof value === 'number'
    ) {
      const date = new Date(value)

      if (!Number.isNaN(date.getTime())) {
        return date.toISOString()
      }
    }
  }

  // Check nested metadata objects.
  for (const value of Object.values(object)) {
    if (value && typeof value === 'object') {
      const result = findDate(value)
      if (result) return result
    }
  }

  return null
}

function formatDate(date: string): string {
  return new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(date))
}

onMounted(async () => {
  try {
    const response = await fetch(metadataUrl, {
      headers: { Accept: 'application/json' },
    })

    if (!response.ok) {
      throw new Error(`Metadata request failed: ${response.status}`)
    }

    const metadata: unknown = await response.json()
    lastUpdated.value = findDate(metadata)
  } catch (error) {
    console.error('Could not load dataset metadata:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <footer
    class="border-t border-gray-200 bg-gray-50
           dark:border-gray-800 dark:bg-gray-900"
  >
    <div
      class="mx-auto flex max-w-7xl flex-col items-center
             justify-between gap-3 px-6 py-6 text-sm
             text-gray-500 sm:flex-row dark:text-gray-400"
    >
      <p>
        Source code available on
        <a
          :href="repositoryUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="font-medium text-blue-600 hover:underline
                 dark:text-blue-400"
        >
          GitHub
        </a>
      </p>

      <p>
        Data last updated:
        <span class="font-medium text-gray-700 dark:text-gray-200">
          {{
            loading
              ? 'Loading...'
              : lastUpdated
                ? formatDate(lastUpdated)
                : 'Date unavailable'
          }}
        </span>
      </p>
    </div>
  </footer>
</template>
