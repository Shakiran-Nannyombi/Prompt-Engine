import { ref, onMounted, watch } from 'vue'
import gsap from 'gsap'
import { useTheme } from '@/composables/useTheme'

export function useCoachChat(props, emit) {
    const { isDarkMode, toggleTheme, initTheme } = useTheme()
    const sidebarCollapsed = ref(window.innerWidth < 1024)
    const sidebarRef = ref(null)

    const toggleSidebar = () => {
        const isOpening = sidebarCollapsed.value
        sidebarCollapsed.value = !sidebarCollapsed.value

        if (window.innerWidth < 1024) {
            if (isOpening) {
                gsap.fromTo(sidebarRef.value,
                    { x: '-100%', opacity: 0 },
                    { x: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }
                )
            } else {
                gsap.to(sidebarRef.value, {
                    x: '-100%',
                    opacity: 0,
                    duration: 0.4,
                    ease: 'power3.in'
                })
            }
        }
    }

    const handleSendMessage = (content) => {
        emit('send-message', content)
    }

    const handleStopGeneration = () => {
        emit('stop-generation')
    }

    const clearError = () => {
        emit('clear-error')
    }

    const resetConversation = () => {
        emit('reset-conversation')
    }

    const downloadPrompt = (prompt) => {
        emit('download-prompt', prompt)
    }

    onMounted(() => {
        initTheme()

        // Sidebar accessibility for mobile
        const handleResize = () => {
            if (window.innerWidth >= 1024) {
                sidebarCollapsed.value = false
                if (sidebarRef.value) gsap.set(sidebarRef.value, { x: 0, opacity: 1 })
            } else {
                sidebarCollapsed.value = true
                if (sidebarRef.value) gsap.set(sidebarRef.value, { x: '-100%', opacity: 0 })
            }
        }
        window.addEventListener('resize', handleResize)
        return () => window.removeEventListener('resize', handleResize)
    })

    return {
        isDarkMode,
        sidebarCollapsed,
        sidebarRef,
        toggleTheme,
        toggleSidebar,
        handleSendMessage,
        handleStopGeneration,
        clearError,
        resetConversation,
        downloadPrompt
    }
}
