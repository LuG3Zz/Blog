<template>
  <button
    :class="
      cn(
        'relative flex items-center justify-center overflow-hidden rainbow-btn',
        props.class,
      )
    "
    :style="{
      minWidth: '7rem',
      minHeight: '2.5rem',
    }"
  >
    <span
      class="btn-content inline-flex items-center justify-center px-4 py-2 font-medium"
      :style="{
        width: '100%',
        height: '100%',
        color: props.textColor
      }"
    >
      <slot />
    </span>
  </button>
</template>

<script lang="ts" setup>
import { cn } from "@/lib/utils";
import { computed } from "vue";

interface GradientButtonProps {
  borderWidth?: number;
  colors?: string[];
  duration?: number;
  borderRadius?: number;
  blur?: number;
  class?: string;
  bgColor?: string;
  textColor?: string;
}

const props = withDefaults(defineProps<GradientButtonProps>(), {
  colors: () => [
    "#FF0000",
    "#FFA500",
    "#FFFF00",
    "#008000",
    "#0000FF",
    "#4B0082",
    "#EE82EE",
    "#FF0000",
  ],
  duration: 2500,
  borderWidth: 2,
  borderRadius: 8,
  blur: 4,
  bgColor: "#000",
  textColor: "#fff",
});

const durationInMilliseconds = computed(() => `${props.duration}ms`);
const allColors = computed(() => props.colors.join(", "));
const borderWidthInPx = computed(() => `${props.borderWidth}px`);
const borderRadiusInPx = computed(() => `${props.borderRadius}px`);
const blurPx = computed(() => `${props.blur}px`);
</script>

<style scoped>
.rainbow-btn {
  padding: v-bind(borderWidthInPx);
  border-radius: v-bind(borderRadiusInPx);
  position: relative;
}

.rainbow-btn::before {
  content: "";
  position: absolute;
  top: -200%;
  left: -200%;
  right: -200%;
  bottom: -200%;
  background: conic-gradient(v-bind(allColors));
  animation: rotate-rainbow v-bind(durationInMilliseconds) linear infinite;
  filter: blur(v-bind(blurPx));
}

.btn-content {
  border-radius: v-bind(borderRadiusInPx);
  background-color: v-bind(bgColor);
  position: relative;
  z-index: 1;
}

@keyframes rotate-rainbow {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
