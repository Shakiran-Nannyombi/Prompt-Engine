<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true,
    validator: (m) => m && typeof m.content === 'string' && ['user', 'assistant', 'system'].includes(m.sender),
  },
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'coach', 'refiner'].includes(v),
  },
})

const isUser = computed(() => props.message.sender === 'user')
const agentName = computed(() => (props.variant === 'coach' ? 'Coach' : 'Refiner'))

// Escape first so model output can never inject HTML, then apply a small markdown subset.
const escapeHtml = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;')

const inline = (s) =>
  s
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')

const rendered = computed(() => {
  const text = escapeHtml(props.message.content || '')
  const blocks = []
  const parts = text.split(/```/)
  parts.forEach((part, i) => {
    if (i % 2 === 1) {
      blocks.push(`<pre><code>${part.replace(/^\w*\n/, '')}</code></pre>`)
      return
    }
    let list = null
    const flush = () => {
      if (list) blocks.push(`<${list.tag}>${list.items.map((li) => `<li>${inline(li)}</li>`).join('')}</${list.tag}>`)
      list = null
    }
    let para = []
    const flushPara = () => {
      if (para.length) blocks.push(`<p>${inline(para.join('<br>'))}</p>`)
      para = []
    }
    part.split('\n').forEach((line) => {
      const ul = line.match(/^\s*[-*•]\s+(.*)/)
      const ol = line.match(/^\s*\d+[.)]\s+(.*)/)
      const h = line.match(/^#{1,4}\s+(.*)/)
      if (ul || ol) {
        flushPara()
        const tag = ul ? 'ul' : 'ol'
        if (!list || list.tag !== tag) {
          flush()
          list = { tag, items: [] }
        }
        list.items.push((ul || ol)[1])
      } else if (h) {
        flushPara()
        flush()
        blocks.push(`<h4>${inline(h[1])}</h4>`)
      } else if (!line.trim()) {
        flushPara()
        flush()
      } else {
        flush()
        para.push(line)
      }
    })
    flushPara()
    flush()
  })
  return blocks.join('')
})

const copied = ref(false)
const copy = async () => {
  try {
    await navigator.clipboard.writeText(props.message.content)
    copied.value = true
    setTimeout(() => (copied.value = false), 1800)
  } catch {
    copied.value = false
  }
}
</script>

<template>
  <div v-if="isUser" class="msg msg-user">
    <div class="user-bubble">{{ message.content }}</div>
  </div>

  <article v-else class="msg msg-agent" :class="`is-${variant}`">
    <header class="agent-head">
      <span class="agent-name">{{ agentName }}</span>
      <button type="button" class="copy-btn" @click="copy">
        <span aria-live="polite">{{ copied ? 'Copied' : 'Copy' }}</span>
      </button>
    </header>
    <div class="agent-body prose-manuscript" v-html="rendered"></div>
  </article>
</template>

<style scoped>
.msg {
  animation: msg-in 220ms ease-out both;
}
@keyframes msg-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
}

.msg-user {
  display: flex;
  justify-content: flex-end;
}
.user-bubble {
  max-width: min(85%, 38rem);
  padding: 0.75rem 1rem;
  background: var(--sheet-tint);
  border: 1px solid var(--rule);
  border-radius: var(--radius-sheet) var(--radius-sheet) 4px var(--radius-sheet);
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  color: var(--ink);
}

.msg-agent {
  max-width: 44rem;
}
.agent-head {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.4rem;
}
.agent-name {
  font-size: 0.875rem;
  font-weight: 650;
  color: var(--pencil);
}
.copy-btn {
  margin-left: auto;
  padding: 0.2rem 0.55rem;
  font: inherit;
  font-size: 0.825rem;
  font-weight: 500;
  color: var(--ink-muted);
  background: transparent;
  border: 1px solid var(--rule);
  border-radius: var(--radius-control);
  cursor: pointer;
}
.copy-btn:hover {
  color: var(--ink);
  border-color: var(--ink-muted);
}

/* Refiner replies read as a revised manuscript on a sheet */
.is-refiner .agent-body {
  padding: 1rem 1.15rem;
  background: var(--sheet);
  border: 1px solid var(--rule);
  border-radius: var(--radius-sheet);
  max-width: none;
}
/* Coach replies read as margin notes */
.is-coach .agent-body,
.is-default .agent-body {
  padding-left: 1rem;
  border-left: 2px solid var(--pencil);
  max-width: none;
}

.agent-body :deep(p),
.agent-body :deep(ul),
.agent-body :deep(ol),
.agent-body :deep(pre),
.agent-body :deep(h4) {
  margin: 0 0 0.75rem;
}
.agent-body :deep(> :last-child) {
  margin-bottom: 0;
}
.agent-body :deep(ul),
.agent-body :deep(ol) {
  padding-left: 1.25rem;
}
.agent-body :deep(ul) {
  list-style: disc;
}
.agent-body :deep(ol) {
  list-style: decimal;
}
.agent-body :deep(li::marker) {
  color: var(--color-primary);
}
.agent-body :deep(li) {
  margin: 0.2rem 0;
}
.agent-body :deep(h4) {
  font-family: var(--font-sans);
  font-size: 1rem;
  font-weight: 650;
}
.agent-body :deep(code) {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.875em;
  padding: 0.1em 0.35em;
  background: var(--sheet-tint);
  border-radius: 4px;
}
.agent-body :deep(pre) {
  padding: 0.8rem 0.9rem;
  background: var(--sheet-tint);
  border-radius: var(--radius-control);
  overflow-x: auto;
  white-space: pre-wrap;
}
.agent-body :deep(pre code) {
  padding: 0;
  background: none;
}
</style>
