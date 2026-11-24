
<script setup lang="ts">
import { RouterLink } from 'vue-router'

defineProps<{
  image: string
  title: string
  description: string
  to: string
}>()
</script>

<template>
  <RouterLink
    :to="to"
    class="group block overflow-hidden rounded-2xl
           border border-gray-200 bg-white
           shadow-sm transition-all duration-300
           hover:-translate-y-1 hover:border-blue-400
           hover:shadow-xl
           focus-visible:outline-2
           focus-visible:outline-offset-4
           focus-visible:outline-blue-500
           dark:border-gray-800 dark:bg-gray-900
           dark:hover:border-blue-500"
  >
    <!-- Image -->
    <div class="aspect-[16/9] overflow-hidden bg-gray-100 dark:bg-gray-800">
      <img
        :src="image"
        :alt="title"
        loading="lazy"
        class="h-full w-full object-cover
               transition-transform duration-500
               group-hover:scale-105"
      />
    </div>

    <!-- Content -->
    <div class="p-6">
      <div class="mb-3 flex items-center justify-between gap-3">
        <h2
          class="text-lg font-semibold text-gray-900
                 transition-colors group-hover:text-blue-600
                 dark:text-white dark:group-hover:text-blue-400"
        >
          {{ title }}
        </h2>

        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="shrink-0 text-gray-400
                 transition-all duration-300
                 group-hover:translate-x-1
                 group-hover:text-blue-600
                 dark:group-hover:text-blue-400"
        >
          <path d="M5 12h14" />
          <path d="m12 5 7 7-7 7" />
        </svg>
      </div>

      <p class="text-sm leading-relaxed text-gray-600 dark:text-gray-400">
        {{ description }}
      </p>
    </div>
  </RouterLink>
</template>
