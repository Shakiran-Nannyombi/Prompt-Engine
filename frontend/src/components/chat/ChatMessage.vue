<template>
  <div 
    class="chat-message flex"
    :class="messageClasses"
  >
    <!-- Avatar (for assistant messages) -->
    <div v-if="message.sender === 'assistant'" class="message-avatar flex-shrink-0 mr-3">
      <div class="w-8 h-8 rounded-full bg-accent flex items-center justify-center">
        <svg class="w-4 h-4 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      </div>
    </div>

    <!-- Message Content -->
    <div class="message-content flex-1 max-w-3xl">
      <!-- Message Bubble -->
      <div :class="bubbleClasses">
        <!-- Message Text -->
        <div class="message-text">
          <!-- Markdown Content -->
          <div 
            v-if="enableMarkdown && message.sender === 'assistant'"
            v-html="renderedMarkdown"
            class="prose prose-sm max-w-none"
            :class="proseClasses"
          ></div>
          
          <!-- Plain Text -->
          <div v-else class="whitespace-pre-wrap">{{ message.content }}</div>
        </div>

        <!-- Message Actions -->
        <div v-if="showActions" class="message-actions mt-2 flex items-center space-x-2">
          <button
            @click="handleCopyMessage"
            class="text-xs text-text opacity-50 hover:opacity-100 transition-opacity"
            title="Copy message"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
          
          <button
            v-if="message.sender === 'assistant' && allowRegenerate"
            @click="handleRegenerateMessage"
            class="text-xs text-text opacity-50 hover:opacity-100 transition-opacity"
            title="Regenerate message"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>

        <!-- Timestamp -->
        <div v-if="showTimestamp" class="message-timestamp mt-1">
          <span class="text-xs text-text opacity-50">
            {{ formatTimestamp(message.timestamp) }}
          </span>
        </div>
      </div>
    </div>

    <!-- User Avatar (for user messages) -->
    <div v-if="message.sender === 'user'" class="message-avatar flex-shrink-0 ml-3">
      <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true,
    validator: (message) => {
      return message && 
             typeof message.content === 'string' && 
             ['user', 'assistant', 'system'].includes(message.sender)
    }
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'coach', 'refiner'].includes(value)
  },
  showTimestamp: {
    type: Boolean,
    default: true
  },
  enableMarkdown: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  allowRegenerate: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['copy-message', 'regenerate-message'])

// Simple markdown renderer (you can replace this with a proper markdown library)
const renderedMarkdown = computed(() => {
  if (!props.enableMarkdown || props.message.sender !== 'assistant') {
    return props.message.content
  }

  let content = props.message.content

  // Code blocks
  content = content.replace(/```([\s\S]*?)```/g, '<pre class="bg-secondary p-3 rounded-lg overflow-x-auto"><code>$1</code></pre>')
  
  // Inline code
  content = content.replace(/`([^`]+)`/g, '<code class="bg-secondary px-1 py-0.5 rounded text-sm">$1</code>')
  
  // Bold text
  content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  
  // Italic text
  content = content.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  // Links
  content = content.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-primary hover:underline" target="_blank" rel="noopener noreferrer">$1</a>')
  
  // Line breaks
  content = content.replace(/\n/g, '<br>')
  
  // Lists
  content = content.replace(/^\* (.+)$/gm, '<li>$1</li>')
  content = content.replace(/(<li>.*<\/li>)/s, '<ul class="list-disc list-inside space-y-1 my-2">$1</ul>')
  
  content = content.replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
  content = content.replace(/(<li>.*<\/li>)/s, '<ol class="list-decimal list-inside space-y-1 my-2">$1</ol>')

  return content
})

const messageClasses = computed(() => {
  return props.message.sender === 'user' ? 'justify-end' : 'justify-start'
})

const bubbleClasses = computed(() => {
  const baseClasses = ['rounded-lg', 'px-4', 'py-3', 'max-w-full']
  
  if (props.message.sender === 'user') {
    return [
      ...baseClasses,
      'bg-primary',
      'text-white',
      'rounded-br-sm'
    ]
  } else {
    const variantClasses = {
      default: ['bg-card-bg', 'border', 'border-card-border', 'text-text'],
      coach: ['bg-card-bg', 'border', 'border-card-border', 'text-text'],
      refiner: ['bg-card-bg', 'border', 'border-card-border', 'text-text']
    }
    
    return [
      ...baseClasses,
      ...variantClasses[props.variant],
      'rounded-bl-sm'
    ]
  }
})

const proseClasses = computed(() => {
  return {
    'prose-invert': props.message.sender === 'user',
    'prose-primary': props.variant === 'coach',
    'prose-accent': props.variant === 'refiner'
  }
})

const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffInHours = (now - date) / (1000 * 60 * 60)
  
  if (diffInHours < 24) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else {
    return date.toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
  }
}

const handleCopyMessage = () => {
  navigator.clipboard.writeText(props.message.content).then(() => {
    // You could emit a success event or show a toast here
    console.log('Message copied to clipboard')
  }).catch(err => {
    console.error('Failed to copy message:', err)
  })
  
  emit('copy-message', props.message)
}

const handleRegenerateMessage = () => {
  emit('regenerate-message', props.message)
}
</script>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        