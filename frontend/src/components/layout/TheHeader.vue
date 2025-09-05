<template>
  <header class="bg-card-bg border-b border-card-border sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
    <div class="container-wide">
      <div class="flex items-center justify-between h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center space-x-4">
          <router-link 
            to="/" 
            class="flex items-center space-x-2 hover:opacity-80 transition-opacity"
          >
            <img 
              src="/PE_logo.svg" 
              alt="Prompt Engine" 
              class="w-8 h-8"
            />
            <span class="text-xl font-bold text-text">Prompt Engine</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <router-link 
            v-for="item in navigationItems" 
            :key="item.name"
            :to="item.path"
            class="nav-link"
            :class="{ 'nav-link-active': $route.path === item.path }"
          >
            {{ item.name }}
          </router-link>
        </nav>

        <!-- Right Side Actions -->
        <div class="flex items-center space-x-4">
          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="p-2 rounded-lg text-text hover:bg-secondary transition-colors"
            :title="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'"
          >
            <svg v-if="isDarkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <!-- Authentication Section -->
          <div v-if="!isAuthenticated" class="flex items-center space-x-2">
            <BaseButton 
              type="outline" 
              size="small"
              @click="$router.push('/login')"
            >
              Login
            </BaseButton>
            <BaseButton 
              type="primary" 
              size="small"
              @click="$router.push('/register')"
            >
              Register
            </BaseButton>
          </div>

          <!-- User Profile Dropdown -->
          <div v-else class="relative">
            <button
              @click="toggleUserMenu"
              class="flex items-center space-x-2 p-2 rounded-lg hover:bg-secondary transition-colors"
            >
              <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <span class="text-white text-sm font-medium">
                  {{ userInitials }}
                </span>
              </div>
              <span class="hidden md:block text-text font-medium">{{ user?.name || 'User' }}</span>
              <svg class="w-4 h-4 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- User Dropdown Menu -->
            <Transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-card-bg border border-card-border rounded-lg shadow-lg py-1 z-50"
              >
                <router-link
                  to="/profile"
                  class="block px-4 py-2 text-sm text-text hover:bg-secondary transition-colors"
                  @click="closeUserMenu"
                >
                  Profile
                </router-link>
                <router-link
                  to="/settings"
                  class="block px-4 py-2 text-sm text-text hover:bg-secondary transition-colors"
                  @click="closeUserMenu"
                >
                  Settings
                </router-link>
                <hr class="my-1 border-card-border">
                <button
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-error hover:bg-secondary transition-colors"
                >
                  Logout
                </button>
              </div>
            </Transition>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 rounded-lg text-text hover:bg-secondary transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Navigation Menu -->
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 transform -translate-y-2"
        enter-to-class="opacity-100 transform translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 transform translate-y-0"
        leave-to-class="opacity-0 transform -translate-y-2"
      >
        <div v-if="showMobileMenu" class="md:hidden border-t border-card-border py-4">
          <nav class="flex flex-col space-y-2">
            <router-link 
              v-for="item in navigationItems" 
              :key="item.name"
              :to="item.path"
              class="nav-link-mobile"
              :class="{ 'nav-link-mobile-active': $route.path === item.path }"
              @click="closeMobileMenu"
            >
              {{ item.name }}
            </router-link>
          </nav>
        </div>
      </Transition>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { BaseButton } from '@/components/base'

// Mock authentication state - replace with actual Pinia store
const isAuthenticated = ref(false)
const user = ref({
  name: 'John Doe',
  email: 'john@example.com'
})

const router = useRouter()
const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const isDarkMode = ref(false)

const navigationItems = [
  { name: 'Home', path: '/' },
  { name: 'Coach', path: '/coach' },
  { name: 'Refiner', path: '/refiner' },
  { name: 'Docs', path: '/docs' },
  { name: 'Tutorials', path: '/tutorials' }
]

const userInitials = computed(() => {
  if (!user.value?.name) return 'U'
  return user.value.name
    .split(' ')
    .map(name => name[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.classList.toggle('dark', isDarkMode.value)
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const handleLogout = () => {
  // Handle logout logic here
  isAuthenticated.value = false
  user.value = null
  closeUserMenu()
  router.push('/')
}

// Close menus when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showUserMenu.value = false
  }
}

// Initialize theme from localStorage
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDarkMode.value = savedTheme === 'dark'
    document.documentElement.classList.toggle('dark', isDarkMode.value)
  } else {
    // Default to system preference
    isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    document.documentElement.classList.toggle('dark', isDarkMode.value)
  }
  
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.nav-link {
  @apply text-text hover:text-primary transition-colors font-medium relative;
}

.nav-link-active {
  @apply text-primary;
}

.nav-link-active::after {
  content: '';
  position: absolute;
  bottom: -1.5rem;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--color-primary);
  border-radius: 1px;
}

.nav-link-mobile {
  @apply block px-4 py-2 text-text hover:text-primary hover:bg-secondary transition-colors rounded-lg font-medium;
}

.nav-link-mobile-active {
  @apply text-primary bg-secondary;
}
</style>
