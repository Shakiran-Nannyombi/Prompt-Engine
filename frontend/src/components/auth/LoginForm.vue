<template>
  <BaseCard variant="elevated" class="max-w-md mx-auto">
    <template #header>
      <div class="text-center">
        <div class="flex items-center justify-center space-x-2 mb-4">
          <img 
            src="/PE_logo.svg" 
            alt="Prompt Engine" 
            class="w-8 h-8"
          />
          <span class="text-xl font-bold text-text">Prompt Engine</span>
        </div>
        <h2 class="text-2xl font-bold text-text mb-2">Welcome Back</h2>
        <p class="text-text opacity-70">Sign in to your account to continue</p>
      </div>
    </template>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Email Field -->
      <BaseInput
        v-model="form.email"
        type="email"
        label="Email Address"
        placeholder="Enter your email"
        :errorMessage="errors.email"
        :required="true"
        :disabled="isLoading"
      />

      <!-- Password Field -->
      <BaseInput
        v-model="form.password"
        type="password"
        label="Password"
        placeholder="Enter your password"
        :errorMessage="errors.password"
        :required="true"
        :disabled="isLoading"
      />

      <!-- Remember Me & Forgot Password -->
      <div class="flex items-center justify-between">
        <label class="flex items-center">
          <input
            v-model="form.rememberMe"
            type="checkbox"
            class="w-4 h-4 text-primary bg-input-bg border-input-border rounded focus:ring-primary-500 focus:ring-2"
            :disabled="isLoading"
          />
          <span class="ml-2 text-sm text-text">Remember me</span>
        </label>
        
        <button
          type="button"
          @click="$emit('forgot-password')"
          class="text-sm text-primary hover:text-primary-600 transition-colors"
          :disabled="isLoading"
        >
          Forgot password?
        </button>
      </div>

      <!-- Divider -->
      <div class="relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-input-border"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-card-bg text-text opacity-70">Or continue with</span>
        </div>
      </div>

      <!-- Google Login Button -->
      <BaseButton
        type="secondary"
        size="large"
        :isLoading="isLoading"
        :disabled="isLoading"
        fullWidth
        @click="$emit('google-login')"
        class="google-button"
      >
        <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        {{ isLoading ? 'Signing in...' : 'Continue with Google' }}
      </BaseButton>

      <!-- Submit Button -->
      <BaseButton
        type="primary"
        size="large"
        :isLoading="isLoading"
        :disabled="!isFormValid"
        fullWidth
        htmlType="submit"
      >
        {{ isLoading ? 'Signing in...' : 'Sign In' }}
      </BaseButton>

      <!-- Error Display -->
      <div v-if="error" class="p-3 bg-error-50 border border-error-200 rounded-lg">
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-sm text-error">{{ error }}</span>
        </div>
      </div>
    </form>

    <template #footer>
      <div class="text-center">
        <p class="text-text opacity-70">
          Don't have an account? 
          <button
            type="button"
            @click="$emit('switch-to-register')"
            class="text-primary hover:text-primary-600 font-medium transition-colors"
            :disabled="isLoading"
          >
            Sign up
          </button>
        </p>
      </div>
    </template>
  </BaseCard>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { BaseCard, BaseInput, BaseButton } from '@/components/base'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['submit', 'forgot-password', 'switch-to-register', 'google-login'])

// Form data
const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

// Form validation errors
const errors = reactive({
  email: '',
  password: ''
})

// Validation rules
const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email) return 'Email is required'
  if (!emailRegex.test(email)) return 'Please enter a valid email address'
  return ''
}

const validatePassword = (password) => {
  if (!password) return 'Password is required'
  if (password.length < 6) return 'Password must be at least 6 characters'
  return ''
}

// Form validation
const isFormValid = computed(() => {
  return form.email && 
         form.password && 
         !errors.email && 
         !errors.password
})

// Handle form submission
const handleSubmit = () => {
  // Clear previous errors
  errors.email = ''
  errors.password = ''
  
  // Validate form
  errors.email = validateEmail(form.email)
  errors.password = validatePassword(form.password)
  
  // If form is valid, emit submit event
  if (isFormValid.value) {
    emit('submit', {
      email: form.email,
      password: form.password,
      rememberMe: form.rememberMe
    })
  }
}

// Clear form
const clearForm = () => {
  form.email = ''
  form.password = ''
  form.rememberMe = false
  errors.email = ''
  errors.password = ''
}

// Expose methods for parent components
defineExpose({
  clearForm
})
</script>
