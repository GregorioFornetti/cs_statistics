
<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type {
  Conferences,
  Journals,
  VenueSelection,
  VenueType,
} from '@/types/data'

const props = withDefaults(
  defineProps<{
    modelValue: VenueSelection[]
    conferences: Conferences
    journals: Journals
    initialLimit?: number
    loadMoreCount?: number
  }>(),
  {
    initialLimit: 100,
    loadMoreCount: 100,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: VenueSelection[]]
}>()

const search = ref('')
const showConferences = ref(true)
const showJournals = ref(true)

const visibleAvailableCount = ref(props.initialLimit)
const visibleSelectedCount = ref(props.initialLimit)

const allVenues = computed<VenueSelection[]>(() => [
  ...Object.entries(props.conferences).map(([id, value]) => ({
    id,
    name: value.name,
    type: 'conference' as const,
  })),
  ...Object.entries(props.journals).map(([id, value]) => ({
    id,
    name: value.name,
    type: 'journal' as const,
  })),
])

function venueKey(venue: VenueSelection) {
  return `${venue.type}:${venue.id}`
}

const selectedKeys = computed(() =>
  new Set(props.modelValue.map(venueKey)),
)

function isTypeEnabled(type: VenueType) {
  return type === 'conference'
    ? showConferences.value
    : showJournals.value
}

function matchesSearch(venue: VenueSelection) {
  return venue.name
    .toLowerCase()
    .includes(search.value.trim().toLowerCase())
}

const availableVenues = computed(() =>
  allVenues.value
    .filter(venue =>
      !selectedKeys.value.has(venueKey(venue)) &&
      isTypeEnabled(venue.type) &&
      matchesSearch(venue),
    )
    .sort((a, b) => a.name.localeCompare(b.name)),
)

const selectedVenues = computed(() =>
  props.modelValue
    .filter(venue =>
      isTypeEnabled(venue.type) &&
      matchesSearch(venue),
    )
    .sort((a, b) => a.name.localeCompare(b.name)),
)

const visibleAvailableVenues = computed(() =>
  availableVenues.value.slice(0, visibleAvailableCount.value),
)

const visibleSelectedVenues = computed(() =>
  selectedVenues.value.slice(0, visibleSelectedCount.value),
)

// Reset pagination whenever the search or filters change.
watch(
  [search, showConferences, showJournals],
  () => {
    visibleAvailableCount.value = props.initialLimit
    visibleSelectedCount.value = props.initialLimit
  },
)

function loadMoreAvailable(event: Event) {
  const element = event.target as HTMLElement

  if (
    element.scrollTop + element.clientHeight >=
    element.scrollHeight - 80
  ) {
    visibleAvailableCount.value = Math.min(
      visibleAvailableCount.value + props.loadMoreCount,
      availableVenues.value.length,
    )
  }
}

function loadMoreSelected(event: Event) {
  const element = event.target as HTMLElement

  if (
    element.scrollTop + element.clientHeight >=
    element.scrollHeight - 80
  ) {
    visibleSelectedCount.value = Math.min(
      visibleSelectedCount.value + props.loadMoreCount,
      selectedVenues.value.length,
    )
  }
}

function addVenue(venue: VenueSelection) {
  if (selectedKeys.value.has(venueKey(venue))) return

  emit('update:modelValue', [...props.modelValue, venue])
}

function removeVenue(venue: VenueSelection) {
  emit(
    'update:modelValue',
    props.modelValue.filter(
      item => venueKey(item) !== venueKey(venue),
    ),
  )
}
</script>

