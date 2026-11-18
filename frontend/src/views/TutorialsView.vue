<script setup>
import { RouterLink } from 'vue-router'
import PublicLayout from '@/components/layout/PublicLayout.vue'

const guides = [
  {
    id: 'refiner-guide',
    title: 'Refine your first prompt',
    summary: 'For when you already have a prompt and want a better one now.',
    cta: { to: '/refiner', label: 'Open the Refiner' },
    steps: [
      { title: 'Sign in', body: 'Any email and password work in this demo. Your session stays in this browser.' },
      { title: 'Open the Refiner', body: 'Each visit starts a fresh session. Use “New session” in the sidebar to clear it and start again.' },
      { title: 'Paste your prompt', body: 'Paste it exactly as you would send it to an AI tool, or pick one of the examples to see how it works.' },
      { title: 'Use the rewrite', body: 'Read the refined version, press Copy, and use it in the AI tool you normally work with.' },
    ],
  },
  {
    id: 'coach-guide',
    title: 'Write one with the Coach',
    summary: 'For when you want to learn how a good prompt is put together.',
    cta: { to: '/coach', label: 'Start a coaching session' },
    steps: [
      { title: 'Describe the task', body: 'Say what you want done. The Coach asks who should do it and what the answer should look like.' },
      { title: 'Add context', body: 'Give the background the task needs. The Coach pushes back if you add more than it needs.' },
      { title: 'Point to references', body: 'Share examples or documents the answer should follow, if you have them.' },
      { title: 'Evaluate and iterate', body: 'Agree how you will judge the answer, then adjust one thing at a time until the prompt works.' },
    ],
  },
]

const tips = [
  { title: 'Name the reader', body: 'Who is the answer for? A sentence about the audience changes tone, length and vocabulary.' },
  { title: 'Ask for a shape', body: 'Bullets, a table, three paragraphs, under 200 words. Say it, or the model guesses.' },
  { title: 'Give one example', body: 'A single good example teaches the format faster than a paragraph describing it.' },
  { title: 'Change one thing at a time', body: 'When an answer is off, edit one part of the prompt and compare, so you know what helped.' },
]

const faqs = [
  {
    q: 'Do I need an account?',
    a: 'This version uses a demo sign-in. Any email and password work, and your session is kept in this browser.',
  },
  {
    q: 'What’s the difference between the Refiner and the Coach?',
    a: 'The Refiner rewrites a prompt you already have in one pass. The Coach takes you through five stages (task, context, references, evaluate, iterate) so you write the prompt yourself.',
  },
  {
    q: 'Is it free?',
    a: 'Yes. Prompt Engine is a portfolio project with no paid plans.',
  },
  {
    q: 'Which AI model does it use?',
    a: 'Both agents run on Llama 3.1 8B, served by Groq. The prompts it produces work with any chat model.',
  },
  {
    q: 'Why is the first reply slow?',
    a: 'The backend sleeps when nobody is using it. The first request can take up to a minute while it wakes up; replies after that are quick.',
  },
]
</script>

