<script setup>
import { reactive } from 'vue'

defineProps({
  isLoading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const emit = defineEmits(['submit'])

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })

const validate = () => {
  errors.email = !form.email.trim()
    ? 'Enter your email address.'
    : /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())
      ? ''
      : 'Enter an email address like name@example.com.'
  errors.password = !form.password
    ? 'Enter your password.'
    : form.password.length < 6
      ? 'Use at least 6 characters.'
      : ''
  return !errors.email && !errors.password
}

const handleSubmit = () => {
  if (validate()) emit('submit', { email: form.email.trim(), password: form.password })
}
</script>

<template>
  <form class="auth-form" novalidate @submit.prevent="handleSubmit">
    <p class="demo-note">This is a demo sign-in. Any email and a password of 6 or more characters will work.</p>

    <div class="form-row">
      <label for="login-email" class="label">Email</label>
      <input
        id="login-email"
        v-model="form.email"
        type="email"
        class="field"
        autocomplete="email"
        :aria-invalid="!!errors.email"
        aria-describedby="login-email-error"
      />
      <p v-if="errors.email" id="login-email-error" class="field-error">{{ errors.email }}</p>
    </div>

    <div class="form-row">
      <label for="login-password" class="label">Password</label>
      <input
        id="login-password"
        v-model="form.password"
        type="password"
        class="field"
        autocomplete="current-password"
        :aria-invalid="!!errors.password"
        aria-describedby="login-password-error"
      />
      <p v-if="errors.password" id="login-password-error" class="field-error">{{ errors.password }}</p>
    </div>

    <p v-if="error" class="form-error" role="alert">{{ error }}</p>

    <button type="submit" class="btn btn-primary submit" :disabled="isLoading">
      <span v-if="isLoading" class="loading-dots" aria-hidden="true">
        <span class="loading-dot"></span><span class="loading-dot"></span><span class="loading-dot"></span>
      </span>
      {{ isLoading ? 'Signing in' : 'Sign in' }}
    </button>

    <p class="switch">
      New here?
      <RouterLink to="/register">Create an account</RouterLink>
    </p>
  </form>
</template>

<style scoped src="./auth-form.css"></style>
