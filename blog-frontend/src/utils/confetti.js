import confetti from 'canvas-confetti';

/**
 * 触发彩带效果
 * @param {Object} options - 配置选项
 * @param {number} options.duration - 彩带持续时间（毫秒）
 * @param {Array<string>} options.colors - 彩带颜色数组
 * @param {number} options.particleCount - 每次发射的彩带数量
 * @param {number} options.spread - 彩带扩散角度
 * @param {number} options.startVelocity - 彩带初始速度
 * @param {Object} options.origin - 彩带起始位置 {x, y}
 * @param {boolean} options.bothSides - 是否两侧同时发射彩带
 */
export function triggerConfetti(options = {}) {
  const {
    duration = 2000,
    colors = ['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082', '#EE82EE'],
    particleCount = 3,
    spread = 55,
    startVelocity = 60,
    origin = { x: 0.5, y: 0.5 },
    bothSides = true
  } = options;

  const end = Date.now() + duration;

  function frame() {
    if (Date.now() > end) return;

    if (bothSides) {
      // 左侧彩带
      confetti({
        particleCount,
        angle: 60,
        spread,
        startVelocity,
        origin: { x: 0, y: 0.5 },
        colors,
      });

      // 右侧彩带
      confetti({
        particleCount,
        angle: 120,
        spread,
        startVelocity,
        origin: { x: 1, y: 0.5 },
        colors,
      });
    } else {
      // 单点彩带
      confetti({
        particleCount,
        angle: 90,
        spread,
        startVelocity,
        origin,
        colors,
      });
    }

    requestAnimationFrame(frame);
  }

  frame();
}

/**
 * 预设的彩带效果 - 彩虹色
 */
export function triggerRainbowConfetti(duration = 2000) {
  const colors = [
    '#FF0000', // 红
    '#FFA500', // 橙
    '#FFFF00', // 黄
    '#008000', // 绿
    '#0000FF', // 蓝
    '#4B0082', // 青
    '#EE82EE'  // 紫
  ];

  triggerConfetti({ duration, colors });
}

/**
 * 预设的彩带效果 - 绿色系
 */
export function triggerGreenConfetti(duration = 2000) {
  const colors = [
    '#10b981', // 绿色
    '#059669',
    '#047857',
    '#065f46',
    '#064e3b',
    '#34d399',
    '#6ee7b7'
  ];

  triggerConfetti({ duration, colors });
}

/**
 * 预设的彩带效果 - 蓝色系
 */
export function triggerBlueConfetti(duration = 2000) {
  const colors = [
    '#3b82f6', // 蓝色
    '#2563eb',
    '#1d4ed8',
    '#1e40af',
    '#1e3a8a',
    '#60a5fa',
    '#93c5fd'
  ];

  triggerConfetti({ duration, colors });
}

export default {
  triggerConfetti,
  triggerRainbowConfetti,
  triggerGreenConfetti,
  triggerBlueConfetti
};
