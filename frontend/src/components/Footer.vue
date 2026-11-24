
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { appData } from '@/stores/appData'

function formatDate(date: string): string {
  return new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(date))
}
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
          href="https://github.com/GregorioFornetti/cs_statistics"
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
            formatDate(appData!.metadata!.download_date)
          }}
        </span>
      </p>
    </div>
  </footer>
</template>
