<template>
  <div
    :class="
      cn(
        'relative mx-auto min-h-fit w-full max-w-[400px] overflow-hidden rounded-2xl p-4',
        // animation styles
        'transition-all duration-200 ease-in-out hover:scale-[103%]',
        // light styles
        'bg-white [box-shadow:0_0_0_1px_rgba(0,0,0,.03),0_2px_4px_rgba(0,0,0,.05),0_12px_24px_rgba(0,0,0,.05)]',
        // dark styles
        'transform-gpu dark:bg-transparent dark:backdrop-blur-md dark:[border:1px_solid_rgba(255,255,255,.1)] dark:[box-shadow:0_-20px_80px_-20px_#ffffff1f_inset]',
      )
    "
  >
    <!-- 关闭按钮 -->
    <button
      class="absolute top-2 right-2 w-6 h-6 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors z-30"
      @click.stop="$emit('close')"
    >
      <span class="text-gray-500 dark:text-gray-400 text-xs">&times;</span>
    </button>

    <div class="grid grid-cols-[40px_1fr] gap-3 items-center cursor-pointer" @click="$emit('click')">
      <!-- 头像或图标 -->
      <div class="w-10 h-10 relative z-10">
        <div
          v-if="avatar"
          class="w-10 h-10 flex items-center justify-center rounded-full overflow-hidden bg-gray-100 absolute top-0 left-0"
        >
          <img
            :src="avatar"
            :alt="name"
            class="w-full h-full object-cover"
            @error="onAvatarError"
          />
        </div>
        <div
          v-else-if="firstLetter"
          class="w-10 h-10 flex items-center justify-center rounded-full absolute top-0 left-0 text-white font-medium"
          :style="`background-color: ${color}`"
        >
          <span class="text-lg">{{ firstLetter }}</span>
        </div>
        <div
          v-else
          class="w-10 h-10 flex items-center justify-center rounded-2xl absolute top-0 left-0"
          :style="`background-color: ${color}`"
        >
          <span class="text-lg">{{ icon }}</span>
        </div>
      </div>

      <!-- 内容 -->
      <div class="min-w-0 z-20">
        <div class="flex flex-row items-center text-lg font-medium dark:text-white">
          <span class="text-sm sm:text-lg truncate max-w-[150px]">{{ name }}</span>
          <span class="mx-1 flex-shrink-0">·</span>
          <span class="text-xs text-gray-500 flex-shrink-0">{{ time }}</span>
        </div>
        <p class="text-sm font-normal dark:text-white/60 truncate">{{ description }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
// 工具函数
function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}

// 默认头像
const DEFAULT_AVATAR = '/assets/default-avatar.png';

type NotificationProps = {
  name: string;
  description: string;
  time: string;
  icon: string;
  color: string;
  avatar?: string | null;
  firstLetter?: string;
};

withDefaults(defineProps<NotificationProps>(), {
  name: "",
  description: "",
  time: "",
  icon: "",
  color: "",
  avatar: null,
  firstLetter: undefined,
});

// 头像错误处理
const onAvatarError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  console.log('头像加载失败:', target.src);
  // 如果头像加载失败，使用默认头像
  target.src = DEFAULT_AVATAR;
};
</script>
