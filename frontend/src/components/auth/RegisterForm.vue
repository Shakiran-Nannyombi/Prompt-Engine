<template>
  <BaseCard variant="elevated" class="max-w-md mx-auto">
    <template #header>
      <div class="text-center">
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

      <!-- Spacing after password fields -->
      <div class="py-2"></div>

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

      <!-- Spacing -->
      <div class="py-4"></div>

      <!-- Divider -->
      <div class="flex items-center justify-center py-2">
        <span class="text-sm text-text opacity-70">Or continue with</span>
      </div>

      <!-- Google Login Button -->
      <BaseButton
        type="secondary"
        size="large"
        :isLoading="isLoading"
        :disabled="isLoading"
        fullWidth
        @click="$emit('google-login')"
        class="google-button no-outline"
      >
        <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        {{ isLoading ? 'Signing up...' : 'Continue with Google' }}
      </BaseButton>

      <!-- Submit Button -->
      <BaseButton
        type="primary"
        size="large"
        :isLoading="isLoading"
        :disabled="!isFormValid"
        fullWidth
        htmlType="submit"
        class="create-account-btn"
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
import { ref, computed, reactive, watch } from 'vue'
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

const emit = defineEmits(['submit', 'view-terms', 'view-privacy', 'switch-to-login', 'google-login'])

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
  // Check if all fields are filled
  const allFieldsFilled = form.name.trim() && 
                         form.email.trim() && 
                         form.password && 
                         form.confirmPassword &&
                         form.acceptTerms
  
  // Check if password meets strength requirements (at least 3/4 strength)
  const passwordStrongEnough = passwordStrength.value >= 3
  
  // Check if passwords match
  const passwordsMatch = form.password === form.confirmPassword
  
  // Check if no validation errors
  const noErrors = !errors.name && 
                   !errors.email && 
                   !errors.password && 
                   !errors.confirmPassword
  
  return allFieldsFilled && passwordStrongEnough && passwordsMatch && noErrors
})

// Real-time validation
const validateField = (fieldName, value) => {
  switch (fieldName) {
    case 'name':
      errors.name = validateName(value)
      break
    case 'email':
      errors.email = validateEmail(value)
      break
    case 'password':
      errors.password = validatePassword(value)
      // Also re-validate confirm password if it exists
      if (form.confirmPassword) {
        errors.confirmPassword = validateConfirmPassword(form.confirmPassword)
      }
      break
    case 'confirmPassword':
      errors.confirmPassword = validateConfirmPassword(value)
      break
  }
}

// Handle form submission
const handleSubmit = () => {
  // Validate all fields
  validateField('name', form.name)
  validateField('email', form.email)
  validateField('password', form.password)
  validateField('confirmPassword', form.confirmPassword)
  
  // If form is valid, emit submit event
  if (isFormValid.value) {
    emit('submit', {
      name: form.name.trim(),
      email: form.email.trim(),
      password: form.password,
      acceptNewsletter: form.acceptNewsletter
    })
  } else {
    // Show error message if form is not valid
    console.log('Form validation failed. Please check all fields.')
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

// Watch for changes and validate in real-time
watch(() => form.name, (newValue) => {
  if (newValue) validateField('name', newValue)
})

watch(() => form.email, (newValue) => {
  if (newValue) validateField('email', newValue)
})

watch(() => form.password, (newValue) => {
  if (newValue) validateField('password', newValue)
})

watch(() => form.confirmPassword, (newValue) => {
  if (newValue) validateField('confirmPassword', newValue)
})

// Expose methods for parent components
defineExpose({
  clearForm
})
</script>

<style scoped>
.no-outline {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.no-outline:focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.no-outline:hover {
  border: none !important;
  outline: none !important;
}

.create-account-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  color: white !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
}

.create-account-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

.create-account-btn:active:not(:disabled) {
  transform: translateY(0) !important;
  box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4) !important;
}

.create-account-btn:disabled {
  background: #9ca3af !important;
  box-shadow: none !important;
  transform: none !important;
}
</style>
