<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :default-active="activeMenu"
          router
          class="admin-menu"
        >
          <el-menu-item index="/admin">
            <el-icon><Dashboard /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/articles">
            <el-icon><Document /></el-icon>
            <span>文章管理</span>
          </el-menu-item>
          
          <!-- 添加文件管理菜单项 -->
          <el-menu-item index="/admin/files">
            <el-icon><Folder /></el-icon>
            <span>文件管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/categories">
            <el-icon><Collection /></el-icon>
            <span>分类管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/tags">
            <el-icon><PriceTag /></el-icon>
            <span>标签管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/comments">
            <el-icon><ChatLineRound /></el-icon>
            <span>评论管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  Document,
  Folder,
  Collection,
  PriceTag,
  ChatLineRound,
  User,
  Dashboard
} from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.admin-menu {
  height: 100%;
  border-right: solid 1px var(--el-border-color);
}

.el-aside {
  background-color: var(--el-menu-bg-color);
}

.el-main {
  padding: 20px;
}
</style>