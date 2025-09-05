<template>
  <div class="h-screen bg-gray-50">
    <div class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="w-16 h-16 bg-secondary-100 rounded-full flex-center mx-auto mb-6">
          <svg class="w-8 h-8 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-neutral-900 mb-4">Refiner Interface</h1>
        <p class="text-neutral-600 mb-6">The refiner chat interface will be implemented here</p>
        <RouterLink to="/" class="btn-secondary">
          Back to Home
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>