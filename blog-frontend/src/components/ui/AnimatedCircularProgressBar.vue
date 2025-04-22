<template>
  <div class="relative" :class="$props.class">
    <svg viewBox="0 0 100 100" class="w-full h-full">
      <!-- Background circle -->
      <circle
        cx="50"
        cy="50"
        r="45"
        fill="none"
        :stroke="gaugeSecondaryColor"
        :stroke-width="circleStrokeWidth"
      />
      <!-- Progress circle -->
      <circle
        ref="progressCircle"
        cx="50"
        cy="50"
        r="45"
        fill="none"
        :stroke="gaugePrimaryColor"
        :stroke-width="circleStrokeWidth"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        transform="rotate(-90 50 50)"
      />
      <!-- Percentage text -->
      <text
        v-if="showPercentage"
        x="50"
        y="55"
        text-anchor="middle"
        font-size="20"
        font-weight="bold"
        :fill="gaugePrimaryColor"
      >
        {{ Math.round(animatedValue) }}%
      </text>
    </svg>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';

const props = defineProps({
  value: {
    type: Number,
    required: true
  },
  min: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 100
  },
  circleStrokeWidth: {
    type: Number,
    default: 8
  },
  showPercentage: {
    type: Boolean,
    default: true
  },
  duration: {
    type: Number,
    default: 1
  },
  gaugePrimaryColor: {
    type: String,
    default: 'white'
  },
  gaugeSecondaryColor: {
    type: String,
    default: 'rgba(255, 255, 255, 0.2)'
  },
  class: {
    type: String,
    default: ''
  }
});

const progressCircle = ref(null);
const animatedValue = ref(0);

const circumference = computed(() => 2 * Math.PI * 45);
const normalizedValue = computed(() => {
  return ((props.value - props.min) / (props.max - props.min)) * 100;
});

const dashOffset = computed(() => {
  return circumference.value * (1 - animatedValue.value / 100);
});

// Animation function
const animateValue = (start, end, duration) => {
  const startTime = performance.now();

  const updateValue = (currentTime) => {
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);

    animatedValue.value = start + progress * (end - start);

    if (progress < 1) {
      requestAnimationFrame(updateValue);
    }
  };

  requestAnimationFrame(updateValue);
};

// Watch for value changes and animate
watch(() => props.value, () => {
  const start = animatedValue.value;
  const end = normalizedValue.value;
  animateValue(start, end, props.duration * 1000);
}, { immediate: false });

// Initialize on mount
onMounted(() => {
  animateValue(0, normalizedValue.value, props.duration * 1000);
});
</script>

<style scoped>
circle {
  transition: stroke-dashoffset 0.3s ease;
}
</style>
