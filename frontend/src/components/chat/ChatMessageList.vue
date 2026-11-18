<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'
import ChatMessage from './ChatMessage.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  loadingMessage: { type: String, default: 'Thinking' },
  variant: { type: String, default: 'default' },
})

const scroller = ref(null)
const showJump = ref(false)

const onScroll = () => {
  const el = scroller.value
  if (!el) return
  showJump.value = el.scrollHeight - el.scrollTop - el.clientHeight > 160
}
const scrollToBottom = (smooth = true) => {
  const el = scroller.value
  if (!el) return
  el.scrollTo({ top: el.scrollHeight, behavior: smooth ? 'smooth' : 'auto' })
}

watch(
  () => [props.messages.length, props.isLoading],
  () => nextTick(() => scrollToBottom(false)),
)
onMounted(() => nextTick(() => scrollToBottom(false)))

defineExpose({ scrollToBottom })
</script>

<template>
  <div class="list-wrap">
    <div ref="scroller" class="list" role="log" aria-live="polite" aria-relevant="additions" @scroll="onScroll">
      <div class="list-inner">
        <ChatMessage v-for="(m, i) in messages" :key="m.id || i" :message="m" :variant="variant" />

        <div v-if="isLoading" class="thinking" role="status">
          <span class="loading-dots" aria-hidden="true">
            <span class="loading-dot"></span><span class="loading-dot"></span><span class="loading-dot"></span>
          </span>
          {{ loadingMessage }}
        </div>
      </div>
    </div>

    <Transition name="fade">
      <button v-if="showJump" type="button" class="jump" @click="scrollToBottom()">Jump to latest</button>
    </Transition>
  </div>
</template>

<style scoped>
.list-wrap {
  position: relative;
  flex: 1;
  min-height: 0;
  display: flex;
}
.list {
  flex: 1;
  overflow-y: auto;
}
.list-inner {
  display: grid;
  gap: 1.75rem;
  width: 100%;
  max-width: 48rem;
  margin: 0 auto;
  padding: 2rem 1.25rem 1.5rem;
}
.thinking {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.925rem;
  color: var(--ink-muted);
}
.thinking .loading-dots {
  color: var(--pencil);
}
.jump {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.45rem 0.9rem;
  font: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--ink);
  background: var(--sheet);
  border: 1px solid var(--rule);
  border-radius: 999px;
  box-shadow: var(--lift);
  cursor: pointer;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 150ms;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
