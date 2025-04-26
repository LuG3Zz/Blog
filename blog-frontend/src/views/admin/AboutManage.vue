<template>
  <div class="container mx-auto px-4 py-8">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-white">关于页面管理</h1>

      <div v-if="isLoading" class="flex justify-center items-center py-10">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
      </div>

      <div v-else-if="error" class="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 p-4 rounded-lg mb-6">
        {{ error }}
      </div>

      <div v-else>
        <form @submit.prevent="saveAboutPage" class="space-y-6">
          <!-- 个人信息部分 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">个人信息</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">姓名</label>
                <input
                  v-model="aboutData.personalInfo.name"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">职位</label>
                <input
                  v-model="aboutData.personalInfo.title"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>
            </div>

            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">头像</label>
              <div class="flex">
                <input
                  v-model="aboutData.personalInfo.avatar"
                  type="text"
                  class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-l-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
                <button
                  @click="openFileSelector('avatar')"
                  class="px-4 py-2 bg-blue-500 text-white rounded-r-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  选择图片
                </button>
              </div>
              <div class="mt-2 flex items-center">
                <div v-if="aboutData.personalInfo.avatar" class="w-16 h-16 mr-2 border border-gray-200 dark:border-gray-700 rounded overflow-hidden flex items-center justify-center">
                  <img :src="aboutData.personalInfo.avatar" alt="头像预览" class="max-w-full max-h-full object-contain" style="width: 60px; height: 60px;" />
                </div>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  选择已上传的图片或输入图片URL
                </p>
              </div>
            </div>

            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">个人简介</label>
              <textarea
                v-model="aboutData.personalInfo.bio"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              ></textarea>
            </div>

            <!-- 联系方式 -->
            <div class="mb-4">
              <div class="flex justify-between items-center mb-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">联系方式</label>
                <button
                  type="button"
                  @click="addContact"
                  class="text-blue-500 hover:text-blue-700 focus:outline-none flex items-center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  添加联系方式
                </button>
              </div>

              <div v-for="(contact, contactIndex) in aboutData.personalInfo.contacts" :key="contactIndex" class="mb-6 border-b dark:border-gray-700 pb-6">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="text-lg font-medium text-gray-800 dark:text-white">联系方式 {{ contactIndex + 1 }}</h3>
                  <button
                    type="button"
                    @click="removeContact(contactIndex)"
                    class="text-red-500 hover:text-red-700 focus:outline-none"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">文本</label>
                    <input
                      v-model="contact.text"
                      type="text"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">链接</label>
                    <input
                      v-model="contact.url"
                      type="text"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">图标 (SVG)</label>
                  <textarea
                    v-model="contact.icon"
                    rows="3"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white font-mono text-sm"
                  ></textarea>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div class="flex items-center">
                    <input
                      type="checkbox"
                      :id="'external-' + contactIndex"
                      v-model="contact.external"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label :for="'external-' + contactIndex" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                      外部链接
                    </label>
                  </div>

                  <div class="flex items-center">
                    <input
                      type="checkbox"
                      :id="'isWechat-' + contactIndex"
                      v-model="contact.isWechat"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label :for="'isWechat-' + contactIndex" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                      是微信联系方式
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 简历文件 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">简历文件</h2>

            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">简历文件路径</label>
              <div class="flex">
                <input
                  v-model="aboutData.resumeFile"
                  type="text"
                  class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-l-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
                <button
                  @click="openFileSelector('resumeFile')"
                  class="px-4 py-2 bg-blue-500 text-white rounded-r-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  选择文件
                </button>
              </div>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                选择已上传的文件或输入文件URL
              </p>
            </div>
          </div>

          <!-- 教育经历 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">教育经历</h2>

            <div v-for="(edu, eduIndex) in aboutData.education" :key="eduIndex" class="mb-6 border-b dark:border-gray-700 pb-6">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-medium text-gray-800 dark:text-white">教育 {{ eduIndex + 1 }}</h3>
                <button
                  type="button"
                  @click="removeEducation(eduIndex)"
                  class="text-red-500 hover:text-red-700 focus:outline-none"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">学位</label>
                  <input
                    v-model="edu.degree"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">学校</label>
                  <input
                    v-model="edu.institution"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">时间段</label>
                <input
                  v-model="edu.period"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">教育描述</label>
                <textarea
                  v-model="edu.description"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                ></textarea>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">背景颜色类</label>
                  <input
                    v-model="edu.bgColor"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">时间段颜色类</label>
                  <input
                    v-model="edu.periodClass"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">标签颜色类</label>
                  <input
                    v-model="edu.tagClasses"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
              </div>

              <div class="mb-4">
                <div class="flex justify-between items-center mb-2">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">成就</label>
                  <button
                    type="button"
                    @click="addEducationAchievement(eduIndex)"
                    class="text-blue-500 hover:text-blue-700 focus:outline-none flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    添加成就
                  </button>
                </div>

                <div class="flex flex-wrap gap-2 mb-2">
                  <div v-for="(achievement, achievementIndex) in edu.achievements" :key="achievementIndex" class="flex items-center bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full">
                    <input
                      v-model="edu.achievements[achievementIndex]"
                      type="text"
                      class="bg-transparent border-none focus:outline-none focus:ring-0 w-auto"
                    />
                    <button
                      type="button"
                      @click="removeEducationAchievement(eduIndex, achievementIndex)"
                      class="ml-2 text-gray-500 hover:text-red-500 focus:outline-none"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <button
              type="button"
              @click="addEducation"
              class="mt-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-300"
            >
              添加教育经历
            </button>
          </div>

          <!-- 工作经历 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">工作经历</h2>

            <div v-for="(job, jobIndex) in aboutData.workExperience" :key="jobIndex" class="mb-6 border-b dark:border-gray-700 pb-6">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-medium text-gray-800 dark:text-white">工作 {{ jobIndex + 1 }}</h3>
                <button
                  type="button"
                  @click="removeWorkExperience(jobIndex)"
                  class="text-red-500 hover:text-red-700 focus:outline-none"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">职位</label>
                  <input
                    v-model="job.title"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">公司</label>
                  <input
                    v-model="job.company"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">时间段</label>
                <input
                  v-model="job.period"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">工作描述</label>
                <textarea
                  v-model="job.description"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                ></textarea>
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">标签颜色类</label>
                <input
                  v-model="job.tagClasses"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">徽章颜色类</label>
                <input
                  v-model="job.badgeColor"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div class="mb-4">
                <div class="flex justify-between items-center mb-2">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">技能标签</label>
                  <button
                    type="button"
                    @click="addJobTag(jobIndex)"
                    class="text-blue-500 hover:text-blue-700 focus:outline-none flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    添加标签
                  </button>
                </div>

                <div class="flex flex-wrap gap-2 mb-2">
                  <div v-for="(tag, tagIndex) in job.tags" :key="tagIndex" class="flex items-center bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full">
                    <input
                      v-model="job.tags[tagIndex]"
                      type="text"
                      class="bg-transparent border-none focus:outline-none focus:ring-0 w-auto"
                    />
                    <button
                      type="button"
                      @click="removeJobTag(jobIndex, tagIndex)"
                      class="ml-2 text-gray-500 hover:text-red-500 focus:outline-none"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <button
              type="button"
              @click="addWorkExperience"
              class="mt-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-300"
            >
              添加工作经历
            </button>
          </div>

          <!-- 专业技能 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">专业技能</h2>

            <div v-for="(skillGroup, groupIndex) in aboutData.skills" :key="groupIndex" class="mb-6 border-b dark:border-gray-700 pb-6">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-medium text-gray-800 dark:text-white">技能组 {{ groupIndex + 1 }}</h3>
                <button
                  type="button"
                  @click="removeSkillGroup(groupIndex)"
                  class="text-red-500 hover:text-red-700 focus:outline-none"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">名称</label>
                  <input
                    v-model="skillGroup.name"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">背景颜色类</label>
                  <input
                    v-model="skillGroup.bgColor"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">进度条颜色类</label>
                <input
                  v-model="skillGroup.barColor"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div class="mb-4">
                <div class="flex justify-between items-center mb-2">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">技能项</label>
                  <button
                    type="button"
                    @click="addSkillItem(groupIndex)"
                    class="text-blue-500 hover:text-blue-700 focus:outline-none flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    添加技能
                  </button>
                </div>

                <div v-for="(item, itemIndex) in skillGroup.items" :key="itemIndex" class="flex items-center gap-4 mb-2">
                  <div class="flex-grow">
                    <input
                      v-model="item.name"
                      type="text"
                      placeholder="技能名称"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>

                  <div class="w-24">
                    <input
                      v-model.number="item.level"
                      type="number"
                      min="0"
                      max="100"
                      placeholder="熟练度"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>

                  <button
                    type="button"
                    @click="removeSkillItem(groupIndex, itemIndex)"
                    class="text-red-500 hover:text-red-700 focus:outline-none"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <button
              type="button"
              @click="addSkillGroup"
              class="mt-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-300"
            >
              添加技能组
            </button>
          </div>

          <!-- 项目经历 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">项目经历</h2>

            <div v-for="(project, projectIndex) in aboutData.projects" :key="projectIndex" class="mb-6 border-b dark:border-gray-700 pb-6">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-medium text-gray-800 dark:text-white">项目 {{ projectIndex + 1 }}</h3>
                <button
                  type="button"
                  @click="removeProject(projectIndex)"
                  class="text-red-500 hover:text-red-700 focus:outline-none"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">项目标题</label>
                <input
                  v-model="project.title"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">主图片</label>
                <div class="flex">
                  <input
                    v-model="project.image"
                    type="text"
                    class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-l-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                  <button
                    @click="openFileSelector('projectImage', projectIndex)"
                    class="px-4 py-2 bg-blue-500 text-white rounded-r-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    选择图片
                  </button>
                </div>
                <div class="mt-2 flex items-center">
                  <div v-if="project.image" class="w-16 h-16 mr-2 border border-gray-200 dark:border-gray-700 rounded overflow-hidden flex items-center justify-center">
                    <img :src="project.image" alt="项目图片预览" class="max-w-full max-h-full object-contain" style="width: 70px; height: 70px;" />
                  </div>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    选择已上传的图片或输入图片URL
                  </p>
                </div>
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">项目描述</label>
                <textarea
                  v-model="project.description"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                ></textarea>
              </div>

              <div class="mb-4">
                <div class="flex justify-between items-center mb-2">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">图片列表</label>
                  <button
                    type="button"
                    @click="addProjectImage(projectIndex)"
                    class="text-blue-500 hover:text-blue-700 focus:outline-none flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    添加图片
                  </button>
                </div>

                <div v-for="(image, imageIndex) in project.images" :key="imageIndex" class="flex items-center gap-4 mb-2">
                  <div class="flex-grow flex">
                    <input
                      v-model="project.images[imageIndex]"
                      type="text"
                      placeholder="图片URL"
                      class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-l-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                    <button
                      type="button"
                      @click="openFileSelector('projectImages', projectIndex, imageIndex)"
                      class="px-4 py-2 bg-blue-500 text-white rounded-r-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    >
                      选择
                    </button>
                  </div>

                  <div v-if="project.images[imageIndex]" class="w-12 h-12 border border-gray-200 dark:border-gray-700 rounded overflow-hidden flex items-center justify-center">
                    <img :src="project.images[imageIndex]" alt="项目图片预览" class="max-w-full max-h-full object-contain" style="width: 50px; height: 50px;" />
                  </div>

                  <button
                    type="button"
                    @click="removeProjectImage(projectIndex, imageIndex)"
                    class="text-red-500 hover:text-red-700 focus:outline-none"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              <div class="mb-4">
                <div class="flex justify-between items-center mb-2">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">技术栈</label>
                  <button
                    type="button"
                    @click="addProjectTechnology(projectIndex)"
                    class="text-blue-500 hover:text-blue-700 focus:outline-none flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    添加技术
                  </button>
                </div>

                <div class="flex flex-wrap gap-2 mb-2">
                  <div v-for="(tech, techIndex) in project.technologies" :key="techIndex" class="flex items-center bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full">
                    <input
                      v-model="project.technologies[techIndex]"
                      type="text"
                      class="bg-transparent border-none focus:outline-none focus:ring-0 w-auto"
                    />
                    <button
                      type="button"
                      @click="removeProjectTechnology(projectIndex, techIndex)"
                      class="ml-2 text-gray-500 hover:text-red-500 focus:outline-none"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <button
              type="button"
              @click="addProject"
              class="mt-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-300"
            >
              添加项目
            </button>
          </div>

          <!-- 联系部分 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">联系部分</h2>

            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">联系信息</label>
              <textarea
                v-model="aboutData.contactSection.message"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              ></textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">邮件链接</label>
                <input
                  v-model="aboutData.contactSection.emailLink"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">按钮文本</label>
                <input
                  v-model="aboutData.contactSection.buttonText"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>
            </div>
          </div>



          <!-- 页脚 -->
          <div class="border dark:border-gray-700 rounded-lg p-4 mb-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">页脚</h2>

            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">页脚文本</label>
              <input
                v-model="aboutData.footer"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>
          </div>

          <!-- 保存按钮 -->
          <div class="flex justify-end">
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-300"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                保存中...
              </span>
              <span v-else>保存更改</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 文件选择器模态框 -->
    <Modal v-if="showFileSelector" @close="showFileSelector = false">
      <div class="w-full max-w-4xl">
        <FileSelector
          :file-type="fileSelectorType"
          @close="showFileSelector = false"
          @select="handleFileSelected"
        />
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { aboutPageApi } from '@/api';
import { useToast } from '@/composables/useToast';
import Modal from '@/components/common/Modal.vue';
import FileSelector from '@/components/admin/FileSelector.vue';
import { API_BASE_URL } from '@/config';

