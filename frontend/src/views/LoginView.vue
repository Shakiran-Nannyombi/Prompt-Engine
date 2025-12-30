<template>
  <div class="login-view">
    <!-- Branding Pane - Image with embedded text -->
    <div class="auth-branding-pane">
      <div 
        class="auth-bg-image" 
        :style="{ backgroundImage: 'url(/login_bg_branded.png)' }"
      ></div>
    </div>

    <!-- Form Pane -->
    <div class="auth-form-pane">
      <div class="auth-container">
        <LoginForm

          :isLoading="isLoading"
          :error="error"
          @submit="handleLogin"
          @switch-to-register="switchToRegister"
          @forgot-password="handleForgotPassword"
        />
        
        <!-- Back to Home at bottom -->
        <router-link to="/" class="auth-back-button-bottom">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import LoginForm from '@/components/auth/LoginForm.vue'
import '@/assets/styles/LoginView.css'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// State
const isLoading = ref(false)
const error = ref('')

const handleLogin = async (formData) => {
  isLoading.value = true
  error.value = ''
  
  try {
    const result = await authStore.login({
      email: formData.email,
      password: formData.password
    })
    
    if (result.success) {
      // Redirect to intended page or home
      const redirectTo = route.query.redirect || '/'
      router.push(redirectTo)
    }
  } catch (err) {
    error.value = err.message || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const switchToRegister = () => {
  router.push('/register')
}

const handleForgotPassword = () => {
  console.log('Forgot password clicked - Demo mode')
  alert('Demo Mode: Password reset not available in demo')
}
</script>

<style>
/* Reset specific global overrides for Auth views */
.auth-form-pane .google-button {
  display: none !important;
}

.auth-form-pane button[type="submit"] {
    background: linear-gradient(135deg, #f60968, #8b5cf6, #3b82f6) !important;
    color: white !important;
    border: none !important;
    transition: all 0.3s ease !important;
    border-radius: 1rem !important;
    font-weight: 700 !important;
    padding: 1.2rem 3rem !important;
    width: auto !important;
    min-width: 250px;
    margin-top: 2rem;
}

.auth-form-pane button[type="submit"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px -5px rgba(246, 9, 104, 0.5) !important;
}

/* Ensure the card styling within the pane is clean */
.auth-form-pane .max-w-md,
.auth-form-pane .w-full {
    max-width: 100% !important;
}
</style>
