<script setup lang="ts">
import type { LoadError } from '@/stores/appData'

defineProps<{
  errors: LoadError[]
}>()

defineEmits<{
  retry: []
}>()
</script>

<template>
  <main
    class="flex min-h-screen flex-col items-center justify-center
           bg-gray-50 px-6 py-12 text-gray-900
           dark:bg-gray-950 dark:text-gray-100"
  >
    <div class="w-full max-w-lg">
      <div
        class="flex h-14 w-14 items-center justify-center rounded-full
               bg-red-100 text-red-600 dark:bg-red-950 dark:text-red-400"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-7 w-7"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 9v4m0 4h.01M10.29 3.86l-8.1 14.02A2 2 0 003.92 21h16.16a2 2 0 001.73-3.12l-8.1-14.02a2 2 0 00-3.46 0z"
          />
        </svg>
      </div>

      <h1 class="mt-6 text-2xl font-bold">
        Unable to load application data
      </h1>

      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Some required files could not be loaded. Please check your
        internet connection and try again.
      </p>

      <div
        class="mt-6 rounded-xl border border-red-200 bg-red-50 p-4
               dark:border-red-900 dark:bg-red-950/30"
      >
        <h2 class="font-semibold text-red-800 dark:text-red-300">
          Failed resources
        </h2>

        <ul class="mt-3 space-y-3">
          <li v-for="error in errors" :key="error.file">
            <p class="text-sm font-medium text-red-800 dark:text-red-300">
              {{ error.file }}
            </p>

            <p class="mt-1 text-xs text-red-700 dark:text-red-400">
              {{ error.message }}
            </p>
          </li>
        </ul>
      </div>

      <button
        class="mt-6 w-full rounded-lg bg-blue-600 px-5 py-3
               font-medium text-white transition hover:bg-blue-700
               focus-visible:outline-2 focus-visible:outline-offset-2
               focus-visible:outline-blue-600"
        @click="$emit('retry')"
      >
        Try again
      </button>
    </div>
  </main>
</template>