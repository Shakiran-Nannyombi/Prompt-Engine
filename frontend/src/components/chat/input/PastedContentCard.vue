<template>
  <div class="relative group flex-shrink-0 w-28 h-28 rounded-2xl overflow-hidden border border-card-border bg-card-bg animate-fade-in p-3 flex flex-col justify-between shadow-sm">
    <div class="overflow-hidden w-full">
      <p class="text-[10px] text-text opacity-50 leading-relaxed font-mono break-words whitespace-pre-wrap line-clamp-4 select-none">
        {{ content.content }}
      </p>
    </div>

    <div class="flex items-center justify-between w-full mt-2">
      <div class="inline-flex items-center justify-center px-1.5 py-[2px] rounded border border-card-border bg-secondary/50">
        <span class="text-[9px] font-bold text-text opacity-60 uppercase tracking-wider font-sans">PASTED</span>
      </div>
    </div>

    <button
      @click.stop="$emit('remove', content.id)"
      class="absolute top-2 right-2 p-[3px] bg-card-bg border border-card-border rounded-full text-text opacity-0 group-hover:opacity-100 hover:text-text transition-all shadow-sm"
    >
      <svg class="w-2 h-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>

<script setup>
defineProps({
  content: {
    type: Object,
    required: true
  }
})

defineEmits(['remove'])
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
