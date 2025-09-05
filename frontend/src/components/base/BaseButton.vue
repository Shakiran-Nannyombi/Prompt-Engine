<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || isLoading"
    @click="handleClick"
    :type="htmlType"
  >
    <!-- Loading spinner -->
    <BaseSpinner 
      v-if="isLoading" 
      size="small" 
      class="mr-2"
    />
    
    <!-- Button content -->
    <slot>
      {{ label }}
    </slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import BaseSpinner from './BaseSpinner.vue'

const props = defineProps({
  type: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: ''
  },
  htmlType: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },
  fullWidth: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const buttonClasses = computed(() => {
  const baseClasses = [
    'inline-flex',
    'items-center',
    'justify-center',
    'font-medium',
    'rounded-lg',
    'transition-all',
    'duration-200',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-2',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
    'disabled:pointer-events-none'
  ]

  // Size classes
  const sizeClasses = {
    small: ['px-3', 'py-1.5', 'text-sm'],
    medium: ['px-4', 'py-2', 'text-sm'],
    large: ['px-6', 'py-3', 'text-base']
  }

  // Type classes
  const typeClasses = {
    primary: [
      'bg-primary',
      'text-white',
      'hover:bg-primary-600',
      'focus:ring-primary-500',
      'shadow-sm',
      'hover:shadow-md'
    ],
    secondary: [
      'bg-secondary',
      'text-text',
      'hover:bg-accent',
      'focus:ring-accent',
      'border',
      'border-accent'
    ],
    outline: [
      'bg-transparent',
      'text-primary',
      'border',
      'border-primary',
      'hover:bg-primary',
      'hover:text-white',
      'focus:ring-primary-500'
    ],
    ghost: [
      'bg-transparent',
      'text-text',
      'hover:bg-secondary',
      'focus:ring-accent'
    ]
  }

  // Full width
  const widthClasses = props.fullWidth ? ['w-full'] : []

  return [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...typeClasses[props.type],
    ...widthClasses
  ]
})

const handleClick = (event) => {
  if (!props.disabled && !props.isLoading) {
    emit('click', event)
  }
}
</script>
