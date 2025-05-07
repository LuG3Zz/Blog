<template>
  <div class="min-h-screen bg-primary dark:bg-dark-primary animate__animated animate__fadeIn">
    <div class="container mx-auto px-4 py-8 animate__animated animate__fadeInUp animate__delay-1s">
      <div class="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden animate__animated animate__zoomIn animate__delay-500ms">
        <!-- 用户资料头部 -->
        <div class="relative">
          <!-- 封面图 -->
          <div class="h-56 bg-gradient-to-r from-blue-500 to-purple-600 relative overflow-hidden animate__animated animate__fadeIn animate__delay-700ms">
            <div class="absolute inset-0 bg-pattern opacity-10"></div>
          </div>

          <!-- 用户头像 -->
          <div class="absolute left-8 -bottom-20 animate__animated animate__bounceIn animate__delay-1000ms">
            <div class="w-40 h-40 rounded-full border-4 border-white dark:border-gray-800 overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center shadow-lg">
              <img v-if="userProfile.avatar" :src="userProfile.avatar" alt="用户头像" class="w-full h-full object-cover" />
              <span v-else class="text-6xl font-bold text-gray-500 dark:text-gray-300">{{ userProfile.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
            </div>
          </div>

          <!-- 编辑按钮 -->
          <div v-if="isCurrentUser" class="absolute right-4 bottom-4 animate__animated animate__fadeInRight animate__delay-1200ms">
            <button
              @click="isEditing = !isEditing"
              class="px-4 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary rounded-lg hover:bg-opacity-90 transition-colors hover:scale-105 transform"
            >
              {{ isEditing ? '取消编辑' : '编辑资料' }}
            </button>
          </div>
        </div>

        <!-- 用户信息 -->
        <div class="pt-24 px-8 pb-8">
          <!-- 查看模式 -->
          <div v-if="!isEditing" class="animate__animated animate__fadeIn animate__delay-1500ms">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white animate__animated animate__fadeInUp animate__delay-1600ms">{{ userProfile.username }}</h1>
            <p class="text-gray-600 dark:text-gray-300 mt-1 animate__animated animate__fadeInUp animate__delay-1700ms">{{ userProfile.email }}</p>
            <p v-if="userProfile.bio" class="mt-4 text-gray-700 dark:text-gray-300 animate__animated animate__fadeInUp animate__delay-1800ms">{{ userProfile.bio }}</p>
            <p v-else class="mt-4 text-gray-500 dark:text-gray-400 italic animate__animated animate__fadeInUp animate__delay-1800ms">暂无个人简介</p>

            <!-- 社交媒体图标 -->
            <div v-if="hasSocialMedia" class="mt-4 flex space-x-3 animate__animated animate__fadeIn animate__delay-2000ms">
              <a v-if="userProfile.social_media?.github" :href="userProfile.social_media.github" target="_blank" class="social-icon github">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a v-if="userProfile.social_media?.bilibili" :href="userProfile.social_media.bilibili" target="_blank" class="social-icon bilibili">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 0 1-.373-.906c0-.356.124-.658.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 0 1 .16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906L17.813 4.653zM5.333 7.24c-.746.018-1.373.276-1.88.773-.506.498-.769 1.13-.786 1.894v7.52c.017.764.28 1.395.786 1.893.507.498 1.134.756 1.88.773h13.334c.746-.017 1.373-.275 1.88-.773.506-.498.769-1.129.786-1.893v-7.52c-.017-.765-.28-1.396-.786-1.894-.507-.497-1.134-.755-1.88-.773H5.333zM8 11.107c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373zm8 0c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373zm-4 2.88c.711 0 1.289.257 1.733.773.444.516.667 1.112.667 1.787v.747c0 .675-.223 1.271-.667 1.787-.444.516-1.022.773-1.733.773-.711 0-1.289-.257-1.733-.773-.444-.516-.667-1.112-.667-1.787v-.747c0-.675.223-1.271.667-1.787.444-.516 1.022-.773 1.733-.773z"/>
                </svg>
              </a>
              <a v-if="userProfile.social_media?.xiaohongshu" :href="userProfile.social_media.xiaohongshu" target="_blank" class="social-icon xiaohongshu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19.2,6.8H4.8C3.4,6.8,2.4,7.9,2.4,9.2v5.6c0,1.3,1.1,2.4,2.4,2.4h14.4c1.3,0,2.4-1.1,2.4-2.4V9.2C21.6,7.9,20.5,6.8,19.2,6.8z M8.4,14.8c-1.3,0-2.4-1.1-2.4-2.4c0-1.3,1.1-2.4,2.4-2.4c1.3,0,2.4,1.1,2.4,2.4C10.8,13.7,9.7,14.8,8.4,14.8z M15.6,14.8c-1.3,0-2.4-1.1-2.4-2.4c0-1.3,1.1-2.4,2.4-2.4c1.3,0,2.4,1.1,2.4,2.4C18,13.7,16.9,14.8,15.6,14.8z"/>
                </svg>
              </a>
              <a v-if="userProfile.social_media?.weibo" :href="userProfile.social_media.weibo" target="_blank" class="social-icon weibo">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.01 0h-16.01c-2.215 0-4 1.785-4 4v16c0 2.215 1.785 4 4 4h16.01c2.215 0 4-1.785 4-4v-16c0-2.215-1.785-4-4-4zm-9.8 14.571c-2.261 0-4.093-1.077-4.093-2.404 0-1.327 1.832-2.404 4.093-2.404 2.262 0 4.093 1.077 4.093 2.404 0 1.327-1.83 2.404-4.093 2.404zm9.8-8.571h-14.009c-.55 0-.991-.441-.991-.991v-.018c0-.55.441-.991.991-.991h14.009c.55 0 .991.441.991.991v.018c0 .55-.441.991-.991.991z"/>
                </svg>
              </a>
              <a v-if="userProfile.social_media?.zhihu" :href="userProfile.social_media.zhihu" target="_blank" class="social-icon zhihu">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M5.721 0c-2.079 0-3.776 1.698-3.776 3.777v16.445c0 2.079 1.698 3.777 3.776 3.777h12.557c2.079 0 3.776-1.698 3.776-3.777v-16.445c0-2.079-1.698-3.777-3.776-3.777h-12.557zm4.551 7.269c-.206.001-.396.069-.553.184-.157.115-.28.278-.357.47l-.001.003-2.298 5.726-.156.387.387-.155 5.726-2.298.3.001c.194-.077.357-.2.472-.357.115-.157.184-.347.184-.553v-2.86c0-.206-.069-.396-.184-.553-.115-.157-.278-.28-.47-.357l-.003-.001-.86-.344-.86-.344c-.194-.077-.357-.2-.472-.357-.115-.157-.184-.347-.184-.553v-.002zm2.177 8.152c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75zm-1.421 1.409c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75zm2.842 0c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75zm-1.421 1.409c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75z"/>
                </svg>
              </a>
            </div>

            <div class="mt-6 flex items-center text-sm text-gray-500 dark:text-gray-400 animate__animated animate__fadeIn animate__delay-2000ms">
              <span class="mr-4">
                <span class="font-medium">{{ userProfile.role || '普通用户' }}</span>
              </span>
              <span>
                注册于 <span class="font-medium">{{ formatDate(userProfile.created_at) }}</span>
              </span>
            </div>
          </div>

          <!-- 编辑模式 -->
          <div v-else class="animate__animated animate__fadeIn">
            <form @submit.prevent="saveProfile" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">用户名</label>
                <p class="text-gray-900 dark:text-white">{{ userProfile.username }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">用户名不可修改</p>
              </div>

              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">邮箱</label>
                <input
                  type="email"
                  id="email"
                  v-model="editForm.email"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div>
                <label for="bio" class="block text-sm font-medium text-gray-700 dark:text-gray-300">个人简介</label>
                <textarea
                  id="bio"
                  v-model="editForm.bio"
                  rows="3"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
                ></textarea>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">头像</label>
                <div class="flex flex-col md:flex-row md:items-start md:space-x-6">
                  <!-- 头像预览 -->
                  <div class="avatar-preview-container mb-4 md:mb-0">
                    <div class="w-32 h-32 md:w-40 md:h-40 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center border-2 border-gray-300 dark:border-gray-600 shadow-md mx-auto md:mx-0">
                      <img v-if="avatarPreview" :src="avatarPreview" alt="头像预览" class="w-full h-full object-cover" />
                      <img v-else-if="userProfile.avatar" :src="userProfile.avatar" alt="当前头像" class="w-full h-full object-cover" />
                      <span v-else class="text-5xl font-bold text-gray-500 dark:text-gray-300">{{ userProfile.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
                    </div>
                    <p v-if="avatarPreview" class="text-xs text-center text-gray-500 dark:text-gray-400 mt-2 md:text-left">预览效果</p>
                  </div>

                  <!-- 上传控件 -->
                  <div class="flex-1">
                    <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                      <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">更新头像</h4>
                      <input
                        type="file"
                        id="avatar-upload"
                        ref="avatarInput"
                        accept="image/*"
                        class="hidden"
                        @change="handleAvatarChange"
                      />
                      <div class="flex flex-wrap gap-2">
                        <button
                          type="button"
                          @click="triggerAvatarUpload"
                          class="px-4 py-2 bg-secondary dark:bg-dark-secondary text-white rounded-md hover:bg-opacity-90 transition-colors text-sm flex items-center"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0l-4 4m4-4v12" />
                          </svg>
                          选择图片
                        </button>
                        <button
                          v-if="avatarFile || avatarPreview"
                          type="button"
                          @click="clearAvatarUpload"
                          class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors text-sm flex items-center"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                          清除选择
                        </button>
                      </div>
                      <div class="mt-4">
                        <p class="text-xs text-gray-500 dark:text-gray-400">支持 JPG, PNG, GIF 格式，最大 2MB</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">建议使用正方形图片以获得最佳效果</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">新密码 (留空则不修改)</label>
                <input
                  type="password"
                  id="password"
                  v-model="editForm.password"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
                />
              </div>

              <!-- 社交媒体链接 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">社交媒体链接</label>
                <div class="space-y-3">
                  <div>
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                      </svg>
                      <label for="github" class="block text-sm font-medium text-gray-700 dark:text-gray-300">GitHub</label>
                    </div>
                    <input
                      type="url"
                      id="github"
                      v-model="editForm.social_media.github"
                      placeholder="https://github.com/username"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white text-sm"
                    />
                  </div>

                  <div>
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 0 1-.373-.906c0-.356.124-.658.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 0 1 .16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906L17.813 4.653zM5.333 7.24c-.746.018-1.373.276-1.88.773-.506.498-.769 1.13-.786 1.894v7.52c.017.764.28 1.395.786 1.893.507.498 1.134.756 1.88.773h13.334c.746-.017 1.373-.275 1.88-.773.506-.498.769-1.129.786-1.893v-7.52c-.017-.765-.28-1.396-.786-1.894-.507-.497-1.134-.755-1.88-.773H5.333zM8 11.107c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373zm8 0c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373zm-4 2.88c.711 0 1.289.257 1.733.773.444.516.667 1.112.667 1.787v.747c0 .675-.223 1.271-.667 1.787-.444.516-1.022.773-1.733.773-.711 0-1.289-.257-1.733-.773-.444-.516-.667-1.112-.667-1.787v-.747c0-.675.223-1.271.667-1.787.444-.516 1.022-.773 1.733-.773z"/>
                      </svg>
                      <label for="bilibili" class="block text-sm font-medium text-gray-700 dark:text-gray-300">哔哩哔哩</label>
                    </div>
                    <input
                      type="url"
                      id="bilibili"
                      v-model="editForm.social_media.bilibili"
                      placeholder="https://space.bilibili.com/123456"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white text-sm"
                    />
                  </div>

                  <div>
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M19.2,6.8H4.8C3.4,6.8,2.4,7.9,2.4,9.2v5.6c0,1.3,1.1,2.4,2.4,2.4h14.4c1.3,0,2.4-1.1,2.4-2.4V9.2C21.6,7.9,20.5,6.8,19.2,6.8z M8.4,14.8c-1.3,0-2.4-1.1-2.4-2.4c0-1.3,1.1-2.4,2.4-2.4c1.3,0,2.4,1.1,2.4,2.4C10.8,13.7,9.7,14.8,8.4,14.8z M15.6,14.8c-1.3,0-2.4-1.1-2.4-2.4c0-1.3,1.1-2.4,2.4-2.4c1.3,0,2.4,1.1,2.4,2.4C18,13.7,16.9,14.8,15.6,14.8z"/>
                      </svg>
                      <label for="xiaohongshu" class="block text-sm font-medium text-gray-700 dark:text-gray-300">小红书</label>
                    </div>
                    <input
                      type="url"
                      id="xiaohongshu"
                      v-model="editForm.social_media.xiaohongshu"
                      placeholder="https://www.xiaohongshu.com/user/profile/123456"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white text-sm"
                    />
                  </div>

                  <div>
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M20.01 0h-16.01c-2.215 0-4 1.785-4 4v16c0 2.215 1.785 4 4 4h16.01c2.215 0 4-1.785 4-4v-16c0-2.215-1.785-4-4-4zm-9.8 14.571c-2.261 0-4.093-1.077-4.093-2.404 0-1.327 1.832-2.404 4.093-2.404 2.262 0 4.093 1.077 4.093 2.404 0 1.327-1.83 2.404-4.093 2.404zm9.8-8.571h-14.009c-.55 0-.991-.441-.991-.991v-.018c0-.55.441-.991.991-.991h14.009c.55 0 .991.441.991.991v.018c0 .55-.441.991-.991.991z"/>
                      </svg>
                      <label for="weibo" class="block text-sm font-medium text-gray-700 dark:text-gray-300">微博</label>
                    </div>
                    <input
                      type="url"
                      id="weibo"
                      v-model="editForm.social_media.weibo"
                      placeholder="https://weibo.com/username"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white text-sm"
                    />
                  </div>

                  <div>
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M5.721 0c-2.079 0-3.776 1.698-3.776 3.777v16.445c0 2.079 1.698 3.777 3.776 3.777h12.557c2.079 0 3.776-1.698 3.776-3.777v-16.445c0-2.079-1.698-3.777-3.776-3.777h-12.557zm4.551 7.269c-.206.001-.396.069-.553.184-.157.115-.28.278-.357.47l-.001.003-2.298 5.726-.156.387.387-.155 5.726-2.298.3.001c.194-.077.357-.2.472-.357.115-.157.184-.347.184-.553v-2.86c0-.206-.069-.396-.184-.553-.115-.157-.278-.28-.47-.357l-.003-.001-.86-.344-.86-.344c-.194-.077-.357-.2-.472-.357-.115-.157-.184-.347-.184-.553v-.002zm2.177 8.152c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75zm-1.421 1.409c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75zm2.842 0c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75zm-1.421 1.409c-.414 0-.75.336-.75.75s.336.75.75.75c.414 0 .75-.336.75-.75s-.336-.75-.75-.75z"/>
                      </svg>
                      <label for="zhihu" class="block text-sm font-medium text-gray-700 dark:text-gray-300">知乎</label>
                    </div>
                    <input
                      type="url"
                      id="zhihu"
                      v-model="editForm.social_media.zhihu"
                      placeholder="https://zhihu.com/people/username"
                      class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white text-sm"
                    />
                  </div>
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">留空则不显示对应社交媒体图标</p>
              </div>

              <div class="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  @click="isEditing = false"
                  class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  取消
                </button>
                <button
                  type="submit"
                  class="px-4 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary rounded-md hover:bg-opacity-90 flex items-center justify-center min-w-[100px]"
                  :disabled="isLoading || isUploading"
                >
                  <svg v-if="isLoading || isUploading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isLoading || isUploading ? '处理中...' : '保存修改' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- 用户活动标签页 -->
      <div class="max-w-4xl mx-auto mt-8 animate__animated animate__fadeIn animate__delay-2200ms">
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="flex -mb-px">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'border-secondary dark:border-dark-secondary text-secondary dark:text-dark-secondary'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600',
                'px-4 py-2 border-b-2 font-medium text-sm'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <div class="mt-6">
          <!-- 文章列表 -->
          <div v-if="activeTab === 'articles'" class="space-y-4 animate__animated animate__fadeIn animate__faster">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">发布的文章</h2>
            <div v-if="isLoading" class="py-4 text-center text-gray-500 dark:text-gray-400">加载中...</div>
            <div v-else-if="articles.length === 0" class="py-4 text-center text-gray-500 dark:text-gray-400">暂无文章</div>
            <div v-else class="space-y-4">
              <div
                v-for="article in articles"
                :key="article.id"
                class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm hover:shadow-md transition-all transform hover:-translate-y-1"
              >
                <h3 class="text-lg font-medium text-gray-900 dark:text-white">
                  <router-link :to="`/article/${article.id}`" class="hover:text-secondary dark:hover:text-dark-secondary">
                    {{ article.title }}
                  </router-link>
                </h3>
                <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">{{ article.excerpt || '暂无摘要' }}</p>
                <div class="mt-2 text-xs text-gray-500 dark:text-gray-500">
                  {{ formatDate(article.created_at) }}
                </div>
              </div>
            </div>
          </div>

          <!-- 评论列表 -->
          <div v-if="activeTab === 'comments'" class="space-y-4 animate__animated animate__fadeIn animate__faster">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">发表的评论</h2>
            <div v-if="isLoading" class="py-4 text-center text-gray-500 dark:text-gray-400">加载中...</div>
            <div v-else-if="comments.length === 0" class="py-4 text-center text-gray-500 dark:text-gray-400">暂无评论</div>
            <div v-else class="space-y-4">
              <div
                v-for="comment in comments"
                :key="comment.id"
                class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm hover:shadow-md transition-all transform hover:-translate-y-1"
              >
                <p class="text-gray-700 dark:text-gray-300">{{ comment.content }}</p>
                <div class="mt-2 text-xs text-gray-500 dark:text-gray-500">
                  {{ formatDate(comment.created_at) }}
                </div>
              </div>
            </div>
          </div>

          <!-- 活动记录 -->
          <div v-if="activeTab === 'activities'" class="space-y-4 animate__animated animate__fadeIn animate__faster">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">活动记录</h2>
            <div v-if="isLoading" class="py-4 text-center text-gray-500 dark:text-gray-400">加载中...</div>
            <div v-else-if="activities.length === 0" class="py-4 text-center text-gray-500 dark:text-gray-400">暂无活动</div>
            <div v-else class="space-y-4">
              <div
                v-for="activity in activities"
                :key="activity.id"
                class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm hover:shadow-md transition-all transform hover:-translate-y-1"
              >
                <p class="text-gray-700 dark:text-gray-300">{{ activity.description }}</p>
                <div class="mt-2 text-xs text-gray-500 dark:text-gray-500">
                  {{ formatDate(activity.created_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userApi, fileApi } from '@/api'
import { Navbar } from '@/components/layout'
import message from '@/utils/message'

export default {
  name: 'UserProfile',
  components: {
    Navbar
  },
  setup() {
    const route = useRoute()
    const router = useRouter()

    // 用户ID，从路由参数获取
    const userId = computed(() => route.params.id)

    // 当前登录用户ID
    const currentUserId = ref(localStorage.getItem('userId'))

    // 是否是当前用户的资料页
    const isCurrentUser = computed(() => userId.value === currentUserId.value)

    // 是否有社交媒体链接
    const hasSocialMedia = computed(() => {
      return userProfile.value.social_media && (
        userProfile.value.social_media.github ||
        userProfile.value.social_media.bilibili ||
        userProfile.value.social_media.xiaohongshu ||
        userProfile.value.social_media.weibo ||
        userProfile.value.social_media.zhihu
      )
    })

    // 用户资料
    const userProfile = ref({})

    // 编辑表单
    const editForm = ref({
      email: '',
      bio: '',
      avatar: '',
      password: '',
      social_media: {
        github: '',
        bilibili: '',
        xiaohongshu: '',
        weibo: '',
        zhihu: ''
      }
    })

    // 头像上传相关
    const avatarInput = ref(null)
    const avatarFile = ref(null)
    const avatarPreview = ref('')
    const isUploading = ref(false)

    // 编辑状态
    const isEditing = ref(false)

    // 加载状态
    const isLoading = ref(false)

    // 标签页
    const activeTab = ref('articles')
    const tabs = [
      { id: 'articles', name: '文章' },
      { id: 'comments', name: '评论' },
      { id: 'activities', name: '活动' }
    ]

    // 用户文章、评论和活动
    const articles = ref([])
    const comments = ref([])
    const activities = ref([])

    // 获取用户资料
    const fetchUserProfile = async () => {
      isLoading.value = true
      try {
        if (isCurrentUser.value) {
          // 如果是当前用户，使用 /users/me 接口
          userProfile.value = await userApi.getUserInfo()
        } else {
          // 否则使用 /users/{id} 接口
          userProfile.value = await userApi.getUserById(userId.value)
        }

        // 初始化编辑表单
        editForm.value = {
          email: userProfile.value.email || '',
          bio: userProfile.value.bio || '',
          avatar: userProfile.value.avatar || '',
          password: '',
          social_media: {
            github: userProfile.value.social_media?.github || '',
            bilibili: userProfile.value.social_media?.bilibili || '',
            xiaohongshu: userProfile.value.social_media?.xiaohongshu || '',
            weibo: userProfile.value.social_media?.weibo || '',
            zhihu: userProfile.value.social_media?.zhihu || ''
          }
        }
      } catch (error) {
        console.error('获取用户资料失败:', error)
        message.error('获取用户资料失败')
      } finally {
        isLoading.value = false
      }
    }

    // 获取用户文章
    const fetchUserArticles = async () => {
      isLoading.value = true
      try {
        articles.value = await userApi.getUserArticles(userId.value)
      } catch (error) {
        console.error('获取用户文章失败:', error)
        message.error('获取用户文章失败')
      } finally {
        isLoading.value = false
      }
    }

    // 获取用户评论
    const fetchUserComments = async () => {
      isLoading.value = true
      try {
        comments.value = await userApi.getUserComments(userId.value)
      } catch (error) {
        console.error('获取用户评论失败:', error)
        message.error('获取用户评论失败')
      } finally {
        isLoading.value = false
      }
    }

    // 获取用户活动
    const fetchUserActivities = async () => {
      isLoading.value = true
      try {
        activities.value = await userApi.getUserActivities(userId.value)
      } catch (error) {
        console.error('获取用户活动失败:', error)
        message.error('获取用户活动失败')
      } finally {
        isLoading.value = false
      }
    }

    // 触发头像上传按钮
    const triggerAvatarUpload = () => {
      avatarInput.value.click()
    }

    // 处理头像文件选择
    const handleAvatarChange = (event) => {
      const file = event.target.files[0]
      if (!file) return

      // 检查文件类型
      const validTypes = ['image/jpeg', 'image/png', 'image/gif']
      if (!validTypes.includes(file.type)) {
        message.error('请选择有效的图片文件（JPG, PNG, GIF）')
        return
      }

      // 检查文件大小
      const maxSize = 2 * 1024 * 1024 // 2MB
      if (file.size > maxSize) {
        message.error('图片大小不能超过 2MB')
        return
      }

      // 保存文件并创建预览
      avatarFile.value = file
      const reader = new FileReader()
      reader.onload = (e) => {
        avatarPreview.value = e.target.result
      }
      reader.readAsDataURL(file)
    }

    // 清除头像选择
    const clearAvatarUpload = () => {
      avatarFile.value = null
      avatarPreview.value = ''
      if (avatarInput.value) {
        avatarInput.value.value = ''
      }
    }

    // 上传头像
    const uploadAvatar = async () => {
      if (!avatarFile.value) return null

      isUploading.value = true
      try {
        // 创建 FormData 对象
        const formData = new FormData()
        formData.append('file', avatarFile.value)

        // 获取认证令牌
        const token = localStorage.getItem('token')

        // 正确处理 token 格式
        let formattedToken = null
        if (token) {
          const lowerToken = token.toLowerCase()
          let cleanToken = token
          if (lowerToken.includes('bearer')) {
            cleanToken = token.replace(/^\s*bearer\s+/i, '')
          }
          formattedToken = `Bearer ${cleanToken}`
        }

        const response = await fileApi.uploadImage(formData, formattedToken)
        message.success('头像上传成功')
        return response.url || response.image_url || response.path
      } catch (error) {
        console.error('头像上传失败:', error)
        message.error('头像上传失败')
        return null
      } finally {
        isUploading.value = false
      }
    }

    // 保存用户资料
    const saveProfile = async () => {
      isLoading.value = true
      try {
        // 如果有新头像，先上传
        let avatarUrl = null
        if (avatarFile.value) {
          avatarUrl = await uploadAvatar()
          if (!avatarUrl) {
            isLoading.value = false
            return // 头像上传失败，不继续保存
          }
        }

        // 构造更新数据，只包含有效字段
        const updateData = {}
        if (editForm.value.email) updateData.email = editForm.value.email
        if (editForm.value.bio) updateData.bio = editForm.value.bio
        if (avatarUrl) updateData.avatar = avatarUrl
        else if (editForm.value.avatar) updateData.avatar = editForm.value.avatar
        if (editForm.value.password) updateData.password = editForm.value.password

        // 处理社交媒体链接
        const socialMedia = {}
        if (editForm.value.social_media.github) socialMedia.github = editForm.value.social_media.github
        if (editForm.value.social_media.bilibili) socialMedia.bilibili = editForm.value.social_media.bilibili
        if (editForm.value.social_media.xiaohongshu) socialMedia.xiaohongshu = editForm.value.social_media.xiaohongshu
        if (editForm.value.social_media.weibo) socialMedia.weibo = editForm.value.social_media.weibo
        if (editForm.value.social_media.zhihu) socialMedia.zhihu = editForm.value.social_media.zhihu

        // 如果有社交媒体链接，添加到更新数据中
        if (Object.keys(socialMedia).length > 0) {
          updateData.social_media = socialMedia
        }

        // 更新用户资料
        const updatedProfile = await userApi.updateUserInfo(updateData)

        // 更新本地数据
        userProfile.value = updatedProfile

        // 重置表单
        editForm.value.password = ''
        clearAvatarUpload()

        // 退出编辑模式
        isEditing.value = false

        message.success('资料更新成功')
      } catch (error) {
        console.error('更新用户资料失败:', error)
        message.error('更新用户资料失败')
      } finally {
        isLoading.value = false
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    // 监听标签页变化
    const handleTabChange = () => {
      if (activeTab.value === 'articles') {
        fetchUserArticles()
      } else if (activeTab.value === 'comments') {
        fetchUserComments()
      } else if (activeTab.value === 'activities') {
        fetchUserActivities()
      }
    }

    // 初始化
    onMounted(() => {
      fetchUserProfile()
      fetchUserArticles() // 默认加载文章标签页
    })

    // 监听标签页变化
    watch(activeTab, handleTabChange)

    return {
      userId,
      isCurrentUser,
      userProfile,
      editForm,
      isEditing,
      isLoading,
      activeTab,
      tabs,
      articles,
      comments,
      activities,
      saveProfile,
      formatDate,
      // 头像上传相关
      avatarInput,
      avatarFile,
      avatarPreview,
      isUploading,
      triggerAvatarUpload,
      handleAvatarChange,
      clearAvatarUpload
    }
  }
}
</script>

<style scoped>
/* 头像预览容器样式 */
.avatar-preview-container {
  position: relative;
  transition: all 0.3s ease;
}

/* 社交媒体图标样式 */
.social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #fff;
  transition: all 0.3s ease;
  transform: scale(1);
}

.social-icon:hover {
  transform: scale(1.2);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.social-icon.github {
  background-color: #333;
}

.social-icon.bilibili {
  background-color: #00a1d6;
}

.social-icon.xiaohongshu {
  background-color: #fe2c55;
}

.social-icon.weibo {
  background-color: #e6162d;
}

.social-icon.zhihu {
  background-color: #0084ff;
}

.dark .social-icon {
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
}

.dark .social-icon:hover {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

/* 头像悬停效果 */
.avatar-preview-container:hover {
  transform: scale(1.02);
}

/* 渐变背景 */
.h-56.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradientAnimation 8s ease infinite;
}

/* 背景图案 */
.bg-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.4' fill-rule='evenodd'%3E%3Ccircle cx='3' cy='3' r='3'/%3E%3Ccircle cx='13' cy='13' r='3'/%3E%3C/g%3E%3C/svg%3E");
  background-size: 20px 20px;
}

/* 社交图标样式 */
.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #fff;
  transition: all 0.3s ease;
  transform: scale(1);
}

.social-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.social-icon.github {
  background-color: #333;
}

.social-icon.bilibili {
  background-color: #00a1d6;
}

.social-icon.xiaohongshu {
  background-color: #fe2c55;
}

.social-icon.weibo {
  background-color: #e6162d;
}

.social-icon.zhihu {
  background-color: #0084ff;
}

/* 暗黑模式下的社交图标 */
.dark .social-icon {
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
}

.dark .social-icon:hover {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
