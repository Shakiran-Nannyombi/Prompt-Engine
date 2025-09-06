<template>
  <div class="document-upload">
    <!-- Header -->
    <div class="p-4 border-b border-card-border">
      <h3 class="text-md font-medium text-text mb-2">Document Upload</h3>
      <p class="text-sm text-text opacity-70">
        Upload a document to enable Q&A and context-aware responses.
      </p>
    </div>

    <!-- Upload Area -->
    <div class="p-4">
      <!-- Drop Zone -->
      <div
        ref="dropZone"
        :class="dropZoneClasses"
        @click="triggerFileSelect"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave"
        @drop.prevent="handleDrop"
      >
        <input
          ref="fileInput"
          type="file"
          :accept="acceptedFileTypes"
          @change="handleFileSelect"
          class="hidden"
        />
        
        <div class="text-center">
          <div class="w-12 h-12 mx-auto mb-3 text-text opacity-50">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p class="text-sm font-medium text-text mb-1">
            {{ isDragOver ? 'Drop your file here' : 'Click to upload or drag and drop' }}
          </p>
          <p class="text-xs text-text opacity-50">
            {{ acceptedFileTypesText }}
          </p>
          <p class="text-xs text-text opacity-50 mt-1">
            Max size: {{ maxFileSizeText }}
          </p>
        </div>
      </div>

      <!-- Upload Progress -->
      <div v-if="uploading" class="mt-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm text-text">Uploading...</span>
          <span class="text-sm text-text opacity-70">{{ uploadProgress }}%</span>
        </div>
        <div class="w-full bg-secondary rounded-full h-2">
          <div 
            class="bg-primary h-2 rounded-full transition-all duration-300"
            :style="{ width: `${uploadProgress}%` }"
          ></div>
        </div>
      </div>

      <!-- Uploaded Document Display -->
      <div v-if="uploadedDocument" class="mt-4">
        <div class="p-3 bg-success-50 border border-success-200 rounded-lg">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-success rounded-full flex items-center justify-center">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-success-800">{{ uploadedDocument.name }}</p>
                <p class="text-xs text-success-600">
                  {{ formatFileSize(uploadedDocument.size) }} • Uploaded successfully
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button 
                @click="viewDocument"
                class="text-success-600 hover:text-success-800 transition-colors"
                title="View document"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
              <button 
                @click="removeDocument"
                class="text-error hover:text-error-600 transition-colors"
                title="Remove document"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="mt-4 p-3 bg-error-50 border border-error-200 rounded-lg">
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-sm text-error">{{ error }}</span>
        </div>
      </div>

      <!-- Recent Documents -->
      <div v-if="recentDocuments.length > 0" class="mt-6">
        <h4 class="text-sm font-medium text-text mb-3">Recent Documents</h4>
        <div class="space-y-2">
          <div
            v-for="doc in recentDocuments"
            :key="doc.id"
            class="flex items-center justify-between p-2 bg-card-bg border border-card-border rounded-lg hover:bg-secondary transition-colors cursor-pointer"
            @click="selectRecentDocument(doc)"
          >
            <div class="flex items-center space-x-2">
              <div class="w-6 h-6 bg-accent rounded flex items-center justify-center">
                <svg class="w-3 h-3 text-text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <p class="text-xs font-medium text-text">{{ doc.name }}</p>
                <p class="text-xs text-text opacity-50">{{ formatFileSize(doc.size) }}</p>
              </div>
            </div>
            <button
              @click.stop="removeRecentDocument(doc.id)"
              class="text-text opacity-50 hover:text-error transition-colors"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { BaseButton } from '@/components/base'

