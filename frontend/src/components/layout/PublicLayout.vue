<script setup>
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
</script>

<template>
  <div class="public-layout">
    <a href="#main" class="skip-link">Skip to content</a>
    <AppHeader />
    <main id="main">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<style scoped>
.public-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
main {
  flex: 1;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: -3rem;
  z-index: 100;
  padding: 0.5rem 0.9rem;
  background: var(--ink);
  color: var(--paper);
  border-radius: var(--radius-control);
  text-decoration: none;
}
.skip-link:focus {
  top: 0.75rem;
}
</style>
