<script setup>
import { RouterLink } from 'vue-router'
import PublicLayout from '@/components/layout/PublicLayout.vue'
import Manuscript from '@/components/manuscript/Manuscript.vue'

const heroDraft = [
  { type: 'add', text: 'You are a technology writer for a small-business newsletter. ', note: 'Give it a role, so it knows whose voice to write in.' },
  { type: 'keep', text: 'Write a ' },
  { type: 'add', text: '600-word ', note: 'Set a length. Open-ended asks get padded answers.' },
  { type: 'keep', text: 'blog post about ' },
  { type: 'cut', text: 'AI. ' },
  { type: 'add', text: 'how owners can use AI to answer customer emails faster.', note: 'Name the reader and the angle.' },
  { type: 'add', text: ' Use three subheadings and end with one step they can try this week.', note: 'Ask for the format you want back.' },
]

const coachStages = [
  { name: 'Task', detail: 'Say what you want done, who should do it and what shape the answer takes.' },
  { name: 'Context', detail: 'Add only the background the task needs, not your whole history.' },
  { name: 'References', detail: 'Point to examples or documents the answer should follow.' },
  { name: 'Evaluate', detail: 'Decide how you will judge whether the answer is right.' },
  { name: 'Iterate', detail: 'Change one thing at a time and compare the results.' },
]

const refinerModes = [
  { name: 'Clarity', detail: 'reorganises rambling prompts' },
  { name: 'Precision', detail: 'pins down technical asks' },
  { name: 'Creative', detail: 'opens up tone and ideas' },
  { name: 'Documents', detail: 'refines against files you upload' },
]

const habits = [
  { habit: 'More words means more control.', fix: 'The Refiner cuts padding and keeps the instructions that change the answer.' },
  { habit: 'Pasting the whole backstory into every prompt.', fix: 'The Coach separates the task from the context it actually needs.' },
  { habit: 'Leaving the model with no role.', fix: 'Both agents add a persona that fits the task.' },
  { habit: 'Asking for confident answers with no way to check them.', fix: 'The Coach’s Evaluate stage asks how you’ll know the answer is right.' },
  { habit: 'Copying “magic prompts” from threads.', fix: 'The Coach explains why each change works, so you can adapt it yourself.' },
  { habit: 'One mega-prompt for planning, writing and checking.', fix: 'Prompts are split into steps you can test one at a time.' },
]
</script>

<template>
  <PublicLayout>
    <!-- Hero -->
    <section class="wrap hero">
      <div class="hero-copy">
        <h1 class="hero-title">Write the prompt you meant.</h1>
        <p class="hero-lede">
          Prompt Engine rewrites vague prompts into clear ones, then shows you why each change works, so the next one
          comes out right the first time.
        </p>
        <div class="hero-actions">
          <RouterLink to="/refiner" class="btn btn-primary">Refine a prompt</RouterLink>
          <RouterLink to="/coach" class="btn btn-secondary">Learn with the Coach</RouterLink>
        </div>
      </div>
      <div class="hero-demo">
        <Manuscript :segments="heroDraft" animate label="Your prompt" />
      </div>
    </section>

    <!-- Two agents -->
    <section class="wrap section" aria-labelledby="agents-title">
      <header class="section-head">
        <h2 id="agents-title" class="section-title">Two ways to get a better prompt</h2>
        <p class="section-lede">Use the Refiner when you need a prompt now. Use the Coach when you want to get better at writing them.</p>
      </header>

      <div class="agents">
        <article class="agent sheet">
          <div class="agent-top">
            <h3 class="agent-name">Refiner</h3>
            <p class="agent-sum">Rewrites your prompt in one pass.</p>
          </div>
          <div class="before-after">
            <p class="ba-row">
              <span class="ba-tag">Before</span>
              <span class="ba-text muted">Summarise this report.</span>
            </p>
            <p class="ba-row">
              <span class="ba-tag">After</span>
              <span class="ba-text">
                You are an analyst briefing a busy manager. Summarise the attached report in five bullet points, lead
                with the decision it asks for, and flag any figures that look inconsistent.
              </span>
            </p>
          </div>
          <dl class="modes">
            <div v-for="m in refinerModes" :key="m.name" class="mode">
              <dt>{{ m.name }}</dt>
              <dd>{{ m.detail }}</dd>
            </div>
          </dl>
          <RouterLink to="/refiner" class="btn btn-primary agent-cta">Open the Refiner</RouterLink>
        </article>

        <article class="agent sheet">
          <div class="agent-top">
            <h3 class="agent-name">Coach</h3>
            <p class="agent-sum">Walks you through writing it yourself, one stage at a time.</p>
          </div>
          <ol class="stages">
            <li v-for="(s, i) in coachStages" :key="s.name" class="stage">
              <span class="stage-no">{{ i + 1 }}</span>
              <div>
                <p class="stage-name">{{ s.name }}</p>
                <p class="stage-detail">{{ s.detail }}</p>
              </div>
            </li>
          </ol>
          <RouterLink to="/coach" class="btn btn-secondary agent-cta">Start a coaching session</RouterLink>
        </article>
      </div>
    </section>

    <!-- Habits -->
    <section class="wrap section" aria-labelledby="habits-title">
      <header class="section-head">
        <h2 id="habits-title" class="section-title">Habits it trains out of you</h2>
        <p class="section-lede">
          The most common prompting mistakes, collected from prompt-engineering discussions while researching the project.
        </p>
      </header>

      <ul class="habits">
        <li v-for="h in habits" :key="h.habit" class="habit">
          <p class="habit-quote">{{ h.habit }}</p>
          <p class="habit-fix">{{ h.fix }}</p>
        </li>
      </ul>
    </section>

    <!-- Close -->
    <section class="wrap section closing">
      <h2 class="closing-title">Start with the prompt you already have.</h2>
      <div class="hero-actions">
        <RouterLink to="/refiner" class="btn btn-primary">Refine a prompt</RouterLink>
        <RouterLink to="/tutorials" class="btn btn-ghost">Read the guides</RouterLink>
      </div>
    </section>
  </PublicLayout>
