

<script setup lang="ts">
import { reactive } from 'vue'
import type { HomeProfile, HeatingType, InsulationLevel, WindowsType, RoofType } from '@/types/home'
import { Loader2, ArrowRight } from 'lucide-vue-next'

// Define props for loading state
defineProps<{
  isLoading: boolean
}>()

// Define emits to send data back to parent component
const emit = defineEmits<{
  (e: 'submit', home: HomeProfile): void
}>()

// Form data setup using reactive
const formData = reactive<HomeProfile>({
  size_sqft: 1500,
  year_built: 2000,
  heating_type: 'gas',
  insulation_level: 'moderate',
  windows_type: 'double',
  roof_type: 'pitched',
  monthly_energy_bill: 150,
  num_occupants: 3,
  location: '',
})

// Form options
const HEATING_OPTIONS: { value: HeatingType; label: string }[] = [
  { value: 'gas', label: 'Natural Gas' },
  { value: 'electric', label: 'Electric' },
  { value: 'heat_pump', label: 'Heat Pump' },
  { value: 'oil', label: 'Oil' },
  { value: 'solar', label: 'Solar Thermal' },
]

const INSULATION_OPTIONS: { value: InsulationLevel; label: string }[] = [
  { value: 'minimal', label: 'Minimal' },
  { value: 'moderate', label: 'Moderate' },
  { value: 'good', label: 'Good' },
  { value: 'excellent', label: 'Excellent' },
]

const WINDOWS_OPTIONS: { value: WindowsType; label: string }[] = [
  { value: 'single', label: 'Single Pane' },
  { value: 'double', label: 'Double Pane' },
  { value: 'triple', label: 'Triple Pane' }
]

const ROOF_OPTIONS: { value: RoofType; label: string }[] = [
  { value: 'flat', label: 'Flat' },
  { value: 'pitched', label: 'Pitched/Sloped' },
  { value: 'metal', label: 'Metal' },
  { value: 'tile', label: 'Tile' }
]

// Submit form
function handleSubmit() {
  emit('submit', formData)
}
</script>

<template>
  <div class="bg-white rounded-lg shadow-lg p-6">
    <h2 class="text-xl font-bold text-gray-700 mb-4">Tell Us About Your Home</h2>
    <p class="text-gray-500 mb-6">Provide details about your home to receive personalized energy-saving recommendations.</p>

    <form @submit.prevent="handleSubmit" class="space-y-8">
      <!-- Home Size and Build Year -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div class="space-y-2">
          <label for="size" class="block text-sm font-medium text-gray-700">Home Size (sq ft)</label>
          <input
            id="size"
            type="number"
            min="100"
            max="50000"
            v-model.number="formData.size_sqft"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="space-y-2">
          <label for="year" class="block text-sm font-medium text-gray-700">Build Year</label>
          <input
            id="year"
            type="number"
            min="1800"
            max="2025"
            v-model.number="formData.year_built"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- Heating and Insulation -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div class="space-y-2">
          <label for="heating_type" class="block text-sm font-medium text-gray-700">Heating Type</label>
          <select
            id="heating_type"
            v-model="formData.heating_type"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option v-for="opt in HEATING_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>

        <div class="space-y-2">
          <label for="insulation_level" class="block text-sm font-medium text-gray-700">Insulation Level</label>
          <select
            id="insulation_level"
            v-model="formData.insulation_level"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option v-for="opt in INSULATION_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>
      </div>

      <!-- Windows and Roof -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div class="space-y-2">
          <label for="windows_type" class="block text-sm font-medium text-gray-700">Windows Type</label>
          <select
            id="windows_type"
            v-model="formData.windows_type"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option v-for="opt in WINDOWS_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>

        <div class="space-y-2">
          <label for="roof_type" class="block text-sm font-medium text-gray-700">Roof Type</label>
          <select
            id="roof_type"
            v-model="formData.roof_type"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option v-for="opt in ROOF_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>
      </div>

      
      <!-- Occupants and Location -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div class="space-y-2">
          <label for="monthly_bill" class="block text-sm font-medium text-gray-700">Monthly Energy Bill (Euro)</label>
          <input
            id="monthly_bill"
            type="number"
            min="100"
            max="5000"
            v-model.number="formData.monthly_energy_bill"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div class="space-y-2">
          <label for="occupants" class="block text-sm font-medium text-gray-700">Number of Occupants</label>
          <input
            id="occupants"
            type="number"
            min="1"
            max="20"
            v-model.number="formData.num_occupants"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="space-y-2">
          <label for="location" class="block text-sm font-medium text-gray-700">Location (optional)</label>
          <input
            id="location"
            type="text"
            v-model="formData.location"
            placeholder="City, State/Country"
            class="w-full p-3 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <button
        type="submit"
        class="w-full p-4 bg-blue-500 text-white rounded-md shadow-sm text-lg font-medium hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        :disabled="isLoading"
      >
        <template v-if="isLoading">
          <Loader2 class="w-5 h-5 mr-2 animate-spin" />
          Analyzing Your Home...
        </template>
        <template v-else>
          Get Energy Recommendations
          <ArrowRight class="w-5 h-5 ml-2" />
        </template>
      </button>
    </form>
  </div>
</template>

