<script setup lang="ts">
import { h } from 'vue'
import type { TableColumn } from '@nuxt/ui'

const { isDragging } = useFileUploadWithStatus()

type Document = {
  id: string
  name: string
  type: 'txt' | 'pdf' | 'docx' | 'xlsx'
  description: string
  updatetime: Date | string
}

// 模拟数据10条
const data = ref<Document[]>([
  {
    id: '4600',
    name: 'example.txt',
    type: 'txt',
    description: '这是一个示例文件',
    updatetime: '2024-03-11T15:30:00'
  },
  {
    id: '4599',
    name: 'example.pdf',
    type: 'pdf',
    description: '这是一个示例文件',
    updatetime: '2024-03-11T10:10:00'
  },
  {
    id: '4598',
    name: 'example.docx',
    type: 'docx',
    description: '这是一个示例文件',
    updatetime: '2024-03-11T08:50:00'
  },
  {
    id: '4597',
    name: 'example.xlsx',
    type: 'xlsx',
    description: '这是一个示例文件',
    updatetime: '2024-03-10T19:45:00'
  }
])

const columns: TableColumn<Document>[] = [
  {
    accessorKey: 'id',
    header: 'ID',
    cell: ({ row }) => `#${row.getValue('id')}`
  },
  {
    accessorKey: 'name',
    header: '名称',
    cell: ({ row }) => {
      return h(
        ULink,
        {
          class: 'text-primary font-medium',
          to: `/docs/${row.getValue('id')}`
        },
        row.getValue('name')
      )
    }
  },
  {
    accessorKey: 'type',
    header: '类型'
  },
  {
    accessorKey: 'description',
    header: '描述'
  },
  {
    accessorKey: 'updatetime',
    header: '更新时间'
  },
  {
    accessorKey: '',
    header: '操作'
  }
]
</script>

<template>
  <UDashboardPanel id="docs" class="relative" :ui="{ body: 'p-0 sm:p-0' }">
    <template #header>
      <DashboardNavbar />
    </template>

    <template #body>
      <DragDropOverlay :show="isDragging" />
      <UContainer ref="docsRef" class="flex-1 flex flex-col gap-4 sm:gap-6">
        <!-- 快速上传 -->
        <UPageHero title="文档管理" description="快速上传文档到知识库">
          <UForm class="flex flex-col justify-center space-y-4">
            <!-- 上传文档 -->
            <UFormField class="w-full">
              <UFileUpload label="托入文件" description="支持TXT, PDF, DOCX, XLSX(最大2MB)" accept=".txt,.pdf,.docx,.xlsx"
                class="min-h-48" highlight />
            </UFormField>
            <div class="flex justify-center">
              <UButton type="submit" label="开始上传" />
            </div>
          </UForm>
        </UPageHero>
        <!-- 文档列表 -->
        <UPageSection class="flex flex-col justify-center gap-4">
          <UTable :data="data" :columns="columns" class="w-full" loading loading-color="primary"
            loading-animation="carousel" />
          <UEmpty v-if="data.length === 0" variant="naked" icon="i-lucide-bell" title="No notifications"
            description="You're all caught up. New notifications will appear here." :actions="[
              {
                icon: 'i-lucide-refresh-cw',
                label: 'Refresh',
                color: 'neutral',
                variant: 'subtle'
              }
            ]" />
          <UPagination show-edges :sibling-count="1" :total="100" />
        </UPageSection>
      </UContainer>
    </template>
  </UDashboardPanel>
</template>
