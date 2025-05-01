<template>
  <div :class="cn('group h-full w-full [perspective:1000px]', props.class)">
    <div
      :class="
        cn(
          'relative h-full rounded-2xl transition-all duration-700 [transform-style:preserve-3d]',
          rotation[0],
        )
      "
    >
      <!-- Front -->
      <div
        class="absolute w-full h-full overflow-hidden rounded-2xl border [backface-visibility:hidden]"
      >
        <slot />
      </div>

      <!-- Back -->
      <div
        :class="
          cn(
            'absolute h-full w-full overflow-hidden rounded-2xl border bg-white shadow-md dark:bg-gradient-to-br dark:from-gray-900 dark:to-gray-800 p-4 text-gray-800 dark:text-slate-200 [backface-visibility:hidden]',
            rotation[1],
          )
        "
      >
        <slot name="back" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { cn } from "@/lib/utils";
import { computed } from "vue";

interface FlipCardProps {
  rotate?: "x" | "y";
  class?: string;
}

const props = withDefaults(defineProps<FlipCardProps>(), {
  rotate: "y",
});
const rotationClass = {
  x: ["group-hover:[transform:rotateX(180deg)]", "[transform:rotateX(180deg)]"],
  y: ["group-hover:[transform:rotateY(180deg)]", "[transform:rotateY(180deg)]"],
};

const rotation = computed(() => rotationClass[props.rotate]);
</script>
