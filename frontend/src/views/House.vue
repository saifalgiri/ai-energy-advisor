
<script setup lang="ts">
import { ref } from 'vue'

import type { HomeProfile, Recommendation } from '@/types/home'
import HomeForm from '@/components/HomeForm.vue'
import RecommendationsList from '@/components/RecommendationsList.vue'
import { useHomeApi } from '@/composables/useHomeApi'

type View = 'form' | 'recommendations'

// State
const view = ref<View>('form')
const recommendations = ref<Recommendation[]>([])
const homeId = ref<string | null>(null)

const { isLoading, error, createHome, getAdvice, clearError } = useHomeApi()

// Submit handler (from HomeForm)
async function handleSubmit(homeData: HomeProfile) {
  clearError()
  recommendations.value = []

  const createdHome = await createHome(homeData)

  if (!createdHome?.id) {
    alert('Failed to create home profile')
    return
  }

  homeId.value = createdHome.id
  view.value = 'recommendations'

  await getAdvice(
    createdHome.id,
    (recommendation) => {
      recommendations.value.push(recommendation)
    },
    () => {
      console.log('Analysis complete')
    }
  )
}

// Back handler (from RecommendationsList)
function handleBack() {
  view.value = 'form'
  recommendations.value = []
  homeId.value = null
}
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- <Header /> -->

    <main class="container mx-auto px-4 py-8 max-w-4xl">
      <!-- Hero -->
      <div
        v-if="view === 'form'"
        class="text-center mb-10 space-y-4"
      >
        <h2 class="text-4xl font-bold">
          Make Your Home
          <span class="text-green-600">Energy Efficient</span>
        </h2>
        <p class="text-muted-foreground max-w-2xl mx-auto">
          Get personalized AI-powered recommendations
        </p>
      </div>

      <!-- Error -->
      <div
        v-if="error"
        class="mb-6 p-4 rounded-lg bg-destructive/10 text-destructive"
      >
        {{ error }}
      </div>

      <!-- HomeForm usage -->
      <HomeForm
        v-if="view === 'form'"
        :is-loading="isLoading"
        @submit="handleSubmit"
      />

      <!-- Recommendations -->
      <RecommendationsList
        v-else
        :recommendations="recommendations"
        :is-loading="isLoading"
        @back="handleBack"
      />
    </main>
  </div>
</template>
