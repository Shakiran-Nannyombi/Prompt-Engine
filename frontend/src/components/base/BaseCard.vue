<template>
  <div :class="cardClasses">
    <!-- Header Slot -->
    <div 
      v-if="$slots.header" 
      class="px-6 py-4 border-b border-card-border"
    >
      <slot name="header" />
    </div>

    <!-- Default Content Slot -->
    <div :class="contentClasses">
      <slot />
    </div>

    <!-- Footer Slot -->
    <div 
      v-if="$slots.footer" 
      class="px-6 py-4 border-t border-card-border"
    >
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'elevated', 'outlined', 'flat'].includes(value)
  },
  padding: {
    type: String,
    default: 'medium',
    validator: (value) => ['none', 'small', 'medium', 'large'].includes(value)
  },
  hover: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: String,
    default: 'lg',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl', '2xl'].includes(value)
  }
})

const emit = defineEmits(['click'])

const cardClasses = computed(() => {
  const baseClasses = [
    'bg-card-bg',
    'border',
    'border-card-border',
    'transition-all',
    'duration-200'
  ]

  // Rounded classes
  const roundedClasses = {
    none: [],
    sm: ['rounded-sm'],
    md: ['rounded-md'],
    lg: ['rounded-lg'],
    xl: ['rounded-xl'],
    '2xl': ['rounded-2xl']
  }

  // Variant classes
  const variantClasses = {
    default: ['shadow-sm'],
    elevated: ['shadow-lg', 'hover:shadow-xl'],
    outlined: ['shadow-none', 'border-2'],
    flat: ['shadow-none', 'border-0']
  }

  // Interactive classes
  const interactiveClasses = []
  if (props.clickable) {
    interactiveClasses.push('cursor-pointer', 'hover:shadow-md', 'hover:scale-[1.02]')
  }
  if (props.hover) {
    interactiveClasses.push('hover:shadow-md')
  }

  return [
    ...baseClasses,
    ...roundedClasses[props.rounded],
    ...variantClasses[props.variant],
    ...interactiveClasses
  ]
})

const contentClasses = computed(() => {
  const paddingClasses = {
    none: [],
    small: ['p-4'],
    medium: ['p-6'],
    large: ['p-8']
  }

  return paddingClasses[props.padding]
})

const handleClick = (event) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>
