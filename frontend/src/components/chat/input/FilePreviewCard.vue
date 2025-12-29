<template>
  <div class="relative group flex-shrink-0 w-24 h-24 rounded-xl overflow-hidden border border-card-border bg-card-bg animate-fade-in transition-all hover:border-text opacity-100">
    <!-- Image Preview -->
    <div v-if="isImage" class="w-full h-full relative">
      <img :src="file.preview" :alt="file.file.name" class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition-colors" />
    </div>

    <!-- File Icon Preview -->
    <div v-else class="w-full h-full p-3 flex flex-col justify-between">
      <div class="flex items-center gap-2">
        <div class="p-1.5 bg-secondary rounded">
          <svg class="w-4 h-4 text-text opacity-70" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <span class="text-[10px] font-medium text-text opacity-70 uppercase tracking-wider truncate">
          {{ fileExtension }}
        </span>
      </div>
      <div class="space-y-0.5">
        <p class="text-xs font-medium text-text truncate" :title="file.file.name">
          {{ file.file.name }}
        </p>
        <p class="text-[10px] text-text opacity-50">
          {{ formattedSize }}
        </p>
      </div>
    </div>

    <!-- Remove Button -->
    <button
      @click.stop="$emit('remove', file.id)"
      class="absolute top-1 right-1 p-1 bg-black/50 hover:bg-black/70 rounded-full text-white opacity-0 group-hover:opacity-100 transition-opacity"
    >
      <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

    <!-- Upload Status -->
    <div v-if="file.uploadStatus === 'uploading'" class="absolute inset-0 bg-black/40 flex items-center justify-center">
      <svg class="w-5 h-5 text-white animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import './input-styles.css'

const props = defineProps({
  file: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['remove'])

const isImage = computed(() => {
  return props.file.type.startsWith('image/') && props.file.preview
})

const fileExtension = computed(() => {
  return props.file.file.name.split('.').pop()
})

const formattedSize = computed(() => {
  const bytes = props.file.file.size
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
})
</script>

<style scoped>
</style>
