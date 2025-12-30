<template>
  <div class="login-view">
    <!-- Branding Pane - Image with embedded text -->
    <div class="auth-branding-pane">
      <div 
        class="auth-bg-image" 
        :style="{ backgroundImage: 'url(/register_bg_branded.png)' }"
      ></div>
    </div>

    <!-- Form Pane -->
    <div class="auth-form-pane">
      <div class="auth-container">
        <RegisterForm


          :isLoading="isLoading"
          :error="error"
          @submit="handleRegister"
          @switch-to-login="switchToLogin"
          @view-terms="viewTerms"
          @view-privacy="viewPrivacy"
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import RegisterForm from '@/components/auth/RegisterForm.vue'
import '@/assets/styles/LoginView.css'

const router = useRouter()
const authStore = useAuthStore()

// State
const isLoading = ref(false)
const error = ref('')

const handleRegister = async (formData) => {
  isLoading.value = true
  error.value = ''
  
  try {
    const result = await authStore.register({
      name: formData.name,
      email: formData.email,
      password: formData.password
    })
    
    if (result.success) {
      // Auto-login after registration and redirect to home
      router.push('/')
    }
  } catch (err) {
    error.value = err.message || 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const switchToLogin = () => {
  router.push('/login')
}

const viewTerms = () => {
  console.log('View terms - Demo mode')
  alert('Demo Mode: Terms of Service')
}

const viewPrivacy = () => {
  console.log('View privacy policy - Demo mode')
  alert('Demo Mode: Privacy Policy')
}
</script>

<style>
/* Synchronized styles with LoginView */
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

.auth-form-pane .max-w-md,
.auth-form-pane .w-full {
    max-width: 100% !important;
}

@media (min-width: 768px) {
    .auth-form-pane form > .base-input-wrapper {
        grid-column: span 1 !important;
    }
}
</style>
