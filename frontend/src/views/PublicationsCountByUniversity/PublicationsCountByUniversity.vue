
<script setup lang="ts">
import DataWorkflow from '@/components/DataWorkflow.vue'

import PublicationsCountByUniversityInput from './PublicationsCountByUniversityInput.vue'
import Loading from '@/views/Loading.vue'
import Error from '@/views/Error.vue'
import PublicationsCountByUniversityResult from './PublicationsCountByUniversityResult.vue'

import { loadPublicationsCountByUniversity } from '@/data_loading/loadPublicationsCountByUniversity'

</script>

<template>
  <DataWorkflow
    :input-component="PublicationsCountByUniversityInput"
    :loading-component="Loading"
    :error-component="Error"
    :result-component="PublicationsCountByUniversityResult"
    :load="loadPublicationsCountByUniversity"
  />
</template>
