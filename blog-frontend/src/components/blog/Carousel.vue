<template>
  <div class="carousel-container w-full relative dark:bg-gray-800 dark:border-gray-700">
    <div class="carousel-header mb-4">
      <h2 class="text-xl font-bold text-gray-800 dark:text-white mb-1">精选推荐</h2>
      <p class="text-sm text-gray-600 dark:text-gray-400">探索我们的精选内容</p>
    </div>

    <div class="carousel-wrapper relative overflow-hidden">
      <div
        class="carousel-slides flex transition-transform duration-500 ease-in-out"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <div
          v-for="(slide, index) in slides"
          :key="index"
          class="carousel-slide w-full flex-shrink-0 relative"
        >
          <img
            :src="slide.image"
            :alt="slide.title"
            class="w-full h-64 object-cover"
          />
          <div class="slide-content absolute bottom-0 left-0 w-full p-4 bg-black bg-opacity-50 text-white">
            <h3 class="text-lg font-bold">{{ slide.title }}</h3>
            <p class="text-sm">{{ slide.description }}</p>
            <router-link
              v-if="slide.id || slide.slug"
              :to="slide.slug ? `/article/${slide.id}`:`/articles/by-slug/${slide.slug}`  "
              class="mt-2 inline-block px-1 py-1 bg-secondary text-white text-sm rounded hover:bg-opacity-90 transition-colors"
            >
              阅读全文
            </router-link>
          </div>
        </div>
      </div>

      <button
        @click="prevSlide"
        class="carousel-control left-2 absolute top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white rounded-full"
        aria-label="Previous slide"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <button
        @click="nextSlide"
        class="carousel-control right-2 absolute top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white rounded-full"
        aria-label="Next slide"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <div class="carousel-indicators flex justify-center mt-4">
        <button
          v-for="(_, index) in slides"
          :key="index"
          @click="goToSlide(index)"
          class="indicator-dot w-2 h-2 mx-1 rounded-full transition-all duration-300 ease-in-out"
          :class="{
            'bg-blue-500 w-3 h-3': currentIndex === index,
            'bg-gray-300 dark:bg-gray-600': currentIndex !== index
          }"
          :aria-label="`Go to slide ${index + 1}`"
        ></button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'Carousel',
  props: {
    featuredPosts: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    // 处理传入的文章数据，转换为轮播图所需的格式
    const processPostData = (posts) => {
      if (!posts || posts.length === 0) return [];

      return posts.map(post => ({
        title: post.title || '无标题',
        description: post.excerpt || post.summary || '无描述',
        image: post.cover_image || `/images/img${Math.floor(Math.random() * 35) + 1}.jpg`,
        id: post.id,
        slug: post.slug
      }));
    };

    // 如果有传入featuredPosts，则使用传入的数据，否则使用默认数据
    const slides = ref(props.featuredPosts.length > 0 ? processPostData(props.featuredPosts) : [
      {
        title: '独立开发者年度奖',
        description: '创新2024 - 提名作品展示',
        image: '/images/img1.jpg'
      },
      {
        title: '每日精选网站',
        description: 'LVXH - AMOT项目设计奖项',
        image: '/images/img5.jpg'
      },
      {
        title: '音频领域的突破',
        description: 'Open Field Audio技术解析',
        image: '/images/img10.jpg'
      },
      {
        title: '手工艺术的数字化',
        description: 'ArtisanCraft案例研究',
        image: '/images/img15.jpg'
      },
      {
        title: '隐藏的设计边界',
        description: 'Disguised Edge探索',
        image: '/images/img20.jpg'
      }
    ])

    const currentIndex = ref(0)
    let autoplayInterval = null

    // 切换到下一张幻灯片
    const nextSlide = () => {
      currentIndex.value = (currentIndex.value + 1) % slides.value.length
    }

    // 切换到上一张幻灯片
    const prevSlide = () => {
      currentIndex.value = (currentIndex.value - 1 + slides.value.length) % slides.value.length
    }

    // 切换到指定幻灯片
    const goToSlide = (index) => {
      currentIndex.value = index
    }

    // 启动自动播放
    const startAutoplay = () => {
      autoplayInterval = setInterval(() => {
        nextSlide()
      }, 5000) // 每5秒切换一次
    }

    // 停止自动播放
    const stopAutoplay = () => {
      if (autoplayInterval) {
        clearInterval(autoplayInterval)
      }
    }

    // 组件挂载时启动自动播放
    onMounted(() => {
      startAutoplay()
    })

    // 组件卸载时清除定时器
    onUnmounted(() => {
      stopAutoplay()
    })

    return {
      slides,
      currentIndex,
      nextSlide,
      prevSlide,
      goToSlide
    }
  }
}
</script>

<style scoped>
.carousel-header {
  text-align: center;
  position: relative;
  z-index: 10;
}

.carousel-container {
  position: relative;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.dark .carousel-container {
  background-color: #1f2937;
  border-color: #374151;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
}

.carousel-wrapper {
  position: relative;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
}

.carousel-slide {
  height: 300px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin: 0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: filter 0.3s ease;
}

.carousel-slide:hover img {
  filter: brightness(1.05);
}

.slide-content {
  position: absolute;
  font-size: medium;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  z-index: 2;
}

.carousel-control {
  z-index: 3;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s ease, background-color 0.3s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-control:hover {
  opacity: 1;
  background-color: rgba(0, 0, 0, 0.7);
}

.indicator-dot {
  transition: background-color 0.3s ease;
}
</style>
