import { createVNode, render } from 'vue'
import MessageComponent from '../components/ui/Message.vue'

let messageInstance = null

// 创建消息实例
const createMessage = () => {
  if (messageInstance) return messageInstance

  // 创建一个div容器
  const container = document.createElement('div')

  // 创建VNode
  const vnode = createVNode(MessageComponent)

  // 渲染VNode
  render(vnode, container)

  // 将容器添加到body
  document.body.appendChild(container)

  messageInstance = vnode.component.exposed
  return messageInstance
}

// 消息类型方法
const message = {
  info(text, duration) {
    const instance = createMessage()
    instance.show(text, 'info', duration)
  },
  success(text, duration) {
    const instance = createMessage()
    instance.show(text, 'success', duration)
  },
  warning(text, duration) {
    const instance = createMessage()
    instance.show(text, 'warning', duration)
  },
  error(text, duration) {
    const instance = createMessage()
    instance.show(text, 'error', duration)
  }
}

export default message