import { ref } from 'vue'
import { useRouter } from 'vue-router'
import message from '@/utils/message'
import confetti from 'canvas-confetti'

/**
 * 处理文章点赞功能
 * @param {Object} options 配置选项
 * @returns {Object} 包含点赞相关方法和状态的对象
 */
export function useArticleLike(options = {}) {
  const { postApi, isComponentMounted } = options
  const router = useRouter()
  const isLiked = ref(false)
  const rafIds = []

  /**
   * 获取点赞状态
   * @param {Number} postId 文章ID
   */
  const fetchLikeStatus = async (postId) => {
    if (!isComponentMounted.value) return

    const token = localStorage.getItem('token')
    if (!token || !postId) return

    try {
      const response = await postApi.getLikeStatus(postId)
      if (!isComponentMounted.value) return
      isLiked.value = response.is_liked
    } catch (error) {
      console.error('获取点赞状态失败:', error)
    }
  }

  /**
   * 处理点赞
   * @param {Object} post 文章对象
   */
  const handleLike = async (post) => {
    if (!isComponentMounted.value) return

    const token = localStorage.getItem('token')
    if (!token) {
      message.warning('请先登录后再点赞')
      router.push('/login')
      return
    }

    try {
      await postApi.likePost(post.id)
      if (!isComponentMounted.value) return

      const wasLiked = isLiked.value
      isLiked.value = !wasLiked
      post.like_count += isLiked.value ? 1 : -1
      message.success(isLiked.value ? '点赞成功' : '已取消点赞')

      // 如果是点赞操作（不是取消点赞），触发彩带效果
      if (isLiked.value) {
        triggerConfetti()
      }
    } catch (error) {
      console.error('点赞失败:', error)
      message.error('点赞失败，请稍后重试')
    }
  }

  /**
   * 触发彩带效果
   */
  const triggerConfetti = () => {
    const end = Date.now() + 2 * 1000; // 2秒
    const colors = ['#ff0000', '#ff4d94', '#ff9999', '#ffcccc']; // 红色系列

    // 帧函数，触发彩带炮
    function frame() {
      if (Date.now() > end || !isComponentMounted.value) {
        return;
      }

      // 左侧彩带炮
      confetti({
        particleCount: 2,
        angle: 60,
        spread: 55,
        startVelocity: 60,
        origin: { x: 0, y: 0.5 },
        colors: colors,
      });

      // 右侧彩带炮
      confetti({
        particleCount: 2,
        angle: 120,
        spread: 55,
        startVelocity: 60,
        origin: { x: 1, y: 0.5 },
        colors: colors,
      });

      // 继续调用帧函数
      const rafId = requestAnimationFrame(frame);
      if (rafId) {
        rafIds.push(rafId);
      }
    }

    // 开始动画
    const rafId = requestAnimationFrame(frame);
    if (rafId) {
      rafIds.push(rafId);
    }
  }

  /**
   * 清理资源
   */
  const cleanup = () => {
    // 清理所有 requestAnimationFrame
    rafIds.forEach(id => {
      cancelAnimationFrame(id)
    })
  }

  return {
    isLiked,
    fetchLikeStatus,
    handleLike,
    cleanup
  }
}
