<script setup lang="ts">
import type { NuxtError } from '#app'

defineProps<{
  error: NuxtError
}>()

useSeoMeta({
  title: '页面未找到',
  description: '我们很抱歉，但此页面无法找到。'
})

useHead({
  htmlAttrs: {
    lang: 'en'
  }
})
</script>

<template>
  <UApp>
    <UError :error="error" />
  </UApp>
</template>