// 状态
const isLoading = ref(true);
const isSaving = ref(false);
const error = ref(null);
const { showToast } = useToast();

// 文件选择器相关
const showFileSelector = ref(false);
const fileSelectorType = ref('');
const currentFieldTarget = ref(null);
const currentProjectIndex = ref(-1);
const currentImageIndex = ref(-1);

// About 页面数据
const aboutData = reactive({
  resumeFile: '',
  personalInfo: {
    name: '',
    title: '',
    avatar: '',
    bio: '',
    contacts: []
  },
  skills: [],
  workExperience: [],
  education: [],
  projects: [],
  contactSection: {
    message: '',
    emailLink: '',
    buttonText: ''
  },
  footer: ''
});

// 获取 About 页面数据
const fetchAboutPage = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await aboutPageApi.getAboutPage();
    console.log('获取到的 About 页面数据:', response);
    if (response && response.content) {
      // 将后端数据复制到本地状态
      Object.assign(aboutData, response.content);
    }
  } catch (err) {
    console.error('获取 About 页面数据失败:', err);
    error.value = '获取 About 页面数据失败，请稍后重试';
  } finally {
    isLoading.value = false;
  }
};

// 保存 About 页面数据
const saveAboutPage = async () => {
  isSaving.value = true;

  try {
    await aboutPageApi.updateAboutPage(aboutData);
    showToast('保存成功', 'success');
  } catch (err) {
    console.error('保存 About 页面数据失败:', err);
    showToast('保存失败，请稍后重试', 'error');
  } finally {
    isSaving.value = false;
  }
};

