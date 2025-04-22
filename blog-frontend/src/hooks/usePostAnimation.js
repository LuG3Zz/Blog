/**
 * 文章列表动画效果的可复用逻辑
 * 封装了鼠标悬停、图片预览等动画效果
 */

export function usePostAnimation() {
  // 动画相关常量
  const POSITIONS = {
    BOTTOM: 0,
    MIDDLE: -80,
    TOP: -160
  }

  // 状态变量
  let lastMousePosition = { x: 0, y: 0 }
  let activePost = null
  let ticking = false
  let mouseTimeout = null
  let isMouseMoving = false
  
  /**
   * 为文章元素添加鼠标事件监听
   * @param {Array} postsElements - 文章DOM元素列表
   * @param {HTMLElement} postPreviewElement - 图片预览容器元素
   */
  const addPostsEventListeners = (postsElements, postPreviewElement) => {
    postsElements.forEach((post, index) => {
      const wrapper = post.querySelector('.post-wrapper')
      let currentPosition = POSITIONS.TOP
      
      post.addEventListener('mouseenter', (e) => {
        activePost = post
        const rect = post.getBoundingClientRect()
        const enterFromTop = lastMousePosition.y < rect.top + rect.height / 2
        
        if (enterFromTop || currentPosition === POSITIONS.BOTTOM) {
          currentPosition = POSITIONS.MIDDLE
          gsap.to(wrapper, {
            y: POSITIONS.MIDDLE,
            duration: 0.4,
            ease: 'power2.out'
          })
        }
        
        const img = document.createElement('img')
        const imagePath = post.dataset.coverImage || `./images/img${(index % 35) + 1}.jpg`;
        img.src = imagePath; // 优先使用封面图，若无则使用默认图片
        img.style.position = 'absolute'
        img.style.top = '0'
        img.style.left = '0'
        img.style.scale = 0
        img.style.zIndex = Date.now()
        
        postPreviewElement.appendChild(img)
        
        gsap.to(img, {
          scale: 1,
          duration: 0.4,
          ease: 'power2.out'
        })
      })
      
      post.addEventListener('mouseleave', (e) => {
        activePost = null
        const rect = post.getBoundingClientRect()
        const leavingFromTop = e.clientY < rect.top + rect.height / 2
        
        currentPosition = leavingFromTop ? POSITIONS.TOP : POSITIONS.BOTTOM
        gsap.to(wrapper, {
          y: currentPosition,
          duration: 0.4,
          ease: 'power2.out'
        })
      })
    })
  }
  
  /**
   * 动画预览函数 - 处理鼠标移出文章列表区域时的图片预览效果
   * @param {HTMLElement} postsListElement - 文章列表容器元素
   * @param {HTMLElement} postPreviewElement - 图片预览容器元素
   */
  const animatePreview = (postsListElement, postPreviewElement) => {
    if (!postsListElement) return
    
    const postsListRect = postsListElement.getBoundingClientRect()
    if (
      lastMousePosition.x < postsListRect.left ||
      lastMousePosition.x > postsListRect.right ||
      lastMousePosition.y < postsListRect.top ||
      lastMousePosition.y > postsListRect.bottom
    ) {
      const previewImages = postPreviewElement.querySelectorAll('img')
      previewImages.forEach(img => {
        gsap.to(img, {
          scale: 0,
          duration: 0.4,
          ease: 'power2.out',
          onComplete: () => img.remove()
        })
      })
    }
  }

  /**
   * 更新文章列表动画 - 处理滚动和鼠标移动时的动画效果
   * @param {HTMLElement} postsListElement - 文章列表容器元素
   * @param {HTMLElement} postPreviewElement - 图片预览容器元素
   * @param {Array} postsElements - 文章DOM元素列表
   */
  const updatePosts = (postsListElement, postPreviewElement, postsElements) => {
    animatePreview(postsListElement, postPreviewElement);

    if (activePost) {
      const rect = activePost.getBoundingClientRect()
      const isStillOver = 
        lastMousePosition.x >= rect.left &&
        lastMousePosition.x <= rect.right &&
        lastMousePosition.y >= rect.top &&
        lastMousePosition.y <= rect.bottom

      if (!isStillOver) {
        const wrapper = activePost.querySelector('.post-wrapper')
        const leavingFronTop = lastMousePosition.y < rect.top + rect.height / 2

        gsap.to(wrapper, {
          y: leavingFronTop ? POSITIONS.TOP : POSITIONS.BOTTOM,
          duration: 0.4,
          ease: 'power2.out'
        })
        activePost = null
      }
    }

    postsElements.forEach((post, index) => {
      if (post === activePost) return

      const rect = post.getBoundingClientRect()
      const isMouseOver =
        lastMousePosition.x >= rect.left &&
        lastMousePosition.x <= rect.right &&
        lastMousePosition.y >= rect.top &&
        lastMousePosition.y <= rect.bottom

        if (isMouseOver) {
          const wrapper = post.querySelector('.post-wrapper')
          const enterFromTop = lastMousePosition.y < rect.top + rect.height / 2

          gsap.to(wrapper, {
            y: POSITIONS.MIDDLE,
            duration: 0.4,
            ease: 'power2.out'
          })
          activePost = post
        }
    })

    ticking = false
  }
  
  /**
   * 设置鼠标移动事件监听
   * @param {HTMLElement} postsListElement - 文章列表容器元素
   * @param {HTMLElement} postPreviewElement - 图片预览容器元素
   */
  const setupMouseMoveListener = (postsListElement, postPreviewElement) => {
    document.addEventListener('mousemove', (e) => {
      lastMousePosition.x = e.clientX
      lastMousePosition.y = e.clientY

      isMouseMoving = true
      if (mouseTimeout) {
        clearTimeout(mouseTimeout)
      }

      if (!postsListElement) return
      
      const postsListRect = postsListElement.getBoundingClientRect()
      const isInsidePostsList = 
        lastMousePosition.x >= postsListRect.left &&
        lastMousePosition.x <= postsListRect.right &&
        lastMousePosition.y >= postsListRect.top &&
        lastMousePosition.y <= postsListRect.bottom

        if (isInsidePostsList) {
          mouseTimeout = setTimeout(() => {
            isMouseMoving = false
            const images = postPreviewElement.querySelectorAll('img')
            if (images.length > 1) {
              const lastImage = images[images.length - 1]
              images.forEach(img => {
                if (img !== lastImage) {
                  gsap.to(img, {
                    scale: 0,
                    duration: 0.4,
                    ease: 'power2.out',
                    onComplete: () => img.remove()
                  })
                }
              })
            }
          }, 2000)
        }

        animatePreview(postsListElement, postPreviewElement)
    })
  }
  
  /**
   * 设置滚动事件监听
   * @param {HTMLElement} postsListElement - 文章列表容器元素
   * @param {HTMLElement} postPreviewElement - 图片预览容器元素
   * @param {Array} postsElements - 文章DOM元素列表
   */
  const setupScrollListener = (postsListElement, postPreviewElement, postsElements) => {
    document.addEventListener(
      'scroll',
      () => {
        if (!ticking) {
          requestAnimationFrame(() => {
            updatePosts(postsListElement, postPreviewElement, postsElements)
          })
          ticking = true
        }
      }, 
      {passive: true}
    )
  }

  return {
    POSITIONS,
    addPostsEventListeners,
    animatePreview,
    updatePosts,
    setupMouseMoveListener,
    setupScrollListener
  }
}
