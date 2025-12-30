<template>
  <div class="tutorials-view">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="navbar-content">
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

        <div class="navbar-actions hidden md:flex">
          <button @click="toggleTheme" class="theme-toggle">
            <svg v-if="!isDarkMode" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.25a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM7.5 12a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM18.894 6.166a.75.75 0 00-1.06-1.06l-1.591 1.59a.75.75 0 101.06 1.061l1.591-1.59zM21.75 12a.75.75 0 01-.75.75h-2.25a.75.75 0 010-1.5H21a.75.75 0 01.75.75zM17.834 18.894a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 10-1.061 1.06l1.59 1.591zM12 18a.75.75 0 01.75.75V21a.75.75 0 01-1.5 0v-2.25A.75.75 0 0112 18zM7.758 17.303a.75.75 0 00-1.061-1.06l-1.591 1.59a.75.75 0 001.06 1.061l1.591-1.59zM6 12a.75.75 0 01-.75.75H3a.75.75 0 010-1.5h2.25A.75.75 0 016 12zM6.697 7.757a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 00-1.061 1.06l1.59 1.591z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path fill-rule="evenodd" d="M9.528 1.718a.75.75 0 01.162.819A8.97 8.97 0 009 6a9 9 0 009 9 8.97 8.97 0 003.463-.69.75.75 0 01.981.98 10.503 10.503 0 01-9.694 6.46c-5.799 0-10.5-4.701-10.5-10.5 0-4.368 2.667-8.112 6.46-9.694a.75.75 0 01.818.162z" clip-rule="evenodd"/>
            </svg>
          </button>
          <RouterLink to="/login" class="navbar-cta">Get Started</RouterLink>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section" id="vanta-tutorials">
      <div class="hero-content">
        <div class="hero-badge">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          Tutorials & Guides
        </div>
        <h1 class="hero-title">Master Prompt-Engine</h1>
        <p class="hero-subtitle">Learn to create perfect prompts in minutes with our comprehensive guides and video tutorials</p>
        <div class="hero-buttons">
          <a href="#quick-start" class="hero-btn primary">Quick Start Guide</a>
          <a href="#videos" class="hero-btn secondary">Watch Videos</a>
        </div>
      </div>
    </div>

    <!-- Quick Start Section -->
    <section id="quick-start" class="section">
      <div class="section-header">
        <h2 class="section-title">Quick Start Guide</h2>
        <p class="section-subtitle">Get up and running in 3 simple steps</p>
      </div>
      
      <div class="steps-grid">
        <div class="step-card">
          <div class="step-number">1</div>
          <div class="step-icon">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
          <h3 class="step-title">Create an Account</h3>
          <p class="step-description">Sign up for free and get instant access to all features</p>
          <RouterLink to="/register" class="step-link">Sign Up Now →</RouterLink>
        </div>

        <div class="step-card">
          <div class="step-number">2</div>
          <div class="step-icon">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <h3 class="step-title">Choose Your Tool</h3>
          <p class="step-description">Start with Coach for guidance or Refiner to improve existing prompts</p>
          <RouterLink to="/coach" class="step-link">Try Coach →</RouterLink>
        </div>

        <div class="step-card">
          <div class="step-number">3</div>
          <div class="step-icon">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </div>
          <h3 class="step-title">Create Perfect Prompts</h3>
          <p class="step-description">Follow the AI guidance and watch your prompts improve instantly</p>
          <a href="#videos" class="step-link">Watch Demo →</a>
        </div>
      </div>
    </section>

    <!-- Video Tutorials Section -->
    <section id="videos" class="section section-dark">
      <div class="section-header">
        <h2 class="section-title">Video Tutorials</h2>
        <p class="section-subtitle">Watch step-by-step guides to master each feature</p>
      </div>

      <div class="videos-grid">
        <div class="video-card">
          <div class="video-thumbnail">
            <div class="play-button">
              <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
            <div class="video-duration">5:30</div>
          </div>
          <div class="video-content">
            <h3 class="video-title">Getting Started with Coach</h3>
            <p class="video-description">Learn how to use the AI Coach to create prompts from scratch with guided assistance</p>
            <div class="video-meta">
              <span class="video-tag">Beginner</span>
              <span class="video-views">2.5k views</span>
            </div>
          </div>
        </div>

        <div class="video-card">
          <div class="video-thumbnail">
            <div class="play-button">
              <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
            <div class="video-duration">4:15</div>
          </div>
          <div class="video-content">
            <h3 class="video-title">Mastering the Refiner</h3>
            <p class="video-description">Discover how to take existing prompts and refine them for better results</p>
            <div class="video-meta">
              <span class="video-tag">Intermediate</span>
              <span class="video-views">1.8k views</span>
            </div>
          </div>
        </div>

        <div class="video-card">
          <div class="video-thumbnail">
            <div class="play-button">
              <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
            <div class="video-duration">6:45</div>
          </div>
          <div class="video-content">
            <h3 class="video-title">Advanced Techniques</h3>
            <p class="video-description">Pro tips and advanced strategies for creating high-quality prompts</p>
            <div class="video-meta">
              <span class="video-tag">Advanced</span>
              <span class="video-views">1.2k views</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Tips & Best Practices -->
    <section class="section">
      <div class="section-header">
        <h2 class="section-title">Tips & Best Practices</h2>
        <p class="section-subtitle">Pro tips to get the most out of Prompt-Engine</p>
      </div>

      <div class="tips-grid">
        <div class="tip-card">
          <div class="tip-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
          </div>
          <h3 class="tip-title">Be Specific</h3>
          <p class="tip-description">The more specific your input, the better the AI can help you craft the perfect prompt</p>
        </div>

        <div class="tip-card">
          <div class="tip-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="tip-title">Define Your Goal</h3>
          <p class="tip-description">Clearly state what you want to achieve with your prompt for targeted results</p>
        </div>

        <div class="tip-card">
          <div class="tip-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <h3 class="tip-title">Iterate & Refine</h3>
          <p class="tip-description">Don't settle for the first version - use Refiner to continuously improve</p>
        </div>

        <div class="tip-card">
          <div class="tip-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <h3 class="tip-title">Add Context</h3>
          <p class="tip-description">Include relevant background information to help the AI understand your needs</p>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="section section-dark">
      <div class="section-header">
        <h2 class="section-title">Frequently Asked Questions</h2>
        <p class="section-subtitle">Find answers to common questions</p>
      </div>

      <div class="faq-container">
        <div 
          v-for="(faq, index) in faqs" 
          :key="index" 
          class="faq-item"
          :class="{ 'active': activeFaq === index }"
          @click="toggleFaq(index)"
        >
          <div class="faq-question">
            <span>{{ faq.question }}</span>
            <svg class="faq-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div class="faq-answer" v-show="activeFaq === index">
            {{ faq.answer }}
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <h2 class="cta-title">Ready to Get Started?</h2>
      <p class="cta-subtitle">Join thousands of users creating perfect prompts</p>
      <RouterLink to="/register" class="cta-button">
        Start Free Trial
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
        </svg>
      </RouterLink>
    </section>

    <!-- Footer Section -->
    <div class="footer-section">
      <div class="footer-content">
        <div class="footer-column">
          <h3 class="footer-title">Join Our Newsletter</h3>
          <div class="newsletter-form">
            <input type="email" placeholder="Enter Your mail" class="newsletter-input">
            <button class="newsletter-button">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
              </svg>
            </button>
          </div>
          <p class="newsletter-disclaimer">* Will send you weekly updates for your better prompt management.</p>
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
            <li><RouterLink to="/docs" class="footer-link">Documentation</RouterLink></li>
            <li><a href="https://github.com/Shakiran-Nannyombi/Prompt-Engine" target="_blank" class="footer-link">GitHub Repository</a></li>
            <li><a href="https://github.com/Shakiran-Nannyombi/Prompt-Engine/issues" target="_blank" class="footer-link">Report Issues</a></li>
            <li><a href="https://github.com/Shakiran-Nannyombi/Prompt-Engine/blob/main/LICENSE" target="_blank" class="footer-link">License</a></li>
          </ul>
        </div>
        
        <div class="footer-column">
          <h3 class="footer-title">Social</h3>
          <ul class="footer-links">
            <li><a href="https://github.com/Shakiran-Nannyombi/Prompt-Engine" target="_blank" class="footer-link social-link">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
              </svg>
            </a></li>
            <li><a href="#" class="footer-link social-link">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
              Twitter
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
              </svg>
            </a></li>
            <li><a href="#" class="footer-link social-link">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
              LinkedIn
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
              </svg>
            </a></li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p class="copyright">© Copyright 2025 Prompt-Engine All Rights Reserved</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'

