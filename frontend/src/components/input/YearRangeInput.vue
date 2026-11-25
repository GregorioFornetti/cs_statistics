<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue: [number, number]
    minYear?: number
    maxYear?: number
  }>(),
  {
    minYear: 1900,
    maxYear: () => new Date().getFullYear(),
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: [number, number]]
}>()

const minValue = computed(() => props.modelValue[0])
const maxValue = computed(() => props.modelValue[1])

const rangeStart = computed(() =>
  ((minValue.value - props.minYear) /
    (props.maxYear - props.minYear)) * 100,
)

const rangeEnd = computed(() =>
  ((maxValue.value - props.minYear) /
    (props.maxYear - props.minYear)) * 100,
)

function updateMin(event: Event) {
  const value = Number((event.target as HTMLInputElement).value)

  emit('update:modelValue', [
    Math.min(value, maxValue.value),
    maxValue.value,
  ])
}

function updateMax(event: Event) {
  const value = Number((event.target as HTMLInputElement).value)

  emit('update:modelValue', [
    minValue.value,
    Math.max(value, minValue.value),
  ])
}
</script>

<template>
  <section class="space-y-5">
    <div class="flex items-center justify-between">
      <label class="text-sm font-semibold text-gray-800 dark:text-gray-200">
        Publication years
      </label>

      <span class="text-sm font-semibold text-blue-600 dark:text-blue-400">
        {{ minValue }} – {{ maxValue }}
      </span>
    </div>

    <div class="space-y-4 rounded-xl border border-gray-200 p-5 dark:border-gray-700">
      <div class="flex items-center justify-between gap-4">
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            Starting year
          </p>
          <p class="text-lg font-semibold">{{ minValue }}</p>
        </div>

        <div class="text-right">
          <p class="text-xs text-gray-500 dark:text-gray-400">
            Ending year
          </p>
          <p class="text-lg font-semibold">{{ maxValue }}</p>
        </div>
      </div>

      <div class="relative h-8">
        <div
          class="absolute top-1/2 h-1.5 w-full -translate-y-1/2 rounded-full
                 bg-gray-200 dark:bg-gray-700"
        />

        <div
          class="absolute top-1/2 h-1.5 -translate-y-1/2 rounded-full bg-blue-600"
          :style="{
            left: `${rangeStart}%`,
            width: `${rangeEnd - rangeStart}%`,
          }"
        />

        <input
          type="range"
          :min="minYear"
          :max="maxYear"
          :value="minValue"
          @input="updateMin"
          class="range-slider absolute inset-0 z-20"
          aria-label="Starting publication year"
        />

        <input
          type="range"
          :min="minYear"
          :max="maxYear"
          :value="maxValue"
          @input="updateMax"
          class="range-slider absolute inset-0 z-30"
          aria-label="Ending publication year"
        />
      </div>

      <div class="flex justify-between text-xs text-gray-400">
        <span>{{ minYear }}</span>
        <span>{{ maxYear }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.range-slider {
  appearance: none;
  width: 100%;
  height: 100%;
  background: transparent;
  pointer-events: none;
  margin: 0;
}

.range-slider::-webkit-slider-runnable-track {
  height: 6px;
  background: transparent;
}

.range-slider::-moz-range-track {
  height: 6px;
  background: transparent;
}

.range-slider::-webkit-slider-thumb {
  appearance: none;
  pointer-events: auto;
  width: 18px;
  height: 18px;
  margin-top: -6px;
  border-radius: 50%;
  background: #2563eb;
  border: 3px solid white;
  box-shadow: 0 0 0 1px #2563eb;
  cursor: grab;
}

.range-slider::-moz-range-thumb {
  pointer-events: auto;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #2563eb;
  border: 3px solid white;
  box-shadow: 0 0 0 1px #2563eb;
  cursor: grab;
}

.range-slider:focus-visible {
  outline: none;
}

.range-slider:focus-visible::-webkit-slider-thumb {
  box-shadow: 0 0 0 4px rgb(37 99 235 / 25%);
}
</style>