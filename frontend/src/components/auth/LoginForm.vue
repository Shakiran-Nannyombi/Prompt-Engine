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

const emit = defineEmits(['submit', 'forgot-password', 'switch-to-register'])

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
