FROM node:20-alpine AS builder

WORKDIR /app

# 复制package相关文件
COPY package.json pnpm-lock.yaml ./

# 安装依赖管理工具
RUN npm install -g pnpm

# 安装依赖
RUN pnpm install

# 复制所有源码
COPY . .

# 设置 Node.js 内存限制, 防止内存溢出
ENV NODE_OPTIONS="--max-old-space-size=4096"

# 构建应用
RUN pnpm build
# RUN pnpm exec nuxt generate

# 生产运行阶段
FROM node:20-alpine

WORKDIR /app

# 安装仅生产依赖
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm
RUN pnpm install --prod --frozen-lockfile

# 从构建阶段复制构建产物
COPY --from=builder /app/.output/public ./public
# COPY --from=builder /app/dist ./public

# 安装 serve 包用于提供静态文件服务

RUN npm install -g serve

# 暴露端口
EXPOSE 3000

# 运行应用
CMD ["serve", "-s", "public", "-l", "3000"]
