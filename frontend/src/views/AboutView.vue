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
    detail: 'The Refiner sorts each prompt into clarity, precision, creative or document work, then rewrites it with a framework that suits it, such as C.O.R.E., R.A.C.E. or C.A.R.',
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
    <section class="wrap about-hero">
      <h1 class="about-title">Most prompts are briefs with the brief left out.</h1>
      <div class="about-lede prose-manuscript">
        <p>
          AI models are capable enough. What usually goes wrong is the request: no role, no reader, no format, and a
          paragraph of backstory where one sentence would do.
        </p>
        <p>
          Prompt Engine fixes the request in two ways. The Refiner rewrites it for you. The Coach takes you through
          writing it yourself, so you need the Refiner less over time.
        </p>
      </div>
    </section>

    <section class="wrap about-section" aria-labelledby="principles-title">
      <h2 id="principles-title" class="side-title">How it works</h2>
      <dl class="rows">
        <div v-for="p in principles" :key="p.name" class="row">
          <dt>{{ p.name }}</dt>
          <dd>{{ p.detail }}</dd>
        </div>
      </dl>
    </section>

    <section class="wrap about-section" aria-labelledby="stack-title">
      <h2 id="stack-title" class="side-title">What it runs on</h2>
      <dl class="rows">
        <div v-for="s in stack" :key="s.part" class="row compact">
          <dt>{{ s.part }}</dt>
          <dd>{{ s.tech }}</dd>
        </div>
      </dl>
    </section>

    <section class="wrap about-section" aria-labelledby="maker-title">
      <h2 id="maker-title" class="side-title">Who made it</h2>
      <div class="maker">
        <p>
          Prompt Engine was designed and built by Shakiran Nannyombi. The source, agent diagrams and research notes are
          on GitHub.
        </p>
        <div class="maker-actions">
          <a href="https://github.com/Shakiran-Nannyombi/Prompt-Engine" target="_blank" rel="noopener" class="btn btn-secondary">
            View the source
          </a>
          <RouterLink to="/refiner" class="btn btn-primary">Try the Refiner</RouterLink>
        </div>
      </div>
    </section>
  </PublicLayout>
</template>

<style scoped>
.about-hero {
  padding-top: 5rem;
  padding-bottom: 1rem;
}
.about-title {
  font-size: clamp(2.4rem, 1.4rem + 4vw, 4rem);
  font-weight: 750;
  letter-spacing: -0.045em;
  line-height: 1.02;
  max-width: 16ch;
}
.about-lede {
  margin-top: 2rem;
  display: grid;
  gap: 1rem;
  font-size: 1.2rem;
  color: var(--ink-muted);
  max-width: 36rem;
}

.about-section {
  display: grid;
  gap: 1.5rem;
  padding-top: 5rem;
}
.side-title {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.rows {
  margin: 0;
  border-top: 1px solid var(--rule);
}
.row {
  display: grid;
  gap: 0.4rem;
  padding: 1.35rem 0;
  border-bottom: 1px solid var(--rule);
}
.row dt {
  font-weight: 600;
  font-size: 1.1rem;
}
.row dd {
  margin: 0;
  color: var(--ink-muted);
  max-width: 38rem;
}
.row.compact {
  padding: 1rem 0;
}
.maker p {
  font-size: 1.1rem;
  max-width: 36rem;
}
.maker-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

@media (min-width: 900px) {
  .about-section {
    grid-template-columns: 14rem minmax(0, 1fr);
    gap: 3rem;
  }
  .row {
    grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
    gap: 2rem;
  }
}
</style>
