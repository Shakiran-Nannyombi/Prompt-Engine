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
      { title: 'Start a session', body: 'Open the Refiner and choose “Start a session”. Each session keeps its own history.' },
      { title: 'Paste your prompt', body: 'Paste it as you would send it to an AI tool. Attach a file if the prompt should be refined against a document.' },
      { title: 'Use the rewrite', body: 'Read the refined version, copy it, and use it in the AI tool you normally work with.' },
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
    <section class="wrap tut-hero">
      <h1 class="tut-title">How to use Prompt Engine</h1>
      <p class="tut-lede">
        Two short guides, one for each agent. Pick the one that matches what you need today.
      </p>
      <nav class="jump" aria-label="Guides on this page">
        <a v-for="g in guides" :key="g.id" :href="`#${g.id}`" class="jump-link">{{ g.title }}</a>
        <a href="#faq" class="jump-link">Questions</a>
      </nav>
    </section>

    <section class="wrap guides">
      <article v-for="g in guides" :id="g.id" :key="g.id" class="guide sheet">
        <header class="guide-head">
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
      <h2 id="tips-title" class="section-title">Four habits worth keeping</h2>
      <ul class="tips">
        <li v-for="t in tips" :key="t.title" class="tip">
          <h3 class="tip-title">{{ t.title }}</h3>
          <p class="tip-body">{{ t.body }}</p>
        </li>
      </ul>
    </section>

    <section id="faq" class="wrap tut-section" aria-labelledby="faq-title">
      <h2 id="faq-title" class="section-title">Questions</h2>
      <div class="faqs">
        <details v-for="f in faqs" :key="f.q" class="faq">
          <summary class="faq-q">
            <span>{{ f.q }}</span>
            <svg class="faq-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
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
.tut-hero {
  padding-top: 5rem;
}
.tut-title {
  font-size: clamp(2.4rem, 1.4rem + 4vw, 4rem);
  font-weight: 750;
  letter-spacing: -0.045em;
  line-height: 1.02;
  max-width: 14ch;
}
.tut-lede {
  margin-top: 1.25rem;
  font-size: 1.15rem;
  color: var(--ink-muted);
  max-width: 34rem;
}
.jump {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1.5rem;
  margin-top: 2rem;
}
.jump-link {
  color: var(--pencil);
  font-weight: 600;
  text-decoration: underline;
  text-decoration-thickness: 1.5px;
  text-underline-offset: 4px;
}

.guides {
  display: grid;
  gap: 1.25rem;
  padding-top: 3.5rem;
}
.guide {
  display: flex;
  flex-direction: column;
  padding: 1.75rem;
  scroll-margin-top: 5rem;
}
.guide-title {
  font-size: 1.6rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}
.guide-sum {
  margin-top: 0.4rem;
  color: var(--ink-muted);
}
.steps {
  list-style: none;
  margin: 1.75rem 0 2rem;
  padding: 0;
}
.step {
  position: relative;
  display: grid;
  grid-template-columns: 2.25rem 1fr;
  gap: 0.75rem;
  padding-bottom: 1.4rem;
}
.step:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 0.85rem;
  top: 2rem;
  bottom: 0.3rem;
  width: 1.5px;
  background: var(--rule);
}
.step-no {
  display: grid;
  place-items: center;
  width: 1.75rem;
  height: 1.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--pencil);
  border: 1.5px solid var(--pencil);
  border-radius: 50%;
  background: var(--sheet);
}
.step-title {
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.step-body {
  margin-top: 0.2rem;
  color: var(--ink-muted);
}
.guide-cta {
  margin-top: auto;
  align-self: flex-start;
}

.tut-section {
  padding-top: 5.5rem;
  scroll-margin-top: 4rem;
}
.section-title {
  font-size: clamp(1.8rem, 1.4rem + 1.6vw, 2.4rem);
  font-weight: 700;
  letter-spacing: -0.035em;
  margin-bottom: 2rem;
}
.tips {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 2rem 2.5rem;
}
.tip {
  padding-top: 1rem;
  border-top: 2px solid var(--ink);
}
.tip-title {
  font-size: 1.1rem;
  font-weight: 650;
}
.tip-body {
  margin-top: 0.4rem;
  color: var(--ink-muted);
}

.faqs {
  border-top: 1px solid var(--rule);
  max-width: 48rem;
}
.faq {
  border-bottom: 1px solid var(--rule);
}
.faq-q {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.15rem 0;
  font-size: 1.075rem;
  font-weight: 600;
  cursor: pointer;
  list-style: none;
}
.faq-q::-webkit-details-marker {
  display: none;
}
.faq-icon {
  flex-shrink: 0;
  color: var(--pencil);
  transition: transform 200ms ease;
}
.faq[open] .faq-icon {
  transform: rotate(45deg);
}
.faq-a {
  padding-bottom: 1.25rem;
  color: var(--ink-muted);
  max-width: 40rem;
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
