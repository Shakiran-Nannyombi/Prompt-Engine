<template>
  <BaseCard variant="elevated" class="w-full">
    <template #header>
      <div class="text-center">
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

      <!-- Remember Me -->
      <div class="flex items-center">
        <input
          v-model="form.rememberMe"
          type="checkbox"
          id="rememberMe"
          class="w-4 h-4 text-primary bg-input-bg border-input-border rounded focus:ring-primary-500 focus:ring-2"
        />
        <label for="rememberMe" class="ml-2 text-sm text-text whitespace-nowrap">
          Remember me
        </label>
      </div>

      <!-- Forgot Password - Own Line -->
      <div class="text-right col-span-2">
        <button
          type="button"
          @click="$emit('forgot-password')"
          class="auth-link-button"
        >
          Forgot Password?
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

      <!-- Switch to Register -->
      <div class="text-center text-sm text-text opacity-70 mt-6">
        Don't have an account?
        <button
          type="button"
          @click="$emit('switch-to-register')"
          class="auth-link-button ml-1"
          :disabled="isLoading"
        >
          Sign up
        </button>
      </div>

    <template #footer>
      <!-- Footer content can go here if needed, but the sign-up link has been moved -->
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
  // Check if all fields are filled
  const allFieldsFilled = form.email.trim() && form.password
  
  // Check if no validation errors
  const noErrors = !errors.email && !errors.password
  
  return allFieldsFilled && noErrors
})

// Real-time validation
const validateField = (fieldName, value) => {
  switch (fieldName) {
    case 'email':
      errors.email = validateEmail(value)
      break
    case 'password':
      errors.password = validatePassword(value)
      break
  }
}

// Handle form submission
const handleSubmit = () => {
  // Validate all fields
  validateField('email', form.email)
  validateField('password', form.password)
  
  // If form is valid, emit submit event
  if (isFormValid.value) {
    emit('submit', {
      email: form.email.trim(),
      password: form.password,
      rememberMe: form.rememberMe
    })
  } else {
    // Show error message if form is not valid
    console.log('Form validation failed. Please check all fields.')
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

// Watch for changes and validate in real-time
watch(() => form.email, (newValue) => {
  if (newValue) validateField('email', newValue)
})

watch(() => form.password, (newValue) => {
  if (newValue) validateField('password', newValue)
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
</style>