// 技能组操作
const addSkillGroup = () => {
  aboutData.skills.push({
    name: '新技能组',
    bgColor: 'bg-blue-500/10 rounded-full blur-xl group-hover:bg-blue-500/20 transition-all duration-300',
    barColor: 'bg-gradient-to-r from-blue-500 to-indigo-600',
    items: []
  });
};

const removeSkillGroup = (index) => {
  aboutData.skills.splice(index, 1);
};

const addSkillItem = (groupIndex) => {
  aboutData.skills[groupIndex].items.push({
    name: '',
    level: 80
  });
};

const removeSkillItem = (groupIndex, itemIndex) => {
  aboutData.skills[groupIndex].items.splice(itemIndex, 1);
};

// 工作经历操作
const addWorkExperience = () => {
  aboutData.workExperience.push({
    title: '',
    company: '',
    period: '',
    description: '',
    tags: [],
    tagClasses: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200',
    badgeColor: 'bg-gradient-to-r from-purple-500 to-pink-600'
  });
};

const removeWorkExperience = (index) => {
  aboutData.workExperience.splice(index, 1);
};

const addJobTag = (jobIndex) => {
  aboutData.workExperience[jobIndex].tags.push('');
};

const removeJobTag = (jobIndex, tagIndex) => {
  aboutData.workExperience[jobIndex].tags.splice(tagIndex, 1);
};

