
<script setup lang="ts">
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import Card from '../components/Card.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <Header />

    <main class="mx-auto w-full max-w-7xl flex-1 px-6 py-12 sm:py-16">
      <section class="mb-12">
        <h1
          class="mb-4 text-3xl font-bold tracking-tight
                 text-gray-900 sm:text-4xl dark:text-white"
        >
          Computer Science Statistics
        </h1>

        <p class="max-w-2xl text-lg leading-relaxed text-gray-600 dark:text-gray-400">
          Explore statistics and insights about scientific
          publications in Computer Science.
        </p>
      </section>

      <section>
        <h2 class="mb-6 text-xl font-semibold text-gray-900 dark:text-white">
          Explore statistics
        </h2>

        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <Card
            image="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800"
            title="Publications count by university"
            description="You can choose which countries, years, and conferences/journals to generate the statistics. It will generate a table ranking the universities by publications count."
            to="/publications-count-by-university"
          />
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>
