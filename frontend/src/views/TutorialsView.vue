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
          <div class="tip-icon">💡</div>
          <h3 class="tip-title">Be Specific</h3>
          <p class="tip-description">The more specific your input, the better the AI can help you craft the perfect prompt</p>
        </div>

        <div class="tip-card">
          <div class="tip-icon">🎯</div>
          <h3 class="tip-title">Define Your Goal</h3>
          <p class="tip-description">Clearly state what you want to achieve with your prompt for targeted results</p>
        </div>

        <div class="tip-card">
          <div class="tip-icon">🔄</div>
          <h3 class="tip-title">Iterate & Refine</h3>
          <p class="tip-description">Don't settle for the first version - use Refiner to continuously improve</p>
        </div>

        <div class="tip-card">
          <div class="tip-icon">📝</div>
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

    <!-- Footer -->
    <footer class="footer">
      <p>© 2025 Prompt-Engine. All rights reserved.</p>
    </footer>
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
  font-size: 3rem;
  margin-bottom: 1rem;
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

/* Footer */
.footer {
  padding: 2rem;
  text-align: center;
  opacity: 0.6;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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
