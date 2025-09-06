<template>
  <BaseCard 
    :clickable="true"
    :hover="true"
    class="video-card group cursor-pointer"
    @click="handleCardClick"
  >
    <!-- Thumbnail -->
    <div class="relative aspect-video bg-secondary rounded-lg overflow-hidden mb-4">
      <img
        v-if="thumbnailUrl"
        :src="thumbnailUrl"
        :alt="videoTitle"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
      />
      <div v-else class="w-full h-full flex items-center justify-center">
        <svg class="w-12 h-12 text-text opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </div>
      
      <!-- Play Button Overlay -->
      <div class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300">
        <div class="w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center transform scale-75 group-hover:scale-100 transition-transform duration-300">
          <svg class="w-6 h-6 text-text ml-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
      </div>
      
      <!-- Duration Badge -->
      <div v-if="duration" class="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white text-xs px-2 py-1 rounded">
        {{ formatDuration(duration) }}
      </div>
      
      <!-- Category Badge -->
      <div v-if="category" class="absolute top-2 left-2 bg-primary text-white text-xs px-2 py-1 rounded">
        {{ category }}
      </div>
    </div>

    <!-- Content -->
    <div class="space-y-3">
      <!-- Title -->
      <h3 class="text-lg font-semibold text-text line-clamp-2 group-hover:text-primary transition-colors">
        {{ videoTitle }}
      </h3>

      <!-- Description -->
      <p v-if="videoDescription" class="text-sm text-text opacity-70 line-clamp-3">
        {{ videoDescription }}
      </p>

      <!-- Metadata -->
      <div class="flex items-center justify-between text-xs text-text opacity-50">
        <div class="flex items-center space-x-4">
          <span v-if="instructor">{{ instructor }}</span>
          <span v-if="publishedAt">{{ formatDate(publishedAt) }}</span>
        </div>
        <div class="flex items-center space-x-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          <span>{{ viewCount || 0 }} views</span>
        </div>
      </div>

      <!-- Tags -->
      <div v-if="tags && tags.length > 0" class="flex flex-wrap gap-1">
        <span
          v-for="tag in tags.slice(0, 3)"
          :key="tag"
          class="text-xs bg-secondary text-text px-2 py-1 rounded"
        >
          {{ tag }}
        </span>
        <span v-if="tags.length > 3" class="text-xs text-text opacity-50">
          +{{ tags.length - 3 }} more
        </span>
      </div>

      <!-- Progress Bar (if watched) -->
      <div v-if="watchProgress > 0" class="space-y-1">
        <div class="flex items-center justify-between text-xs text-text opacity-70">
          <span>Progress</span>
          <span>{{ Math.round(watchProgress) }}%</span>
        </div>
        <div class="w-full bg-secondary rounded-full h-1">
          <div 
            class="bg-primary h-1 rounded-full transition-all duration-300"
            :style="{ width: `${watchProgress}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-between pt-4 border-t border-card-border">
      <div class="flex items-center space-x-2">
        <BaseButton
          v-if="!isBookmarked"
          @click.stop="handleBookmark"
          type="ghost"
          size="small"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
        </BaseButton>
        <BaseButton
          v-else
          @click.stop="handleUnbookmark"
          type="ghost"
          size="small"
        >
          <svg class="w-4 h-4 text-primary" fill="currentColor" viewBox="0 0 24 24">
            <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
        </BaseButton>
        
        <BaseButton
          @click.stop="handleShare"
          type="ghost"
          size="small"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
          </svg>
        </BaseButton>
      </div>
      
      <BaseButton
        @click.stop="handleCardClick"
        type="primary"
        size="small"
      >
        Watch Now
      </BaseButton>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed } from 'vue'
import { BaseCard, BaseButton } from '@/components/base'

const props = defineProps({
  videoId: {
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
  duration: {
    type: Number, // in seconds
    default: 0
  },
  category: {
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
  watchProgress: {
    type: Number,
    default: 0
  },
  isBookmarked: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['play', 'bookmark', 'unbookmark', 'share'])

const handleCardClick = () => {
  emit('play', {
    videoId: props.videoId,
    title: props.videoTitle,
    description: props.videoDescription,
    thumbnailUrl: props.thumbnailUrl,
    duration: props.duration
  })
}

const handleBookmark = () => {
  emit('bookmark', props.videoId)
}

const handleUnbookmark = () => {
  emit('unbookmark', props.videoId)
}

const handleShare = () => {
  emit('share', {
    videoId: props.videoId,
    title: props.videoTitle,
    url: `${window.location.origin}/tutorials/${props.videoId}`
  })
}

const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  } else {
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  
  if (diffInDays === 0) return 'Today'
  if (diffInDays === 1) return 'Yesterday'
  if (diffInDays < 7) return `${diffInDays} days ago`
  if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`
  if (diffInDays < 365) return `${Math.floor(diffInDays / 30)} months ago`
  return `${Math.floor(diffInDays / 365)} years ago`
}
</script>

<style scoped>
.video-card {
  transition: all 0.3s ease;
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
