<script setup lang="ts">
const input = ref('')
const loading = ref(false)

function generateChatId() {
  return crypto.randomUUID()
}

const { model } = useModels()

const {
  dropzoneRef,
  isDragging,
  files,
  isUploading,
  uploadedFiles,
  addFiles,
  removeFile,
  clearFiles
} = useFileUploadWithStatus()

async function createChat(prompt: string) {
  input.value = prompt
  loading.value = true

  const chatId = generateChatId()

  // 先上传文件（如果有）
  if (files.value.length > 0) {
    await addFiles(files.value.map(f => f.file), chatId)
  }

  const parts: Array<{ type: string, text?: string, mediaType?: string, url?: string }> = [{ type: 'text', text: prompt }]

  if (uploadedFiles.value.length > 0) {
    parts.push(...uploadedFiles.value)
  }

  const chat = await $fetch('/api/chats', {
    method: 'POST',
    body: {
      id: chatId,
      message: {
        role: 'user',
        parts
      }
    }
  })

  refreshNuxtData('chats')
  navigateTo(`/chat/${chat?.id}`)
}

async function onSubmit() {
  await createChat(input.value)
  clearFiles()
}

const quickChats = [
  {
    label: '为什么使用 Nuxt UI?',
    icon: 'i-logos-nuxt-icon'
  },
  {
    label: '帮助我创建一个 Vue 组合式函数',
    icon: 'i-logos-vue'
  },
  {
    label: '告诉我更多关于 UnJS 的信息',
    icon: 'i-logos-unjs'
  },
  {
    label: '为什么我应该考虑 VueUse?',
    icon: 'i-logos-vueuse'
  },
  {
    label: 'Tailwind CSS 最佳实践',
    icon: 'i-logos-tailwindcss-icon'
  },
  {
    label: '在 Bordeaux 天气如何?',
    icon: 'i-lucide-sun'
  },
  {
    label: '展示我销售数据的图表',
    icon: 'i-lucide-line-chart'
  }
]
</script>

<template>
  <UDashboardPanel id="home" :ui="{ body: 'p-0 sm:p-0' }">
    <template #header>
      <DashboardNavbar />
    </template>

    <template #body>
      <DragDropOverlay :show="isDragging" />
      <UContainer ref="dropzoneRef" class="flex-1 flex flex-col justify-center gap-4 sm:gap-6 py-8">
        <h1 class="text-3xl sm:text-4xl text-highlighted font-bold">
          你想咨询什么内容?
        </h1>

        <UChatPrompt v-model="input" :status="loading ? 'streaming' : 'ready'" :disabled="isUploading"
          class="[view-transition-name:chat-prompt]" placeholder="输入你的问题..." variant="subtle" :ui="{ base: 'px-1.5' }"
          @submit="onSubmit">
          <template v-if="files.length > 0" #header>
            <div class="flex flex-wrap gap-2">
              <FileAvatar v-for="fileWithStatus in files" :key="fileWithStatus.id" :name="fileWithStatus.file.name"
                :type="fileWithStatus.file.type" :preview-url="fileWithStatus.previewUrl"
                :status="fileWithStatus.status" :error="fileWithStatus.error" removable
                @remove="removeFile(fileWithStatus.id)" />
            </div>
          </template>

          <template #footer>
            <div class="flex items-center gap-1">
              <FileUploadButton @files-selected="addFiles($event)" />
              <ModelSelect v-model="model" />
            </div>

            <UChatPromptSubmit color="neutral" size="sm" :disabled="isUploading" />
          </template>
        </UChatPrompt>

        <div class="flex flex-wrap gap-2">
          <UButton v-for="quickChat in quickChats" :key="quickChat.label" :icon="quickChat.icon"
            :label="quickChat.label" size="sm" color="neutral" variant="outline" class="rounded-full"
            @click="createChat(quickChat.label)" />
        </div>
      </UContainer>
    </template>
  </UDashboardPanel>
</template>
