<script setup>
import { nextTick, ref, computed } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false },
  placeholder: { type: String, default: 'Type your message' },
  label: { type: String, default: 'Message' },
})
const emit = defineEmits(['send-message'])

const message = ref('')
const textareaRef = ref(null)
const canSend = computed(() => message.value.trim().length > 0 && !props.disabled)

const resize = () => {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = `${Math.min(el.scrollHeight, 320)}px`
}

const send = async () => {
  if (!canSend.value) return
  emit('send-message', { message: message.value.trim() })
  message.value = ''
  await nextTick()
  resize()
}

const onKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
    e.preventDefault()
    send()
  }
}
</script>

<template>
  <form class="composer" @submit.prevent="send">
    <label for="composer-input" class="sr-only">{{ label }}</label>
    <textarea
      id="composer-input"
      ref="textareaRef"
      v-model="message"
      class="composer-input"
      rows="1"
      :placeholder="placeholder"
      @input="resize"
      @keydown="onKeydown"
    ></textarea>
    <div class="composer-bar">
      <span class="composer-hint">Enter sends. Shift + Enter adds a new line.</span>
      <button type="submit" class="btn btn-primary composer-send" :disabled="!canSend">Send</button>
    </div>
  </form>
</template>

<style scoped>
.composer {
  background: var(--sheet);
  border: 1px solid var(--rule);
  border-radius: var(--radius-sheet);
  padding: 0.85rem 0.85rem 0.65rem 1rem;
  transition: border-color 150ms, box-shadow 150ms;
}
.composer:focus-within {
  border-color: var(--pencil);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--pencil) 18%, transparent);
}
.composer-input {
  display: block;
  width: 100%;
  min-height: 1.6em;
  max-height: 20rem;
  resize: none;
  border: none;
  outline: none;
  background: transparent;
  color: var(--ink);
  font-family: var(--font-serif);
  font-size: 1.05rem;
  line-height: 1.6;
}
.composer-input::placeholder {
  color: var(--ink-muted);
}
.composer-input:focus-visible {
  outline: none;
}
.composer-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 0.6rem;
}
.composer-hint {
  font-size: 0.8rem;
  color: var(--ink-muted);
}
.composer-send {
  min-height: 2.35rem;
  padding: 0 1rem;
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}
@media (max-width: 520px) {
  .composer-hint {
    display: none;
  }
  .composer-bar {
    justify-content: flex-end;
  }
}
</style>
