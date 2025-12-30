<template>
  <div class="about-view" :class="{ 'dark': isDarkMode }">
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
          <RouterLink to="/about" class="nav-link active">About</RouterLink>
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
            <RouterLink to="/tutorials" class="navbar-cta">
              Tutorials
            </RouterLink>
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
          <RouterLink to="/about" class="mobile-nav-link active" @click="showMobileMenu = false">About Us</RouterLink>
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

    <!-- Main Content -->
    <main class="about-main ">
      <!-- Section 1: The Mission -->
      <section class="mission-section py-24 px-6 md:px-12">
        <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div class="mission-text">
            <h2 class="section-tag">THE MISSION</h2>
            <h3 class="section-title">Mastering the Art of Guidance</h3>
            <p class="section-desc">We bridge the gap between human intent and machine execution. In an era where AI capability is boundless, the bottleneck is no longer technology—it's communication. Prompt-Engine exists to help you command AI with precision, clarity, and creative flair.</p>
            <div class="mission-points mt-12 space-y-8">
              <div class="point flex items-start gap-4">
                <div class="point-icon bg-primary/10 p-3 rounded-2xl">
                  <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <h4 class="text-lg font-bold">Iterative Excellence</h4>
                  <p class="text-sm opacity-70">Transform rough ideas into production-ready prompts through a scientific, multi-stage refinement process.</p>
                </div>
              </div>
              <div class="point flex items-start gap-4">
                <div class="point-icon bg-blue-500/10 p-3 rounded-2xl">
                  <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <div>
                  <h4 class="text-lg font-bold">Institutional Logic</h4>
                  <p class="text-sm opacity-70">Built on proven engineering principles, ensuring your prompts are structured for maximum LLM performance.</p>
                </div>
              </div>
            </div>
          </div>
          <div class="mission-visual relative">
             <div class="glass-box p-8 rounded-3xl backdrop-blur-xl border border-white/10 shadow-2xl overflow-hidden relative group">
                <div class="absolute -top-24 -right-24 w-48 h-48 bg-blue-500/30 blur-[100px] group-hover:bg-blue-500/50 transition-all duration-500"></div>
                <div class="absolute -bottom-24 -left-24 w-48 h-48 bg-purple-500/30 blur-[100px] group-hover:bg-purple-500/50 transition-all duration-500"></div>
                <div class="relative z-10">
                  <div class="flex items-center gap-3 mb-6">
                    <div class="w-3 h-3 rounded-full bg-red-400"></div>
                    <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
                    <div class="w-3 h-3 rounded-full bg-green-400"></div>
                  </div>
                  <div class="space-y-4">
                    <div class="h-2 w-3/4 bg-white/20 rounded"></div>
                    <div class="h-2 w-full bg-white/20 rounded"></div>
                    <div class="h-2 w-5/6 bg-white/20 rounded"></div>
                    <div class="h-32 w-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-xl border border-white/5 flex items-center justify-center">
                       <span class="text-xs opacity-50 font-mono">REFINING PROMPT...</span>
                    </div>
                  </div>
                </div>
             </div>
          </div>
        </div>
      </section>

      <!-- Section 2: Core Philosophy -->
      <section class="philosophy-section py-24 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-b from-transparent via-primary/5 to-transparent"></div>
        <div class="max-w-6xl mx-auto px-6 relative z-10 flex flex-col items-center text-center">
          <h2 class="section-tag inline-block px-6 py-2 rounded-full border border-primary/20 mb-8">WHY IT WORKS</h2>
          <h3 class="text-4xl md:text-5xl font-black mb-32 tracking-tight">The Three Pillars of Precision</h3>
        
          <div class="grid md:grid-cols-3 gap-12 justify-center pt-12">
            <div class="philosophy-card p-10 group">
              <div class="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mb-10 group-hover:bg-primary/20 transition-all duration-300">
                <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h4 class="text-2xl font-bold mb-4">Structural Analysis</h4>
              <p class="opacity-60 text-base leading-relaxed">We decompose your prompts into atomic elements—instruction, context, and output constraints—to ensure the model never misses the point.</p>
            </div>

            <div class="philosophy-card p-10 group lg:translate-y-12">
              <div class="w-16 h-16 bg-blue-500/10 rounded-2xl flex items-center justify-center mb-10 group-hover:bg-blue-500/20 transition-all duration-300">
                <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0010 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h4 class="text-2xl font-bold mb-4">Contextual Weighting</h4>
              <p class="opacity-60 text-base leading-relaxed">Optimization isn't just about adding words; it's about strategic emphasis. We help you highlight what matters most to the LLM.</p>
            </div>

            <div class="philosophy-card p-10 group">
              <div class="w-16 h-16 bg-fuchsia-500/10 rounded-2xl flex items-center justify-center mb-10 group-hover:bg-fuchsia-500/20 transition-all duration-300">
                <svg class="w-8 h-8 text-fuchsia-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.82.551l-1.293 1.293A2 2 0 003 18.465V19a2 2 0 002 2h14a2 2 0 002-2v-.535a2 2 0 00-.572-1.414l-1.293-1.293zm0-8a2 2 0 01.572 1.414V8a2 2 0 01-2 2H5a2 2 0 01-2-2V7.414a2 2 0 01.572-1.414l1.293-1.293A2 2 0 016.278 4.136l1.293-1.293A2 2 0 018.985 2h6.03a2 2 0 011.414.586l1.293 1.293a2 2 0 01.572 1.414z" />
                </svg>
              </div>
              <h4 class="text-2xl font-bold mb-4">Dynamic Adaptability</h4>
              <p class="opacity-60 text-base leading-relaxed">From GPT-4 to Claude 3, prompting nuances change. Our engine adapts its logic to the specific architecture of the model you're targeting.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 3: The Call to Action -->
      <section class="about-cta py-32 px-6">
        <div class="max-w-4xl mx-auto rounded-[3rem] bg-gradient-to-br from-blue-600 to-purple-700 p-1 bg-white/5 relative group overflow-hidden">
          <div class="absolute inset-0 bg-white/5 group-hover:opacity-20 transition-opacity"></div>
          <div class="relative z-10 p-12 md:p-20 flex flex-col items-center text-center bg-[#0a0a0c] rounded-[2.9rem]">
             <h2 class="text-3xl md:text-5xl font-black mb-8 leading-tight">Ready to transform your<br><span class="cta-highlight">AI workflow?</span></h2>
             <p class="text-lg opacity-70 mb-24 max-w-2xl">Join thousands of prompt engineers, developers, and creators who use Prompt-Engine to stay ahead of the curve.</p>
             <div class="flex flex-col sm:flex-row gap-6 justify-center">
                <RouterLink to="/register" class="px-10 py-4 cta-primary-button font-bold rounded-2xl">Get Started Free</RouterLink>
                <RouterLink to="/coach" class="px-10 py-4 cta-secondary-button font-bold rounded-2xl">Talk to Coach</RouterLink>
             </div>
          </div>
        </div>
      </section>
    </main>

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
            <li><RouterLink to="/about" class="footer-link">About</RouterLink></li>
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
                <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.746-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001.012.001z"/>
              </svg>
              Instagram
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
import '@/assets/styles/AboutView.css'
import gsap from 'gsap'

