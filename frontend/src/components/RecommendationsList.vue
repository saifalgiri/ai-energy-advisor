

<script setup lang="ts">
import type { Recommendation } from '@/types/home'
import RecommendationCard from '@/components/RecommendationCard.vue'

const props = defineProps<{
  recommendations: Recommendation[]
  isLoading: boolean
}>()

const emit = defineEmits<{
  (e: 'back'): void
}>()
</script>

<template>
  <div class="space-y-6">
    <!-- Header Card -->
    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="bg-gradient-to-r from-blue-500 to-teal-500 pb-6 px-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="p-2 rounded-xl bg-primary/10">
              <!-- Lightbulb icon -->
              <span class="w-6 h-6 text-primary">💡</span>
            </div>
            <div>
              <h2 class="text-2xl text-white font-semibold">
                Your Energy Recommendations
              </h2>
              <p class="text-gray-200">
                <template v-if="props.isLoading">
                  Analyzing your home and generating personalized advice...
                </template>
                <template v-else>
                  {{ props.recommendations.length }} recommendations tailored for your home
                </template>
              </p>
            </div>
          </div>
          <!-- Back Button (Desktop) -->
          <button
            class="hidden sm:flex bg-transparent text-white border border-white rounded-lg px-4 py-2 hover:bg-white hover:text-gray-800"
            @click="emit('back')"
          >
            <span class="w-4 h-4 mr-2">←</span>
            Edit Home Details
          </button>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="props.isLoading && props.recommendations.length === 0" class="py-16 text-center">
        <div class="flex flex-col items-center justify-center space-y-4">
          <div class="relative">
            <div class="p-4 rounded-full bg-primary/10 animate-pulse">
              <span class="text-primary text-3xl">✨</span>
            </div>
            <span class="w-6 h-6 text-primary absolute animate-spin">🔄</span>
          </div>
          <div class="space-y-2">
            <h3 class="text-lg font-medium">AI is analyzing your home...</h3>
            <p class="text-gray-500 text-sm max-w-md">
              Our AI is reviewing your home details and generating personalized energy-saving recommendations. This usually takes a few seconds.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Back Button -->
    <button
      class="sm:hidden w-full bg-transparent text-primary border border-primary rounded-lg px-4 py-2 hover:bg-primary hover:text-white"
      @click="emit('back')"
    >
      <span class="w-4 h-4 mr-2">←</span>
      Edit Home Details
    </button>

    <!-- Recommendations Grid -->
    <div v-if="props.recommendations.length > 0" class="grid gap-4 md:grid-cols-2">
      <RecommendationCard
        v-for="(rec, index) in props.recommendations"
        :key="`${rec.title}-${index}`"
        :recommendation="rec"
        :index="index"
      />
    </div>

    <!-- Loading More Recommendations Indicator -->
    <div v-if="props.isLoading && props.recommendations.length > 0" class="flex items-center justify-center gap-2 py-4 text-gray-500">
      <span class="animate-spin">🔄</span>
      <span class="text-sm">Loading more recommendations...</span>
    </div>
  </div>
</template>

