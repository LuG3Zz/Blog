import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // 根据当前工作目录中的 `mode` 加载 .env 文件
  // 设置第三个参数为 '' 来加载所有环境变量，而不管是否有 `VITE_` 前缀。
  const env = loadEnv(mode, process.cwd(), '')

  console.log(`运行模式: ${mode}, 命令: ${command}`)

  return {
  base: '/',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    proxy: {
      // 使用通配符代理所有API请求到后端服务器
      // 代理带有API前缀的请求
      '^/api/v1': {
        target: 'http://127.0.0.1:8000',
        //target: 'http://39.105.192.244:8000',
        changeOrigin: true,
        secure: true,
        // 设置转发的头部信息，保留客户端真实IP
        headers: (req) => {
          // 动态获取客户端IP
          const clientIP = req.socket.remoteAddress || '127.0.0.1';
          return {
            'X-Forwarded-For': clientIP,
            'X-Real-IP': clientIP,
            'Forwarded': `for=${clientIP}`
          };
        },
        // 支持 WebSocket
        ws: true,
        // 启用调试日志
        configure: (proxy) => {
          proxy.on('error', (err) => {
            console.log('代理错误:', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('代理请求:', req.method, req.url);
            console.log('代理请求头:', proxyReq.getHeaders());
            console.log('原始请求头:', req.headers);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('代理响应:', proxyRes.statusCode, req.url);
            console.log('响应头:', proxyRes.headers);
          });
        }
      },
      // WebSocket路径单独代理
      '^/ws': {
        target: 'http://127.0.0.1:8000',
        //target: 'http://39.105.192.244:8000',
        changeOrigin: true,
        secure: true,
        // 设置转发的头部信息，保留客户端真实IP
        headers: (req) => {
          // 动态获取客户端IP
          const clientIP = req.socket.remoteAddress || '127.0.0.1';
          return {
            'X-Forwarded-For': clientIP,
            'X-Real-IP': clientIP,
            'Forwarded': `for=${clientIP}`
          };
        },
        // 支持 WebSocket
        ws: true,
        // 启用调试日志
        configure: (proxy) => {
          proxy.on('error', (err) => {
            console.log('代理错误:', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('代理请求:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('代理响应:', proxyRes.statusCode, req.url);
          });
        }
      },
      // 静态文件路径单独代理
      '^/static': {
        target: 'http://127.0.0.1:8000',
        //target: 'http://39.105.192.244:8000',
        changeOrigin: true,
        secure: true,
        configure: (proxy) => {
          proxy.on('error', (err) => {
            console.log('静态文件代理错误:', err);
          });
        }
      },
    },
    cors: true,
    // 添加开发服务器启动时的日志
    hmr: {
      overlay: true
    }
  },
  // 添加公共资源配置
  publicDir: 'public',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // 确保图片等静态资源被正确处理
    assetsInlineLimit: 4096,
    // 启用源码映射，便于调试
    sourcemap: true,
    // 增加块大小警告限制，避免过多警告
    chunkSizeWarningLimit: 800, // 从默认的500KB增加到800KB
    // 优化构建过程
    rollupOptions: {
      output: {
        // 更细致地按类型分块
        manualChunks: (id) => {
          // Vue相关库
          if (id.includes('node_modules/vue/') ||
              id.includes('node_modules/@vue/') ||
              id.includes('node_modules/vue-router/')) {
            return 'vue-core';
          }

          // Pinia状态管理
          if (id.includes('node_modules/pinia/')) {
            return 'vue-store';
          }

          // Ant Design Vue UI库
          if (id.includes('node_modules/ant-design-vue/') ||
              id.includes('node_modules/@ant-design/')) {
            return 'ui-vendor';
          }

          // Markdown相关
          if (id.includes('node_modules/markdown-it/') ||
              id.includes('node_modules/markdown-it-')) {
            return 'markdown';
          }

          // Vditor编辑器
          if (id.includes('node_modules/vditor/')) {
            return 'editor';
          }

          // 语法高亮
          if (id.includes('node_modules/highlight.js/') ||
              id.includes('node_modules/prismjs/')) {
            return 'syntax-highlight';
          }

          // 数学公式
          if (id.includes('node_modules/katex/')) {
            return 'math';
          }

          // 图表库
          if (id.includes('node_modules/chart.js/')) {
            return 'charts';
          }

          // 动画库
          if (id.includes('node_modules/gsap/') ||
              id.includes('node_modules/lenis/') ||
              id.includes('node_modules/animate.css/') ||
              id.includes('node_modules/motion-v/')) {
            return 'animations';
          }

          // 工具库
          if (id.includes('node_modules/axios/') ||
              id.includes('node_modules/date-fns/') ||
              id.includes('node_modules/lodash/') ||
              id.includes('node_modules/clsx/') ||
              id.includes('node_modules/tailwind-merge/')) {
            return 'utils';
          }

          // 其他第三方库
          if (id.includes('node_modules/')) {
            return 'vendor';
          }
        },
        // 添加文件名哈希，便于缓存控制
        entryFileNames: 'js/[name].[hash].js',
        chunkFileNames: 'js/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]'
      }
    },
    // 压缩选项
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: process.env.NODE_ENV === 'production',
        drop_debugger: process.env.NODE_ENV === 'production'
      }
    }
  },
  // 添加环境变量配置
  define: {
    // 在这里定义全局常量替换方式
    // 注意：对于 import.meta.env.* 的访问，Vite 已经提供了内置支持
  },
  // 优化开发体验
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'axios']
  }
  }
})