const isDarkMode = ref(false)
const activeFaq = ref(null)

const faqs = [
  {
    question: "How do I get started with Prompt-Engine?",
    answer: "Simply create a free account, choose between Coach or Refiner, and start creating prompts. Coach guides you through the process, while Refiner helps improve existing prompts."
  },
  {
    question: "What's the difference between Coach and Refiner?",
    answer: "Coach helps you create prompts from scratch with AI guidance through a 4-stage process. Refiner takes your existing prompts and suggests improvements for better results."
  },
  {
    question: "Is Prompt-Engine free to use?",
    answer: "Yes! Prompt-Engine offers a free tier with access to all core features. Premium plans with advanced features are also available."
  },
  {
    question: "Can I use Prompt-Engine for any type of prompt?",
    answer: "Absolutely! Prompt-Engine works with all types of prompts - from content creation and coding to data analysis and creative writing."
  },
  {
    question: "How does the AI coaching work?",
    answer: "The AI Coach asks targeted questions about your goals, analyzes your needs, and guides you through creating an optimized prompt step by step."
  }
]

const toggleFaq = (index) => {
  activeFaq.value = activeFaq.value === index ? null : index
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
}

let vantaEffect = null

onMounted(() => {
  // Initialize theme
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  }

  // Initialize Vanta effect
  const loadScript = (src) => {
    return new Promise((resolve, reject) => {
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

  if (window.VANTA && window.VANTA.WAVES) {
    initVanta()
  } else {
    Promise.all([
      loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js'),
      loadScript('https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js')
    ]).then(() => {
      return loadScript('https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.waves.min.js')
    }).then(() => {
      setTimeout(initVanta, 100)
    }).catch(console.error)
  }
})

const initVanta = () => {
  if (window.VANTA && window.VANTA.WAVES) {
    const isDark = document.documentElement.classList.contains('dark')
    vantaEffect = window.VANTA.WAVES({
      el: "#vanta-tutorials",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: isDark ? 0x1a1a2e : 0x3b82f6,
      shininess: 30.00,
      waveHeight: 15.00,
      waveSpeed: 0.75,
      zoom: 0.75
    })
  }
}

onUnmounted(() => {
  if (vantaEffect) {
    vantaEffect.destroy()
  }
})
</script>

<style scoped src="@/assets/styles/AboutView.css"></style>
<style scoped>
.tutorials-view {
  min-height: 100vh;
  background: var(--color-background);
  color: var(--color-text);
}

/* Hero Section */
.hero-section {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 8rem 2rem 4rem;
}

.hero-content {
  max-width: 800px;
  text-align: center;
  position: relative;
  z-index: 10;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(var(--color-primary-rgb, 59, 130, 246), 0.1);
  border: 1px solid rgba(var(--color-primary-rgb, 59, 130, 246), 0.3);
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: 2rem;
}

.hero-title {
  font-size: 4rem;
  font-weight: 950;
  letter-spacing: -0.05em;
  background: linear-gradient(135deg, #f60968, #3b82f6);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.8;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-btn {
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.hero-btn.primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.hero-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.hero-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--color-text);
}

.hero-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

/* Sections */
.section {
  padding: 5rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-dark {
  background: rgba(0, 0, 0, 0.02);
}

.tutorials-view:global(.dark) .section-dark {
  background: rgba(255, 255, 255, 0.02);
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.125rem;
  opacity: 0.7;
}

/* Steps Grid */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.step-card {
  position: relative;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.5rem;
  transition: all 0.3s ease;
}

.step-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.step-number {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 50%;
  font-size: 1.25rem;
  font-weight: 900;
  color: white;
}

.step-icon {
  width: 4rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--color-primary-rgb, 59, 130, 246), 0.1);
  border-radius: 1rem;
  color: var(--color-primary);
  margin-bottom: 1.5rem;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
}

.step-description {
  opacity: 0.8;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.step-link {
  color: var(--color-primary);
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
}

.step-link:hover {
  transform: translateX(5px);
  display: inline-block;
}

/* Videos Grid */
.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.video-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.video-thumbnail {
  position: relative;
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
}

.play-button {
  width: 4rem;
  height: 4rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366f1;
  transition: all 0.3s ease;
}

.video-card:hover .play-button {
  transform: scale(1.1);
}

.video-duration {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: white;
}

.video-content {
  padding: 1.5rem;
}

.video-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
}

.video-description {
  opacity: 0.8;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.video-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
}

.video-tag {
  padding: 0.25rem 0.75rem;
  background: rgba(var(--color-primary-rgb, 59, 130, 246), 0.2);
  border-radius: 0.5rem;
  color: var(--color-primary);
  font-weight: 600;
}

.video-views {
  opacity: 0.6;
}

/* Tips Grid */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.tip-card {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-5px);
  border-color: var(--color-primary);
}

