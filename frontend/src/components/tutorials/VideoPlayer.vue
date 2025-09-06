<template>
  <div class="video-player bg-card-bg rounded-lg overflow-hidden">
    <!-- Video Container -->
    <div class="relative aspect-video bg-black">
      <video
        ref="videoRef"
        :src="videoUrl"
        :poster="thumbnailUrl"
        class="w-full h-full"
        @loadedmetadata="handleLoadedMetadata"
        @timeupdate="handleTimeUpdate"
        @ended="handleEnded"
        @play="handlePlay"
        @pause="handlePause"
        @click="togglePlayPause"
      >
        Your browser does not support the video tag.
      </video>

      <!-- Loading Overlay -->
      <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <BaseSpinner variant="logo" size="large" color="white" />
      </div>

      <!-- Play/Pause Overlay -->
      <div 
        v-if="showPlayOverlay"
        class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 cursor-pointer"
        @click="togglePlayPause"
      >
        <div class="w-20 h-20 bg-white bg-opacity-90 rounded-full flex items-center justify-center">
          <svg v-if="!isPlaying" class="w-8 h-8 text-text ml-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
          <svg v-else class="w-8 h-8 text-text" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
          </svg>
        </div>
      </div>

      <!-- Video Controls Overlay -->
      <div 
        v-if="showControls"
        class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4"
        @mouseenter="showControls = true"
        @mouseleave="hideControlsTimer = setTimeout(() => showControls = false, 3000)"
      >
        <!-- Progress Bar -->
        <div class="mb-3">
          <div 
            class="w-full h-1 bg-white bg-opacity-30 rounded-full cursor-pointer"
            @click="handleProgressClick"
          >
            <div 
              class="h-full bg-primary rounded-full transition-all duration-200"
              :style="{ width: `${progressPercentage}%` }"
            ></div>
          </div>
        </div>

        <!-- Control Buttons -->
        <div class="flex items-center justify-between text-white">
          <div class="flex items-center space-x-4">
            <!-- Play/Pause Button -->
            <button @click="togglePlayPause" class="hover:opacity-80 transition-opacity">
              <svg v-if="!isPlaying" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
              <svg v-else class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
              </svg>
            </button>

            <!-- Volume Button -->
            <button @click="toggleMute" class="hover:opacity-80 transition-opacity">
              <svg v-if="!isMuted" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 14.142M6.343 6.343L4.93 4.93A1 1 0 003.515 6.343v11.314a1 1 0 001.414 1.414l1.414-1.414M9 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
              </svg>
            </button>

            <!-- Time Display -->
            <span class="text-sm font-mono">
              {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
            </span>
          </div>

          <div class="flex items-center space-x-4">
            <!-- Speed Button -->
            <button @click="cyclePlaybackSpeed" class="hover:opacity-80 transition-opacity">
              <span class="text-sm font-medium">{{ playbackSpeed }}x</span>
            </button>

            <!-- Fullscreen Button -->
            <button @click="toggleFullscreen" class="hover:opacity-80 transition-opacity">
              <svg v-if="!isFullscreen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9V4.5M9 9H4.5M9 9L3.5 3.5M15 9v4.5M15 9h4.5M15 9l5.5-5.5M9 15v4.5M9 15H4.5M9 15l-5.5 5.5M15 15v-4.5M15 15h4.5m0 0l5.5 5.5" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Video Info -->
    <div class="p-6">
      <div class="flex items-start justify-between mb-4">
        <div class="flex-1">
          <h2 class="text-xl font-bold text-text mb-2">{{ videoTitle }}</h2>
          <div class="flex items-center space-x-4 text-sm text-text opacity-70">
            <span v-if="instructor">{{ instructor }}</span>
            <span>{{ formatDate(publishedAt) }}</span>
            <span>{{ viewCount }} views</span>
          </div>
        </div>
        
        <div class="flex items-center space-x-2">
          <BaseButton
            @click="handleBookmark"
            type="ghost"
            size="small"
          >
            <svg v-if="!isBookmarked" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            <svg v-else class="w-4 h-4 text-primary" fill="currentColor" viewBox="0 0 24 24">
              <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </BaseButton>
          
          <BaseButton
            @click="handleShare"
            type="ghost"
            size="small"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
          </BaseButton>
        </div>
      </div>

      <!-- Description -->
      <div v-if="videoDescription" class="prose prose-sm max-w-none text-text">
        <p>{{ videoDescription }}</p>
      </div>

      <!-- Tags -->
      <div v-if="tags && tags.length > 0" class="mt-4">
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in tags"
            :key="tag"
            class="text-xs bg-secondary text-text px-3 py-1 rounded-full"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { BaseButton, BaseSpinner } from '@/components/base'

const props = defineProps({
  videoId: {
    type: String,
    required: true
  },
  videoUrl: {
    type: String,
    required: true
  },
  videoTitle: {
    type: String,
    required: true
  },
  videoDescription: {
    type: String,
    default: ''
  },
  thumbnailUrl: {
    type: String,
    default: ''
  },
  instructor: {
    type: String,
    default: ''
  },
  publishedAt: {
    type: String,
    default: ''
  },
  viewCount: {
    type: Number,
    default: 0
  },
  tags: {
    type: Array,
    default: () => []
  },
  isBookmarked: {
    type: Boolean,
    default: false
  },
  autoplay: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['play', 'pause', 'ended', 'bookmark', 'share', 'time-update'])

const videoRef = ref(null)
const isLoading = ref(true)
const isPlaying = ref(false)
const isMuted = ref(false)
const isFullscreen = ref(false)
const showControls = ref(true)
const showPlayOverlay = ref(true)
const currentTime = ref(0)
const duration = ref(0)
const playbackSpeed = ref(1)
const hideControlsTimer = ref(null)

const progressPercentage = computed(() => {
  if (duration.value === 0) return 0
  return (currentTime.value / duration.value) * 100
})

const playbackSpeeds = [0.5, 0.75, 1, 1.25, 1.5, 2]

const handleLoadedMetadata = () => {
  isLoading.value = false
  duration.value = videoRef.value.duration
  if (props.autoplay) {
    play()
  }
}

const handleTimeUpdate = () => {
  currentTime.value = videoRef.value.currentTime
  emit('time-update', {
    currentTime: currentTime.value,
    duration: duration.value,
    progress: progressPercentage.value
  })
}

const handleEnded = () => {
  isPlaying.value = false
  showPlayOverlay.value = true
  emit('ended')
}

const handlePlay = () => {
  isPlaying.value = true
  showPlayOverlay.value = false
  emit('play')
}

const handlePause = () => {
  isPlaying.value = false
  emit('pause')
}

const togglePlayPause = () => {
  if (videoRef.value.paused) {
    play()
  } else {
    pause()
  }
}

const play = () => {
  videoRef.value?.play()
}

const pause = () => {
  videoRef.value?.pause()
}

const toggleMute = () => {
  isMuted.value = !isMuted.value
  videoRef.value.muted = isMuted.value
}

const cyclePlaybackSpeed = () => {
  const currentIndex = playbackSpeeds.indexOf(playbackSpeed.value)
  const nextIndex = (currentIndex + 1) % playbackSpeeds.length
  playbackSpeed.value = playbackSpeeds[nextIndex]
  videoRef.value.playbackRate = playbackSpeed.value
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    videoRef.value?.requestFullscreen()
    isFullscreen.value = true
  } else {
    document.exitFullscreen()
    isFullscreen.value = false
  }
}

const handleProgressClick = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  const clickX = event.clientX - rect.left
  const percentage = clickX / rect.width
  const newTime = percentage * duration.value
  videoRef.value.currentTime = newTime
}

