<template>
  <div :class="containerClasses">
    <!-- Logo Spinner (default) -->
    <div v-if="variant === 'logo'" class="logo-spinner">
      <img 
        :src="logoSrc" 
        :alt="altText"
        :class="logoClasses"
        class="animate-spin"
      />
    </div>

    <!-- Dots Spinner -->
    <div v-else-if="variant === 'dots'" class="flex space-x-1">
      <div 
        v-for="i in 3" 
        :key="i"
        :class="dotClasses"
        :style="{ animationDelay: `${(i - 1) * 0.1}s` }"
      ></div>
    </div>

    <!-- Pulse Spinner -->
    <div v-else-if="variant === 'pulse'" :class="pulseClasses"></div>

    <!-- Ring Spinner -->
    <div v-else-if="variant === 'ring'" :class="ringClasses">
      <div class="ring-inner"></div>
    </div>

    <!-- Loading text -->
    <p 
      v-if="text" 
      :class="textClasses"
    >
      {{ text }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'xl'].includes(value)
  },
  variant: {
    type: String,
    default: 'logo',
    validator: (value) => ['logo', 'dots', 'pulse', 'ring'].includes(value)
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'accent', 'white', 'text'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  centered: {
    type: Boolean,
    default: false
  }
})

const logoSrc = computed(() => {
  // Use the logo from public folder
  return '/PE_logo.svg'
})

const altText = computed(() => {
  return props.text || 'Loading...'
})

const containerClasses = computed(() => {
  const baseClasses = ['inline-flex', 'items-center', 'justify-center']
  
  if (props.centered) {
    baseClasses.push('w-full', 'h-full', 'min-h-[200px]')
  }
  
  if (props.text) {
    baseClasses.push('flex-col', 'space-y-2')
  } else {
    baseClasses.push('flex-row')
  }
  
  return baseClasses
})

const logoClasses = computed(() => {
  const sizeClasses = {
    small: ['w-6', 'h-6'],
    medium: ['w-8', 'h-8'],
    large: ['w-12', 'h-12'],
    xl: ['w-16', 'h-16']
  }
  
  return sizeClasses[props.size]
})

const dotClasses = computed(() => {
  const baseClasses = ['rounded-full', 'animate-bounce']
  
  const sizeClasses = {
    small: ['w-1', 'h-1'],
    medium: ['w-2', 'h-2'],
    large: ['w-3', 'h-3'],
    xl: ['w-4', 'h-4']
  }
  
  const colorClasses = {
    primary: ['bg-primary'],
    secondary: ['bg-secondary'],
    accent: ['bg-accent'],
    white: ['bg-white'],
    text: ['bg-text']
  }
  
  return [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...colorClasses[props.color]
  ]
})

const pulseClasses = computed(() => {
  const baseClasses = ['rounded-full', 'animate-pulse']
  
  const sizeClasses = {
    small: ['w-4', 'h-4'],
    medium: ['w-6', 'h-6'],
    large: ['w-8', 'h-8'],
    xl: ['w-12', 'h-12']
  }
  
  const colorClasses = {
    primary: ['bg-primary'],
    secondary: ['bg-secondary'],
    accent: ['bg-accent'],
    white: ['bg-white'],
    text: ['bg-text']
  }
  
  return [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...colorClasses[props.color]
  ]
})

const ringClasses = computed(() => {
  const baseClasses = [
    'rounded-full',
    'border-2',
    'border-transparent',
    'animate-spin'
  ]
  
  const sizeClasses = {
    small: ['w-4', 'h-4', 'border-t-2'],
    medium: ['w-6', 'h-6', 'border-t-2'],
    large: ['w-8', 'h-8', 'border-t-2'],
    xl: ['w-12', 'h-12', 'border-t-2']
  }
  
  const colorClasses = {
    primary: ['border-t-primary'],
    secondary: ['border-t-secondary'],
    accent: ['border-t-accent'],
    white: ['border-t-white'],
    text: ['border-t-text']
  }
  
  return [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...colorClasses[props.color]
  ]
})

const textClasses = computed(() => {
  const baseClasses = ['text-text', 'font-medium']
  
  const sizeClasses = {
    small: ['text-xs'],
    medium: ['text-sm'],
    large: ['text-base'],
    xl: ['text-lg']
  }
  
  return [
    ...baseClasses,
    ...sizeClasses[props.size]
  ]
})
</script>

<style scoped>
.logo-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.ring-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50%;
  height: 50%;
  border-radius: 50%;
  background-color: currentColor;
  opacity: 0.3;
}
</style>
