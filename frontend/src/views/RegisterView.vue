<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import AuthLayout from '@/components/auth/AuthLayout.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(false)
const error = ref('')

const handleRegister = async ({ name, email, password }) => {
  isLoading.value = true
  error.value = ''
  try {
    const result = await authStore.register({ name, email, password })
    if (result.success) router.push('/refiner')
  } catch (err) {
    error.value = err.message || 'Couldn’t create the account. Check your details and try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <AuthLayout title="Create an account" subtitle="Free, and takes a few seconds." image="/register_bg_branded.png">
    <RegisterForm :is-loading="isLoading" :error="error" @submit="handleRegister" />
  </AuthLayout>
</template>