.tip-icon {
  width: 4rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--color-primary-rgb, 99, 102, 241), 0.1);
  border-radius: 1rem;
  color: var(--color-primary);
  margin: 0 auto 1rem;
}

.tip-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
}

.tip-description {
  opacity: 0.8;
  line-height: 1.6;
}

/* FAQ */
.faq-container {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  margin-bottom: 1rem;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.faq-item:hover {
  border-color: var(--color-primary);
}

.faq-item.active {
  background: rgba(var(--color-primary-rgb, 59, 130, 246), 0.1);
}

.faq-question {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 700;
  font-size: 1.125rem;
}

.faq-icon {
  width: 1.5rem;
  height: 1.5rem;
  transition: transform 0.3s ease;
}

.faq-item.active .faq-icon {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
  opacity: 0.8;
  line-height: 1.8;
}

/* CTA Section */
.cta-section {
  padding: 5rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
}

.cta-title {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 1rem;
}

.cta-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1.25rem 2.5rem;
  background: white;
  color: #6366f1;
  border-radius: 0.75rem;
  font-weight: 800;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* Footer Section */
.footer-section {
  background: var(--color-secondary);
  padding: 4rem 2rem 0;
  width: 100%;
  position: relative;
  z-index: 2;
  margin-top: 5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.footer-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.newsletter-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.newsletter-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background: var(--color-input-bg);
  border: 1px solid var(--color-input-border);
  border-radius: 0.5rem;
  color: var(--color-text);
  font-size: 0.9rem;
}

.newsletter-input::placeholder {
  color: var(--color-text);
  opacity: 0.5;
}

.newsletter-button {
  padding: 0.75rem;
  background: var(--color-primary);
  border: none;
  border-radius: 0.5rem;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.newsletter-button:hover {
  background: var(--color-accent);
  transform: translateY(-2px);
}

.newsletter-disclaimer {
  font-size: 0.8rem;
  color: var(--color-text);
  line-height: 1.4;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-link {
  color: var(--color-text);
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-link:hover {
  color: var(--color-primary);
  transform: translateX(5px);
}

.social-link {
  justify-content: space-between;
}

.social-link svg:last-child {
  opacity: 0.7;
  transition: all 0.3s ease;
}

.social-link:hover svg:last-child {
  opacity: 1;
  transform: translate(2px, -2px);
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem 0;
  text-align: center;
}

.copyright {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

/* Responsive Design for CTA and Footer */
@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 3rem;
    text-align: center;
  }

  .footer-column {
    align-items: center;
  }

  .footer-links {
    justify-content: center;
  }

  .newsletter-form {
    width: 100%;
    max-width: 400px;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .steps-grid,
  .videos-grid,
  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>
