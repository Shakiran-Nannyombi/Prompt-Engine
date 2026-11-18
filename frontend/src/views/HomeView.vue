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
                Watch Demo
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
              <h4 class="card-title-small">Proven Results</h4>
            </div>
            
            <div class="floating-card-small animated-card">
              <div class="card-icon-small">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4 0h-2v6h2v-6zm2.5-9H19V1h-2v1H7V1H5v1H4.5C3.67 2 3 2.67 3 3.5v15c0 .83.67 1.5 1.5 1.5h15c.83 0 1.5-.67 1.5-1.5v-15c0-.83-.67-1.5-1.5-1.5z"/>
                </svg>
              </div>
              <h4 class="card-title-small">Real-time Feedback</h4>
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
        
        <div class="tabs-container">
          <div class="tab active">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            Smart Coaching
          </div>
          <div class="tab">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
            </svg>
            Document Refinement
          </div>
          <div class="tab">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            Prompt Optimization
          </div>
          <div class="tab">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4 0h-2v6h2v-6zm2.5-9H19V1h-2v1H7V1H5v1H4.5C3.67 2 3 2.67 3 3.5v15c0 .83.67 1.5 1.5 1.5h15c.83 0 1.5-.67 1.5-1.5v-15c0-.83-.67-1.5-1.5-1.5z"/>
            </svg>
            Real-time Results
          </div>
        </div>
        
        <div class="feature-content">
          <div class="feature-text">
            <h2 class="feature-main-title">Intelligent prompt coaching that delivers results</h2>
            <p class="feature-main-description">Our Prompt-Engine doesn't just create prompts—it coaches you through a proven 4-stage process. Whether you're a beginner or expert, it provides step-by-step guidance, applies established frameworks, and delivers optimized prompts for your specific use case.</p>
            
            <div class="feature-items">
              <div class="feature-item">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                Proven 4-stage coaching process
              </div>
              <div class="feature-item">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                Document-based prompt refinement
              </div>
            </div>
          </div>
          
          <div class="feature-visual">
            <div class="visual-cards">
              <div class="visual-card">
                <div class="card-content">
                  <span class="card-label">Input:</span>
                  <span class="card-text">"Write a blog post about AI"</span>
                </div>
              </div>
              <div class="visual-card">
                <div class="card-content">
                  <span class="card-label">Coaching:</span>
                  <span class="card-text">"Let's add context, target audience, and specific goals to make this more effective"</span>
                </div>
              </div>
              <div class="visual-card">
                <div class="card-content">
                  <span class="card-label">Output:</span>
                  <span class="card-text">"Write a comprehensive blog post about AI for small business owners, focusing on practical applications and ROI"</span>
                </div>
              </div>
            </div>
            <div class="avatar-group">
              <div class="avatar">
                <svg class="avatar-icon" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
              <div class="avatar active">
                <svg class="avatar-icon" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <div class="avatar">
                <svg class="avatar-icon" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
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
          <h1 class="hero-title">How our Prompt-Engine works in<br><span class="title-highlight">3 simple steps</span></h1>
        </div>
        
        <div class="steps-content">
          <div class="step-panel animated-panel">
            <div class="step-number">1</div>
            <div class="step-content">
              <h2 class="step-title">Ask anything</h2>
              <p class="step-description">Just type your question, task, or idea—like "Draft a client email," "Summarize this blog," or "Plan my week."</p>
              
              <div class="step-features">
                <div class="step-feature animated-feature">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                  Natural language input—no special commands.
                </div>
                <div class="step-feature animated-feature">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
                  </svg>
                  Smart prompt suggestions to guide you.
                </div>
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
                <span class="input-text">How do I create an effective prompt for content writing?</span>
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
        <h1 class="cta-title">Unleash your ideas.<br><span class="cta-highlight">Work 10x faster.</span></h1>
        <p class="cta-description">Start your free trial today and see why thousands trust our AI to work smarter, faster, and better.</p>
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
import { onMounted, onUnmounted, ref } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'
import gsap from 'gsap'

const router = useRouter()
const authStore = useAuthStore()

// Logout handler
const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

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

const fullText = 'Meet your new AI-Powered prompt engineering Agents'
const typingSpeed = 100 // milliseconds per character
const deletingSpeed = 50 // milliseconds per character
const pauseTime = 5000 // 5 seconds pause

let vantaEffect = null
let vantaCtaEffect = null
let scrollHandler = null
let navbarScrollHandler = null

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

  // Initialize VANTA.TOPOLOGY for CTA section
  if (window.VANTA && window.VANTA.TOPOLOGY) {
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
      // Wait 5 seconds before starting to delete
      setTimeout(() => {
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
  scrollHandler = () => {
    const scrollY = window.scrollY
    const vantaHero = document.getElementById('vanta-hero')
    
    if (vantaHero) {
      // Calculate zoom based on scroll position
      // Start at 1.2x zoom, zoom out to 1.0x as you scroll
      const maxScroll = window.innerHeight * 2 // Adjust this value to control zoom speed
      const scrollProgress = Math.min(scrollY / maxScroll, 1)
      const scale = 1.2 - (scrollProgress * 0.2) // From 1.2 to 1.0
      
      vantaHero.style.transform = `scale(${scale})`
    }
  }

  window.addEventListener('scroll', scrollHandler)
  
  // Navbar scroll handler
  navbarScrollHandler = () => {
    const navbar = document.querySelector('.navbar')
    if (navbar) {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled')
      } else {
        navbar.classList.remove('scrolled')
      }
    }
  }
  
  window.addEventListener('scroll', navbarScrollHandler)
  
  // Start typewriter animation cleanup first to avoid duplicates
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
  if (navbarScrollHandler) {
    window.removeEventListener('scroll', navbarScrollHandler)
    navbarScrollHandler = null
  }
  
  // Clean up typewriter animation
  if (typewriterInterval) {
    clearTimeout(typewriterInterval)
    typewriterInterval = null
  }
})
</script>

