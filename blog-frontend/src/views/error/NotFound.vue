<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-primary dark:bg-dark-primary text-secondary dark:text-dark-secondary">
    <div class="error-container">
      <div class="error-code">404</div>
      <h1 class="error-title">页面未找到</h1>
      <p class="error-message">抱歉，您访问的页面不存在或已被移除。</p>
      <router-link to="/" class="error-button">
        返回首页
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.error-container {
  text-align: center;
  padding: 2rem;
  max-width: 600px;
  border: 4px solid;
  background-color: #fff;
  position: relative;
  border-radius: 16px;
  transition: 0.25s ease;
}

.error-container:before,
.error-container:after {
  content: "";
  display: block;
  position: absolute;
  height: 100%;
  width: 100%;
  border: 4px solid;
  background-color: #fff;
  border-radius: 16px;
  transform-origin: center center;
  z-index: -1;
  transition: 0.25s ease;
  top: 0;
  left: 0;
}

.error-container:before {
  transform: translatey(-2%) rotate(-6deg);
}

.error-container:after {
  transform: translatey(2%) rotate(6deg);
}

.error-container:hover {
  transform: rotate(5deg);
}

.error-container:hover:before {
  transform: translatey(-2%) rotate(-4deg);
}

.error-container:hover:after {
  transform: translatey(2%) rotate(4deg);
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.error-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.error-message {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #64748b;
}

.error-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #2c3e50;
  color: white;
  font-weight: 600;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background-color 0.3s;
}

.error-button:hover {
  background-color: #1e293b;
}

/* 暗黑模式适配 */
.dark .error-container,
.dark .error-container:before,
.dark .error-container:after {
  background-color: #1e293b;
  border-color: #cbd5e1;
}

.dark .error-code,
.dark .error-title {
  color: #e2e8f0;
}

.dark .error-message {
  color: #94a3b8;
}

.dark .error-button {
  background-color: #cbd5e1;
  color: #1e293b;
}

.dark .error-button:hover {
  background-color: #e2e8f0;
}
</style>
