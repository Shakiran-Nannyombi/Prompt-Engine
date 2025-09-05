<template>
  <Teleport to="body">
    <Transition
      name="modal"
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click="handleBackdropClick"
      >
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>

        <!-- Modal Container -->
        <div class="flex min-h-full items-center justify-center p-4">
          <Transition
            name="modal-content"
            enter-active-class="transition-all duration-300"
            enter-from-class="opacity-0 scale-95 translate-y-4"
            enter-to-class="opacity-100 scale-100 translate-y-0"
            leave-active-class="transition-all duration-200"
            leave-from-class="opacity-100 scale-100 translate-y-0"
            leave-to-class="opacity-0 scale-95 translate-y-4"
          >
            <div
              v-if="isOpen"
              :class="modalClasses"
              @click.stop
            >
              <!-- Header -->
              <div 
                v-if="$slots.header || showCloseButton" 
                class="flex items-center justify-between px-6 py-4 border-b border-card-border"
              >
                <div class="flex-1">
                  <slot name="header">
                    <h3 class="text-lg font-semibold text-text">
                      {{ title }}
                    </h3>
                  </slot>
                </div>
                
                <!-- Close Button -->
                <button
                  v-if="showCloseButton"
                  type="button"
                  class="ml-4 p-2 text-text hover:text-primary transition-colors rounded-lg hover:bg-secondary"
                  @click="closeModal"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Body -->
              <div :class="bodyClasses">
                <slot name="body">
                  <slot />
                </slot>
              </div>

              <!-- Footer -->
              <div 
                v-if="$slots.footer" 
                class="flex items-center justify-end space-x-3 px-6 py-4 border-t border-card-border"
              >
                <slot name="footer" />
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'xl', 'full'].includes(value)
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  },
  closeOnEscape: {
    type: Boolean,
    default: true
  },
  persistent: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:isOpen', 'close'])

const modalClasses = computed(() => {
  const baseClasses = [
    'relative',
    'bg-card-bg',
    'border',
    'border-card-border',
    'rounded-lg',
    'shadow-xl',
    'max-h-[90vh]',
    'overflow-hidden'
  ]

  const sizeClasses = {
    small: ['w-full', 'max-w-sm'],
    medium: ['w-full', 'max-w-md'],
    large: ['w-full', 'max-w-lg'],
    xl: ['w-full', 'max-w-2xl'],
    full: ['w-full', 'max-w-4xl']
  }

  return [
    ...baseClasses,
    ...sizeClasses[props.size]
  ]
})

const bodyClasses = computed(() => {
  const baseClasses = ['px-6', 'py-4', 'overflow-y-auto']
  
  // Adjust max height based on whether header/footer exist
  const hasHeader = props.$slots?.header || props.title || props.showCloseButton
  const hasFooter = props.$slots?.footer
  
  if (hasHeader && hasFooter) {
    baseClasses.push('max-h-[calc(90vh-8rem)]')
  } else if (hasHeader || hasFooter) {
    baseClasses.push('max-h-[calc(90vh-4rem)]')
  } else {
    baseClasses.push('max-h-[90vh]')
  }
  
  return baseClasses
})

const closeModal = () => {
  if (!props.persistent) {
    emit('update:isOpen', false)
    emit('close')
  }
}

const handleBackdropClick = () => {
  if (props.closeOnBackdrop && !props.persistent) {
    closeModal()
  }
}

const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && props.closeOnEscape && !props.persistent) {
    closeModal()
  }
}

// Handle escape key
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    document.addEventListener('keydown', handleEscapeKey)
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden'
  } else {
    document.removeEventListener('keydown', handleEscapeKey)
    // Restore body scroll
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  if (props.isOpen) {
    document.addEventListener('keydown', handleEscapeKey)
    document.body.style.overflow = 'hidden'
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscapeKey)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* Custom scrollbar for modal body */
.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: var(--color-scrollbar-track);
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}
</style>
