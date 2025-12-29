<template>
  <div class="relative" ref="dropdownRef">
    <button
      @click="isOpen = !isOpen"
      class="inline-flex items-center justify-center relative shrink-0 transition font-base duration-300 ease-[cubic-bezier(0.165,0.85,0.45,1)] h-8 rounded-xl px-3 min-w-[4rem] active:scale-[0.98] whitespace-nowrap !text-xs pl-2.5 pr-2 gap-1 text-text opacity-70 hover:opacity-100 hover:bg-secondary"
      :class="{ 'bg-secondary opacity-100': isOpen }"
    >
      <div class="font-ui inline-flex gap-[3px] text-[14px] h-[14px] leading-none items-baseline">
        <div class="flex items-center gap-[4px]">
          <div class="whitespace-nowrap select-none font-medium">{{ currentModel.name }}</div>
        </div>
      </div>
      <div class="flex items-center justify-center opacity-75 w-5 h-5">
        <svg 
          class="shrink-0 opacity-75 transition-transform duration-200 w-4 h-4" 
          :class="{ 'rotate-180': isOpen }"
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </button>

    <div v-if="isOpen" class="absolute bottom-full right-0 mb-2 w-[260px] bg-card-bg border border-card-border rounded-2xl shadow-2xl overflow-hidden z-50 flex flex-col p-1.5 animate-fade-in origin-bottom-right">
      <button
        v-for="model in models"
        :key="model.id"
        @click="selectModel(model.id)"
        class="w-full text-left px-3 py-2.5 rounded-xl flex items-start justify-between group transition-colors hover:bg-secondary"
      >
        <div class="flex flex-col gap-0.5">
          <div class="flex items-center gap-2">
            <span class="text-[13px] font-semibold text-text">
              {{ model.name }}
            </span>
            <span 
              v-if="model.badge"
              class="px-1.5 py-[1px] rounded-full text-[10px] font-medium border"
              :class="model.badge === 'Upgrade' ? 'border-primary/30 text-primary bg-primary/10' : 'border-card-border text-text opacity-70'"
            >
              {{ model.badge }}
            </span>
          </div>
          <span class="text-[11px] text-text opacity-60">
            {{ model.description }}
          </span>
        </div>
        <svg 
          v-if="selectedModel === model.id"
          class="w-4 h-4 text-primary mt-1" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </button>

      <div class="h-px bg-card-border my-1 mx-2" />

      <button class="w-full text-left px-3 py-2.5 rounded-xl flex items-center justify-between group transition-colors hover:bg-secondary text-text">
        <span class="text-[13px] font-semibold">More models</span>
        <svg class="w-4 h-4 -rotate-90 text-text opacity-50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import './input-styles.css'

const props = defineProps({
  models: {
    type: Array,
    required: true
  },
  selectedModel: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['select'])

const isOpen = ref(false)
const dropdownRef = ref(null)

const currentModel = computed(() => {
  return props.models.find(m => m.id === props.selectedModel) || props.models[0]
})

const selectModel = (id) => {
  emit('select', id)
  isOpen.value = false
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<style scoped>
</style>