<template>
  <PublicLayout>
    <section class="wrap">
      <header class="page-head">
        <span class="pill-badge">Tutorials &amp; guides</span>
        <h1 class="page-title">Master <span class="text-gradient">Prompt-Engine</span></h1>
        <p class="page-lede">Two short guides, one for each agent. Pick the one that matches what you need today.</p>
        <nav class="jump" aria-label="Guides on this page">
          <a v-for="g in guides" :key="g.id" :href="`#${g.id}`" class="btn btn-secondary">{{ g.title }}</a>
          <a href="#faq" class="btn btn-ghost">Questions</a>
        </nav>
      </header>
    </section>

    <section class="wrap guides">
      <article v-for="g in guides" :id="g.id" :key="g.id" class="guide card">
        <header>
          <h2 class="guide-title">{{ g.title }}</h2>
          <p class="guide-sum">{{ g.summary }}</p>
        </header>
        <ol class="steps">
          <li v-for="(s, i) in g.steps" :key="s.title" class="step">
            <span class="step-no">{{ i + 1 }}</span>
            <div>
              <h3 class="step-title">{{ s.title }}</h3>
              <p class="step-body">{{ s.body }}</p>
            </div>
          </li>
        </ol>
        <RouterLink :to="g.cta.to" class="btn btn-primary guide-cta">{{ g.cta.label }}</RouterLink>
      </article>
    </section>

    <section class="wrap tut-section" aria-labelledby="tips-title">
      <header class="page-head">
        <span class="pill-badge">Best practices</span>
        <h2 id="tips-title" class="section-title">Four habits <span class="text-gradient">worth keeping</span></h2>
      </header>
      <ul class="tips">
        <li v-for="t in tips" :key="t.title" class="tip card">
          <h3 class="tip-title">{{ t.title }}</h3>
          <p class="tip-body">{{ t.body }}</p>
        </li>
      </ul>
    </section>

    <section id="faq" class="wrap tut-section" aria-labelledby="faq-title">
      <header class="page-head">
        <span class="pill-badge">FAQ</span>
        <h2 id="faq-title" class="section-title">Frequently asked questions</h2>
      </header>
      <div class="faqs card">
        <details v-for="f in faqs" :key="f.q" class="faq">
          <summary class="faq-q">
            <span>{{ f.q }}</span>
            <svg class="faq-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">
              <path d="M12 5v14M5 12h14" />
            </svg>
          </summary>
          <p class="faq-a">{{ f.a }}</p>
        </details>
      </div>
    </section>
  </PublicLayout>
</template>

<style scoped>
.jump {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.6rem;
  margin-top: 0.5rem;
}
.guides {
  display: grid;
  gap: 1.5rem;
}
.guide {
  display: flex;
  flex-direction: column;
  padding: 2rem;
  scroll-margin-top: 7rem;
}
.guide-title {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-text);
}
.guide-sum {
  margin-top: 0.4rem;
  color: var(--color-text-muted);
}
.steps {
  list-style: none;
  margin: 1.75rem 0 2rem;
  padding: 0;
}
.step {
  position: relative;
  display: grid;
  grid-template-columns: 2.5rem 1fr;
  gap: 0.85rem;
  padding-bottom: 1.4rem;
}
.step:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 1rem;
  top: 2.25rem;
  bottom: 0.3rem;
  width: 2px;
  background: rgba(var(--color-primary-rgb), 0.2);
}
.step-no {
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  font-size: 0.85rem;
  font-weight: 800;
  color: #ffffff;
  background: var(--brand-gradient);
  border-radius: 50%;
  box-shadow: var(--brand-shadow);
}
.step-title,
.step-body,
.tip-title,
.tip-body,
.guide-title,
.guide-sum {
  margin-left: 0;
  margin-right: 0;
}
.step-title {
  margin: 0.2rem 0 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-text);
}
.step-body {
  margin-top: 0.2rem;
  line-height: 1.6;
  color: var(--color-text-muted);
}
.guide-cta {
  margin-top: auto;
  align-self: flex-start;
}

.tut-section {
  padding-top: 5.5rem;
  scroll-margin-top: 6rem;
}
.tips {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 1.25rem;
}
.tip {
  padding: 1.75rem 1.5rem;
  border-top: 4px solid var(--color-primary);
}
.tip-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-text);
}
.tip-body {
  margin-top: 0.5rem;
  line-height: 1.6;
  color: var(--color-text-muted);
}

.faqs {
  max-width: 50rem;
  margin: 0 auto;
  padding: 0.5rem 1.75rem;
}
.faq + .faq {
  border-top: 1px solid var(--color-card-border);
}
.faq-q {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.2rem 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--color-text);
  cursor: pointer;
  list-style: none;
}
.faq-q::-webkit-details-marker {
  display: none;
}
.faq-icon {
  flex-shrink: 0;
  color: var(--color-primary);
  transition: transform 200ms ease;
}
.faq[open] .faq-icon {
  transform: rotate(45deg);
}
.faq-a {
  padding-bottom: 1.25rem;
  line-height: 1.65;
  color: var(--color-text-muted);
}

@media (min-width: 900px) {
  .guides {
    grid-template-columns: 1fr 1fr;
  }
  .tips {
    grid-template-columns: repeat(4, 1fr);
  }
}
@media (min-width: 600px) and (max-width: 899px) {
  .tips {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
