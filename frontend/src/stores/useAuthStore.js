import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    // State
    const user = ref(null)
    const isAuthenticated = ref(false)

    // Initialize from localStorage
    const initAuth = () => {
        const storedUser = localStorage.getItem('demo_user')
        if (storedUser) {
            try {
                user.value = JSON.parse(storedUser)
                isAuthenticated.value = true
            } catch (e) {
                console.error('Failed to parse stored user:', e)
                localStorage.removeItem('demo_user')
            }
        }
    }

    // Login (demo - accepts any credentials)
    const login = async (credentials) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                // Create demo user from credentials
                const demoUser = {
                    email: credentials.email,
                    name: credentials.email.split('@')[0],
                    loginTime: new Date().toISOString()
                }

                user.value = demoUser
                isAuthenticated.value = true
                localStorage.setItem('demo_user', JSON.stringify(demoUser))

                resolve({ success: true, user: demoUser })
            }, 800) // Simulate network delay
        })
    }

    // Register (demo - accepts any data)
    const register = async (userData) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                // Create demo user from registration data
                const demoUser = {
                    email: userData.email,
                    name: userData.name || userData.email.split('@')[0],
                    registeredAt: new Date().toISOString()
                }

                user.value = demoUser
                isAuthenticated.value = true
                localStorage.setItem('demo_user', JSON.stringify(demoUser))

                resolve({ success: true, user: demoUser })
            }, 1000) // Simulate network delay
        })
    }

    // Logout
    const logout = () => {
        user.value = null
        isAuthenticated.value = false
        localStorage.removeItem('demo_user')
    }

    // Check if user is authenticated
    const checkAuth = () => {
        return isAuthenticated.value
    }

    // Computed
    const userName = computed(() => user.value?.name || 'User')
    const userEmail = computed(() => user.value?.email || '')

    // Initialize on store creation
    initAuth()

    return {
        // State
        user,
        isAuthenticated,

        // Getters
        userName,
        userEmail,

        // Actions
        login,
        register,
        logout,
        checkAuth,
        initAuth
    }
})