const handleBookmark = () => {
  emit('bookmark', props.videoId)
}

const handleShare = () => {
  emit('share', {
    videoId: props.videoId,
    title: props.videoTitle,
    url: `${window.location.origin}/tutorials/${props.videoId}`
  })
}

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  } else {
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

// Keyboard shortcuts
const handleKeydown = (event) => {
  if (!videoRef.value) return
  
  switch (event.key) {
    case ' ':
      event.preventDefault()
      togglePlayPause()
      break
    case 'ArrowLeft':
      event.preventDefault()
      videoRef.value.currentTime = Math.max(0, videoRef.value.currentTime - 10)
      break
    case 'ArrowRight':
      event.preventDefault()
      videoRef.value.currentTime = Math.min(duration.value, videoRef.value.currentTime + 10)
      break
    case 'ArrowUp':
      event.preventDefault()
      videoRef.value.volume = Math.min(1, videoRef.value.volume + 0.1)
      break
    case 'ArrowDown':
      event.preventDefault()
      videoRef.value.volume = Math.max(0, videoRef.value.volume - 0.1)
      break
    case 'f':
    case 'F':
      event.preventDefault()
      toggleFullscreen()
      break
    case 'm':
    case 'M':
      event.preventDefault()
      toggleMute()
      break
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  if (hideControlsTimer.value) {
    clearTimeout(hideControlsTimer.value)
  }
})

// Watch for fullscreen changes
watch(isFullscreen, (newValue) => {
  if (newValue) {
    document.addEventListener('fullscreenchange', () => {
      isFullscreen.value = !!document.fullscreenElement
    })
  }
})
</script>

<style scoped>
.video-player {
  max-width: 100%;
}

/* Custom scrollbar for description */
.prose::-webkit-scrollbar {
  width: 4px;
}

.prose::-webkit-scrollbar-track {
  background: var(--color-scrollbar-track);
  border-radius: 2px;
}

.prose::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 2px;
}

.prose::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}
</style>
