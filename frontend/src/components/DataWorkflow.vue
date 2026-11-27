<script setup lang="ts" generic="TInput, TData, TErrors">
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { ref, type Component } from 'vue'

type WorkflowResponse<T, E> =
  | { data: T; errors?: never }
  | { errors: E; data?: never }

type WorkflowStatus = 'idle' | 'loading' | 'error' | 'success'

const props = defineProps<{
  inputComponent: Component
  loadingComponent: Component
  errorComponent: Component
  resultComponent: Component

  load: (input: TInput) => Promise<WorkflowResponse<TData, TErrors>>
}>()

const status = ref<WorkflowStatus>('idle')
const errors = ref<TErrors | null>(null)
const resultData = ref<TData | null>(null)

let lastInput: TInput | undefined

async function submit(input: TInput) {
  lastInput = input

  status.value = 'loading'
  errors.value = null
  resultData.value = null

  try {
    const response = await props.load(input)

    if ('errors' in response) {
      errors.value = response.errors
      status.value = 'error'
      return
    }

    resultData.value = response.data
    status.value = 'success'
  } catch (error) {
    errors.value = error as TErrors
    status.value = 'error'
  }
}

function retry() {
  if (lastInput !== undefined) {
    submit(lastInput)
  }
}
</script>

<template>
  <Header />

  <component
    v-if="status === 'idle'"
    :is="inputComponent"
    @submit="submit"
  />

  <component
    v-else-if="status === 'loading'"
    :is="loadingComponent"
  />

  <component
    v-else-if="status === 'error'"
    :is="errorComponent"
    :errors="errors"
    @retry="retry"
  />

  <component
    v-else-if="status === 'success' && resultData !== null"
    :is="resultComponent"
    :data="resultData"
  />

  <Footer />
</template>