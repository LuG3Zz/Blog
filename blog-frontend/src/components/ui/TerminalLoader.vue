<template>
  <div class="terminal-loader dark:bg-gray-900 dark:border-gray-700">
    <div class="terminal-header dark:bg-gray-800">
      <div class="terminal-title dark:text-gray-300">Status</div>
      <div class="terminal-controls">
        <div class="control close"></div>
        <div class="control minimize"></div>
        <div class="control maximize"></div>
      </div>
    </div>
    <div class="text dark:text-green-400">Loading...</div>
  </div>
</template>

<style scoped>
.terminal-loader {
  @apply border bg-white text-gray-800 p-4 w-64 rounded-lg relative overflow-hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.terminal-header {
  @apply flex justify-between items-center px-2 py-1 bg-gray-100;
  border-top-left-radius: inherit;
  border-top-right-radius: inherit;
}

.terminal-title {
  @apply text-sm font-medium;
}

.terminal-controls {
  @apply flex gap-1;
}

.control {
  @apply w-3 h-3 rounded-full bg-gray-300;
}

.control.close {
  @apply bg-red-500;
}

.control.minimize {
  @apply bg-yellow-500;
}

.control.maximize {
  @apply bg-green-500;
}

.text {
  @apply inline-block overflow-hidden whitespace-nowrap mt-4;
  border-right: 2px solid #4ade80;
  animation:
    typeAndDelete 4s steps(11) infinite,
    blinkCursor 0.5s step-end infinite alternate;
}

@keyframes blinkCursor {
  50% {
    border-right-color: transparent;
  }
}

@keyframes typeAndDelete {
  0%, 10% {
    width: 0;
  }
  45%, 55% {
    width: 6.2em;
  }
  90%, 100% {
    width: 0;
  }
}

/* 暗黑模式适配 */
.dark .terminal-loader {
  @apply bg-gray-900 border-gray-700;
}

.dark .terminal-header {
  @apply bg-gray-800;
}

.dark .terminal-title {
  @apply text-gray-300;
}

.dark .text {
  @apply text-green-400;
  border-right-color: #4ade80;
}
</style>
