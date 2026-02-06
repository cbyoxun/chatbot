<script setup lang="ts">
const { isDragging } = useFileUploadWithStatus()
</script>

<template>
  <UDashboardPanel id="chat" class="relative" :ui="{ body: 'p-0 sm:p-0' }">
    <template #header>
      <DashboardNavbar />
    </template>

    <template #body>
      <DragDropOverlay :show="isDragging" />
      <UContainer ref="dropzoneRef" class="flex-1 flex flex-col gap-4 sm:gap-6">
        <!-- ToDo 文档编辑 -->
        <UPageHeader title="文档标题" />
      </UContainer>
    </template>
  </UDashboardPanel>
</template>
