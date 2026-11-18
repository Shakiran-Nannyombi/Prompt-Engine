<script setup>
import { RouterLink } from 'vue-router'
import PublicLayout from '@/components/layout/PublicLayout.vue'

const principles = [
  {
    name: 'Break the prompt into parts',
    detail: 'Every prompt is read as an instruction, the context it needs and the shape of the answer. Gaps in any one of them are what produce vague output.',
  },
  {
    name: 'Emphasis over volume',
    detail: 'Adding words rarely helps. The engine keeps what changes the answer and cuts the rest, so the model sees what matters.',
  },
  {
    name: 'Proven frameworks, chosen for you',
    detail: 'The Refiner sorts each prompt as a clarity, precision or creative problem, then rewrites it with a framework that suits it, such as C.O.R.E., R.A.C.E. or C.A.R.',
  },
]

const stack = [
  { part: 'Interface', tech: 'Vue 3, Vite and Tailwind CSS' },
  { part: 'Agents', tech: 'FastAPI with LangGraph and LangChain' },
  { part: 'Model', tech: 'Llama 3.1 8B, served by Groq' },
  { part: 'Memory', tech: 'Supabase Postgres for sessions and checkpoints' },
]
</script>

<template>
  <PublicLayout>
    <section class="wrap">
      <header class="page-head">
        <span class="pill-badge">The mission</span>
        <h1 class="page-title">Most prompts are briefs with <span class="text-gradient">the brief left out.</span></h1>
        <p class="page-lede">
          AI models are capable enough. What usually goes wrong is the request: no role, no reader, no format, and a
          paragraph of backstory where one sentence would do. Prompt Engine fixes the request in two ways: the Refiner
          rewrites it for you, and the Coach teaches you to write it yourself.
        </p>
      </header>
    </section>

    <section class="wrap about-section" aria-labelledby="principles-title">
      <header class="page-head">
        <span class="pill-badge">Why it works</span>
        <h2 id="principles-title" class="section-title">Three ideas behind <span class="text-gradient">every rewrite</span></h2>
      </header>
      <div class="pillars">
        <article v-for="(p, i) in principles" :key="p.name" class="pillar card">
          <span class="pillar-no">{{ i + 1 }}</span>
          <h3 class="pillar-name">{{ p.name }}</h3>
          <p class="pillar-detail">{{ p.detail }}</p>
        </article>
      </div>
    </section>

    <section class="wrap about-section" aria-labelledby="stack-title">
      <div class="stack card">
        <div class="stack-intro">
          <span class="pill-badge">Under the hood</span>
          <h2 id="stack-title" class="section-title">What it runs on</h2>
          <p class="page-lede">
            Designed and built by Shakiran Nannyombi. The source, agent diagrams and research notes are on GitHub.
          </p>
          <div class="stack-actions">
            <RouterLink to="/refiner" class="btn btn-primary">Try the Refiner</RouterLink>
            <a href="https://github.com/Shakiran-Nannyombi/Prompt-Engine" target="_blank" rel="noopener" class="btn btn-secondary">View the source</a>
          </div>
        </div>
        <dl class="stack-list">
          <div v-for="s in stack" :key="s.part" class="stack-row">
            <dt>{{ s.part }}</dt>
            <dd>{{ s.tech }}</dd>
          </div>
        </dl>
      </div>
    </section>
  </PublicLayout>
</template>

<style scoped>
.about-section {
  padding-top: 5rem;
}
.pillars {
  display: grid;
  gap: 1.5rem;
}
.pillar {
  padding: 2rem;
}
.pillar-no {
  display: grid;
  place-items: center;
  width: 2.75rem;
  height: 2.75rem;
  margin-bottom: 1.25rem;
  font-weight: 800;
  color: #ffffff;
  background: var(--brand-gradient);
  border-radius: 0.9rem;
  box-shadow: var(--brand-shadow);
}
.pillar-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-text);
}
.pillar-detail {
  margin-top: 0.6rem;
  line-height: 1.65;
  color: var(--color-text-muted);
}

.stack {
  display: grid;
  gap: 2.5rem;
  padding: 2.25rem;
}
.stack-intro {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}
.stack-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
.stack-list {
  margin: 0;
  display: grid;
  align-content: center;
}
.stack-row {
  display: grid;
  grid-template-columns: 7rem 1fr;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid var(--color-card-border);
}
.stack-row:last-child {
  border-bottom: none;
}
.stack-row dt {
  font-weight: 700;
  color: var(--color-primary-strong);
}
.stack-row dd {
  margin: 0;
  color: var(--color-text);
}

@media (min-width: 900px) {
  .pillars {
    grid-template-columns: repeat(3, 1fr);
  }
  .stack {
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    padding: 3rem;
  }
}
</style>
