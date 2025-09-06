<template>
  <div class="coach-progress-tracker">
    <!-- Header -->
    <div class="p-4 border-b border-card-border">
      <h2 class="text-lg font-semibold text-text mb-2">Progress Tracker</h2>
      <div class="text-sm text-text opacity-70 mb-3">
        Current Step: <span class="font-medium text-primary">{{ formattedCurrentStep }}</span>
      </div>
      
      <!-- Progress Bar -->
      <div class="w-full bg-secondary rounded-full h-2.5 mb-3">
        <div 
          class="bg-primary h-2.5 rounded-full transition-all duration-300" 
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>
      <div class="text-xs text-text opacity-50">
        Progress: {{ stepsCompleted }}/{{ totalSteps }} steps completed
      </div>
    </div>

    <!-- Captured Details -->
    <div class="p-4 flex-1 overflow-y-auto">
      <div class="space-y-4">
        <!-- Task Section -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-medium text-text">Task</h3>
            <div class="flex items-center space-x-1">
              <div 
                class="w-2 h-2 rounded-full"
                :class="currentState.task ? 'bg-success' : 'bg-secondary'"
              ></div>
              <span class="text-xs text-text opacity-70">
                {{ currentState.task ? 'Completed' : 'Pending' }}
              </span>
            </div>
          </div>
          <div class="p-3 bg-card-bg border border-card-border rounded-lg">
            <p class="text-sm text-text">
              {{ currentState.task || 'Task not defined yet' }}
            </p>
          </div>
        </div>

        <!-- Context Section -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-medium text-text">Context</h3>
            <div class="flex items-center space-x-1">
              <div 
                class="w-2 h-2 rounded-full"
                :class="currentState.context ? 'bg-success' : 'bg-secondary'"
              ></div>
              <span class="text-xs text-text opacity-70">
                {{ currentState.context ? 'Completed' : 'Pending' }}
              </span>
            </div>
          </div>
          <div class="p-3 bg-card-bg border border-card-border rounded-lg">
            <p class="text-sm text-text">
              {{ currentState.context || 'Context not provided yet' }}
            </p>
          </div>
        </div>

        <!-- References Section -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-medium text-text">References</h3>
            <div class="flex items-center space-x-1">
              <div 
                class="w-2 h-2 rounded-full"
                :class="currentState.references ? 'bg-success' : 'bg-secondary'"
              ></div>
              <span class="text-xs text-text opacity-70">
                {{ currentState.references ? 'Completed' : 'Pending' }}
              </span>
            </div>
          </div>
          <div class="p-3 bg-card-bg border border-card-border rounded-lg">
            <p class="text-sm text-text">
              {{ currentState.references || 'References not provided yet' }}
            </p>
          </div>
        </div>

        <!-- Final Prompt Section -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-medium text-text">Final Prompt</h3>
            <div class="flex items-center space-x-1">
              <div 
                class="w-2 h-2 rounded-full"
                :class="currentState.finalPrompt ? 'bg-success' : 'bg-secondary'"
              ></div>
              <span class="text-xs text-text opacity-70">
                {{ currentState.finalPrompt ? 'Completed' : 'Pending' }}
              </span>
            </div>
          </div>
          <div class="p-3 bg-card-bg border border-card-border rounded-lg">
            <p class="text-sm text-text">
              {{ currentState.finalPrompt || 'Final prompt not created yet' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="p-4 border-t border-card-border space-y-3">
      <BaseButton 
        @click="resetProgress"
        type="outline"
        size="small"
        fullWidth
      >
        Reset Progress
      </BaseButton>
      
      <!-- Completion Section -->
      <div v-if="isCompleted" class="space-y-3">
        <div class="text-center">
          <div class="text-2xl mb-2">🎉</div>
          <p class="text-sm font-medium text-success">Congratulations! Your prompt is ready.</p>
        </div>
        <BaseButton 
          v-if="currentState.finalPrompt"
          @click="downloadPrompt"
          type="primary"
          size="small"
          fullWidth
        >
          Download Final Prompt
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { BaseButton } from '@/components/base'

const props = defineProps({
  currentState: {
    type: Object,
    default: () => ({
      task: '',
      context: '',
      references: '',
      finalPrompt: '',
      currentStep: 'task'
    })
  },
  totalSteps: {
    type: Number,
    default: 4
  }
})

const emit = defineEmits(['reset-progress', 'download-prompt'])

const formattedCurrentStep = computed(() => {
  if (!props.currentState.currentStep) return 'Getting Started'
  return props.currentState.currentStep
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
})

const stepsCompleted = computed(() => {
  let completed = 0
  if (props.currentState.task) completed++
  if (props.currentState.context) completed++
  if (props.currentState.references) completed++
  if (props.currentState.finalPrompt) completed++
  return completed
})

const progressPercentage = computed(() => {
  return (stepsCompleted.value / props.totalSteps) * 100
})

const isCompleted = computed(() => {
  return stepsCompleted.value === props.totalSteps
})

const resetProgress = () => {
  if (confirm('Are you sure you want to reset your progress? This will clear all captured details.')) {
    emit('reset-progress')
  }
}

const downloadPrompt = () => {
  if (!props.currentState.finalPrompt) return
  
  const element = document.createElement('a')
  const file = new Blob([props.currentState.finalPrompt], { type: 'text/plain' })
  element.href = URL.createObjectURL(file)
  element.download = 'engineered_prompt.txt'
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
  
  emit('download-prompt', props.currentState.finalPrompt)
}
</script>

<style scoped>
.coach-progress-tracker {
  @apply flex flex-col h-full bg-card-bg;
}

/* Custom scrollbar */
.coach-progress-tracker .overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.coach-progress-tracker .overflow-y-auto::-webkit-scrollbar-track {
  background: var(--color-scrollbar-track);
  border-radius: 2px;
}

.coach-progress-tracker .overflow-y-auto::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 2px;
}

.coach-progress-tracker .overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}
</style>
