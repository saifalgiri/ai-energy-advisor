

<script setup lang="ts">
import { computed } from 'vue'
import type { Recommendation } from '@/types/home'

const props = defineProps<{
  recommendation: Recommendation
  index: number
}>()

// Category configurations
const CATEGORY_CONFIG = {
  heating: { icon: '🔥', color: 'text-orange-500', bg: 'bg-orange-500/10' },
  insulation: { icon: '🧣', color: 'text-blue-500', bg: 'bg-blue-500/10' },
  windows: { icon: '🌬️', color: 'text-cyan-500', bg: 'bg-cyan-500/10' },
  appliances: { icon: '🔌', color: 'text-purple-500', bg: 'bg-purple-500/10' },
  habits: { icon: '🍃', color: 'text-green-500', bg: 'bg-green-500/10' },
  renewable: { icon: '☀️', color: 'text-yellow-500', bg: 'bg-yellow-500/10' },
} as const

const PRIORITY_CONFIG = {
  high: { label: 'High Priority', variant: 'bg-red-500' },
  medium: { label: 'Medium Priority', variant: 'bg-yellow-500' },
  low: { label: 'Low Priority', variant: 'bg-green-500' },
} as const

const categoryConfig = computed(() => {
  return CATEGORY_CONFIG[props.recommendation.category] ?? CATEGORY_CONFIG.habits
})

const priorityConfig = computed(() => {
  return PRIORITY_CONFIG[props.recommendation.priority]
})

const animationDelay = computed(() => ({
  animationDelay: `${props.index * 100}ms`,
}))
</script>

<template>
  <!-- Card container with dynamic styles and animations -->
  <div
    :class="[
      'overflow-hidden shadow-lg rounded-lg transition-all duration-300',
      'border-l-4',
      recommendation.priority === 'high' && 'border-l-red-500',
      recommendation.priority === 'medium' && 'border-l-yellow-500',
      recommendation.priority === 'low' && 'border-l-green-500',
    ]"
    :style="animationDelay"
  >
    <!-- Card Header -->
    <div class="p-6 flex items-start justify-between">
      <div class="flex items-start gap-3">
        <!-- Icon with dynamic category background -->
        <div :class="['p-3 rounded-lg', categoryConfig.bg]">
          <span :class="['text-3xl', categoryConfig.color]">{{ categoryConfig.icon }}</span>
        </div>

        <div class="space-y-2">
          <h3 class="text-lg font-semibold text-gray-800">{{ props.recommendation.title }}</h3>
          <span
            :class="[
              'text-xs font-medium text-white py-1 px-2 rounded-full',
              priorityConfig.variant
            ]"
          >
            {{ priorityConfig.label }}
          </span>
        </div>
      </div>
    </div>

    <!-- Card Content -->
    <div class="p-6 space-y-4">
      <!-- Recommendation Description -->
      <p class="text-sm text-gray-600">{{ props.recommendation.description }}</p>

      <!-- Estimated Cost and Savings -->
      <div class="grid grid-cols-2 gap-3">
        <div class="flex items-center gap-3 p-4 rounded-lg bg-gray-100">
          <span class="text-gray-500 text-lg">💸</span>
          <div>
            <p class="text-xs text-gray-500">Est. Cost</p>
            <p class="text-sm font-medium text-gray-700">{{ props.recommendation.estimated_cost }}</p>
          </div>
        </div>

        <div class="flex items-center gap-3 p-4 rounded-lg bg-blue-100">
          <span class="text-blue-500 text-lg">📉</span>
          <div>
            <p class="text-xs text-gray-500">Est. Savings</p>
            <p class="text-sm font-medium text-blue-500">{{ props.recommendation.estimated_savings }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

