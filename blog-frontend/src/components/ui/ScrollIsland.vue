<template>
  <MotionConfig
    :transition="{
      duration: 0.7,
      type: 'spring',
      bounce: 0.5,
    }"
  >
    <div
      :class="
        cn(
          'fixed left-1/2 top-12 z-[999] -translate-x-1/2 bg-primary/90 backdrop-blur-lg border-radius',
          $props.class,
        )
      "
      @click="() => (open = !open)"
    >
      <motion.div
        id="motion-id"
        layout
        :initial="{
          height: props.height,
          width: 0,
        }"
        :animate="{
          height: open && isSlotAvailable ? 'auto' : props.height,
          width: open && isSlotAvailable ? 320 : 180,
        }"
        class="bg-natural-900 relative cursor-pointer overflow-hidden text-secondary dark:text-dark-secondary"
      >
        <header class="flex cursor-pointer items-center" :class="{ 'h-9 gap-1 px-2': !open, 'h-11 gap-2 px-4': open }">
          <AnimatedCircularProgressBar
            :value="scrollPercentage * 100"
            :min="0"
            :max="100"
            :circle-stroke-width="10"
            :class="{ 'w-5': !open, 'w-6': open }"
            :show-percentage="false"
            :duration="0.3"
            :gauge-secondary-color="isDark ? '#6b728055' : '#6b728099'"
            :gauge-primary-color="isDark ? '#3b82f6' : '#3b82f6'"
          />
          <h1 class="grow text-center font-bold" :class="{ 'text-xs': !open, 'text-base': open }">{{ title }}</h1>
          <NumberFlow
            :value="scrollPercentage"
            :format="{ style: 'percent' }"
            locales="en-US"
            :class="{ 'text-xs': !open, 'text-sm': open }"
          />
        </header>
        <motion.div
          v-if="open"
          class="mb-2 flex h-full max-h-60 flex-col gap-1 overflow-y-auto px-4 text-sm"
        >
          <!-- 如果有传入标题列表，显示标题列表 -->
          <div v-if="headings && headings.length > 0" class="py-2">
            <!-- 调试信息 -->
             <div class="text-xs text-gray-400 mb-1 flex justify-between">
              <div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">目录</div>
            <div class="text-xs text-gray-400 mb-1 ">标题数量: {{ headings.length }}</div>
          </div>
            <ul class="space-y-1 max-h-48 overflow-y-auto pr-2 text-left">
              <li
                v-for="(heading, index) in headings"
                :key="index"
                @click.stop="scrollToHeading(heading.id)"
                class="py-1 px-2 rounded cursor-pointer transition-colors duration-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                :class="{
                  'pl-2': heading.level === 1,
                  'pl-4': heading.level === 2,
                  'pl-6': heading.level === 3,
                  'pl-8': heading.level === 4,
                  'pl-10': heading.level >= 5,
                  'font-medium': heading.level <= 2
                }"
              >
                <span class="line-clamp-1">{{ heading.text }}</span>
              </li>
            </ul>
          </div>
          <!-- 如果没有标题列表才显示插槽内容 -->
          <slot v-if="isSlotAvailable && (!headings || headings.length === 0)" />
        </motion.div>
      </motion.div>
    </div>
  </MotionConfig>
</template>

<script setup>
import { cn } from "@/lib/utils";
import NumberFlow from "@number-flow/vue";
import { useColorMode } from "@vueuse/core";
import { motion, MotionConfig } from "motion-v";
import { computed, onMounted, onUnmounted, ref, useSlots, watch } from "vue";
import AnimatedCircularProgressBar from "./AnimatedCircularProgressBar.vue";

const props = defineProps({
  class: {
    type: String,
    default: "",
  },
  title: {
    type: String,
    default: "Progress",
  },
  height: {
    type: Number,
    default: 36,
  },
  headings: {
    type: Array,
    default: () => [],
    required: false,
  },
});

const open = ref(false);
const slots = useSlots();

const scrollPercentage = ref(0);

// 检测暗色模式
const isDark = ref(false);
const checkDarkMode = () => {
  isDark.value = document.documentElement.classList.contains('dark');
};

const isSlotAvailable = computed(() => !!slots.default);
const borderRadius = computed(() => `${props.height / 2}px`);

onMounted(() => {
  if (typeof window === 'undefined') return;

  window.addEventListener("scroll", updatePageScroll);
  updatePageScroll();

  // 初始检查暗色模式
  checkDarkMode();

  // 设置 MutationObserver 监听 html 元素的类变化
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'class') {
        checkDarkMode();
      }
    });
  });

  observer.observe(document.documentElement, { attributes: true });

  // 输出标题列表，用于调试
  console.log('ScrollIsland 组件挂载，标题列表:', props.headings);
});

function updatePageScroll() {
  scrollPercentage.value = window.scrollY / (document.body.scrollHeight - window.innerHeight);
}

// 滚动到指定标题
function scrollToHeading(id) {
  if (!id) return;

  const element = document.getElementById(id);
  if (!element) {
    console.warn(`找不到ID为 ${id} 的元素`);
    return;
  }

  // 计算元素的位置
  const rect = element.getBoundingClientRect();
  const absoluteElementTop = rect.top + window.pageYOffset;

  // 计算偏移量，使标题位于页面中间位置
  const viewportHeight = window.innerHeight;
  const offset = viewportHeight * 0.2; // 视口高度的20%

  // 滚动到元素位置减去偏移量
  window.scrollTo({
    top: absoluteElementTop - offset,
    behavior: 'smooth'
  });

  // 添加高亮效果
  element.classList.add('highlight-heading');
  setTimeout(() => {
    if (document.body.contains(element)) {
      element.classList.remove('highlight-heading');
    }
  }, 2000);
}

// 监听标题列表变化
watch(() => props.headings, (newHeadings, oldHeadings) => {
  console.log('ScrollIsland 组件标题列表变化:', newHeadings);
  console.log('旧标题列表长度:', oldHeadings ? oldHeadings.length : 0);
  console.log('新标题列表长度:', newHeadings ? newHeadings.length : 0);
}, { deep: true });

onUnmounted(() => {
  window.removeEventListener("scroll", updatePageScroll);
});
</script>

<style scoped>
.border-radius {
  border-radius: v-bind(borderRadius);
}

/* 添加阴影和边框效果 */
.bg-primary\/90 {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 暗色模式下的样式调整 */
:global(.dark) .bg-primary\/90 {
  background-color: rgba(26, 26, 26, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

/* 标题列表样式 */
ul {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

ul::-webkit-scrollbar {
  width: 4px;
}

ul::-webkit-scrollbar-track {
  background: transparent;
}

ul::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 20px;
}

/* 高亮标题样式 */
:global(.highlight-heading) {
  animation: highlight-pulse 2s ease-in-out;
}

@keyframes highlight-pulse {
  0% {
    background-color: rgba(59, 130, 246, 0);
  }
  30% {
    background-color: rgba(59, 130, 246, 0.2);
  }
  100% {
    background-color: rgba(59, 130, 246, 0);
  }
}
</style>
