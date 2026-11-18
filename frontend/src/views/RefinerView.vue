<script setup>
import { ref, onMounted } from 'vue'
import WorkspaceLayout from '@/components/chat/WorkspaceLayout.vue'
import ChatInterface from '@/components/chat/ChatInterface.vue'
import { refinerAPI, getLatestMessage } from '@/service/api.js'

const messages = ref([])
const isLoading = ref(false)
const error = ref('')
const currentThreadId = ref(null)

const examples = [
  'Write a blog post about remote work.',
  'Summarise this meeting for my team.',
  'Explain recursion to a beginner.',
]

const friendlyError = (err) => {
  if (err.code === 'ECONNABORTED') return 'The Refiner took too long to answer. It may be waking up; send your prompt again in a moment.'
  if (!err.response) return 'Couldn’t reach the Refiner. Check your connection and send the prompt again.'
  return err.response?.data?.detail || 'The Refiner couldn’t process that prompt. Try again, or shorten it.'
}

const handleSendMessage = async (payload) => {
  const messageContent = typeof payload === 'string' ? payload : payload.message
  if (!messageContent) return
  messages.value.push({ id: Date.now(), sender: 'user', content: messageContent, timestamp: new Date().toISOString() })
  isLoading.value = true
  error.value = ''
  try {
    const history = messages.value.map((m) => ({ role: m.sender === 'user' ? 'user' : 'assistant', content: m.content }))
    const response = await refinerAPI.sendMessage(messageContent, history, currentThreadId.value)
    messages.value.push({
      id: Date.now() + 1,
      sender: 'assistant',
      content: getLatestMessage(response),
      timestamp: new Date().toISOString(),
    })
  } catch (err) {
    error.value = friendlyError(err)
    console.error('Refiner error:', err)
  } finally {
    isLoading.value = false
  }
}

const createNewThread = async () => {
  try {
    const response = await refinerAPI.createNewThread()
    currentThreadId.value = response.data.thread_id
  } catch {
    currentThreadId.value = `refiner-${Date.now()}`
  }
}

const handleNewSession = async () => {
  messages.value = []
  error.value = ''
  await createNewThread()
}

onMounted(createNewThread)
</script>

<template>
  <WorkspaceLayout title="Refiner" subtitle="Paste a prompt and get a clearer one back." @new-session="handleNewSession">
    <template #sidebar>
      <div class="side-note">
        <p class="side-note-title">What the Refiner changes</p>
        <ul>
          <li>Adds a role and a reader</li>
          <li>Sets length and format</li>
          <li>Cuts words that don’t change the answer</li>
        </ul>
      </div>
    </template>

    <ChatInterface
      :messages="messages"
      :is-loading="isLoading"
      loading-message="Refining your prompt"
      :error="error"
      variant="refiner"
      placeholder="Paste the prompt you want to improve"
      input-label="Prompt to refine"
      empty-title="Paste a prompt to refine"
      empty-text="Send it exactly as you would to an AI tool. You’ll get a rewritten version you can copy straight back."
      :examples="examples"
      @send-message="handleSendMessage"
      @clear-error="error = ''"
    />
  </WorkspaceLayout>
</template>

<style scoped>
.side-note {
  padding: 0.9rem 0.85rem;
  border: 1px dashed var(--rule);
  border-radius: var(--radius-control);
  font-size: 0.9rem;
  color: var(--ink-muted);
}
.side-note-title {
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 0.4rem;
}
.side-note ul {
  margin: 0;
  padding-left: 1.1rem;
  display: grid;
  gap: 0.25rem;
}
</style>
