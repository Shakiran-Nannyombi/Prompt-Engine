import { ref, onMounted } from 'vue'

export function useTheme() {
    const isDarkMode = ref(false)

    const toggleTheme = () => {
        isDarkMode.value = !isDarkMode.value
        applyTheme()
    }

    const applyTheme = () => {
        if (isDarkMode.value) {
            document.documentElement.classList.add('dark')
            localStorage.setItem('theme', 'dark')
        } else {
            document.documentElement.classList.remove('dark')
            localStorage.setItem('theme', 'light')
        }
    }

    const initTheme = () => {
        const savedTheme = localStorage.getItem('theme')
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            isDarkMode.value = true
            document.documentElement.classList.add('dark')
        } else {
            isDarkMode.value = false
            document.documentElement.classList.remove('dark')
        }
    }

    return {
        isDarkMode,
        toggleTheme,
        initTheme
    }
}