const props = defineProps({
  acceptedFileTypes: {
    type: String,
    default: '.txt,.md,.pdf,.doc,.docx,.rtf'
  },
  maxFileSize: {
    type: Number,
    default: 10 * 1024 * 1024 // 10MB
  },
  multiple: {
    type: Boolean,
    default: false
  },
  recentDocuments: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['file-uploaded', 'file-removed', 'document-selected'])

const fileInput = ref(null)
const dropZone = ref(null)
const isDragOver = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadedDocument = ref(null)
const error = ref('')

const acceptedFileTypesText = computed(() => {
  const types = props.acceptedFileTypes.split(',').map(type => type.trim())
  return types.join(', ').toUpperCase()
})

const maxFileSizeText = computed(() => {
  if (props.maxFileSize >= 1024 * 1024) {
    return `${Math.round(props.maxFileSize / (1024 * 1024))}MB`
  } else {
    return `${Math.round(props.maxFileSize / 1024)}KB`
  }
})

const dropZoneClasses = computed(() => {
  const baseClasses = [
    'border-2',
    'border-dashed',
    'rounded-lg',
    'p-6',
    'cursor-pointer',
    'transition-all',
    'duration-200'
  ]
  
  if (isDragOver.value) {
    baseClasses.push('border-primary', 'bg-primary-50')
  } else {
    baseClasses.push('border-card-border', 'hover:border-accent', 'hover:bg-secondary')
  }
  
  if (uploading.value) {
    baseClasses.push('pointer-events-none', 'opacity-50')
  }
  
  return baseClasses
})

const triggerFileSelect = () => {
  if (!uploading.value) {
    fileInput.value?.click()
  }
}

const handleDragOver = (event) => {
  event.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = (event) => {
  event.preventDefault()
  isDragOver.value = false
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  
  const files = Array.from(event.dataTransfer.files)
  if (files.length > 0) {
    handleFiles(files)
  }
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    handleFiles(files)
  }
  // Clear the input so the same file can be selected again
  event.target.value = ''
}

const handleFiles = async (files) => {
  if (files.length === 0) return
  
  const file = files[0] // For now, only handle single file
  
  // Validate file type
  const validTypes = props.acceptedFileTypes.split(',').map(type => type.trim().toLowerCase())
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
  
  if (!validTypes.includes(fileExtension)) {
    error.value = `File type ${fileExtension} is not supported. Please upload: ${acceptedFileTypesText.value}`
    return
  }
  
  // Validate file size
  if (file.size > props.maxFileSize) {
    error.value = `File size exceeds the maximum limit of ${maxFileSizeText.value}`
    return
  }
  
  error.value = ''
  uploading.value = true
  uploadProgress.value = 0
  
  try {
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      uploadProgress.value += Math.random() * 30
      if (uploadProgress.value >= 100) {
        uploadProgress.value = 100
        clearInterval(progressInterval)
      }
    }, 200)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    uploadedDocument.value = {
      id: Date.now(),
      name: file.name,
      size: file.size,
      type: file.type,
      uploadedAt: new Date().toISOString()
    }
    
    emit('file-uploaded', uploadedDocument.value)
    
  } catch (err) {
    error.value = 'Failed to upload document. Please try again.'
    console.error('Upload error:', err)
  } finally {
    uploading.value = false
    uploadProgress.value = 0
  }
}

const removeDocument = () => {
  if (uploadedDocument.value) {
    emit('file-removed', uploadedDocument.value)
    uploadedDocument.value = null
  }
}

const viewDocument = () => {
  if (uploadedDocument.value) {
    // You could implement document viewing logic here
    console.log('View document:', uploadedDocument.value)
  }
}

const selectRecentDocument = (doc) => {
  emit('document-selected', doc)
}

const removeRecentDocument = (docId) => {
  // You could implement recent document removal logic here
  console.log('Remove recent document:', docId)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped>
.document-upload {
  @apply bg-card-bg;
}

/* Custom scrollbar for recent documents */
.document-upload .space-y-2::-webkit-scrollbar {
  width: 4px;
}

.document-upload .space-y-2::-webkit-scrollbar-track {
  background: var(--color-scrollbar-track);
  border-radius: 2px;
}

.document-upload .space-y-2::-webkit-scrollbar-thumb {
  background: var(--color-scrollbar-thumb);
  border-radius: 2px;
}

.document-upload .space-y-2::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}
</style>
