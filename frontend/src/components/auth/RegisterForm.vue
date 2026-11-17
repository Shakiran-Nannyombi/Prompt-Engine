<script setup>
import { reactive } from 'vue'

defineProps({
  isLoading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const emit = defineEmits(['submit'])

const form = reactive({ name: '', email: '', password: '' })
const errors = reactive({ name: '', email: '', password: '' })

const validate = () => {
  errors.name = form.name.trim().length < 2 ? 'Enter your name.' : ''
  errors.email = !form.email.trim()
    ? 'Enter your email address.'
    : /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())
      ? ''
      : 'Enter an email address like name@example.com.'
  errors.password = form.password.length < 8 ? 'Use at least 8 characters.' : ''
  return !errors.name && !errors.email && !errors.password
}

const handleSubmit = () => {
  if (validate()) {
    emit('submit', { name: form.name.trim(), email: form.email.trim(), password: form.password })
  }
}
</script>

<template>
  <form class="auth-form" novalidate @submit.prevent="handleSubmit">
    <p class="demo-note">This is a demo account. Nothing is sent to a server; it’s kept in this browser.</p>

    <div class="form-row">
      <label for="reg-name" class="label">Name</label>
      <input
        id="reg-name"
        v-model="form.name"
        type="text"
        class="field"
        autocomplete="name"
        :aria-invalid="!!errors.name"
        aria-describedby="reg-name-error"
      />
      <p v-if="errors.name" id="reg-name-error" class="field-error">{{ errors.name }}</p>
    </div>

    <div class="form-row">
      <label for="reg-email" class="label">Email</label>
      <input
        id="reg-email"
        v-model="form.email"
        type="email"
        class="field"
        autocomplete="email"
        :aria-invalid="!!errors.email"
        aria-describedby="reg-email-error"
      />
      <p v-if="errors.email" id="reg-email-error" class="field-error">{{ errors.email }}</p>
    </div>

    <div class="form-row">
      <label for="reg-password" class="label">Password</label>
      <input
        id="reg-password"
        v-model="form.password"
        type="password"
        class="field"
        autocomplete="new-password"
        :aria-invalid="!!errors.password"
        aria-describedby="reg-password-hint"
      />
      <p id="reg-password-hint" :class="errors.password ? 'field-error' : 'field-hint'">
        {{ errors.password || 'At least 8 characters.' }}
      </p>
    </div>

    <p v-if="error" class="form-error" role="alert">{{ error }}</p>

    <button type="submit" class="btn btn-primary submit" :disabled="isLoading">
      <span v-if="isLoading" class="loading-dots" aria-hidden="true">
        <span class="loading-dot"></span><span class="loading-dot"></span><span class="loading-dot"></span>
      </span>
      {{ isLoading ? 'Creating account' : 'Create account' }}
    </button>

    <p class="switch">
      Already have an account?
      <RouterLink to="/login">Sign in</RouterLink>
    </p>
  </form>
</template>

<style scoped src="./auth-form.css"></style>