</template>

<style scoped>
.hero {
  display: grid;
  gap: 3rem;
  padding-top: 3.5rem;
  padding-bottom: 2rem;
  align-items: center;
}
.hero-title {
  font-size: clamp(2.75rem, 1.6rem + 5vw, 4.75rem);
  font-weight: 750;
  letter-spacing: -0.045em;
  line-height: 0.98;
  font-variation-settings: 'opsz' 96;
  max-width: 11ch;
}
.hero-lede {
  margin-top: 1.5rem;
  font-size: 1.15rem;
  line-height: 1.6;
  color: var(--ink-muted);
  max-width: 34rem;
}
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 2rem;
}

.section {
  padding-top: 6rem;
}
.section-head {
  max-width: 40rem;
  margin-bottom: 2.5rem;
}
.section-title {
  font-size: clamp(1.9rem, 1.4rem + 2vw, 2.75rem);
  font-weight: 700;
  letter-spacing: -0.035em;
}
.section-lede {
  margin-top: 0.9rem;
  font-size: 1.075rem;
  color: var(--ink-muted);
}

/* Agents */
.agents {
  display: grid;
  gap: 1.25rem;
}
.agent {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  padding: 1.75rem;
}
.agent-name {
  font-size: 1.6rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}
.agent-sum {
  margin-top: 0.35rem;
  color: var(--ink-muted);
}
.agent-cta {
  margin-top: auto;
  align-self: flex-start;
}

.before-after {
  display: grid;
  gap: 0.9rem;
  padding: 1.1rem 1.2rem;
  background: var(--paper);
  border-radius: var(--radius-control);
}
.ba-row {
  display: grid;
  grid-template-columns: 4rem 1fr;
  gap: 0.75rem;
  align-items: baseline;
}
.ba-tag {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--ink-muted);
}
.ba-text {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  line-height: 1.6;
}
.ba-text.muted {
  color: var(--ink-muted);
  text-decoration: line-through;
  text-decoration-color: var(--pencil);
  text-decoration-thickness: 2px;
}

.modes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.5rem;
  margin: 0;
}
.mode dt {
  font-weight: 600;
}
.mode dd {
  margin: 0.15rem 0 0;
  font-size: 0.925rem;
  color: var(--ink-muted);
}

.stages {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
}
.stage {
  display: grid;
  grid-template-columns: 2.25rem 1fr;
  gap: 0.75rem;
  padding: 0.85rem 0;
  border-top: 1px solid var(--rule);
}
.stage:first-child {
  border-top: none;
  padding-top: 0;
}
.stage-no {
  display: grid;
  place-items: center;
  width: 1.75rem;
  height: 1.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--pencil);
  border: 1.5px solid var(--pencil);
  border-radius: 50%;
}
.stage-name {
  font-weight: 600;
}
.stage-detail {
  margin-top: 0.1rem;
  font-size: 0.95rem;
  color: var(--ink-muted);
}

/* Habits */
.habits {
  list-style: none;
  margin: 0;
  padding: 0;
  border-top: 1px solid var(--rule);
}
.habit {
  display: grid;
  gap: 0.5rem;
  padding: 1.4rem 0;
  border-bottom: 1px solid var(--rule);
}
.habit-quote {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 1.2rem;
  line-height: 1.45;
  color: var(--ink-muted);
  text-decoration: line-through;
  text-decoration-color: color-mix(in srgb, var(--pencil) 70%, transparent);
  text-decoration-thickness: 1.5px;
}
.habit-fix {
  font-size: 1.025rem;
  max-width: 38rem;
}

/* Closing */
.closing {
  padding-bottom: 1rem;
}
.closing-title {
  font-size: clamp(2rem, 1.3rem + 3vw, 3.25rem);
  font-weight: 750;
  letter-spacing: -0.04em;
  max-width: 16ch;
}

@media (min-width: 900px) {
  .agents {
    grid-template-columns: 1fr 1fr;
  }
  .habit {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 2.5rem;
    align-items: baseline;
  }
}

@media (min-width: 1024px) {
  .hero {
    grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
    gap: 4rem;
    padding-top: 6rem;
  }
}
</style>
