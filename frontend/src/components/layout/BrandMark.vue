<script setup>
defineProps({
  size: { type: Number, default: 28 },
})
</script>

<template>
  <svg :width="size" :height="size" viewBox="0 0 32 32" aria-hidden="true" class="brand-mark">
    <rect width="32" height="32" rx="7" class="mark-bg" />
    <path d="M8 11h16" class="mark-line" />
    <path d="M8 17h7" class="mark-line" />
    <path d="M17 23.5l3.5-7 3.5 7" class="mark-caret" />
  </svg>
</template>

<style scoped>
.mark-bg {
  fill: var(--ink);
}
.mark-line {
  stroke: var(--paper);
  stroke-width: 2.4;
  stroke-linecap: round;
}
.mark-caret {
  fill: none;
  stroke: var(--pencil);
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}
:global(.dark) .mark-caret {
  stroke: #2f5bea;
}
</style>
