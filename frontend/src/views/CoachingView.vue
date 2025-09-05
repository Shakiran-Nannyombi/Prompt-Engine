<template>
  <div class="h-screen bg-gray-50">
    <div class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="w-16 h-16 bg-primary-100 rounded-full flex-center mx-auto mb-6">
          <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-neutral-900 mb-4">Coaching Interface</h1>
        <p class="text-neutral-600 mb-6">The coaching chat interface will be implemented here</p>
        <RouterLink to="/" class="btn-primary">
          Back to Home
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>