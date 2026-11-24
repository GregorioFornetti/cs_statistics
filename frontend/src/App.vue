<script setup lang="ts">
import { onMounted } from 'vue'
import { appStatus, appLoadErrors, loadAppData } from '@/stores/appData'

import Loading from '@/views/Loading.vue'
import ErrorPage from '@/views/Error.vue'

onMounted(() => {
  void loadAppData()
})
</script>

<template>
  <Loading v-if="appStatus === 'idle' || appStatus === 'loading'" />

  <ErrorPage
    v-else-if="appStatus === 'error'"
    :errors="appLoadErrors"
    @retry="loadAppData"
  />

  <RouterView v-else-if="appStatus === 'ready'" />
</template>