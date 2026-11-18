<script setup>
import { computed } from 'vue'
import WorkspaceLayout from './WorkspaceLayout.vue'
import ChatInterface from './ChatInterface.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  isLoading: Boolean,
  loadingMessage: String,
  error: String,
  progressInfo: { type: Object, required: true },
})

const emit = defineEmits(['send-message', 'clear-error', 'reset-conversation', 'download-prompt'])

const stages = computed(() => {
  const p = props.progressInfo
  return [
    { key: 'task', name: 'Task', detail: 'What you want done', done: !!p.task, active: p.currentStep === 'task' },
    { key: 'context', name: 'Context', detail: 'Only the background it needs', done: !!p.context, active: p.currentStep === 'context' },
    { key: 'references', name: 'References', detail: 'Examples to follow', done: p.references?.length > 0, active: p.currentStep === 'references' },
    { key: 'final', name: 'Final prompt', detail: 'Ready to use', done: !!p.finalPrompt, active: p.currentStep === 'final_prompt' },
  ]
})
const doneCount = computed(() => stages.value.filter((s) => s.done).length)

const examples = [
  'I want to write a cover letter for a junior developer role.',
  'I need a prompt that turns meeting notes into action items.',
]
</script>

<template>
  <WorkspaceLayout title="Coach" subtitle="Build a prompt one stage at a time." @new-session="emit('reset-conversation')">
    <template #sidebar>
      <section class="progress" aria-labelledby="progress-title">
        <div class="progress-head">
          <h2 id="progress-title" class="progress-title">Your progress</h2>
          <span class="progress-count">{{ doneCount }} of {{ stages.length }}</span>
        </div>
        <ol class="stages">
          <li
            v-for="(s, i) in stages"
            :key="s.key"
            class="stage"
            :class="{ done: s.done, active: s.active }"
            :aria-current="s.active ? 'step' : undefined"
          >
            <span class="stage-mark" aria-hidden="true">
              <svg v-if="s.done" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>
              <template v-else>{{ i + 1 }}</template>
            </span>
            <span class="stage-text">
              <span class="stage-name">{{ s.name }}<span v-if="s.done" class="sr-only"> (done)</span></span>
              <span class="stage-detail">{{ s.detail }}</span>
            </span>
          </li>
        </ol>
        <button
          v-if="progressInfo.finalPrompt"
          type="button"
          class="btn btn-secondary download"
          @click="emit('download-prompt', progressInfo.finalPrompt)"
        >
          Download prompt
        </button>
      </section>
    </template>

    <ChatInterface
      :messages="messages"
      :is-loading="isLoading"
      :loading-message="loadingMessage || 'The Coach is thinking'"
      :error="error"
      variant="coach"
      placeholder="Tell the Coach what you want the AI to do"
      input-label="Message to the Coach"
      empty-title="What do you want the AI to do?"
      empty-text="Describe the task in a sentence. The Coach will ask about context and references, then help you put the final prompt together."
      :examples="examples"
      @send-message="(p) => emit('send-message', p)"
      @clear-error="emit('clear-error')"
    />
  </WorkspaceLayout>
</template>

<style scoped>
.progress-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 0 0.35rem;
  margin-bottom: 0.75rem;
}
.progress-title {
  font-size: 0.925rem;
  font-weight: 650;
  letter-spacing: 0;
}
.progress-count {
  font-size: 0.85rem;
  color: var(--ink-muted);
}
.stages {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
}
.stage {
  position: relative;
  display: grid;
  grid-template-columns: 1.75rem 1fr;
  gap: 0.6rem;
  padding: 0.5rem 0.35rem 0.85rem;
}
.stage:not(:last-child)::before {
  content: '';
  position: absolute;
  left: calc(0.35rem + 0.75rem);
  top: 2.1rem;
  bottom: 0;
  width: 1.5px;
  background: var(--rule);
}
.stage.done:not(:last-child)::before {
  background: var(--pencil);
}
.stage-mark {
  display: grid;
  place-items: center;
  width: 1.5rem;
  height: 1.5rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--ink-muted);
  background: var(--sheet);
  border: 1.5px solid var(--rule);
  border-radius: 50%;
}
.stage.active .stage-mark {
  color: var(--pencil);
  border-color: var(--pencil);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--pencil) 18%, transparent);
}
.stage.done .stage-mark {
  color: var(--on-pencil);
  background: var(--pencil);
  border-color: var(--pencil);
}
.stage-text {
  display: grid;
}
.stage-name {
  font-weight: 600;
  font-size: 0.95rem;
}
.stage-detail {
  font-size: 0.825rem;
  color: var(--ink-muted);
}
.download {
  width: 100%;
  margin-top: 0.75rem;
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
