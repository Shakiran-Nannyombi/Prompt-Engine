<template>
  <div class="login-view">
    <!-- Back to Home Button -->
    <div class="back-button-container">
      <router-link 
        to="/" 
        class="back-button"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Home
      </router-link>
    </div>

    <!-- Main Content Container -->
    <div class="main-container">
      <!-- Left Side - Logo -->
      <div class="logo-section">
        <div class="logo-container">
          <img 
            src="/PE_logo.svg" 
            alt="Prompt Engine" 
            class="logo-image"
          />
          <h1 class="logo-title">Prompt Engine</h1>
          <p class="logo-subtitle">Your AI-powered prompt optimization platform</p>
          <div class="feature-list">
            <div class="feature-item">
              <svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>AI-Powered Optimization</span>
            </div>
            <div class="feature-item">
              <svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span>Lightning Fast Results</span>
            </div>
            <div class="feature-item">
              <svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span>Secure & Private</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side - Form -->
      <div class="form-section">
        <div class="form-container">
          <div class="form-header">
            <h2 class="form-title">Welcome Back</h2>
            <p class="form-subtitle">Sign in to continue your journey</p>
          </div>
          <LoginForm
            :isLoading="isLoading"
            :error="error"
            @submit="handleLogin"
            @switch-to-register="switchToRegister"
            @forgot-password="handleForgotPassword"
            @google-login="handleGoogleLogin"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LoginForm from '@/components/auth/LoginForm.vue'

const router = useRouter()

// State
const isLoading = ref(false)
const error = ref('')

// Handle login form submission
const handleLogin = async (formData) => {
  isLoading.value = true
  error.value = ''
  
  try {
    // TODO: Implement actual login API call
    console.log('Login data:', formData)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Redirect to dashboard or home after successful login
    router.push('/')
  } catch (err) {
    error.value = err.message || 'Login failed. Please check your credentials.'
  } finally {
    isLoading.value = false
  }
}

// Handle Google login
const handleGoogleLogin = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    // TODO: Implement Google OAuth integration
    console.log('Google login initiated')
    
    // Simulate Google OAuth flow
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Redirect after successful Google login
    router.push('/')
  } catch (err) {
    error.value = err.message || 'Google login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// Switch to register page
const switchToRegister = () => {
  router.push('/register')
}

// Handle forgot password
const handleForgotPassword = () => {
  // TODO: Implement forgot password flow
  console.log('Forgot password clicked')
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  background: var(--color-background);
  color: var(--color-text);
  position: relative;
}

.back-button-container {
  position: absolute;
  top: 2rem;
  left: 2rem;
  z-index: 10;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: var(--color-card-bg);
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  color: var(--color-text);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.main-container {
  display: flex;
  min-height: 100vh;
}

.logo-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary, #6366f1));
  position: relative;
  overflow: hidden;
}

.logo-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.logo-container {
  text-align: center;
  max-width: 32rem;
  position: relative;
  z-index: 2;
}

.logo-image {
  width: 140px;
  height: 140px;
  margin: 0 auto 2rem;
  display: block;
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.2));
}

.logo-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.logo-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  max-width: 28rem;
  margin: 0 auto 3rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 24rem;
  margin: 0 auto;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.feature-icon {
  width: 24px;
  height: 24px;
  color: white;
  flex-shrink: 0;
}

.feature-item span {
  color: white;
  font-weight: 500;
  font-size: 1rem;
}

.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  background: var(--color-background);
  position: relative;
}

.form-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 49%, rgba(0, 0, 0, 0.02) 50%, transparent 51%);
  background-size: 20px 20px;
}

.form-container {
  width: 100%;
  max-width: 28rem;
  position: relative;
  z-index: 2;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 1rem;
  color: var(--color-text);
  opacity: 0.7;
}

/* Responsive design */
@media (max-width: 1024px) {
  .main-container {
    flex-direction: column;
  }
  
  .logo-section {
    order: -1;
    padding: 2rem 1rem;
  }
  
  .logo-image {
    width: 100px;
    height: 100px;
    margin-bottom: 1.5rem;
  }
  
  .logo-title {
    font-size: 2.5rem;
  }
  
  .logo-subtitle {
    font-size: 1.125rem;
    margin-bottom: 2rem;
  }
  
  .feature-list {
    gap: 1rem;
  }
  
  .feature-item {
    padding: 0.75rem;
  }
  
  .form-section {
    padding: 2rem 1rem;
  }
  
  .form-title {
    font-size: 1.75rem;
  }
}

@media (max-width: 768px) {
  .back-button-container {
    top: 1rem;
    left: 1rem;
  }
  
  .back-button {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
  
  .form-section,
  .logo-section {
    padding: 1.5rem 1rem;
  }
  
  .logo-image {
    width: 80px;
    height: 80px;
  }
  
  .logo-title {
    font-size: 2rem;
  }
  
  .logo-subtitle {
    font-size: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .feature-list {
    gap: 0.75rem;
  }
  
  .feature-item {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
  
  .feature-icon {
    width: 20px;
    height: 20px;
  }
  
  .form-title {
    font-size: 1.5rem;
  }
  
  .form-subtitle {
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .main-container {
    padding-top: 4rem;
  }
  
  .back-button-container {
    top: 1rem;
    left: 1rem;
    right: 1rem;
  }
  
  .back-button {
    justify-content: center;
  }
}
</style>