// State
const isDarkMode = ref(false)
const showMobileMenu = ref(false)
const isScrolled = ref(false)

// Vanta effects
let vantaEffect = null

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
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
  initVanta() // Update Vanta effect on theme change
}

// Vanta Initialization
const initVanta = () => {
  if (vantaEffect) vantaEffect.destroy()
  
  const isDark = document.documentElement.classList.contains('dark')
  
  try {
    vantaEffect = window.VANTA.WAVES({
      el: "#vanta-about",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: isDark ? 0x0f172a : 0x3b82f6,
      shininess: isDark ? 60.00 : 50.00,
      waveHeight: 20.00,
      waveSpeed: 0.80,
      zoom: 0.85
    })
  } catch (err) {
    console.error('Vanta failed to load:', err)
  }
}

// Navbar Scroll Logic
const navbarScrollHandler = () => {
  const navbar = document.querySelector('.navbar')
  if (navbar) {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled')
    } else {
      navbar.classList.remove('scrolled')
    }
  }
}

onMounted(() => {
  // Check theme
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  }

  window.addEventListener('scroll', navbarScrollHandler)
  navbarScrollHandler() // Initial check
  
  // Load Vanta scripts if not already present
  if (window.THREE && window.VANTA) {
    initVanta()
  } else {
    setTimeout(initVanta, 500)
  }

  // Initial animations
  gsap.from('.about-title', {
    y: 30,
    opacity: 0,
    duration: 1,
    delay: 0.2,
    ease: 'power3.out'
  })
  
  gsap.from('.about-subtitle', {
    y: 20,
    opacity: 0,
    duration: 1,
    delay: 0.4,
    ease: 'power3.out'
  })
})

onUnmounted(() => {
  window.removeEventListener('scroll', navbarScrollHandler)
  if (vantaEffect) vantaEffect.destroy()
})
</script>