// 教育经历操作
const addEducation = () => {
  aboutData.education.push({
    degree: '',
    institution: '',
    period: '',
    description: '',
    achievements: [],
    bgColor: 'bg-purple-500/10',
    periodClass: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200',
    tagClasses: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200'
  });
};

const removeEducation = (index) => {
  aboutData.education.splice(index, 1);
};

const addEducationAchievement = (eduIndex) => {
  aboutData.education[eduIndex].achievements.push('');
};

const removeEducationAchievement = (eduIndex, achievementIndex) => {
  aboutData.education[eduIndex].achievements.splice(achievementIndex, 1);
};

// 项目经历操作
const addProject = () => {
  aboutData.projects.push({
    title: '',
    image: '',
    images: [],
    description: '',
    technologies: []
  });
};

const removeProject = (index) => {
  aboutData.projects.splice(index, 1);
};

const addProjectImage = (projectIndex) => {
  aboutData.projects[projectIndex].images.push('');
};

const removeProjectImage = (projectIndex, imageIndex) => {
  aboutData.projects[projectIndex].images.splice(imageIndex, 1);
};

const addProjectTechnology = (projectIndex) => {
  aboutData.projects[projectIndex].technologies.push('');
};

const removeProjectTechnology = (projectIndex, techIndex) => {
  aboutData.projects[projectIndex].technologies.splice(techIndex, 1);
};

