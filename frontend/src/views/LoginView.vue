<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import AuthLayout from '@/components/auth/AuthLayout.vue'
import LoginForm from '@/components/auth/LoginForm.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isLoading = ref(false)
const error = ref('')

const handleLogin = async ({ email, password }) => {
  isLoading.value = true
  error.value = ''
  try {
    const result = await authStore.login({ email, password })
    if (result.success) router.push(route.query.redirect || '/refiner')
  } catch (err) {
    error.value = err.message || 'Sign-in failed. Check your details and try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <AuthLayout title="Sign in" subtitle="Pick up where you left off.">
    <LoginForm :is-loading="isLoading" :error="error" @submit="handleLogin" />
  </AuthLayout>
</template>
