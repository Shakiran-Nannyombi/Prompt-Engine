<script setup>
/* The Home page's footer, shared by every public page. */
import { RouterLink } from 'vue-router'

const repo = 'https://github.com/Shakiran-Nannyombi/Prompt-Engine'
const year = new Date().getFullYear()
</script>

<template>
  <footer class="footer-section">
    <div class="footer-content">
      <div class="footer-column">
        <h3 class="footer-title">Prompt-Engine</h3>
        <p class="newsletter-disclaimer footer-about">
          Two AI agents for better prompts: the Refiner rewrites them, the Coach teaches you how.
        </p>
      </div>

      <div class="footer-column">
        <h3 class="footer-title">Pages</h3>
        <ul class="footer-links">
          <li><RouterLink to="/" class="footer-link">Home</RouterLink></li>
          <li><RouterLink to="/coach" class="footer-link">Coach</RouterLink></li>
          <li><RouterLink to="/refiner" class="footer-link">Refiner</RouterLink></li>
          <li><RouterLink to="/tutorials" class="footer-link">Tutorials</RouterLink></li>
        </ul>
      </div>

      <div class="footer-column">
        <h3 class="footer-title">Resources</h3>
        <ul class="footer-links">
          <li><RouterLink to="/about" class="footer-link">About</RouterLink></li>
          <li><a :href="repo" target="_blank" rel="noopener" class="footer-link">GitHub Repository</a></li>
          <li><a :href="`${repo}/issues`" target="_blank" rel="noopener" class="footer-link">Report Issues</a></li>
          <li><a :href="`${repo}/blob/main/LICENSE`" target="_blank" rel="noopener" class="footer-link">License</a></li>
        </ul>
      </div>

      <div class="footer-column">
        <h3 class="footer-title">Social</h3>
        <ul class="footer-links">
          <li>
            <a :href="repo" target="_blank" rel="noopener" class="footer-link social-link">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
              GitHub
            </a>
          </li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <p class="copyright">© Copyright {{ year }} Prompt-Engine. All Rights Reserved</p>
    </div>
  </footer>
</template>

<style scoped>
.footer-about {
  max-width: 28ch;
  line-height: 1.6;
}
</style>
