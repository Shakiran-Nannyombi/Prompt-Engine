<script setup>
import ChatMessageList from './ChatMessageList.vue'
import UnifiedChatInput from './UnifiedChatInput.vue'

defineProps({
  messages: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  loadingMessage: { type: String, default: 'Thinking' },
  error: { type: String, default: '' },
  variant: { type: String, default: 'default' },
  placeholder: { type: String, default: 'Type your message' },
  inputLabel: { type: String, default: 'Message' },
  emptyTitle: { type: String, default: '' },
  emptyText: { type: String, default: '' },
  examples: { type: Array, default: () => [] },
})

const emit = defineEmits(['send-message', 'clear-error'])
const send = (payload) => emit('send-message', payload)
</script>

<template>
  <div class="chat">
    <ChatMessageList
      v-if="messages.length || isLoading"
      :messages="messages"
      :is-loading="isLoading"
      :loading-message="loadingMessage"
      :variant="variant"
    />

    <div v-else class="empty">
      <div class="empty-inner">
        <h2 class="empty-title">{{ emptyTitle }}</h2>
        <p class="empty-text">{{ emptyText }}</p>
        <div v-if="examples.length" class="examples">
          <p class="examples-label">Or try one of these</p>
          <button
            v-for="ex in examples"
            :key="ex"
            type="button"
            class="example"
            :disabled="isLoading"
            @click="send({ message: ex })"
          >
            {{ ex }}
          </button>
        </div>
      </div>
    </div>

    <div class="composer-wrap">
      <div v-if="error" class="error" role="alert">
        <p>{{ error }}</p>
        <button type="button" class="error-close" aria-label="Dismiss error" @click="emit('clear-error')">Dismiss</button>
      </div>
      <UnifiedChatInput :disabled="isLoading" :placeholder="placeholder" :label="inputLabel" @send-message="send" />
    </div>
  </div>
</template>

<style scoped>
.chat {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
.empty {
  flex: 1;
  overflow-y: auto;
  display: flex;
}
.empty-inner {
  width: 100%;
  max-width: 48rem;
  margin: auto;
  padding: 2.5rem 1.25rem;
}
.empty-title {
  font-size: clamp(1.75rem, 1.3rem + 1.6vw, 2.4rem);
  font-weight: 750;
  line-height: 1.12;
  letter-spacing: -0.035em;
  max-width: 18ch;
  color: var(--color-text);
}
.empty-text {
  margin-top: 0.75rem;
  color: var(--ink-muted);
  max-width: 34rem;
}
.examples {
  display: grid;
  gap: 0.6rem;
  margin-top: 2rem;
}
.examples-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--ink-muted);
}
.example {
  text-align: left;
  padding: 0.8rem 1rem;
  font-family: var(--font-serif);
  font-size: 1rem;
  line-height: 1.5;
  color: var(--ink);
  background: var(--sheet);
  border: 1px solid var(--rule);
  border-radius: var(--radius-control);
  cursor: pointer;
  transition: border-color 150ms;
}
.example:hover:not(:disabled) {
  border-color: var(--pencil);
}
.composer-wrap {
  width: 100%;
  max-width: 48rem;
  margin: 0 auto;
  padding: 0.5rem 1.25rem 1.25rem;
}
.error {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.6rem;
  padding: 0.6rem 0.8rem;
  font-size: 0.925rem;
  color: var(--danger);
  border: 1px solid color-mix(in srgb, var(--danger) 45%, transparent);
  border-radius: var(--radius-control);
}
.error-close {
  margin-left: auto;
  font: inherit;
  font-weight: 600;
  color: inherit;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
}
</style>
