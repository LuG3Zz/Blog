<template>
  <div class="clock-card">
    <div class="clock-header">
      <h3 class="clock-title">当前时间</h3>
      <p class="clock-date">{{ currentDate }}</p>
    </div>
    <div class="flip-clock">
      <div class="flip-unit-container">
        <div class="flip-unit" v-for="(digit, index) in digits" :key="index">
          <div class="top" :style="{ transform: digit.flipped ? 'rotateX(-180deg)' : 'rotateX(0)' }">
            <span>{{ digit.current }}</span>
          </div>
          <div class="bottom" :style="{ transform: digit.flipped ? 'rotateX(0)' : 'rotateX(180deg)' }">
            <span>{{ digit.next }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FlipClock',
  data() {
    return {
      digits: [],
      interval: null,
      currentDate: this.formatDate(new Date())
    }
  },
  mounted() {
    this.initDigits()
    this.startClock()
  },
  beforeUnmount() {
    if (this.interval) {
      clearInterval(this.interval)
    }
  },
  methods: {
    initDigits() {
      const now = new Date()
      const timeStr = this.formatTime(now)
      this.digits = timeStr.split('').map(num => ({
        current: num,
        next: num,
        flipped: false
      }))
    },
    formatTime(date) {
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      return `${hours}:${minutes}:${seconds}`
    },
    startClock() {
      this.interval = setInterval(() => {
        const now = new Date()
        const newTimeStr = this.formatTime(now)
        const newDigits = newTimeStr.split('')

        // 更新日期
        this.currentDate = this.formatDate(now)

        newDigits.forEach((newDigit, index) => {
          if (newDigit !== this.digits[index].current) {
            this.digits[index].next = newDigit
            this.digits[index].flipped = true

            setTimeout(() => {
              this.digits[index].current = newDigit
              this.digits[index].flipped = false
            }, 300)
          }
        })
      }, 1000)
    },
    formatDate(date) {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
      return date.toLocaleDateString('zh-CN', options)
    }
  }
}
</script>

<style scoped>
/* 卡片样式 */
.clock-card {
  background-color: #ffffff;
  background-image: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  width: 100%;
  margin: 0 auto;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  position: relative;
  border: 1px solid #e5e7eb;
}

/* 添加卡片装饰元素 */
.clock-card::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -50px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: rgba(59, 130, 246, 0.1);
  z-index: 0;
}

/* 暗黑模式卡片样式 */
:global(.dark) .clock-card {
  background-color: #1f2937;
  background-image: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  border-color: #374151;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2), 0 1px 3px rgba(0, 0, 0, 0.15);
}

:global(.dark) .clock-card::before {
  background-color: rgba(59, 130, 246, 0.15);
}

/* 卡片悬停效果 */
.clock-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
}

:global(.dark) .clock-card:hover {
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.25), 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* 卡片标题样式 */
.clock-header {
  margin-bottom: 1rem;
  text-align: center;
}

.clock-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.5rem 0;
}

:global(.dark) .clock-title {
  color: #e5e7eb;
}

.clock-date {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

:global(.dark) .clock-date {
  color: #9ca3af;
}

/* 翻页时钟样式 */
.flip-clock {
  display: flex;
  justify-content: center;
  font-family: 'SaansTRIAL-Medium', sans-serif;
  margin: 10px 0;
  width: 100%;
}

.flip-unit-container {
  display: flex;
  gap: 0.5%;
  width: 100%;
  max-width: 300px;
}

.flip-unit {
  position: relative;
  width: 15%;
  height: 0;
  padding-bottom: 25%;
  perspective: 600px;
}

.top, .bottom {
  position: absolute;
  width: 100%;
  height: 60%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #3b82f6; /* 蓝色背景 */
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
  backface-visibility: hidden;
}

:global(.dark) .top, :global(.dark) .bottom {
  background: #2563eb; /* 暗黑模式下的蓝色 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
}

.top span, .bottom span {
  font-size: clamp(1rem, 4vw, 1.75rem);
  font-weight: 600;
  color: #ffffff;
}
</style>