// 联系方式操作
const addContact = () => {
  aboutData.personalInfo.contacts.push({
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
    text: '新联系方式',
    url: '',
    external: false,
    isWechat: false
  });
};

const removeContact = (index) => {
  aboutData.personalInfo.contacts.splice(index, 1);
};

// 文件选择器相关方法
const openFileSelector = (target, projectIndex = -1, imageIndex = -1) => {
  currentFieldTarget.value = target;
  currentProjectIndex.value = projectIndex;
  currentImageIndex.value = imageIndex;

  // 根据目标字段设置文件类型筛选
  if (target === 'avatar' || target === 'projectImage' || target === 'projectImages') {
    fileSelectorType.value = 'image';
  } else {
    fileSelectorType.value = '';
  }

  showFileSelector.value = true;
};

const handleFileSelected = (file) => {
  console.log('AboutManage 接收到选择的文件:', file);

  // 使用API_BASE_URL拼接完整URL
  let fileUrl = '';

  // 如果file.url已经是完整URL，则直接使用
  if (file.url && (file.url.startsWith('http://') || file.url.startsWith('https://'))) {
    fileUrl = file.url;
  }
  // 如果file.url是相对路径，则使用API_BASE_URL拼接
  else if (file.url) {
    // 确保路径格式正确
    const relativePath = file.url.startsWith('/') ? file.url : `/${file.url}`;
    fileUrl = `${API_BASE_URL}${relativePath}`;
  }
  // 如果没有url，则使用file.id构建下载URL
  else if (file.id) {
    fileUrl = `${API_BASE_URL}/api/v1/files/download/${file.id}`;
  }

  console.log('使用的文件URL:', fileUrl);
  console.log('当前目标字段:', currentFieldTarget.value);
  console.log('当前项目索引:', currentProjectIndex.value);
  console.log('当前图片索引:', currentImageIndex.value);

  // 根据当前目标字段设置文件URL
  if (currentFieldTarget.value === 'avatar') {
    aboutData.personalInfo.avatar = fileUrl;
    console.log('设置头像URL:', fileUrl);
  } else if (currentFieldTarget.value === 'resumeFile') {
    aboutData.resumeFile = fileUrl;
    console.log('设置简历文件URL:', fileUrl);
  } else if (currentFieldTarget.value === 'projectImage' && currentProjectIndex.value >= 0) {
    aboutData.projects[currentProjectIndex.value].image = fileUrl;
    console.log('设置项目主图URL:', fileUrl);
  } else if (currentFieldTarget.value === 'projectImages' && currentProjectIndex.value >= 0 && currentImageIndex.value >= 0) {
    aboutData.projects[currentProjectIndex.value].images[currentImageIndex.value] = fileUrl;
    console.log('设置项目图片URL:', fileUrl);
  } else {
    console.warn('未找到匹配的目标字段');
  }

  showFileSelector.value = false;
  showToast('图片已选择，请记得点击页面底部的"保存更改"按钮保存所有修改', 'info');
};

// 组件挂载时获取数据
onMounted(() => {
  fetchAboutPage();
});
</script>
