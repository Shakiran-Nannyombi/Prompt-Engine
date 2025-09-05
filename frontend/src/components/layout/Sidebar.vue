<template>
  <aside 
    :class="sidebarClasses"
    :style="{ width: isCollapsed ? collapsedWidth : width }"
  >
    <!-- Sidebar Header (Optional) -->
    <div v-if="showHeader || $slots.header" class="sidebar-header">
      <slot name="header">
        <div class="flex items-center justify-between p-4">
          <h3 class="text-text font-semibold">{{ title }}</h3>
          <button
            v-if="collapsible"
            @click="toggleCollapse"
            class="p-1 rounded text-text hover:text-primary hover:bg-secondary transition-colors"
            :title="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          >
            <svg 
              class="w-4 h-4 transition-transform duration-200"
              :class="{ 'rotate-180': isCollapsed }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        </div>
      </slot>
    </div>

    <!-- Sidebar Content -->
    <div class="sidebar-content">
      <slot />
    </div>

    <!-- Sidebar Footer (Optional) -->
    <div v-if="$slots.footer" class="sidebar-footer">
      <slot name="footer" />
    </div>

    <!-- Mobile Overlay -->
    <div
      v-if="isMobile && isOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
      @click="closeSidebar"
    ></div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  width: {
    type: String,
    default: '280px'
  },
  collapsedWidth: {
    type: String,
    default: '60px'
  },
  position: {
    type: String,
    default: 'left',
    validator: (value) => ['left', 'right'].includes(value)
  },
  collapsible: {
    type: Boolean,
    default: false
  },
  defaultCollapsed: {
    type: Boolean,
    default: false
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  title: {
    type: String,
    default: ''
  },
  sticky: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'floating', 'bordered'].includes(value)
  }
})

const emit = defineEmits(['toggle', 'collapse', 'expand'])

const isCollapsed = ref(props.defaultCollapsed)
const isMobile = ref(false)
const isOpen = ref(true)

const sidebarClasses = computed(() => {
  const baseClasses = [
    'bg-card-bg',
    'transition-all',
    'duration-300',
    'ease-in-out',
    'flex',
    'flex-col',
    'h-full'
  ]

  // Position classes
  const positionClasses = {
    left: ['border-r', 'border-card-border'],
    right: ['border-l', 'border-card-border']
  }

  // Variant classes
  const variantClasses = {
    default: [],
    floating: ['shadow-lg', 'rounded-lg', 'm-4'],
    bordered: ['border-2', 'border-card-border']
  }

  // Sticky classes
  const stickyClasses = props.sticky ? ['sticky', 'top-16'] : []

  // Mobile classes
  const mobileClasses = isMobile.value ? [
    'fixed',
    'top-16',
    'bottom-0',
    'z-50',
    'transform',
    'transition-transform',
    'duration-300',
    'ease-in-out'
  ] : []

  // Mobile position classes
  const mobilePositionClasses = isMobile.value ? {
    left: ['left-0', isOpen.value ? 'translate-x-0' : '-translate-x-full'],
    right: ['right-0', isOpen.value ? 'translate-x-0' : 'translate-x-full']
  } : {}

  return [
    ...baseClasses,
    ...positionClasses[props.position],
    ...variantClasses[props.variant],
    ...stickyClasses,
    ...mobileClasses,
    ...(mobilePositionClasses[props.position] || [])
  ]
})

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
  emit('toggle', isCollapsed.value)
  
  if (isCollapsed.value) {
    emit('collapse')
  } else {
    emit('expand')
  }
}

const closeSidebar = () => {
  if (isMobile.value) {
    isOpen.value = false
  }
}

const checkMobile = () => {
  isMobile.value = window.innerWidth < 1024 // lg breakpoint
  if (!isMobile.value) {
    isOpen.value = true
  }
}

// Handle window resize
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

// Expose methods for parent components
defineExpose({
  toggleCollapse,
  closeSidebar,
  isCollapsed: computed(() => isCollapsed.value),
  isOpen: computed(() => isOpen.value)
})
</script>

<style scoped>
.sidebar-header {
  @apply border-b border-card-border flex-shrink-0;
}

.sidebar-content {
  @apply flex-1 overflow-y-auto;
}

.sidebar-footer {
  @apply border-t border-card-border flex-shrink-0;
}

/* Custom scrollbar for sidebar content */
.sidebar-content::-webkit-scrollbar {
  width: 4px;
}

.sidebar-content::-webkit-scrollbar-track {
  background: var(--color-scrollbar-track);
  border-radius: 2px;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 2px;
}

.sidebar-content::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}

/* Collapsed state styles */
.sidebar-content:has(.collapsed-content) {
  @apply px-2;
}

.collapsed-content {
  @apply flex flex-col items-center space-y-2;
}

.collapsed-content .nav-item {
  @apply w-full flex justify-center p-2;
}

.collapsed-content .nav-item span {
  @apply hidden;
}

.collapsed-content .nav-item svg {
  @apply w-5 h-5;
}
</style>
