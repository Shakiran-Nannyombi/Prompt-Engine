import { ref, computed, nextTick } from 'vue'

export function useChatInput(emit) {
    const message = ref('')
    const files = ref([])
    const pastedContent = ref([])
    const isDragging = ref(false)
    const selectedModel = ref('sonnet-4.5')
    const isThinkingEnabled = ref(false)
    const textareaRef = ref(null)
    const fileInputRef = ref(null)

    const hasContent = computed(() => {
        return message.value.trim().length > 0 || files.value.length > 0 || pastedContent.value.length > 0
    })

    const adjustTextareaHeight = () => {
        nextTick(() => {
            if (textareaRef.value) {
                textareaRef.value.style.height = 'auto'
                textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 384) + 'px'
            }
        })
    }

    const handleInput = () => {
        adjustTextareaHeight()
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    const handleSend = () => {
        if (!hasContent.value) return

        emit('send-message', {
            message: message.value.trim(),
            files: files.value,
            pastedContent: pastedContent.value,
            model: selectedModel.value,
            isThinkingEnabled: isThinkingEnabled.value
        })

        // Clear state
        message.value = ''
        files.value = []
        pastedContent.value = []
        adjustTextareaHeight()
    }

    const triggerFileUpload = () => {
        if (fileInputRef.value) fileInputRef.value.click()
    }

    const processFiles = (fileList) => {
        const newFiles = Array.from(fileList).map(file => {
            const isImage = file.type.startsWith('image/') || /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(file.name)
            return {
                id: Math.random().toString(36).substr(2, 9),
                file,
                type: isImage ? 'image/unknown' : (file.type || 'application/octet-stream'),
                preview: isImage ? URL.createObjectURL(file) : null,
                uploadStatus: 'complete'
            }
        })
        files.value = [...files.value, ...newFiles]
    }

    const handleFileSelect = (e) => {
        if (e.target.files) {
            processFiles(e.target.files)
        }
        e.target.value = ''
    }

    const removeFile = (id) => {
        files.value = files.value.filter(f => f.id !== id)
    }

    const removePastedContent = (id) => {
        pastedContent.value = pastedContent.value.filter(c => c.id !== id)
    }

    const handlePaste = (e) => {
        const items = e.clipboardData.items
        const pastedFiles = []

        for (let i = 0; i < items.length; i++) {
            if (items[i].kind === 'file') {
                const file = items[i].getAsFile()
                if (file) pastedFiles.push(file)
            }
        }

        if (pastedFiles.length > 0) {
            e.preventDefault()
            processFiles(pastedFiles)
            return
        }

        const text = e.clipboardData.getData('text')
        if (text.length > 700) {
            e.preventDefault()
            const snippet = {
                id: Math.random().toString(36).substr(2, 9),
                content: text,
                timestamp: new Date()
            }
            pastedContent.value.push(snippet)
        }
    }

    const onDragOver = () => { isDragging.value = true }
    const onDragLeave = () => { isDragging.value = false }
    const onDrop = (e) => {
        isDragging.value = false
        if (e.dataTransfer.files) {
            processFiles(e.dataTransfer.files)
        }
    }

    return {
        message,
        files,
        pastedContent,
        isDragging,
        selectedModel,
        isThinkingEnabled,
        textareaRef,
        fileInputRef,
        hasContent,
        handleInput,
        handleKeyDown,
        handleSend,
        triggerFileUpload,
        handleFileSelect,
        removeFile,
        removePastedContent,
        handlePaste,
        onDragOver,
        onDragLeave,
        onDrop
    }
}
