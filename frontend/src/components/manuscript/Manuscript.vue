<script setup>
/*
 * A prompt shown as a manuscript under edit.
 * segments: [{ type: 'keep' | 'cut' | 'add' | 'mark', text, note? }]
 * Each non-"keep" segment is one edit. With `animate`, edits are applied one
 * by one on mount (and on Replay); reduced motion shows the finished draft.
 */
import { computed, onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({
  segments: { type: Array, required: true },
  animate: { type: Boolean, default: false },
  label: { type: String, default: 'Your prompt' },
  stepMs: { type: Number, default: 950 },
  startDelayMs: { type: Number, default: 700 },
})

const edits = computed(() => {
  let step = 0
  let noteNo = 0
  return props.segments.map((seg) => {
    const isEdit = seg.type !== 'keep'
    const body = seg.text.trimEnd()
    return {
      ...seg,
      body,
      tail: seg.text.slice(body.length),
      step: isEdit ? ++step : 0,
      noteNo: seg.note ? ++noteNo : null,
    }
  })
})
const totalSteps = computed(() => edits.value.filter((s) => s.step).length)
const notes = computed(() => edits.value.filter((s) => s.noteNo))

const reduceMotion = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
const step = ref(props.animate && !reduceMotion ? 0 : totalSteps.value)
const done = computed(() => step.value >= totalSteps.value)
const applied = (seg) => seg.step > 0 && step.value >= seg.step

let timer = null
const clear = () => {
  if (timer) clearTimeout(timer)
  timer = null
}
const tick = () => {
  if (step.value >= totalSteps.value) return
  step.value += 1
  timer = setTimeout(tick, props.stepMs)
}
const play = () => {
  clear()
  if (reduceMotion) {
    step.value = totalSteps.value
    return
  }
  step.value = 0
  timer = setTimeout(tick, props.startDelayMs)
}

onMounted(() => {
  if (props.animate && !reduceMotion) play()
})
onUnmounted(clear)
</script>

<template>
  <figure class="manuscript">
    <div class="ms-head">
      <span class="ms-label">{{ label }}</span>
      <span class="ms-status" aria-live="polite">
        {{ done ? `${totalSteps} edits` : step === 0 ? 'Original draft' : 'Editing…' }}
      </span>
      <button v-if="animate" type="button" class="ms-replay" :disabled="!done" @click="play">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M3 12a9 9 0 1 0 3-6.7L3 8" />
          <path d="M3 3v5h5" />
        </svg>
        Replay
      </button>
    </div>

    <div class="ms-body">
      <p class="ms-text">
        <template v-for="(seg, i) in edits" :key="i">
          <span v-if="seg.type === 'keep'">{{ seg.text }}</span>
          <template v-else>
            <span v-if="seg.type === 'cut'" class="seg-cut" :class="{ on: applied(seg) }">{{ seg.body }}</span>
            <span v-else-if="seg.type === 'mark'" class="seg-mark" :class="{ on: applied(seg) }">{{ seg.body }}</span>
            <Transition v-else name="ins">
              <ins v-if="applied(seg)" class="seg-add">{{ seg.body }}</ins>
            </Transition>
            <sup v-if="seg.noteNo && applied(seg)" class="note-ref" aria-hidden="true">{{ seg.noteNo }}</sup>
            <span v-if="seg.type !== 'add' || applied(seg)">{{ seg.tail }}</span>
          </template>
        </template>
      </p>

      <ol v-if="notes.length" class="ms-notes" aria-label="Why each edit was made">
        <li v-for="n in notes" :key="n.noteNo" class="ms-note" :class="{ on: applied(n) }">
          <span class="note-no">{{ n.noteNo }}</span>
          <span class="note-text">{{ n.note }}</span>
        </li>
      </ol>
    </div>
  </figure>
</template>

<style scoped>
.manuscript {
  margin: 0;
  background: var(--sheet);
  border: 1px solid var(--rule);
  border-radius: var(--radius-sheet);
  box-shadow: var(--lift);
  overflow: hidden;
}
.ms-head {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 1rem 0.7rem 1.25rem;
  border-bottom: 1px solid var(--rule);
  font-size: 0.875rem;
}
.ms-label {
  font-weight: 600;
  color: var(--ink);
}
.ms-status {
  color: var(--ink-muted);
}
.ms-replay {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.3rem 0.6rem;
  font: inherit;
  font-weight: 500;
  color: var(--pencil);
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-control);
  cursor: pointer;
}
.ms-replay:hover:not(:disabled) {
  background: var(--sheet-tint);
}
.ms-replay:disabled {
  color: var(--ink-muted);
  cursor: default;
}

.ms-body {
  display: grid;
  gap: 1.25rem;
  padding: 1.4rem 1.25rem 1.5rem;
}
.ms-text {
  font-family: var(--font-serif);
  font-size: clamp(1.05rem, 0.95rem + 0.4vw, 1.25rem);
  line-height: 1.7;
  color: var(--ink);
  margin: 0;
}

/* Cut: a blue-pencil strike drawn across the words */
.seg-cut {
  background-image: linear-gradient(var(--pencil), var(--pencil));
  background-repeat: no-repeat;
  background-position: 0 58%;
  background-size: 0% 2px;
  transition: background-size 450ms ease, color 450ms ease;
}
.seg-cut.on {
  background-size: 100% 2px;
  color: var(--ink-muted);
}

/* Mark: highlighter swept across */
.seg-mark {
  background-image: linear-gradient(color-mix(in srgb, var(--highlight) 70%, transparent), color-mix(in srgb, var(--highlight) 70%, transparent));
  background-repeat: no-repeat;
  background-position: 0 85%;
  background-size: 0% 45%;
  transition: background-size 500ms ease;
}
.seg-mark.on {
  background-size: 100% 45%;
}
.dark .seg-mark.on {
  color: #1b1f3b;
}

/* Add: inserted text in blue pencil */
.seg-add {
  text-decoration: none;
  color: var(--pencil);
  font-style: italic;
}
.ins-enter-active {
  transition: opacity 450ms ease, filter 450ms ease;
}
.ins-enter-from {
  opacity: 0;
  filter: blur(4px);
}

.note-ref {
  font-family: var(--font-sans);
  font-size: 0.7em;
  font-weight: 700;
  color: var(--pencil);
  margin-left: 0.12em;
  animation: ref-in 300ms ease both;
}
@keyframes ref-in {
  from {
    opacity: 0;
  }
}

.ms-notes {
  list-style: none;
  margin: 0;
  padding: 1rem 0 0;
  border-top: 1px dashed var(--rule);
  display: grid;
  gap: 0.7rem;
}
.ms-note {
  display: grid;
  grid-template-columns: 1.4rem 1fr;
  align-items: baseline;
  opacity: 0.18;
  transition: opacity 400ms ease;
}
.ms-note.on {
  opacity: 1;
}
.note-no {
  font-weight: 700;
  font-size: 0.8rem;
  color: var(--pencil);
}
.note-text {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 0.98rem;
  line-height: 1.45;
  color: var(--ink-muted);
}

@media (min-width: 1024px) {
  .ms-body {
    grid-template-columns: minmax(0, 1fr) 14rem;
    gap: 1.75rem;
    padding: 1.75rem 1.5rem 1.9rem 1.75rem;
  }
  .ms-notes {
    padding: 0 0 0 1.25rem;
    border-top: none;
    border-left: 1px dashed var(--rule);
    align-content: start;
  }
}
</style>
