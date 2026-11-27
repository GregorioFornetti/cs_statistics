
<script setup lang="ts">
import { computed, ref } from 'vue'
import type { UniversityPublicationsCount } from '@/types/data'

const props = defineProps<{
  data: UniversityPublicationsCount[]
}>()

const search = ref('')
const sortBy = ref<'publicationsCount' | 'name'>('publicationsCount')
const sortDirection = ref<'asc' | 'desc'>('desc')

const totalPublications = computed(() =>
  props.data.reduce((total, item) => total + item.publicationsCount, 0)
)

const averagePublications = computed(() =>
  props.data.length
    ? totalPublications.value / props.data.length
    : 0
)

const filteredData = computed(() => {
  const query = search.value.trim().toLowerCase()

  return props.data
    .filter(item =>
      !query ||
      item.name.toLowerCase().includes(query) ||
      item.institutionId.toLowerCase().includes(query) ||
      item.country?.toLowerCase().includes(query) ||
      item.countryIsoCode?.toLowerCase().includes(query)
    )
    .sort((a, b) => {
      const comparison =
        sortBy.value === 'name'
          ? a.name.localeCompare(b.name)
          : a.publicationsCount - b.publicationsCount

      return sortDirection.value === 'asc'
        ? comparison
        : -comparison
    })
})

const maxPublications = computed(() =>
  Math.max(...props.data.map(item => item.publicationsCount), 1)
)

function toggleSort(field: 'publicationsCount' | 'name') {
  if (sortBy.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = field
    sortDirection.value = field === 'name' ? 'asc' : 'desc'
  }
}

function getFlagUrl(isoCode?: string) {
  return isoCode
    ? `https://flagcdn.com/w40/${isoCode.toLowerCase()}.png`
    : undefined
}

function formatNumber(value: number) {
  return new Intl.NumberFormat().format(value)
}
</script>

<template>
  <main class="mx-auto min-h-screen max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <!-- Page heading -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white sm:text-3xl">
        Publications by University
      </h1>

      <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
        Publication distribution across the selected institutions.
      </p>
    </div>

    <!-- Summary cards -->
    <div class="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
      <div class="rounded-xl border border-gray-200 bg-white p-5 dark:border-gray-700 dark:bg-gray-800">
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">
          Total publications
        </p>
        <p class="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
          {{ formatNumber(totalPublications) }}
        </p>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white p-5 dark:border-gray-700 dark:bg-gray-800">
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">
          Institutions
        </p>
        <p class="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
          {{ formatNumber(data.length) }}
        </p>
      </div>

      <div class="rounded-xl border border-gray-200 bg-white p-5 dark:border-gray-700 dark:bg-gray-800">
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">
          Average publications
        </p>
        <p class="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
          {{ formatNumber(Math.round(averagePublications)) }}
        </p>
      </div>
    </div>

    <!-- Results -->
    <section class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
      <div class="flex flex-col gap-4 border-b border-gray-200 p-4 dark:border-gray-700 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
            Institutions
          </h2>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Showing {{ formatNumber(filteredData.length) }} of
            {{ formatNumber(data.length) }} institutions
          </p>
        </div>

        <input
          v-model="search"
          type="search"
          placeholder="Search institutions..."
          class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-gray-600 dark:bg-gray-900 dark:text-white sm:max-w-xs"
        />
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-gray-50 text-xs uppercase text-gray-500 dark:bg-gray-900/50 dark:text-gray-400">
            <tr>
              <th class="px-4 py-3">#</th>

              <th class="px-4 py-3">
                <button
                  class="flex items-center gap-1 font-semibold"
                  @click="toggleSort('name')"
                >
                  Institution
                  <span v-if="sortBy === 'name'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </button>
              </th>

              <th class="px-4 py-3">Country</th>

              <th class="px-4 py-3 text-right">
                <button
                  class="ml-auto flex items-center gap-1 font-semibold"
                  @click="toggleSort('publicationsCount')"
                >
                  Publications
                  <span v-if="sortBy === 'publicationsCount'">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </button>
              </th>

              <th class="hidden px-4 py-3 sm:table-cell">
                Distribution
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr
              v-for="(institution, index) in filteredData"
              :key="institution.institutionId"
              class="transition-colors hover:bg-gray-50 dark:hover:bg-gray-700/40"
            >
              <td class="px-4 py-3 text-gray-400">
                {{ index + 1 }}
              </td>

              <td class="max-w-md px-4 py-3">
                <p class="truncate font-medium text-gray-900 dark:text-white">
                  {{ institution.name }}
                </p>
                <p class="mt-0.5 truncate text-xs text-gray-400">
                  {{ institution.institutionId }}
                </p>
              </td>

              <td class="px-4 py-3 text-gray-600 dark:text-gray-300">
                <div class="flex items-center gap-2 whitespace-nowrap">
                  <img
                    v-if="getFlagUrl(institution.countryIsoCode)"
                    :src="getFlagUrl(institution.countryIsoCode)"
                    :alt="institution.country || institution.countryIsoCode"
                    class="h-4 w-6 rounded-sm object-cover"
                    loading="lazy"
                  />
                  <span>
                    {{ institution.country || institution.countryIsoCode || '—' }}
                  </span>
                </div>
              </td>

              <td class="px-4 py-3 text-right font-semibold tabular-nums text-gray-900 dark:text-white">
                {{ formatNumber(institution.publicationsCount) }}
              </td>

              <td class="hidden px-4 py-3 sm:table-cell">
                <div class="h-2 w-full overflow-hidden rounded-full bg-gray-100 dark:bg-gray-700">
                  <div
                    class="h-full rounded-full bg-blue-500"
                    :style="{
                      width: `${institution.publicationsCount / maxPublications * 100}%`
                    }"
                  />
                </div>
              </td>
            </tr>

            <tr v-if="filteredData.length === 0">
              <td colspan="5" class="px-4 py-12 text-center text-gray-500 dark:text-gray-400">
                No institutions found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</template>
