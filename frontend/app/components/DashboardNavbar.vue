<template>
  <UDashboardNavbar
    class="sticky lg:absolute top-0 inset-x-0 border-b-0 z-10 bg-default/75 backdrop-blur lg:bg-transparent lg:backdrop-blur-none pointer-events-none"
    :ui="{ left: 'pointer-events-auto', right: 'pointer-events-auto' }">
    <template #left>
      <!-- 返回首页 -->
      <ULink as="button" to="/">
        <UButton color="neutral" variant="ghost" icon="i-lucide-house" />
      </ULink>
      <USeparator orientation="vertical" class="h-5" />
      <!-- 不是首页的时候显示 -->
      <ULink as="button" v-if="$route.fullPath !== '/'">
        <UButton color="neutral" variant="ghost" icon="i-lucide-undo-2" @click="$router.back()" />
      </ULink>
    </template>
    <template #right>
      <!-- 文档管理按钮 -->
      <ULink as="button" to="/docs">
        <UButton color="neutral" variant="ghost" icon="i-lucide-library" />
      </ULink>
      <!-- 系统管理按钮 -->
      <UButton color="neutral" variant="ghost" icon="i-lucide-settings" @click="systemConfigRef?.open()" />
      <UColorModeButton />
      <UButton color="neutral" variant="ghost" icon="i-lucide-plus" to="/" class="lg:hidden" />
    </template>
  </UDashboardNavbar>

  <!-- 系统配置组件 -->
  <SystemConfig ref="systemConfigRef" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SystemConfig from './SystemConfig.vue'

// 系统配置组件引用
const systemConfigRef = ref<InstanceType<typeof SystemConfig> | null>(null)
</script>
