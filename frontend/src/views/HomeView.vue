<template>
  <div class="bg-transparent">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-content">
        <!-- Logo and Brand -->
        <div class="navbar-brand">
          <img src="@/assets/images/logo.svg" alt="Prompt-Engine Logo" class="logo-icon" />
          <span class="brand-name">Prompt-Engine</span>
        </div>
        
        <div class="navbar-links hidden md:flex">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
          <RouterLink to="/coach" class="nav-link">Coach</RouterLink>
          <RouterLink to="/refiner" class="nav-link">Refiner</RouterLink>
          <RouterLink to="/about" class="nav-link">About</RouterLink>
        </div>


        <div class="navbar-actions-wrapper flex items-center justify-end flex-1">
          <div class="navbar-actions hidden md:flex">
            <button @click="toggleTheme" class="theme-toggle" :aria-label="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'">
              <svg v-if="!isDarkMode" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2.25a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM7.5 12a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM18.894 6.166a.75.75 0 00-1.06-1.06l-1.591 1.59a.75.75 0 101.06 1.061l1.591-1.59zM21.75 12a.75.75 0 01-.75.75h-2.25a.75.75 0 010-1.5H21a.75.75 0 01.75.75zM17.834 18.894a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 10-1.061 1.06l1.59 1.591zM12 18a.75.75 0 01.75.75V21a.75.75 0 01-1.5 0v-2.25A.75.75 0 0112 18zM7.758 17.303a.75.75 0 00-1.061-1.06l-1.591 1.59a.75.75 0 001.06 1.061l1.591-1.59zM6 12a.75.75 0 01-.75.75H3a.75.75 0 010-1.5h2.25A.75.75 0 016 12zM6.697 7.757a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 00-1.061 1.06l1.59 1.591z"/>
              </svg>
              <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M9.528 1.718a.75.75 0 01.162.819A8.97 8.97 0 009 6a9 9 0 009 9 8.97 8.97 0 003.463-.69.75.75 0 01.981.98 10.503 10.503 0 01-9.694 6.46c-5.799 0-10.5-4.701-10.5-10.5 0-4.368 2.667-8.112 6.46-9.694a.75.75 0 01.818.162z" clip-rule="evenodd"/>
              </svg>
            </button>
            <RouterLink v-if="!authStore.isAuthenticated" to="/login" class="navbar-cta">
              Login
            </RouterLink>
            <button v-else @click="handleLogout" class="navbar-cta">
              Logout
            </button>
          </div>
        </div>

        <!-- Mobile Menu Toggle (Always Outside hidden desktop actions) -->
        <button 
          @click="toggleMobileMenu" 
          class="menu-toggle md:hidden"
          aria-label="Toggle menu"
          style="z-index: 10001;"
        >
          <svg v-if="!showMobileMenu" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

    </nav>

    <!-- Mobile Menu (Outside nav to break out of transform context) -->
    <Transition
      @enter="onMenuEnter"
      @leave="onMenuLeave"
    >
      <div v-if="showMobileMenu" class="mobile-menu md:hidden fixed inset-0 z-[1000000] flex flex-col">
        <div class="mobile-menu-header p-4 border-b border-card-border flex items-center justify-between">
          <div class="navbar-brand">
            <img src="@/assets/images/logo.svg" alt="Prompt-Engine Logo" class="logo-icon" />
            <span class="brand-name">Prompt-Engine</span>
          </div>
          <button @click="showMobileMenu = false" class="p-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mobile-menu-links">
          <RouterLink to="/" class="mobile-nav-link" @click="showMobileMenu = false">Home</RouterLink>
          <RouterLink to="/coach" class="mobile-nav-link" @click="showMobileMenu = false">Coach</RouterLink>
          <RouterLink to="/refiner" class="mobile-nav-link" @click="showMobileMenu = false">Refiner</RouterLink>
          <RouterLink to="/tutorials" class="mobile-nav-link" @click="showMobileMenu = false">Tutorials</RouterLink>
          <RouterLink to="/about" class="mobile-nav-link" @click="showMobileMenu = false">About Us</RouterLink>
        </div>
        <div class="mobile-menu-actions">
          <button @click="toggleTheme" class="mobile-theme-toggle">
            <span class="mr-2">{{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}</span>
            <svg v-if="!isDarkMode" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.25a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM7.5 12a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM18.894 6.166a.75.75 0 00-1.06-1.06l-1.591 1.59a.75.75 0 101.06 1.061l1.591-1.59zM21.75 12a.75.75 0 01-.75.75h-2.25a.75.75 0 010-1.5H21a.75.75 0 01.75.75zM17.834 18.894a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 10-1.061 1.06l1.59 1.591zM12 18a.75.75 0 01.75.75V21a.75.75 0 01-1.5 0v-2.25A.75.75 0 0112 18zM7.758 17.303a.75.75 0 00-1.061-1.06l-1.591 1.59a.75.75 0 001.06 1.061l1.591-1.59zM6 12a.75.75 0 01-.75.75H3a.75.75 0 010-1.5h2.25A.75.75 0 016 12zM6.697 7.757a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 00-1.061 1.06l1.59 1.591z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path fill-rule="evenodd" d="M9.528 1.718a.75.75 0 01.162.819A8.97 8.97 0 009 6a9 9 0 009 9 8.97 8.97 0 003.463-.69.75.75 0 01.981.98 10.503 10.503 0 01-9.694 6.46c-5.799 0-10.5-4.701-10.5-10.5 0-4.368 2.667-8.112 6.46-9.694a.75.75 0 01.818.162z" clip-rule="evenodd"/>
            </svg>
          </button>
          <RouterLink to="/tutorials" class="mobile-cta" @click="showMobileMenu = false">
            Try Tutorials
          </RouterLink>
        </div>
      </div>
    </Transition>

    <!-- Hero Section 1 -->
    <div class="hero-wrapper">
      <div id="vanta-hero" class="hero-section">
        <div class="hero-content-right">
          <div class="hero-text-content">
            <h1 class="hero-main-title">
              <span class="typewriter-text" ref="typewriterText"></span>
            </h1>
            <p class="hero-description">
              Automate prompt creation, refine existing prompts, and boost productivity with intelligent AI agents that understand your needs.
            </p>
            <div class="hero-buttons">
              <RouterLink to="/register" class="hero-btn primary-btn">
                Get Started for Free
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
                </svg>
              </RouterLink>
              <RouterLink to="/tutorials" class="hero-btn secondary-btn">
                See How It Works
              </RouterLink>
            </div>
          </div>
          
          <div class="floating-cards-row">
            <div class="floating-card-small animated-card">
              <div class="card-icon-small">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <h4 class="card-title-small">Smart AI Coaching</h4>
            </div>
            
            <div class="floating-card-small animated-card">
              <div class="card-icon-small">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                </svg>
              </div>
              <h4 class="card-title-small">Instant Refinement</h4>
            </div>
            
            <div class="floating-card-small animated-card">
              <div class="card-icon-small">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <h4 class="card-title-small">Works With Any AI</h4>
            </div>
            
            <div class="floating-card-small animated-card">
              <div class="card-icon-small">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4 0h-2v6h2v-6zm2.5-9H19V1h-2v1H7V1H5v1H4.5C3.67 2 3 2.67 3 3.5v15c0 .83.67 1.5 1.5 1.5h15c.83 0 1.5-.67 1.5-1.5v-15c0-.83-.67-1.5-1.5-1.5z"/>
                </svg>
              </div>
              <h4 class="card-title-small">Step-by-step Guidance</h4>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hero Section 2  -->
    <div class="hero-section-scrollable features-section">
      <div class="hero-content">
        <div class="features-header">
          <button class="features-btn">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
            Features
          </button>
          <h1 class="hero-title">What makes our Prompt-Engine stand out?</h1>
        </div>
        
        <div class="tabs-container" role="tablist" aria-label="Features">
          <button
            v-for="(f, i) in features"
            :key="f.tab"
            type="button"
            role="tab"
            class="tab"
            :class="{ active: activeFeature === i }"
            :aria-selected="activeFeature === i"
            @click="activeFeature = i"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path :d="f.icon" /></svg>
            {{ f.tab }}
          </button>
        </div>

        <div class="feature-content" role="tabpanel">
          <div class="feature-text">
            <h2 class="feature-main-title">{{ currentFeature.title }}</h2>
            <p class="feature-main-description">{{ currentFeature.description }}</p>

            <div class="feature-items">
              <div v-for="(point, i) in currentFeature.points" :key="point" class="feature-item">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path :d="i === 0 ? icons.star : icons.check" /></svg>
                {{ point }}
              </div>
            </div>
          </div>

          <div class="feature-visual">
            <div class="visual-cards">
              <div v-for="card in currentFeature.example" :key="card.label" class="visual-card">
                <div class="card-content">
                  <span class="card-label">{{ card.label }}:</span>
                  <span class="card-text">"{{ card.text }}"</span>
                </div>
              </div>
            </div>
            <div class="avatar-group">
              <button
                v-for="(f, i) in features"
                :key="f.tab"
                type="button"
                class="avatar"
                :class="{ active: activeFeature === i }"
                :aria-label="`Show ${f.tab}`"
                @click="activeFeature = i"
              >
                <svg class="avatar-icon" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path :d="f.icon" /></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hero Section 3  -->
    <div class="hero-section-scrollable">
      <div class="hero-content">
        <div class="how-it-works-header">
          <button class="how-it-works-btn">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            How it works
          </button>
          <h1 class="hero-title">How our Prompt-Engine works in <br><span class="title-highlight">3 simple steps</span></h1>
        </div>
        
        <div class="steps-content">
          <div class="step-panel animated-panel">
            <div class="step-number">{{ activeStep + 1 }}</div>
            <div class="step-content">
              <h2 class="step-title">{{ currentStep.title }}</h2>
              <p class="step-description">{{ currentStep.description }}</p>

              <div class="step-features">
                <div v-for="(point, i) in currentStep.points" :key="point" class="step-feature animated-feature">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path :d="i === 0 ? icons.check : icons.chat" /></svg>
                  {{ point }}
                </div>
              </div>

              <div class="step-switcher" role="tablist" aria-label="Steps">
                <button
                  v-for="(st, i) in steps"
                  :key="st.title"
                  type="button"
                  role="tab"
                  class="step-dot"
                  :class="{ active: activeStep === i }"
                  :aria-selected="activeStep === i"
                  @click="activeStep = i"
                >
                  {{ i + 1 }}. {{ st.short }}
                </button>
              </div>
            </div>
          </div>

          <div class="chat-example-panel animated-panel">
            <div class="chat-header">
              <div class="chat-logo">
                <div class="logo-circle">P</div>
              </div>
              <span class="chat-title">Prompt-Engine</span>
            </div>
            
            <div class="chat-messages">
              <div class="message-line animated-line"></div>
              <div class="message-line animated-line"></div>
              <div class="message-line animated-line"></div>
            </div>
            
            <div class="chat-input-area">
              <div class="input-field">
                <span class="input-text">{{ currentStep.chat }}</span>
                <div class="input-tags">
                  <span class="tag">Content</span>
                  <span class="tag">Writing</span>
                </div>
              </div>
              <div class="input-actions">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hero Section 4 - Call to Action -->
    <div class="hero-section-scrollable">
      <div class="cta-content" id="vanta-cta"></div>
      <div class="cta-text">
        <h1 class="cta-title">Unleash your ideas. <br><span class="cta-highlight">Write better prompts.</span></h1>
        <p class="cta-description">It's free to use. Bring a rough idea and leave with a clear, structured prompt you can use in any AI tool.</p>
        <RouterLink to="/register" class="cta-button">
          Get Started for Free
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </RouterLink>
      </div>
    </div>

    <!-- Spacer between sections and footer -->
    <div class="hero-section-spacer"></div>

    <AppFooter />
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import AppFooter from '@/components/layout/AppFooter.vue'
import '@/assets/styles/HomeView.css'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'
import gsap from 'gsap'

const router = useRouter()
const authStore = useAuthStore()

// Logout handler
const handleLogout = () => {
  authStore.logout()
  router.push('/')
}


// Feature tabs and "how it works" steps
const icons = {
  star: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
  doc: 'M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z',
  check: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z',
  bolt: 'M7 2v11h3v9l7-12h-4l4-8z',
  chat: 'M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z',
}

const features = [
  {
    tab: 'Smart Coaching',
    icon: icons.star,
    title: 'Coaching that teaches you as you go',
    description: 'The Coach walks you through a structured process (task, context, references, then the final prompt) and explains each step, so you get better at prompting every time you use it.',
    points: ['Guided, step-by-step process', 'Explains why each change helps'],
    example: [
      { label: 'Input', text: 'Write a blog post about AI' },
      { label: 'Coaching', text: 'Who is it for, and what should they take away from it?' },
      { label: 'Output', text: 'Write a 600-word blog post for small-business owners on three practical ways to use AI in customer support.' },
    ],
  },
  {
    tab: 'Instant Refinement',
    icon: icons.doc,
    title: 'Paste a prompt, get a sharper one back',
    description: 'The Refiner rewrites your prompt in one pass using proven frameworks, adding a role, a clear audience and the format you need.',
    points: ['Framework-based rewrites', 'Copy the result in one click'],
    example: [
      { label: 'Input', text: 'Summarise this report' },
      { label: 'Refiner', text: 'Adds a role, a length and a structure' },
      { label: 'Output', text: 'You are an analyst briefing a busy manager. Summarise the report in five bullet points, leading with the decision it asks for.' },
    ],
  },
  {
    tab: 'Prompt Optimization',
    icon: icons.check,
    title: 'Shorter prompts that say more',
    description: "Long prompts aren't better prompts. Prompt-Engine cuts the filler and backstory the model doesn't need, and keeps the instructions that change the answer.",
    points: ['Removes padding and repetition', 'Keeps what matters to the model'],
    example: [
      { label: 'Input', text: "I've been working on this project for a while and wondered if you could maybe help me write an email to my team about it..." },
      { label: 'Optimizing', text: 'Cut the backstory, keep the ask' },
      { label: 'Output', text: 'Write a short, friendly email telling my team the launch moves to Friday, and ask them to confirm by Wednesday.' },
    ],
  },
  {
    tab: 'Ready-to-use Results',
    icon: icons.bolt,
    title: 'Prompts you can use straight away',
    description: 'Every result is a complete prompt you can paste into ChatGPT, Claude, Gemini or any other AI tool. No special syntax and no lock-in.',
    points: ['Works with any AI model', 'Copy or download in one click'],
    example: [
      { label: 'Input', text: 'Explain recursion' },
      { label: 'Result', text: 'Adds a clear role, level and format' },
      { label: 'Output', text: 'You are a patient tutor. Explain recursion to a beginner in under 200 words, with one Python example and one common mistake to avoid.' },
    ],
  },
]
const activeFeature = ref(0)
const currentFeature = computed(() => features[activeFeature.value])

const steps = [
  {
    short: 'Ask',
    title: 'Ask anything',
    description: 'Just type your question, task or idea, like "Draft a client email", "Summarise this blog" or "Plan my week".',
    points: ['Natural language input, no special commands.', 'Example prompts to get you started.'],
    chat: 'How do I create an effective prompt for content writing?',
  },
  {
    short: 'Refine',
    title: 'Get coached or refined',
    description: 'Choose the Coach to build your prompt step by step, or the Refiner to rewrite it for you in one go.',
    points: ['The Coach asks the right questions.', 'The Refiner applies proven frameworks.'],
    chat: 'Who is the audience, and what format should the answer take?',
  },
  {
    short: 'Use',
    title: 'Copy and use it',
    description: 'Take the finished prompt to any AI tool and get a clearer, more useful answer the first time.',
    points: ['Works with any chat model.', 'Copy or download it in one click.'],
    chat: 'Write a 600-word blog post for small-business owners on using AI in customer support.',
  },
]
const activeStep = ref(0)
const currentStep = computed(() => steps[activeStep.value])

// Theme toggle
const isDarkMode = ref(false)
const showMobileMenu = ref(false)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const onMenuEnter = (el, done) => {
  gsap.fromTo(el,
    { y: '-100%', opacity: 0 },
    { y: '0%', opacity: 1, duration: 0.4, ease: 'power2.out', onComplete: done }
  )
}

const onMenuLeave = (el, done) => {
  gsap.to(el, {
    y: '-100%',
    opacity: 0,
    duration: 0.3,
    ease: 'power2.in',
    onComplete: done
  })
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
  
  // Reinitialize VANTA effects with new theme colors
  reinitializeVantaEffects()
}

// Typewriter animation
const typewriterText = ref(null)
let typewriterInterval = null
let currentText = ''
let currentIndex = 0
let isDeleting = false

const fullText = 'Meet your new AI-Powered prompt engineering agents'
const typingSpeed = 100 // milliseconds per character
const deletingSpeed = 50 // milliseconds per character
const pauseTime = 5000 // 5 seconds pause

let vantaEffect = null
let vantaCtaEffect = null
let scrollHandler = null

// Function to reinitialize VANTA effects with current theme
const reinitializeVantaEffects = () => {
  // Destroy existing effects
  if (vantaEffect) {
    vantaEffect.destroy()
    vantaEffect = null
  }
  if (vantaCtaEffect) {
    vantaCtaEffect.destroy()
    vantaCtaEffect = null
  }
  
  // Reinitialize with current theme
  setTimeout(() => {
    initializeVantaEffects()
  }, 100)
}

// Function to initialize VANTA effects
const initializeVantaEffects = () => {
  // Initialize VANTA.HALO for first hero section
  if (window.VANTA && window.VANTA.HALO) {
    const isDarkMode = document.documentElement.classList.contains('dark')
    vantaEffect = window.VANTA.HALO({
      el: "#vanta-hero",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      backgroundColor: isDarkMode ? 0x60740 : 0x9a9cde,
      amplitudeFactor: 1.30,
      xOffset: 0.17,
      size: 1.20
    })
  }

  // CTA background is created lazily by the IntersectionObserver below
  if (ctaVisible) initCtaEffect()
}

// The topology effect is CPU-heavy, so it only runs while the CTA is near the screen
let ctaVisible = false
let ctaObserver = null
const initCtaEffect = () => {
  if (vantaCtaEffect || !window.VANTA || !window.VANTA.TOPOLOGY) return
  const isDarkMode = document.documentElement.classList.contains('dark')
    vantaCtaEffect = window.VANTA.TOPOLOGY({
      el: "#vanta-cta",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: isDarkMode ? 0x4e5296 : 0xc0f4a,
      backgroundColor: isDarkMode ? 0x222 : 0x7f85e8
    })
}

// Typewriter animation function
const typeWriter = () => {
  if (!typewriterText.value) return
  
  if (isDeleting) {
    // Deleting characters
    currentText = fullText.substring(0, currentIndex - 1)
    currentIndex--
    
    if (currentIndex === 0) {
      isDeleting = false
      // Start typing again immediately after clearing
      typeWriter()
      return
    }
  } else {
    // Typing characters
    currentText = fullText.substring(0, currentIndex + 1)
    currentIndex++
    
    if (currentText === fullText) {
      // Show the full line, then wait before deleting
      typewriterText.value.innerHTML = fullText.replace('AI-Powered', '<span class="colors-text">AI-Powered</span>')
      typewriterInterval = setTimeout(() => {
        isDeleting = true
        typeWriter()
      }, pauseTime)
      return
    }
  }
  
  // Update the text with special styling for "AI-Powered"
  let displayText = currentText
  
  // Add gradient to "AI-Powered"
  if (currentText.includes('AI-Powered')) {
    displayText = displayText.replace('AI-Powered', '<span class="colors-text">AI-Powered</span>')
  }
  
  typewriterText.value.innerHTML = displayText
  
  // Continue typing/deleting
  const speed = isDeleting ? deletingSpeed : typingSpeed
  typewriterInterval = setTimeout(typeWriter, speed)
}

onMounted(() => {
  // Initialize theme
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDarkMode.value = false
    document.documentElement.classList.remove('dark')
  }

  const loadScript = (src) => {
    return new Promise((resolve, reject) => {
      // Check if script is already loaded
      if (document.querySelector(`script[src="${src}"]`)) {
        resolve()
        return
      }
      
      const script = document.createElement('script')
      script.src = src
      script.async = true
      script.onload = resolve
      script.onerror = reject
      document.head.appendChild(script)
    })
  }

  // Check if VANTA is already loaded
  if (window.VANTA) {
    initializeVantaEffects()
  } else {
    // Load scripts and initialize VANTA
    Promise.all([
      loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js'),
      loadScript('https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js')
    ]).then(() => {
        // Load Vanta effects after dependencies
        return Promise.all([
            loadScript('https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.halo.min.js'),
            loadScript('https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.topology.min.js')
        ])
    }).then(() => {
      // Initialize VANTA effects
      // Small delay to ensure scripts are parsed and executed
      setTimeout(() => {
        initializeVantaEffects()
      }, 100)
    }).catch(error => {
      console.error('Failed to load VANTA scripts:', error)
    })
  }

  // Add scroll handler for zoom effect
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const vantaHero = document.getElementById('vanta-hero')
  const navbar = document.querySelector('.navbar')
  let ticking = false

  const update = () => {
    ticking = false
    const y = window.scrollY
    if (vantaHero && !reduceMotion) {
      // Zoom the hero background from 1.2x to 1x over the first two screens
      const progress = Math.min(y / (window.innerHeight * 2), 1)
      vantaHero.style.transform = `scale(${(1.2 - progress * 0.2).toFixed(4)})`
    }
    if (navbar) navbar.classList.toggle('scrolled', y > 50)
  }

  scrollHandler = () => {
    if (!ticking) {
      ticking = true
      requestAnimationFrame(update)
    }
  }
  window.addEventListener('scroll', scrollHandler, { passive: true })
  update()

  const ctaEl = document.getElementById('vanta-cta')
  if (ctaEl && 'IntersectionObserver' in window) {
    ctaObserver = new IntersectionObserver(
      ([entry]) => {
        ctaVisible = entry.isIntersecting
        if (ctaVisible) {
          initCtaEffect()
        } else if (vantaCtaEffect) {
          vantaCtaEffect.destroy()
          vantaCtaEffect = null
        }
      },
      { rootMargin: '200px 0px' },
    )
    ctaObserver.observe(ctaEl)
  } else {
    ctaVisible = true
  }

  if (typewriterInterval) clearTimeout(typewriterInterval)
  setTimeout(() => {
    // Reset state for cleaner re-entry
    currentIndex = 0
    isDeleting = false
    if(typewriterText.value) typewriterText.value.innerHTML = ''
    typeWriter()
  }, 1000) // Start after 1 second delay
})

onUnmounted(() => {
  // Clean up VANTA effects
  if (vantaEffect) {
    vantaEffect.destroy()
    vantaEffect = null
  }
  if (vantaCtaEffect) {
    vantaCtaEffect.destroy()
    vantaCtaEffect = null
  }
  
  // Clean up scroll handlers
  if (scrollHandler) {
    window.removeEventListener('scroll', scrollHandler)
    scrollHandler = null
  }
  if (ctaObserver) {
    ctaObserver.disconnect()
    ctaObserver = null
  }
  
  // Clean up typewriter animation
  if (typewriterInterval) {
    clearTimeout(typewriterInterval)
    typewriterInterval = null
  }
})
</script>