<template>
  <section class="space-y-4">
    <div class="flex items-center justify-between">
      <label class="text-sm font-semibold text-gray-800 dark:text-gray-200">
        Conferences and journals
      </label>

      <span class="text-xs text-gray-500 dark:text-gray-400">
        {{ modelValue.length }} selected
      </span>
    </div>

    <!-- Search and filters -->
    <div class="space-y-3">
      <input
        v-model="search"
        type="search"
        placeholder="Search conferences and journals..."
        class="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5
               text-sm outline-none transition placeholder:text-gray-400
               focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20
               dark:border-gray-700 dark:bg-gray-900 dark:text-white"
      />

      <div class="flex flex-wrap gap-4">
        <label class="flex cursor-pointer items-center gap-2 text-sm">
          <input
            v-model="showConferences"
            type="checkbox"
            class="h-4 w-4 rounded accent-blue-600"
          />
          Conferences
        </label>

        <label class="flex cursor-pointer items-center gap-2 text-sm">
          <input
            v-model="showJournals"
            type="checkbox"
            class="h-4 w-4 rounded accent-blue-600"
          />
          Journals
        </label>
      </div>
    </div>

    <!-- Selection containers -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
      <!-- Available -->
      <div class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-700">
        <div class="border-b border-gray-200 bg-gray-50 px-4 py-3 dark:border-gray-700 dark:bg-gray-800/70">
          <h3 class="text-sm font-semibold">
            Available
            <span class="ml-1 font-normal text-gray-500">
              ({{ availableVenues.length }})
            </span>
          </h3>
        </div>

        <div
          class="h-72 space-y-1 overflow-y-auto p-2"
          @scroll.passive="loadMoreAvailable"
        >
          <button
            v-for="venue in visibleAvailableVenues"
            :key="venueKey(venue)"
            type="button"
            @click="addVenue(venue)"
            class="group flex w-full items-center gap-3 rounded-lg px-3 py-2.5
                   text-left transition hover:bg-blue-50
                   dark:hover:bg-blue-950/40"
          >
            <span
              class="flex h-7 w-7 shrink-0 items-center justify-center rounded-md
                     bg-gray-100 text-gray-500 dark:bg-gray-800"
            >
              <span v-if="venue.type === 'conference'" class="text-xs font-bold">C</span>
              <span v-else class="text-xs font-bold">J</span>
            </span>

            <span
                class="min-w-0 flex-1"
                :title="venue.name"
            >
                <span class="block truncate text-sm font-semibold text-gray-900 dark:text-gray-100">
                    {{ venue.id }}
                </span>

                <span class="block truncate text-xs text-gray-500 dark:text-gray-400">
                    {{ venue.name }}
                </span>

                <span class="text-xs text-gray-400">
                    {{ venue.type === 'conference' ? 'Conference' : 'Journal' }}
                </span>
            </span>

            <span class="text-lg text-gray-400 transition group-hover:text-blue-600">
              +
            </span>
          </button>

          <p
            v-if="availableVenues.length === 0"
            class="px-3 py-8 text-center text-sm text-gray-400"
          >
            No available items found.
          </p>

          <p
            v-else-if="visibleAvailableCount < availableVenues.length"
            class="px-3 py-3 text-center text-xs text-gray-400"
          >
            Scroll down to load more
          </p>
        </div>
      </div>

      <!-- Selected -->
      <div class="overflow-hidden rounded-xl border border-blue-200 dark:border-blue-900">
        <div class="border-b border-blue-200 bg-blue-50 px-4 py-3 dark:border-blue-900 dark:bg-blue-950/40">
          <h3 class="text-sm font-semibold text-blue-800 dark:text-blue-300">
            Selected
            <span class="ml-1 font-normal text-blue-600 dark:text-blue-400">
              ({{ selectedVenues.length }})
            </span>
          </h3>
        </div>

        <div
          class="h-72 space-y-1 overflow-y-auto p-2"
          @scroll.passive="loadMoreSelected"
        >
          <button
            v-for="venue in visibleSelectedVenues"
            :key="venueKey(venue)"
            type="button"
            @click="removeVenue(venue)"
            class="group flex w-full items-center gap-3 rounded-lg px-3 py-2.5
                   text-left transition hover:bg-red-50
                   dark:hover:bg-red-950/30"
          >
            <span
              class="flex h-7 w-7 shrink-0 items-center justify-center rounded-md
                     bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300"
            >
              <span v-if="venue.type === 'conference'" class="text-xs font-bold">C</span>
              <span v-else class="text-xs font-bold">J</span>
            </span>

            <span
                class="min-w-0 flex-1"
                :title="venue.name"
            >
                <span class="block truncate text-sm font-semibold text-gray-900 dark:text-gray-100">
                    {{ venue.id }}
                </span>

                <span class="block truncate text-xs text-gray-500 dark:text-gray-400">
                    {{ venue.name }}
                </span>

                <span class="text-xs text-gray-400">
                    {{ venue.type === 'conference' ? 'Conference' : 'Journal' }}
                </span>
            </span>

            <span class="text-lg text-gray-400 transition group-hover:text-red-600">
              ×
            </span>
          </button>

          <p
            v-if="selectedVenues.length === 0"
            class="px-3 py-8 text-center text-sm text-gray-400"
          >
            No selected items.
          </p>

          <p
            v-else-if="visibleSelectedCount < selectedVenues.length"
            class="px-3 py-3 text-center text-xs text-gray-400"
          >
            Scroll down to load more
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
