<template>
  <div class="min-h-screen bg-primary dark:bg-dark-primary animate__animated animate__fadeIn">
    <Navbar />
    <div class="container mx-auto px-4 py-8 animate__animated animate__fadeInUp animate__delay-1s">
      <!-- 装饰元素 -->
      <div class="fixed -z-10 top-0 left-0 right-0 bottom-0 overflow-hidden opacity-50 dark:opacity-30 pointer-events-none">
        <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-gradient-to-r from-blue-300 to-purple-300 dark:from-blue-600 dark:to-purple-600 rounded-full filter blur-3xl"></div>
        <div class="absolute bottom-1/3 right-1/4 w-96 h-96 bg-gradient-to-r from-pink-300 to-orange-300 dark:from-pink-600 dark:to-orange-600 rounded-full filter blur-3xl"></div>
        <div class="absolute top-2/3 right-1/3 w-80 h-80 bg-gradient-to-r from-green-300 to-teal-300 dark:from-green-600 dark:to-teal-600 rounded-full filter blur-3xl"></div>
      </div>
      <!-- 顶部个人信息区域 - Inspira UI 风格卡片 -->
      <div class="max-w-5xl mx-auto mb-16">
        <div class="relative overflow-hidden rounded-3xl bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl shadow-[0_20px_50px_rgba(8,_112,_184,_0.2)] dark:shadow-[0_20px_50px_rgba(66,_153,_225,_0.2)] border border-blue-100/50 dark:border-blue-900/50 hover:shadow-[0_25px_60px_rgba(8,_112,_184,_0.3)] dark:hover:shadow-[0_25px_60px_rgba(66,_153,_225,_0.3)] transition-all duration-500 transform hover:scale-[101%]">
          <!-- 背景装饰 -->
          <div class="absolute -top-24 -right-24 w-64 h-64 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full opacity-20 blur-3xl animate-pulse"></div>
          <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-gradient-to-tr from-pink-400 to-orange-500 rounded-full opacity-20 blur-3xl animate-pulse" style="animation-delay: 1s"></div>
          <div class="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-purple-50/50 dark:from-blue-900/20 dark:to-purple-900/20 opacity-50"></div>

          <!-- 装饰线条 -->
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500"></div>

          <div class="relative z-10 p-8 md:p-12 flex flex-col md:flex-row items-center md:items-start gap-10">
            <!-- 头像区域 -->
            <div class="relative group">
              <div class="absolute -inset-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-md opacity-70 group-hover:opacity-100 transition duration-500"></div>
              <div class="w-40 h-40 md:w-48 md:h-48 rounded-full overflow-hidden border-4 border-white dark:border-gray-700 shadow-lg animate__animated animate__fadeIn animate__delay-500ms relative hover:scale-105 transition-transform duration-300 group-hover:border-blue-200 dark:group-hover:border-blue-800">
                <img :src="resumeData.personalInfo.avatar" :alt="resumeData.personalInfo.name" class="absolute inset-0 w-full h-full object-cover object-center" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-4">
                  <span class="text-white text-sm font-medium">个人照片</span>
                </div>
              </div>
            </div>

            <!-- 个人信息 -->
            <div class="flex-1 text-center md:text-left">
              <div class="inline-block">
                <h1 class="text-3xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent mb-2 animate__animated animate__fadeInUp animate__delay-700ms">
                  {{ resumeData.personalInfo.name }}
                  <span class="inline-block ml-2">✨</span>
                </h1>
                <div class="h-1 w-1/3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-1 mb-4"></div>
              </div>

              <h2 class="text-xl md:text-2xl font-medium text-gray-700 dark:text-gray-300 mb-4 animate__animated animate__fadeInUp animate__delay-800ms flex items-center gap-2">
                <span class="inline-block w-3 h-3 bg-green-500 rounded-full animate-pulse"></span>
                {{ resumeData.personalInfo.title }}
              </h2>

              <p class="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl animate__animated animate__fadeInUp animate__delay-900ms leading-relaxed font-description">
                {{ resumeData.personalInfo.bio }}
              </p>

              <!-- 联系方式 -->
              <div class="flex flex-wrap justify-center md:justify-start gap-4 animate__animated animate__fadeInUp animate__delay-1000ms">
                <a v-for="(contact, index) in resumeData.personalInfo.contacts" :key="index"
                   @click="contact.isWechat ? toggleWechatQR() : null"
                   :href="contact.isWechat ? 'javascript:void(0)' : contact.url"
                   :target="contact.external ? '_blank' : '_self'"
                   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200
                          shadow-[0_4px_10px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_10px_rgba(0,0,0,0.3)]
                          hover:shadow-[0_6px_20px_rgba(8,112,184,0.2)] dark:hover:shadow-[0_6px_20px_rgba(66,153,225,0.3)]
                          hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50
                          dark:hover:bg-gradient-to-r dark:hover:from-gray-700 dark:hover:to-gray-800
                          transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 border border-gray-100 dark:border-gray-600"
                   :class="{ 'cursor-pointer': contact.isWechat }">
                  <span v-html="contact.icon" class="text-blue-500 dark:text-blue-400"></span>
                  <span>{{ contact.text }}</span>
                </a>

                <!-- 下载简历按钮 -->
                <button @click="downloadResume"
                   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full
                          bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium
                          shadow-[0_4px_10px_rgba(59,130,246,0.3)]
                          hover:shadow-[0_6px_20px_rgba(59,130,246,0.5)]
                          transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 border border-blue-400/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span>下载简历🎉</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 技能部分 - Inspira UI 风格卡片 -->
      <div class="max-w-5xl mx-auto mb-16 animate__animated animate__fadeInUp animate__delay-1100ms">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              专业技能
            </h2>
            <div class="h-1 w-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-2"></div>
          </div>
          <div class="hidden md:flex space-x-1">
            <span class="w-3 h-3 bg-blue-500 rounded-full animate-ping" style="animation-duration: 2s"></span>
            <span class="w-3 h-3 bg-purple-500 rounded-full animate-ping" style="animation-duration: 2.5s"></span>
            <span class="w-3 h-3 bg-pink-500 rounded-full animate-ping" style="animation-duration: 3s"></span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- 技能卡片 -->
          <div v-for="(category, index) in resumeData.skills" :key="index"
               class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg rounded-2xl
                      shadow-[0_10px_30px_rgba(0,0,0,0.1)] dark:shadow-[0_10px_30px_rgba(0,0,0,0.3)]
                      border border-gray-100/80 dark:border-gray-700/80 p-8
                      hover:shadow-[0_15px_35px_rgba(8,112,184,0.2)] dark:hover:shadow-[0_15px_35px_rgba(66,153,225,0.3)]
                      transition-all duration-500 overflow-hidden relative group
                      transform hover:scale-[102%] hover:-translate-y-1">

            <!-- 装饰元素 -->
            <div class="absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-20" :class="category.bgColor"></div>
            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r" :class="category.barColor"></div>

            <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 relative z-10 flex items-center">
              <span class="inline-block w-2 h-8 rounded-full mr-3" :class="category.barColor.replace('from-', 'bg-')"></span>
              {{ category.name }}
            </h3>

            <div class="space-y-4 relative z-10">
              <div v-for="(skill, skillIndex) in category.items" :key="skillIndex" class="group/skill">
                <div class="flex justify-between mb-2">
                  <span class="text-sm font-semibold text-gray-700 dark:text-gray-300 group-hover/skill:text-blue-600 dark:group-hover/skill:text-blue-400 transition-colors duration-300">{{ skill.name }}</span>
                  <span class="text-sm font-medium px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300">{{ skill.level }}%</span>
                </div>
                <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2.5 overflow-hidden p-0.5">
                  <div class="h-1.5 rounded-full transition-all duration-1000 ease-out group-hover/skill:shadow-[0_0_8px_rgba(59,130,246,0.5)]"
                       :class="category.barColor"
                       :style="{ width: '0%' }"
                       :data-width="skill.level + '%'"
                       ref="skillBar"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- 工作经历 - Inspira UI 风格的时间线 -->
      <div class="max-w-5xl mx-auto mb-16 animate__animated animate__fadeInUp animate__delay-1200ms">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              工作经历
            </h2>
            <div class="h-1 w-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-2"></div>
          </div>
        </div>

        <div class="relative">
          <!-- 时间线 -->
          <div class="absolute left-0 md:left-1/2 top-0 bottom-0 w-1 bg-gradient-to-b from-blue-400 via-purple-500 to-pink-500 rounded-full transform md:translate-x-px"></div>

          <!-- 工作经历项 -->
          <div v-for="(job, index) in resumeData.workExperience" :key="index"
               class="relative mb-16 group"
               :class="{ 'mb-0': index === resumeData.workExperience.length - 1 }">
            <div class="flex flex-col md:flex-row items-center">
              <div class="flex-1" :class="index % 2 === 0 ? 'md:text-right md:pr-12 mb-6 md:mb-0 order-2 md:order-1' : 'md:pl-12 mb-6 md:mb-0 order-2'">
                <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg rounded-2xl
                            shadow-[0_10px_30px_rgba(0,0,0,0.1)] dark:shadow-[0_10px_30px_rgba(0,0,0,0.3)]
                            border border-gray-100/80 dark:border-gray-700/80 p-8
                            hover:shadow-[0_15px_35px_rgba(8,112,184,0.2)] dark:hover:shadow-[0_15px_35px_rgba(66,153,225,0.3)]
                            transition-all duration-500 transform hover:scale-[102%] hover:-translate-y-1"
                     :class="index % 2 === 0 ? 'md:ml-auto' : ''">

                  <!-- 装饰元素 -->
                  <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r" :class="job.badgeColor"></div>

                  <div class="flex items-start mb-4">
                    <div class="flex-1">
                      <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-1 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-300">{{ job.title }}</h3>
                      <h4 class="text-lg font-medium text-gray-600 dark:text-gray-300 mb-1 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                        {{ job.company }}
                      </h4>
                      <div class="text-sm text-blue-600 dark:text-blue-400 font-medium mb-3 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        {{ job.period }}
                      </div>
                    </div>
                  </div>

                  <p class="text-gray-600 dark:text-gray-400 mb-4 leading-relaxed font-description">{{ job.description }}</p>

                  <div class="flex flex-wrap gap-2">
                    <span v-for="(tag, tagIndex) in job.tags" :key="tagIndex"
                          class="px-3 py-1 rounded-full text-xs font-medium transition-all duration-300 transform hover:scale-110 hover:shadow-md"
                          :class="job.tagClasses">
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="w-14 h-14 rounded-full flex items-center justify-center text-white font-bold
                          shadow-[0_0_15px_rgba(59,130,246,0.5)] z-10 transition-all duration-500
                          group-hover:shadow-[0_0_25px_rgba(59,130,246,0.7)] group-hover:scale-110"
                   :class="[job.badgeColor, index % 2 === 0 ? 'order-1 md:order-2' : 'order-1']">
                <span>{{ resumeData.workExperience.length - index }}</span>
              </div>

              <div class="flex-1 hidden md:block" :class="index % 2 === 0 ? 'md:pl-12 order-3' : 'md:text-right md:pr-12 order-3'">
                <!-- 空白区域，保持平衡布局 -->
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 教育经历 - Inspira UI 风格卡片 -->
      <div class="max-w-5xl mx-auto mb-16 animate__animated animate__fadeInUp animate__delay-1250ms">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path d="M12 14l9-5-9-5-9 5 9 5z" />
                <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
              </svg>
              教育经历
            </h2>
            <div class="h-1 w-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-2"></div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div v-for="(edu, index) in resumeData.education" :key="index"
               class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg rounded-2xl
                      shadow-[0_10px_30px_rgba(0,0,0,0.1)] dark:shadow-[0_10px_30px_rgba(0,0,0,0.3)]
                      border border-gray-100/80 dark:border-gray-700/80 p-8
                      hover:shadow-[0_15px_35px_rgba(8,112,184,0.2)] dark:hover:shadow-[0_15px_35px_rgba(66,153,225,0.3)]
                      transition-all duration-500 overflow-hidden relative group
                      transform hover:scale-[102%] hover:-translate-y-1">
            <!-- 装饰元素 -->
            <div class="absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-20" :class="edu.bgColor"></div>
            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-purple-600"></div>

            <div class="relative z-10">
              <div class="flex justify-between items-start mb-5">
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-1 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-300 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path d="M12 14l9-5-9-5-9 5 9 5z" />
                    </svg>
                    {{ edu.degree }}
                  </h3>
                  <h4 class="text-lg font-medium text-gray-600 dark:text-gray-300 mb-1 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    {{ edu.institution }}
                  </h4>
                  <div class="text-sm text-blue-600 dark:text-blue-400 font-medium mb-3 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ edu.period }}
                  </div>
                </div>
              </div>

              <p class="text-gray-600 dark:text-gray-400 mb-4 leading-relaxed font-description">{{ edu.description }}</p>

              <div class="flex flex-wrap gap-2">
                <span v-for="(achievement, achIndex) in edu.achievements" :key="achIndex"
                      class="px-3 py-1 rounded-full text-xs font-medium transition-all duration-300 transform hover:scale-110 hover:shadow-md"
                      :class="edu.tagClasses">
                  {{ achievement }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 作品集 - Inspira UI 风格的网格布局 -->
      <div class="max-w-5xl mx-auto mb-16 animate__animated animate__fadeInUp animate__delay-1300ms">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              项目经历
            </h2>
            <div class="h-1 w-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-2"></div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- 作品项 -->
          <div v-for="(project, index) in resumeData.projects" :key="index"
               class="group bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg rounded-2xl
                      shadow-[0_10px_30px_rgba(0,0,0,0.1)] dark:shadow-[0_10px_30px_rgba(0,0,0,0.3)]
                      border border-gray-100/80 dark:border-gray-700/80
                      overflow-hidden hover:shadow-[0_15px_35px_rgba(8,112,184,0.2)] dark:hover:shadow-[0_15px_35px_rgba(66,153,225,0.3)]
                      transition-all duration-500 transform hover:-translate-y-2">
            <div class="relative overflow-hidden aspect-video">
              <img :src="project.image" :alt="project.title + ' 缩略图'" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
              <div class="absolute inset-0 bg-gradient-to-t from-black/90 to-black/70 opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center">
                <button @click.stop="showProjectDetails(project)" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-full transition-all duration-300 transform hover:scale-105 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  查看详情
                </button>
              </div>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-300">{{ project.title }}</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2 text-sm font-description">{{ project.description }}</p>
              <div class="flex flex-wrap gap-2">
                <span v-for="(tech, techIndex) in project.technologies" :key="techIndex"
                      class="px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 text-xs font-medium
                             transition-all duration-300 transform hover:scale-110 hover:shadow-sm">
                  {{ tech }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 联系部分 - Inspira UI 风格的卡片 -->
      <div class="max-w-5xl mx-auto mb-16 animate__animated animate__fadeInUp animate__delay-1400ms">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              联系我
            </h2>
            <div class="h-1 w-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-2"></div>
          </div>
        </div>

        <div class="relative overflow-hidden rounded-3xl bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl
                    shadow-[0_20px_50px_rgba(8,_112,_184,_0.2)] dark:shadow-[0_20px_50px_rgba(66,_153,_225,_0.2)]
                    border border-blue-100/50 dark:border-blue-900/50
                    hover:shadow-[0_25px_60px_rgba(8,_112,_184,_0.3)] dark:hover:shadow-[0_25px_60px_rgba(66,_153,_225,_0.3)]
                    transition-all duration-500 transform hover:scale-[101%]">
          <!-- 背景装饰 -->
          <div class="absolute -top-24 -left-24 w-64 h-64 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full opacity-20 blur-3xl animate-pulse"></div>
          <div class="absolute -bottom-24 -right-24 w-64 h-64 bg-gradient-to-tr from-pink-400 to-orange-500 rounded-full opacity-20 blur-3xl animate-pulse" style="animation-delay: 1s"></div>
          <div class="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-purple-50/50 dark:from-blue-900/20 dark:to-purple-900/20 opacity-50"></div>

          <!-- 装饰线条 -->
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500"></div>

          <div class="relative z-10 p-10 md:p-16 text-center">
            <div class="inline-block mb-6 p-4 rounded-full bg-blue-50 dark:bg-blue-900/30">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-blue-500 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>

            <h3 class="text-2xl md:text-3xl font-bold text-gray-800 dark:text-gray-100 mb-4">让我们一起创造精彩</h3>

            <p class="text-gray-600 dark:text-gray-300 mb-10 max-w-2xl mx-auto leading-relaxed font-description text-sm">
              {{ resumeData.contactSection.message }}
            </p>

            <a :href="resumeData.contactSection.emailLink"
               class="inline-flex items-center justify-center gap-3 px-8 py-4 rounded-full
                      bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium
                      shadow-[0_10px_20px_rgba(59,130,246,0.3)]
                      hover:shadow-[0_15px_30px_rgba(59,130,246,0.5)]
                      transition-all duration-300 transform hover:-translate-y-1 hover:scale-105"
               @click.prevent="sendEmail">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              {{ resumeData.contactSection.buttonText }}
            </a>

            <div class="mt-10 flex justify-center space-x-6">
              <a v-for="(contact, index) in resumeData.personalInfo.contacts.filter(c => c.external)" :key="index"
                 :href="contact.url" target="_blank" rel="noopener noreferrer"
                 class="text-gray-500 hover:text-blue-500 dark:text-gray-400 dark:hover:text-blue-400 transition-colors duration-300">
                <span v-html="contact.icon" class="w-6 h-6"></span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- 项目详情模态对话框 -->
      <transition name="modal">
        <div v-if="selectedProject" class="fixed inset-0 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="closeProjectDetails">
        <div class="bg-white dark:bg-gray-800 rounded-2xl max-w-3xl w-full max-h-[95vh] overflow-hidden shadow-2xl">
          <!-- 模态框头部 -->
          <div class="p-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white flex justify-between items-center">
            <h3 class="text-xl font-bold">{{ selectedProject.title }}</h3>
            <button @click="closeProjectDetails" class="p-1 rounded-full hover:bg-white/20 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 模态框内容 -->
          <div class="overflow-y-auto max-h-[calc(90vh-120px)]">
            <!-- 项目图片轮播 -->
            <div class="relative w-full h-56 md:h-72 lg:h-80 overflow-hidden bg-gray-100 dark:bg-gray-900">
              <!-- 轮播图片 -->
              <transition-group name="fade" tag="div" class="h-full flex items-center justify-center">
                <img
                  v-for="(image, index) in selectedProject.images"
                  :key="image"
                  :src="image"
                  :alt="`${selectedProject.title} - 图片 ${index + 1}`"
                  class="absolute inset-0 max-w-full max-h-full object-contain transition-opacity duration-500 m-auto"
                  :class="{ 'opacity-0': currentImageIndex !== index, 'opacity-100': currentImageIndex === index }"
                />
              </transition-group>

              <!-- 渐变遮罩 -->
              <div class="absolute inset-0 bg-gradient-to-b from-transparent to-black/50 flex items-end">
                <div class="p-4 w-full">
                  <h3 class="text-xl font-bold text-white drop-shadow-md">{{ selectedProject.title }}</h3>
                </div>
              </div>

              <!-- 轮播控制按钮 -->
              <div class="absolute inset-x-0 top-1/2 flex justify-between items-center px-4 -translate-y-1/2">
                <button @click="prevImage" class="w-10 h-10 rounded-full bg-black/30 text-white flex items-center justify-center hover:bg-black/50 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <button @click="nextImage" class="w-10 h-10 rounded-full bg-black/30 text-white flex items-center justify-center hover:bg-black/50 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>

              <!-- 轮播指示器 -->
              <div class="absolute bottom-2 inset-x-0 flex justify-center gap-2">
                <button
                  v-for="(_, index) in selectedProject.images"
                  :key="index"
                  @click="currentImageIndex = index; resetSlideshowTimer();"
                  class="w-2 h-2 rounded-full transition-all duration-300"
                  :class="currentImageIndex === index ? 'bg-white scale-125' : 'bg-white/50 hover:bg-white/80'"
                ></button>
              </div>
            </div>

            <!-- 项目内容 -->
            <div class="p-6">
              <!-- 项目描述 -->
              <div class="mb-6">
                <h4 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-2">项目描述</h4>
                <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed font-description text-sm">{{ selectedProject.description }}</p>
              </div>

              <!-- 技术栈 -->
              <div>
                <h4 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-2">技术栈</h4>
                <div class="flex flex-wrap gap-2">
                  <span v-for="(tech, techIndex) in selectedProject.technologies" :key="techIndex"
                        class="px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 text-sm font-medium">
                    {{ tech }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 模态框底部 -->
          <div class="p-4 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-100 dark:border-gray-700 flex justify-end">
            <button @click="closeProjectDetails"
                    class="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">
              关闭
            </button>
          </div>
        </div>
      </div>
      </transition>

      <!-- 微信二维码弹窗 -->
      <transition name="modal">
        <div v-if="showWechatQR" class="fixed inset-0  backdrop-blur-sm z-50 overflow-hidden m-0 p-0" @click.self="showWechatQR = false">
          <div class="absolute inset-0 flex items-start justify-center p-[13rem] ">
            <div class="bg-white dark:bg-gray-800 rounded-xl max-w-xs w-full overflow-hidden ">
              <!-- 弹窗头部 -->
              <div class="py-2 px-3 bg-gradient-to-r from-blue-500 to-green-500 text-white shadow-md relative">
                <h3 class="text-base font-bold inline-block">微信扫码</h3>
                <button @click="showWechatQR = false" class="p-1 rounded-full hover:bg-white/20 transition-colors absolute right-2 top-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- 弹窗内容 -->
              <div class="p-3 text-center">
                <div class="w-36 h-36 bg-white rounded-lg shadow-inner mb-2 overflow-hidden mx-auto p-3 flex items-center justify-center">
                  <img src="/images/wechat-qr.png" alt="微信二维码" class="max-w-full max-h-full object-contain" style="width: 10%;" />
                </div>
                <p class="text-gray-700 dark:text-gray-300 text-xs">扫码添加微信（备注来意）</p>
              </div>

              <!-- 弹窗底部 -->
              <div class="py-2 px-3 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-100 dark:border-gray-700 text-right">
                <button @click="showWechatQR = false" class="px-2 py-1 text-xs bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">
                  关闭
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- 页脚 -->
      <footer class="max-w-5xl mx-auto pb-12 text-center">
        <div class="h-px w-full bg-gradient-to-r from-transparent via-gray-300 dark:via-gray-700 to-transparent mb-8"></div>
        <p class="text-gray-500 dark:text-gray-400 font-medium">
          {{ resumeData.footer }}
        </p>
        <p class="text-sm text-gray-400 dark:text-gray-500 mt-2">使用 Inspira UI 风格设计</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import Navbar from '@/components/layout/Navbar.vue';
import confetti from 'canvas-confetti';
import { aboutPageApi } from '@/api';

// 项目详情相关状态
const selectedProject = ref(null);
const currentImageIndex = ref(0);
const slideInterval = ref(null);

// 微信二维码弹窗状态
const showWechatQR = ref(false);

// 显示项目详情
const showProjectDetails = (project) => {


  selectedProject.value = project;
  currentImageIndex.value = 0; // 重置图片索引
  // 防止背景滚动
  document.body.style.overflow = 'hidden';
  setTimeout(() => {
    window.scrollTo({ top: 1080, behavior: 'smooth' });
  }, 150);
  // 启动自动轮播
  startSlideshow();
  triggerConfetti();
};

// 关闭项目详情
const closeProjectDetails = () => {
  selectedProject.value = null;
  // 恢复背景滚动
  document.body.style.overflow = '';
  window.scrollTo({ top: 1800, behavior: 'smooth' });
  // 停止自动轮播
  stopSlideshow();
};

// 切换到上一张图片
const prevImage = () => {
  if (!selectedProject.value) return;
  const imagesLength = selectedProject.value.images.length;
  currentImageIndex.value = (currentImageIndex.value - 1 + imagesLength) % imagesLength;
  resetSlideshowTimer();
};

// 切换到下一张图片
const nextImage = () => {
  if (!selectedProject.value) return;
  const imagesLength = selectedProject.value.images.length;
  currentImageIndex.value = (currentImageIndex.value + 1) % imagesLength;
  resetSlideshowTimer();
};

// 启动自动轮播
const startSlideshow = () => {
  stopSlideshow(); // 先停止之前的轮播
  slideInterval.value = setInterval(() => {
    nextImage();
  }, 5000); // 5秒切换一次
};

// 停止自动轮播
const stopSlideshow = () => {
  if (slideInterval.value) {
    clearInterval(slideInterval.value);
    slideInterval.value = null;
  }
};

// 重置轮播计时器
const resetSlideshowTimer = () => {
  stopSlideshow();
  startSlideshow();
};

// 初始化技能进度条动画
const initSkillBars = async () => {
  await nextTick();

  // 使用 Intersection Observer 检测进度条是否可见
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // 当进度条可见时设置实际宽度
        const bar = entry.target;
        const width = bar.getAttribute('data-width');
        setTimeout(() => {
          bar.style.width = width;
        }, 300); // 延迟一下以创造逐个动画效果

        // 一旦动画完成，停止观察
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.1 });

  // 获取所有进度条元素
  const bars = document.querySelectorAll('[data-width]');
  bars.forEach(bar => {
    observer.observe(bar);
  });
};

// 下载简历并触发五彩纸屑效果
const downloadResume = async () => {
  try {
    // 触发五彩纸屑效果
    triggerConfetti();

    // 下载简历文件
    const resumeUrl = '/简历.pdf';

    // 使用fetch获取文件并直接下载
    const response = await fetch(resumeUrl);
    const blob = await response.blob();

    // 创建一个指向blob的URL
    const blobUrl = window.URL.createObjectURL(blob);

    // 创建一个链接元素并设置属性
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = `${resumeData.value.personalInfo.name}_简历.pdf`;
    link.style.display = 'none';

    // 添加到DOM并模拟点击
    document.body.appendChild(link);
    link.click();

    // 清理
    setTimeout(() => {
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    }, 100);
  } catch (error) {
    console.error('下载简历时出错:', error);
    // 如果出错，回退到原始的下载方式
    const link = document.createElement('a');
    link.href = '/简历.pdf';
    link.download = `${resumeData.value.personalInfo.name}_简历.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

// 五彩纸屑效果
const triggerConfetti = () => {
  // 两侧彩带炮效果
  const end = Date.now() + 1000; // 1秒后结束

  // 左侧彩带炮
  const leftConfetti = () => {
    confetti({
      particleCount: 20,
      angle: 60,
      spread: 70,
      origin: { x: 0, y: 0.6 },
      colors: ['#5D8BF4', '#4649FF', '#7DE5ED', '#81C6E8', '#1F4690'],
      shapes: ['square', 'circle'],
      scalar: 1.2
    });

    if (Date.now() < end) {
      requestAnimationFrame(leftConfetti);
    }
  };

  // 右侧彩带炮
  const rightConfetti = () => {
    confetti({
      particleCount: 20,
      angle: 120,
      spread: 70,
      origin: { x: 1, y: 0.6 },
      colors: ['#FF9F29', '#EC38BC', '#7303C0', '#FF5B00', '#38E54D'],
      shapes: ['square', 'circle'],
      scalar: 1.2
    });

    if (Date.now() < end) {
      requestAnimationFrame(rightConfetti);
    }
  };

  // 中间的彩带炮
  confetti({
    particleCount: 100,
    spread: 100,
    origin: { y: 0.5 },
    colors: ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'],
    disableForReducedMotion: true
  });

  // 启动两侧彩带炮
  leftConfetti();
  rightConfetti();
};

// 添加键盘事件监听器
const handleKeyDown = (e) => {
  if (e.key === 'Escape') {
    if (selectedProject.value) {
      closeProjectDetails();
    }
    if (showWechatQR.value) {
      showWechatQR.value = false;
    }
  }
};

// 显示微信二维码
const toggleWechatQR = () => {
  showWechatQR.value = !showWechatQR.value;
  triggerConfetti();
};

// 发送邮件
const sendEmail = () => {
  // 获取邮件链接
  const emailLink = resumeData.value.contactSection.emailLink;

  // 如果链接以 mailto: 开头，直接打开邮件客户端
  if (emailLink.startsWith('mailto:')) {
    window.location.href = emailLink;
  } else {
    // 否则，打开链接
    window.open(emailLink, '_blank');
  }

  // 触发五彩纸屑效果
  triggerConfetti();
};

// 从后端获取 About 页面内容
const fetchAboutPageContent = async () => {
  try {
    const response = await aboutPageApi.getAboutPage();
    console.log('获取到的 About 页面数据:', response);
    if (response && response.content) {
      resumeData.value = response.content;
    }
  } catch (error) {
    console.error('获取 About 页面内容失败:', error);
  }
};

onMounted(async () => {
  // 获取 About 页面内容
  await fetchAboutPageContent();

  // 初始化技能进度条
  initSkillBars();

  // 添加键盘事件监听器
  window.addEventListener('keydown', handleKeyDown);
});

// 组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});

const resumeData = ref({
  resumeFile: '/简历.pdf', // 简历文件路径
  personalInfo: {
    name: '陆炳任',
    title: '后端开发',
    avatar: '/images/image.png',
    bio: '性格开朗、稳重、有活力，待人热情、真诚；对待工作认真负责，善于沟通、协调有较强的组织能力与团队精神；上进心强、勤于学习能不断提高自身的能力与综合素质，参与开发多个项目。',
    contacts: [
      {
        icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
        text: 'Brownlu0911@gmail.com',
        url: 'mailto:Brownlu0911@gmail.com',
        external: false
      },
      {
        icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>',
        text: '18154521838',
        url: 'tel:+8618154521838',
        external: false
      },
      {
        icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
        text: 'GitHub',
        url: 'https://github.com',
        external: true
      },
      {
        icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178A1.17 1.17 0 0 1 4.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178 1.17 1.17 0 0 1-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 0 1 .598.082l1.584.926a.272.272 0 0 0 .14.047c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 0 1-.023-.156.49.49 0 0 1 .201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89c-.135-.01-.27-.027-.407-.03zm-2.53 3.274c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.969-.982z"/></svg>',
        text: '微信',
        url: 'javascript:void(0)',
        external: false,
        isWechat: true
      },
      // {
      //   icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>',
      //   text: 'Instagram',
      //   url: 'https://instagram.com',
      //   external: true
      // }
    ]
  },
  skills: [
    {
      name: '前端开发',
      bgColor: 'bg-blue-500/10 rounded-full blur-xl group-hover:bg-blue-500/20 transition-all duration-300',
      barColor: 'bg-gradient-to-r from-blue-500 to-indigo-600',
      items: [
        { name: 'Vue.js', level: 95 },
        { name: 'typeScript', level: 85 },
        { name: 'CSS/SCSS', level: 90 }
      ]
    },
    {
      name: '后端技术',
      bgColor: 'bg-green-500/10 rounded-full blur-xl group-hover:bg-green-500/20 transition-all duration-300',
      barColor: 'bg-gradient-to-r from-green-500 to-teal-600',
      items: [
        { name: 'Python', level: 80 },
        { name: 'Java', level: 80 },
        { name: 'C/C++', level: 75 },
        { name: 'SpringBoot', level: 75 },
        { name: 'MySQL', level: 70 }
      ]
    },
    {
      name: '工具与方法',
      bgColor: 'bg-purple-500/10 rounded-full blur-xl group-hover:bg-purple-500/20 transition-all duration-300',
      barColor: 'bg-gradient-to-r from-purple-500 to-pink-600',
      items: [
        { name: 'Git/GitHub', level: 90 },
        { name: 'Linux', level: 85 },
        { name: 'Docker/podman', level: 85 },
        { name: 'Maven', level: 75 }
      ]
    }
  ],
  workExperience: [
    // {
    //   title: '高级前端开发工程师',
    //   company: '科技创新有限公司',
    //   period: '2020年 - 至今',
    //   description: '负责公司核心产品的前端架构设计和开发，优化用户体验和性能，指导初级开发人员，参与技术决策。',
    //   tags: ['Vue.js', 'TypeScript', 'Tailwind CSS'],
    //   tagClasses: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200',
    //   badgeColor: 'bg-gradient-to-r from-blue-500 to-indigo-600'
    // },
    // {
    //   title: '前端开发工程师',
    //   company: '互联网科技有限公司',
    //   period: '2018年 - 2020年',
    //   description: '负责公司电商平台的前端开发，实现响应式设计，优化加载速度，提升用户转化率。',
    //   tags: ['React', 'Redux', 'SCSS'],
    //   tagClasses: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200',
    //   badgeColor: 'bg-gradient-to-r from-green-500 to-teal-600'
    // },
    {
      title: '后端开发实习生',
      company: '武汉正奇云网络科技有限公司',
      period: '2024年暑期实习',
      description: '参与公司官网和内部管理系统的后端接口开发，学习后端技术栈和开发流程。',
      tags: ['Java', 'SpringBoot', 'MySQL'],
      tagClasses: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200',
      badgeColor: 'bg-gradient-to-r from-purple-500 to-pink-600'
    }
  ],
  education: [
    {
      degree: '计算机科学与技术 学士',
      institution: '中南民族大学',
      period: '2021年 - 2025年',
      description: '主修后端开发相关课程，在校期间参与多个实际项目开发，课程设计类课程均分为90，拥有很强的动手能力和工程项目实践经验。并积极参加竞赛，是学校超算实验室团队的成员。',
      achievements: ['GPA 3.2/5.0', 'ASC24竞赛二等奖', '优秀志愿者','CET-4','蓝桥杯三等奖'],
      bgColor: 'bg-purple-500/10',
      periodClass: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200',
      tagClasses: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200'
    },
    // {
    //   degree: '前端开发与设计 证书',
    //   institution: '国际网络学院',
    //   period: '2016年 - 2017年',
    //   description: '在学习期间获得前端开发专业证书，掌握现代前端框架和工具。',
    //   achievements: ['优秀学员', '最佳项目奖'],
    //   bgColor: 'bg-blue-500/10',
    //   periodClass: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200',
    //   tagClasses: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200'
    // }
  ],
  projects: [
    {
      title: 'His大健康体检系统',
      image: '/images/project-1.png',
      images: [
        '/images/project-1.png',
        '/images/project-2.png',
        '/images/project-3.png',
        '/images/project-4.png'
      ],
      description: `  HIS 大健康系统是为 体检中心开发并实施的体检系统。体检人可以在业务端系统购买
体检套餐，并且预约体检日期，也可以下载到自己的体检报告；体检中心工作人员在
MIS 端可以管理各个模块的业务数据，并且为体检人完成签到、打印引导单等服务；
体检医生在 MIS 系统中可以为体检人录入体检结果。
HIS 大健康系统采用了 6 节点的 MySQL 集群，使用 MyCat 管理数据库集群。由于实
现了读写分离，数据库 IO 性能得到了大幅提升。在抗风险测试中，6 个 MySQL 节
点，最多可以宕机 4 个，数据库集群依然可以正常工作，数据不受任何影响，而且宕
机节点重新上线之后数据会自动同步。
本系统的支付模块采用了支付宝支付，不仅可以实现付款，还实现了退款。为了避免后
端系统没有收到付款或退款结果，大健康系统采用了主动查询付款或退款结果，然后同
步更新订单状态。作为一种方案的补充，系统还使用了定时器技术，定期核对订单的
付款和退款结果，并且关闭超期未付款的本订单。
为了提升商品页面详情内容加载速度，大健康系统使用了 SpringCache 技术，自动对
常用商品缓存。客户打开商品页面，后端系统直接从 Redis 缓存中提取商品信息，从
而降低了数据库的负载，提升了数据读取速度。
`,
      technologies: ['SpringBoot', 'MySQL集群', 'Vue3','Redis','MongoDB']
    },
    {
      title: 'EHO互联网医疗系统',
      image: '/images/project2-1.png',
      images: [
        '/images/project2-1.png',
        '/images/project2-2.png',
        '/images/project2-3.png',
      ],
      description: `EHO 医疗系统采用了前后端分离的架构设计。后端项目由 Maven 工具搭建，采用
MyBatis 作为持久层框架。由于医疗系统产生的数据量非常大，为了减少数据库分库分
表和冷热数据归档的维护，本项目采用了 HBase 作为数据库，Phoenix 作为 SQL
层，实现了单表存储百亿行记录的情况下，读写性能不输于 MySQL`,
      technologies: ['HBase', 'MyBatis', 'Maven']
    },
    {
      title: 'ASC24世界大学生超算竞赛 团体二等奖',
      image: '/images/award1.jpg',
      images: [
        '/images/award1.jpg',

      ],
      description: `荣获团体二等奖，主要负责最后一题的优化包括：
1. OpenCAEPoro的部署工作
2. 修改动态内存分配方式为一次性的静态分配，减少内存分配时间
3. 更改编译方式为O3优化
4. 平台适配工作（使用华为的Kgcc与Hmpi）`,
      technologies: ['React Native', 'Firebase']
    }
  ],
  contactSection: {
    message: '如果您对我的经历项目感兴趣，或者有任何合作机会，欢迎随时与我联系。我期待能够与您一起创造出色的数字体验和价值。🎉',
    emailLink: 'mailto:brownlu0911@gmail.com',
    buttonText: '发送邮件'
  },
  footer: '© 2025 Brown Lu · 后端开发 · 保留所有权利'
});
</script>

<style scoped>
/* 自定义描述文本字体 */
.font-description {
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 0.9rem; /* 缩小字体大小 */
  letter-spacing: 0.01em;
  line-height: 1.5;
}

/* 保持原有样式不变 */
.bg-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23000000' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
}

/* 轮播图片淡入淡出效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 模态框动画 */
@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-enter-active {
  animation: modalFadeIn 0.3s ease-out;
}

.modal-leave-active {
  animation: modalFadeIn 0.3s ease-out reverse;
}
</style>