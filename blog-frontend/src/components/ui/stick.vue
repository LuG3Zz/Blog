<style scoped>
  .container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }

  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: fixed !important;
    bottom: 40px !important;
    right: 40px !important;
    cursor: pointer;
    user-select: none;
    z-index: 99999 !important; /* 增加z-index确保在最上层 */
    transform: scale(0.8);
    transition: transform 0.3s ease, filter 0.3s ease;
    pointer-events: auto !important;
    width: 60px; /* 添加固定宽度 */
    height: 150px; /* 添加固定高度 */
  }

  .container:hover {
    transform: scale(0.9);
    filter: drop-shadow(0 0 10px rgba(255, 200, 0, 0.5));
  }

  .simple-text {
    position: absolute;
    bottom: -10px;
    width: 80px;
    text-align: center;
    color: #333;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    
    font-size: 10pt;
    font-weight: 700;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
    border: 1px solid rgba(0, 0, 0, 0.1);
  }

  .container:hover .simple-text {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }

  /* 暗黑模式下的文本样式 */
  html.dark .simple-text {
    color: #f0f0f0;
    background-color: rgba(30, 30, 30, 0.9);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  /* 添加颜色指示器 */
  .simple-text::before {
    content: '';
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 5px;
    background-color: #ffd700;
    box-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
  }

  html.dark .simple-text::before {
    background-color: #3b82f6;
    box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
  }

  .torch {
    display: flex;
    justify-content: center;
    height: 150px;
  }

  .head,
  .stick {
    position: absolute;
    width: 30px;
    transform-style: preserve-3d;
    transform: rotateX(-30deg) rotateY(45deg);
  }

  .stick {
    position: relative;
    height: 120px;
  }

  .face {
    position: absolute;
    transform-style: preserve-3d;
    width: 30px;
    height: 30px;
    display: grid;
    grid-template-columns: 50% 50%;
    grid-template-rows: 50% 50%;
    background-color: #000000;
  }

  .top {
    transform: rotateX(90deg) translateZ(15px);
  }

  .left {
    transform: rotateY(-90deg) translateZ(15px);
  }

  .right {
    transform: rotateY(0deg) translateZ(15px);
  }

  .top div,
  .left div,
  .right div {
    width: 102%;
    height: 102%;
  }

  .top div:nth-child(1),
  .left div:nth-child(3),
  .right div:nth-child(3) {
    background-color: #ffff9760;
  }

  .top div:nth-child(2),
  .left div:nth-child(1),
  .right div:nth-child(1) {
    background-color: #ffd80060;
  }

  .top div:nth-child(3),
  .left div:nth-child(4),
  .right div:nth-child(4) {
    background-color: #ffffff60;
  }

  .top div:nth-child(4),
  .left div:nth-child(2),
  .right div:nth-child(2) {
    background-color: #ff8f0060;
  }

  .side {
    position: absolute;
    width: 30px;
    height: 120px;
    display: grid;
    grid-template-columns: 50% 50%;
    grid-template-rows: repeat(8, 12.5%);
    cursor: pointer;
    translate: 0 12px;
  }

  .side-left {
    transform: rotateY(-90deg) translateZ(15px) translateY(8px);
  }

  .side-right {
    transform: rotateY(0deg) translateZ(15px) translateY(8px);
  }

  .side-left div,
  .side-right div {
    width: 103%;
    height: 103%;
  }

  .side div:nth-child(1) {
    background-color: #443622;
  }

  .side div:nth-child(2),
  .side div:nth-child(2) {
    background-color: #2e2517;
  }

  .side div:nth-child(3),
  .side div:nth-child(5) {
    background-color: #4b3b23;
  }

  .side div:nth-child(4),
  .side div:nth-child(10) {
    background-color: #251e12;
  }

  .side div:nth-child(6) {
    background-color: #292115;
  }

  .side div:nth-child(7) {
    background-color: #4b3c26;
  }

  .side div:nth-child(8) {
    background-color: #292115;
  }

  .side div:nth-child(9) {
    background-color: #4b3a21;
  }

  .side div:nth-child(11),
  .side div:nth-child(15) {
    background-color: #3d311d;
  }

  .side div:nth-child(12) {
    background-color: #2c2315;
  }

  .side div:nth-child(13) {
    background-color: #493a22;
  }

  .side div:nth-child(14) {
    background-color: #2b2114;
  }

  .side div:nth-child(16) {
    background-color: #271e10;
  }

  .container input:checked ~ .torch .face {
    filter: drop-shadow(0px 0px 2px rgb(255, 255, 255))
      drop-shadow(0px 0px 10px rgba(255, 237, 156, 0.7))
      drop-shadow(0px 0px 25px rgba(255, 227, 101, 0.4));
  }

  .container input:checked ~ .torch .top div:nth-child(1),
  .container input:checked ~ .torch .left div:nth-child(3),
  .container input:checked ~ .torch .right div:nth-child(3) {
    background-color: #ffff97;
  }

  .container input:checked ~ .torch .top div:nth-child(2),
  .container input:checked ~ .torch .left div:nth-child(1),
  .container input:checked ~ .torch .right div:nth-child(1) {
    background-color: #ffd800;
  }

  .container input:checked ~ .torch .top div:nth-child(3),
  .container input:checked ~ .torch .left div:nth-child(4),
  .container input:checked ~ .torch .right div:nth-child(4) {
    background-color: #ffffff;
  }

  .container input:checked ~ .torch .top div:nth-child(4),
  .container input:checked ~ .torch .left div:nth-child(2),
  .container input:checked ~ .torch .right div:nth-child(2) {
    background-color: #ff8f00;
  }

  .container input:checked ~ .torch .side div:nth-child(1) {
    background-color: #7c623e;
  }

  .container input:checked ~ .torch .side div:nth-child(2),
  .container input:checked ~ .torch .side div:nth-child(2) {
    background-color: #4c3d26;
  }

  .container input:checked ~ .torch .side div:nth-child(3),
  .container input:checked ~ .torch .side div:nth-child(5) {
    background-color: #937344;
  }

  .container input:checked ~ .torch .side div:nth-child(4),
  .container input:checked ~ .torch .side div:nth-child(10) {
    background-color: #3c2f1c;
  }

  .container input:checked ~ .torch .side div:nth-child(6) {
    background-color: #423522;
  }

  .container input:checked ~ .torch .side div:nth-child(7) {
    background-color: #9f7f50;
  }

  .container input:checked ~ .torch .side div:nth-child(8) {
    background-color: #403320;
  }

  .container input:checked ~ .torch .side div:nth-child(9) {
    background-color: #977748;
  }

  .container input:checked ~ .torch .side div:nth-child(11),
  .container input:checked ~ .torch .side div:nth-child(15) {
    background-color: #675231;
  }

  .container input:checked ~ .torch .side div:nth-child(12) {
    background-color: #3d301d;
  }

  .container input:checked ~ .torch .side div:nth-child(13) {
    background-color: #987849;
  }

  .container input:checked ~ .torch .side div:nth-child(14) {
    background-color: #3b2e1b;
  }

  .container input:checked ~ .torch .side div:nth-child(16) {
    background-color: #372a17;
  }
</style>

<script setup>
import { onMounted, computed } from 'vue';
import { useThemeStore } from '@/stores';

// 定义 props
const props = defineProps({
  initialDarkMode: {
    type: Boolean,
    default: false
  }
});

// 定义事件
const emit = defineEmits(['update:darkMode']);

// 获取主题状态管理实例
const themeStore = useThemeStore();

// 使用全局主题状态
const isDarkMode = computed(() => themeStore.isDark);

// 切换暗黑模式
const toggleDarkMode = () => {
  console.log('切换暗黑模式，当前状态:', isDarkMode.value);
  themeStore.toggleTheme();
  console.log('切换后状态:', isDarkMode.value);
  // 发出事件，保持兼容性
  emit('update:darkMode', isDarkMode.value);
};

// 组件挂载时初始化主题
onMounted(() => {
  // 确保主题已经初始化
  if (typeof themeStore.initTheme === 'function') {
    themeStore.initTheme();
  }
});
</script>

<template>
  <div class="container" @click.stop.prevent="toggleDarkMode">
    <div class="simple-text">{{ isDarkMode ? '亮色' : '暗色' }}</div>
    <input :checked="isDarkMode" type="checkbox" />
    <div class="checkmark"></div>
    <div class="torch">
      <div class="head">
        <div class="face top">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div class="face left">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div class="face right">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
      </div>
      <div class="stick">
        <div class="side side-left">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div class="side side-right">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
      </div>
    </div>
  </div>
</template>
