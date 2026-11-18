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
  background: var(--color-background);
}
main {
  flex: 1;
  /* clear the floating navbar */
  padding-top: 7rem;
  padding-bottom: 6rem;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: -3rem;
  z-index: 100001;
  padding: 0.5rem 0.9rem;
  background: var(--color-text);
  color: var(--color-background);
  border-radius: 0.75rem;
  text-decoration: none;
}
.skip-link:focus {
  top: 0.75rem;
}
</style>
