// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@nuxtjs/mdc',
    '@nuxthub/core',
    'nuxt-auth-utils',
    'nuxt-charts'
  ],

  // 添加静态生成配置
  ssr: false,
  devtools: {
    enabled: false
  },

  css: ['~/assets/css/main.css'],

  mdc: {
    headings: {
      anchorLinks: false
    },
    highlight: {
      // noApiRoute: true
      shikiEngine: 'javascript'
    }
  },

  // UI 配置
  ui: {
    // 优化图标配置
    fonts: false,
    content: true
  },

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || '/api'
    }
  },

  // 构建优化配置
  build: {
    // 配置 chunk 分割策略
    rollupOptions: {
      output: {
        manualChunks: {
          // 将图标库单独分割
          'icon-libraries': ['@iconify-json/lucide'],
          // 将 UI 库单独分割
          'ui-libs': ['@nuxt/ui'],
          // 将核心依赖单独分割
          'core-vendors': ['vue', 'vue-router']
        }
      }
    },
    // 增加 chunk 大小警告限制
    chunkSizeWarningLimit: 1000,
    // 启用并行构建
    parallel: true
  },
  // 禁用服务器端渲染
  generate: {
    // 配置静态生成选项
    routes: ['/'] // 预生成的路由
  },

  // 暂时禁用预渲染以解决构建问题
  // routeRules: {
  //   '/': { prerender: true }
  // },

  compatibilityDate: '2025-01-15',

  // 缓存配置
  nitro: {
    // 启用构建缓存
    buildCache: true,
    // 优化服务器构建
    esbuild: {
      options: {
        target: 'es2019',
        // 启用压缩
        minify: true
      }
    },
    experimental: {
      openAPI: true
    },
    // 代理配置
    devProxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        secure: false
      }
    }
  },

  hub: {
    db: 'sqlite',
    blob: true
  },

  // Vite 配置
  vite: {
    // 优化依赖
    optimizeDeps: {
      // 强制预构建依赖
      include: ['vue', 'vue-router', '@nuxt/ui'],
      // 排除不需要预构建的依赖
      exclude: ['@iconify-json/simple-icons']
    },
    // 构建配置
    build: {
      // 禁用源码映射以加快构建
      sourcemap: false
    },
    // 开发服务器代理配置
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:5001',
          changeOrigin: true,
          secure: false
        }
      }
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
