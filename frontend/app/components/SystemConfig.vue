<template>
  <USlideover v-model:open="showSystemConfig" title="系统配置" :width="600">
    <template #body>
      <div class="space-y-6">
        <!-- AI服务管理 -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">AI大模型管理</h3>
            <UButton size="sm" variant="primary" @click="openProviderModal()">
              <template #icon>
                <i-lucide-plus class="w-4 h-4" />
              </template>
              添加模型
            </UButton>
          </div>
          <div class="space-y-2">
            <!-- <div v-if="aiProviders.length === 0" class="text-center text-muted-foreground py-8">
              暂无AI服务，请点击添加按钮添加
            </div> -->
            <UPageList divide>
              <template #body>
                <div v-for="(provider, index) in aiProviders" :key="provider.id"
                  class="flex items-center justify-between p-3 border rounded-lg">
                  <div class="flex items-center space-x-2">
                    <UAvatar icon="i-lucide-image" size="md" />
                    <div>
                      <div class="font-medium">{{ provider.name }}</div>
                      <div class="text-sm text-muted-foreground">{{ provider.provider_type }}</div>
                      <div class="text-xs text-muted-foreground">{{ provider.host }}</div>
                    </div>
                    <UUser :name="provider.name" :description="provider.provider_type" :avatar="provider.logo"
                      size="xl" />
                  </div>
                  <div class="flex space-x-2">
                    <UButton size="sm" variant="ghost" icon="i-lucide-edit" @click="openProviderModal(provider)" />
                    <UButton size="sm" variant="ghost" color="danger" icon="i-lucide-trash-2"
                      @click="deleteProvider(provider.id)" />
                  </div>
                </div>
              </template>
            </UPageList>
            <UEmpty v-if="aiProviders.length === 0" title="暂无配置，请点击添加模型按钮" />
          </div>
        </div>

        <!-- 其他系统配置 -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold">其他配置</h3>
          <div class="space-y-3">
            <div class="space-x-2">
              <label class="text-sm font-medium">系统名称</label>
              <UInput v-model="systemConfig.systemName" placeholder="输入系统名称" class="w-full" />
            </div>
            <div class="space-x-2">
              <label class="text-sm font-medium">默认语言</label>
              <USelect v-model="systemConfig.defaultLanguage" :items="['zh-CN', 'en-US']" class="w-full" />
            </div>
          </div>
        </div>
      </div>
    </template>
  </USlideover>

  <!-- AI服务商编辑弹窗 -->
  <UModal v-model:open="showProviderModal" :title="editingProvider ? '编辑AI服务商' : '添加AI服务商'"
    :ui="{ footer: 'justify-end' }">
    <template #body>
      <UForm class="space-y-4">
        <UFormField label="AI服务商">
          <USelect v-model="providerForm.provider_type" :items="providerTypes"
            @update:model-value="onProviderTypeChange" class="w-full" />
        </UFormField>
        <UFormField label="API Host">
          <UInput v-model="providerForm.host" placeholder="输入API Host" class="w-full" />
        </UFormField>
        <UFormField label="API Key">
          <UInput v-model="providerForm.api_key" placeholder="输入API Key" class="w-full" />
        </UFormField>
      </UForm>
    </template>
    <template #footer="{ close }">
      <UButton label="取消" variant="primary" @click="close" />
      <UButton label="保存" variant="ghost" @click="saveProvider" :loading="savingProvider" />
    </template>
  </UModal>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 控制侧边栏显示
const showSystemConfig = ref(false)

// 控制服务商编辑弹窗显示
const showProviderModal = ref(false)

// 编辑中的服务商
const editingProvider = ref<any>(null)

// 保存状态
const savingProvider = ref(false)

// AI服务商列表
const aiProviders = ref<any[]>([])

// 系统配置
const systemConfig = ref({
  systemName: 'Chat System',
  defaultLanguage: 'zh-CN'
})

// 服务商类型选项
const providerTypes = [
  { label: 'OpenAI', value: 'openai' },
  { label: 'DeepSeek', value: 'deepseek' },
  { label: 'Anthropic', value: 'anthropic' },
  { label: 'Google', value: 'google' },
  { label: 'Qwen', value: 'qwen' }
]

// 服务商默认Host映射
const providerDefaultHosts = {
  openai: 'https://api.openai.com/v1',
  deepseek: 'https://api.deepseek.com/v1',
  anthropic: 'https://api.anthropic.com/v1',
  google: 'https://generativelanguage.googleapis.com/v1',
  qwen: 'https://dashscope.aliyuncs.com/api/v1'
}

// 服务商表单
const providerForm = ref({
  name: '',
  provider_type: 'openai',
  host: providerDefaultHosts.openai,
  api_key: ''
})

// 加载AI服务商列表
const loadAiProviders = async () => {
  try {
    const response = await $fetch('/api/config/ai-providers')
    if (response.ok) {
      const data = await response.json()
      aiProviders.value = data
    } else {
      console.error('Failed to load AI providers:', response.statusText)
    }
  } catch (error) {
    console.error('Error loading AI providers:', error)
  }
}

// 打开服务商编辑弹窗
const openProviderModal = (provider: any = null) => {
  editingProvider.value = provider
  if (provider) {
    // 编辑模式，填充表单
    providerForm.value = {
      name: provider.name,
      provider_type: provider.provider_type,
      host: provider.host,
      api_key: '' // 不显示已保存的API Key
    }
  } else {
    // 添加模式，重置表单
    providerForm.value = {
      name: '',
      provider_type: 'openai',
      host: providerDefaultHosts.openai,
      api_key: ''
    }
  }
  showProviderModal.value = true
}

// 服务商类型变更处理
const onProviderTypeChange = (type: string) => {
  providerForm.value.host = providerDefaultHosts[type as keyof typeof providerDefaultHosts] || ''
}

// 保存服务商
const saveProvider = async () => {
  try {
    savingProvider.value = true

    if (editingProvider.value) {
      // 更新现有服务商
      const response = await $fetch(`/api/config/ai-providers/${editingProvider.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(providerForm.value)
      })

      if (response.ok) {
        await loadAiProviders()
        showProviderModal.value = false
      } else {
        const error = await response.json()
        console.error('Failed to update provider:', error)
      }
    } else {
      // 添加新服务商
      const response = await $fetch('/api/config/ai-providers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(providerForm.value)
      })

      if (response.ok) {
        await loadAiProviders()
        showProviderModal.value = false
      } else {
        const error = await response.json()
        console.error('Failed to add provider:', error)
      }
    }
  } catch (error) {
    console.error('Error saving provider:', error)
  } finally {
    savingProvider.value = false
  }
}

// 删除服务商
const deleteProvider = async (id: number) => {
  try {
    if (confirm('确定要删除这个AI服务商吗？')) {
      const response = await $fetch(`/api/config/ai-providers/${id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        await loadAiProviders()
      } else {
        const error = await response.json()
        console.error('Failed to delete provider:', error)
      }
    }
  } catch (error) {
    console.error('Error deleting provider:', error)
  }
}

// 暴露方法给父组件
defineExpose({
  open: () => {
    showSystemConfig.value = true
    loadAiProviders()
  }
})

// 组件挂载时加载AI服务商列表
onMounted(() => {
  loadAiProviders()
})
</script>
