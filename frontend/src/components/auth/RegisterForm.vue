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
        <h2 class="text-2xl font-bold text-text mb-2">Create Account</h2>
        <p class="text-text opacity-70">Join Prompt Engine to get started</p>
      </div>
    </template>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Name Field -->
      <BaseInput
        v-model="form.name"
        type="text"
        label="Full Name"
        placeholder="Enter your full name"
        :errorMessage="errors.name"
        :required="true"
        :disabled="isLoading"
      />

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
        placeholder="Create a password"
        :errorMessage="errors.password"
        :required="true"
        :disabled="isLoading"
        :showCharacterCount="true"
        :maxLength="50"
      />

      <!-- Confirm Password Field -->
      <BaseInput
        v-model="form.confirmPassword"
        type="password"
        label="Confirm Password"
        placeholder="Confirm your password"
        :errorMessage="errors.confirmPassword"
        :required="true"
        :disabled="isLoading"
      />

      <!-- Password Strength Indicator -->
      <div v-if="form.password" class="space-y-2">
        <div class="text-sm text-text opacity-70">Password Strength:</div>
        <div class="flex space-x-1">
          <div 
            v-for="i in 4" 
            :key="i"
            class="h-1 flex-1 rounded"
            :class="passwordStrength >= i ? strengthColor : 'bg-secondary'"
          ></div>
        </div>
        <div class="text-xs text-text opacity-50">
          {{ passwordStrengthText }}
        </div>
      </div>

      <!-- Terms and Conditions -->
      <div class="space-y-3">
        <label class="flex items-start space-x-3">
          <input
            v-model="form.acceptTerms"
            type="checkbox"
            class="w-4 h-4 text-primary bg-input-bg border-input-border rounded focus:ring-primary-500 focus:ring-2 mt-0.5"
            :disabled="isLoading"
            required
          />
          <span class="text-sm text-text">
            I agree to the 
            <button
              type="button"
              @click="$emit('view-terms')"
              class="text-primary hover:text-primary-600 transition-colors"
            >
              Terms of Service
            </button>
            and 
            <button
              type="button"
              @click="$emit('view-privacy')"
              class="text-primary hover:text-primary-600 transition-colors"
            >
              Privacy Policy
            </button>
          </span>
        </label>

        <label class="flex items-start space-x-3">
          <input
            v-model="form.acceptNewsletter"
            type="checkbox"
            class="w-4 h-4 text-primary bg-input-bg border-input-border rounded focus:ring-primary-500 focus:ring-2 mt-0.5"
            :disabled="isLoading"
          />
          <span class="text-sm text-text">
            I'd like to receive updates and tips via email
          </span>
        </label>
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
        {{ isLoading ? 'Creating Account...' : 'Create Account' }}
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
          Already have an account? 
          <button
            type="button"
            @click="$emit('switch-to-login')"
            class="text-primary hover:text-primary-600 font-medium transition-colors"
            :disabled="isLoading"
          >
            Sign in
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

const emit = defineEmits(['submit', 'view-terms', 'view-privacy', 'switch-to-login'])

// Form data
const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
  acceptNewsletter: false
})

// Form validation errors
const errors = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Validation rules
const validateName = (name) => {
  if (!name) return 'Name is required'
  if (name.length < 2) return 'Name must be at least 2 characters'
  return ''
}

const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email) return 'Email is required'
  if (!emailRegex.test(email)) return 'Please enter a valid email address'
  return ''
}

const validatePassword = (password) => {
  if (!password) return 'Password is required'
  if (password.length < 8) return 'Password must be at least 8 characters'
  if (!/(?=.*[a-z])/.test(password)) return 'Password must contain at least one lowercase letter'
  if (!/(?=.*[A-Z])/.test(password)) return 'Password must contain at least one uppercase letter'
  if (!/(?=.*\d)/.test(password)) return 'Password must contain at least one number'
  return ''
}

const validateConfirmPassword = (confirmPassword) => {
  if (!confirmPassword) return 'Please confirm your password'
  if (confirmPassword !== form.password) return 'Passwords do not match'
  return ''
}

// Password strength calculation
const passwordStrength = computed(() => {
  if (!form.password) return 0
  
  let strength = 0
  if (form.password.length >= 8) strength++
  if (/(?=.*[a-z])/.test(form.password)) strength++
  if (/(?=.*[A-Z])/.test(form.password)) strength++
  if (/(?=.*\d)/.test(form.password)) strength++
  if (/(?=.*[!@#$%^&*])/.test(form.password)) strength++
  
  return Math.min(strength, 4)
})

const strengthColor = computed(() => {
  switch (passwordStrength.value) {
    case 1: return 'bg-error'
    case 2: return 'bg-warning'
    case 3: return 'bg-primary'
    case 4: return 'bg-success'
    default: return 'bg-secondary'
  }
})

const passwordStrengthText = computed(() => {
  switch (passwordStrength.value) {
    case 0: return 'Enter a password'
    case 1: return 'Very weak'
    case 2: return 'Weak'
    case 3: return 'Good'
    case 4: return 'Strong'
    default: return ''
  }
})

// Form validation
const isFormValid = computed(() => {
  return form.name && 
         form.email && 
         form.password && 
         form.confirmPassword &&
         form.acceptTerms &&
         !errors.name && 
         !errors.email && 
         !errors.password && 
         !errors.confirmPassword
})

// Handle form submission
const handleSubmit = () => {
  // Clear previous errors
  errors.name = ''
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = ''
  
  // Validate form
  errors.name = validateName(form.name)
  errors.email = validateEmail(form.email)
  errors.password = validatePassword(form.password)
  errors.confirmPassword = validateConfirmPassword(form.confirmPassword)
  
  // If form is valid, emit submit event
  if (isFormValid.value) {
    emit('submit', {
      name: form.name,
      email: form.email,
      password: form.password,
      acceptNewsletter: form.acceptNewsletter
    })
  }
}

// Clear form
const clearForm = () => {
  form.name = ''
  form.email = ''
  form.password = ''
  form.confirmPassword = ''
  form.acceptTerms = false
  form.acceptNewsletter = false
  errors.name = ''
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = ''
}

// Expose methods for parent components
defineExpose({
  clearForm
})
</script>
