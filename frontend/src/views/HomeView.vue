<template>
  <div class="bg-transparent">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-content">
        <!-- Logo and Brand -->
        <div class="navbar-brand">
          <img src="/PE_logo.svg" alt="Prompt-Engine Logo" class="logo-icon" />
          <span class="brand-name">Prompt-Engine</span>
        </div>
        
        <!-- Navigation Links -->
        <div class="navbar-links">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
          <RouterLink to="/coach" class="nav-link">Coach</RouterLink>
          <RouterLink to="/refiner" class="nav-link">Refiner</RouterLink>
          <RouterLink to="/about " class="nav-link">Documentation</RouterLink>
        </div>
        
        <!-- Theme Toggle and CTA Button -->
        <div class="navbar-actions">
          <button @click="toggleTheme" class="theme-toggle" :class="{ 'dark': isDarkMode }">
            <svg v-if="!isDarkMode" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.25a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM7.5 12a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM18.894 6.166a.75.75 0 00-1.06-1.06l-1.591 1.59a.75.75 0 101.06 1.061l1.591-1.59zM21.75 12a.75.75 0 01-.75.75h-2.25a.75.75 0 010-1.5H21a.75.75 0 01.75.75zM17.834 18.894a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 10-1.061 1.06l1.59 1.591zM12 18a.75.75 0 01.75.75V21a.75.75 0 01-1.5 0v-2.25A.75.75 0 0112 18zM7.758 17.303a.75.75 0 00-1.061-1.06l-1.591 1.59a.75.75 0 001.06 1.061l1.591-1.59zM6 12a.75.75 0 01-.75.75H3a.75.75 0 010-1.5h2.25A.75.75 0 016 12zM6.697 7.757a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 00-1.061 1.06l1.59 1.591z"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path fill-rule="evenodd" d="M9.528 1.718a.75.75 0 01.162.819A8.97 8.97 0 009 6a9 9 0 009 9 8.97 8.97 0 003.463-.69.75.75 0 01.981.98 10.503 10.503 0 01-9.694 6.46c-5.799 0-10.5-4.701-10.5-10.5 0-4.368 2.667-8.112 6.46-9.694a.75.75 0 01.818.162z" clip-rule="evenodd"/>
            </svg>
          </button>
          <RouterLink to="/tutorials" class="navbar-cta">
            Tutorials
          </RouterLink>
        </div>
      </div>
    </nav>

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
      <div class="cta-content" id="vanta-cta">
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
    </div>

    <!-- Spacer between sections and footer -->
    <div class="hero-section-spacer"></div>

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
import { RouterLink } from 'vue-router'
import '@/assets/styles/HomeView.css'
import { onMounted, onUnmounted, ref } from 'vue'

// Theme toggle
const isDarkMode = ref(false)

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

  // Load VANTA scripts dynamically
  const loadScript = (src) => {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = src
      script.onload = resolve
      script.onerror = reject
      document.head.appendChild(script)
    })
  }

  // Load scripts and initialize VANTA
  Promise.all([
    loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js'),
    loadScript('https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.halo.min.js'),
    loadScript('https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js'),
    loadScript('https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.topology.min.js')
  ]).then(() => {
    // Initialize VANTA effects
    initializeVantaEffects()
  }).catch(error => {
    console.error('Failed to load VANTA scripts:', error)
  })

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
  
  // Start typewriter animation
  setTimeout(() => {
    typeWriter()
  }, 1000) // Start after 1 second delay
})

onUnmounted(() => {
  // Clean up VANTA effects
  if (vantaEffect) {
    vantaEffect.destroy()
  }
  if (vantaCtaEffect) {
    vantaCtaEffect.destroy()
  }
  
  // Clean up scroll handlers
  if (scrollHandler) {
    window.removeEventListener('scroll', scrollHandler)
  }
  if (navbarScrollHandler) {
    window.removeEventListener('scroll', navbarScrollHandler)
  }
  
  // Clean up typewriter animation
  if (typewriterInterval) {
    clearTimeout(typewriterInterval)
  }
})
</script>

