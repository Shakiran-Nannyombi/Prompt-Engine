<template>
  <div class="w-full">
    <!-- Label -->
    <label 
      v-if="label" 
      :for="inputId"
      class="block text-sm font-medium text-text mb-2"
    >
      {{ label }}
      <span v-if="required" class="text-error ml-1">*</span>
    </label>

    <!-- Input Container -->
    <div class="relative">
      <!-- Input Field -->
      <input
        :id="inputId"
        ref="inputRef"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
        @keydown="handleKeydown"
        v-bind="$attrs"
      />

      <!-- Icon (if provided) -->
      <div 
        v-if="$slots.icon" 
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
      >
        <slot name="icon" />
      </div>

      <!-- Right Icon (if provided) -->
      <div 
        v-if="$slots.rightIcon" 
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
      >
        <slot name="rightIcon" />
      </div>

      <!-- Clear Button -->
      <button
        v-if="showClearButton && modelValue && !disabled && !readonly"
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-text hover:text-primary transition-colors"
        @click="clearInput"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Error Message -->
    <p 
      v-if="errorMessage" 
      class="mt-2 text-sm text-error"
    >
      {{ errorMessage }}
    </p>

    <!-- Helper Text -->
    <p 
      v-if="helperText && !errorMessage" 
      class="mt-2 text-sm text-text opacity-70"
    >
      {{ helperText }}
    </p>
  </div>
</template>

<script setup>
import { computed, ref, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'password', 'email', 'number', 'tel', 'url', 'search'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  errorMessage: {
    type: String,
    default: ''
  },
  helperText: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  showClearButton: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'keydown', 'clear'])

const inputRef = ref(null)
const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const inputClasses = computed(() => {
  const baseClasses = [
    'block',
    'w-full',
    'rounded-lg',
    'border',
    'transition-all',
    'duration-200',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-2',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
    'disabled:bg-secondary'
  ]

  // Size classes
  const sizeClasses = {
    small: ['px-3', 'py-1.5', 'text-sm'],
    medium: ['px-4', 'py-2', 'text-sm'],
    large: ['px-4', 'py-3', 'text-base']
  }

  // State classes
  const stateClasses = props.errorMessage
    ? [
        'border-error',
        'focus:ring-error-500',
        'bg-error-50'
      ]
    : [
        'border-input-border',
        'bg-input-bg',
        'text-text',
        'focus:border-primary',
        'focus:ring-primary-500'
      ]

  // Icon padding
  const iconPadding = props.$slots?.icon ? ['pl-10'] : []
  const rightIconPadding = (props.$slots?.rightIcon || props.showClearButton) ? ['pr-10'] : []

  return [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...stateClasses,
    ...iconPadding,
    ...rightIconPadding
  ]
})

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const handleKeydown = (event) => {
  emit('keydown', event)
}

const clearInput = () => {
  emit('update:modelValue', '')
  emit('clear')
  nextTick(() => {
    inputRef.value?.focus()
  })
}

// Expose focus method for parent components
defineExpose({
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur()
})
</script>
