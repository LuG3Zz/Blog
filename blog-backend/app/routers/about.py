"""
About页面路由模块
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.core import security
from app.core.permissions import is_admin
from app.schemas.about import AboutPageResponse, AboutPageCreate, AboutPageUpdate
from app.services.about_service import AboutPageService
from app.models.user import User

router = APIRouter(prefix="/about", tags=["about"])

@router.get("")
async def get_about_page(db: Session = Depends(get_db)):
    """
    获取About页面内容
    """
    about_page = AboutPageService.get_about_page(db)
    if not about_page:
        # 如果不存在，创建一个默认的
        default_content = {
            "resumeFile": "/简历.pdf",
            "personalInfo": {
                "name": "陆炳任",
                "title": "后端开发",
                "avatar": "/images/image.png",
                "bio": "性格开朗、稳重、有活力，待人热情、真诚；对待工作认真负责，善于沟通、协调有较强的组织能力与团队精神；上进心强、勤于学习能不断提高自身的能力与综合素质，参与开发多个项目。",
                "contacts": [
                    {
                        "icon": "<svg xmlns=\"http://www.w3.org/2000/svg\" class=\"h-5 w-5\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z\" /></svg>",
                        "text": "Brownlu0911@gmail.com",
                        "url": "mailto:Brownlu0911@gmail.com",
                        "external": False
                    },
                    {
                        "icon": "<svg xmlns=\"http://www.w3.org/2000/svg\" class=\"h-5 w-5\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z\" /></svg>",
                        "text": "18154521838",
                        "url": "tel:+8618154521838",
                        "external": False
                    },
                    {
                        "icon": "<svg xmlns=\"http://www.w3.org/2000/svg\" class=\"h-5 w-5\" fill=\"currentColor\" viewBox=\"0 0 24 24\"><path d=\"M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z\"/></svg>",
                        "text": "GitHub",
                        "url": "https://github.com",
                        "external": True
                    },
                    {
                        "icon": "<svg xmlns=\"http://www.w3.org/2000/svg\" class=\"h-5 w-5\" fill=\"currentColor\" viewBox=\"0 0 24 24\"><path d=\"M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178A1.17 1.17 0 0 1 4.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178 1.17 1.17 0 0 1-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 0 1 .598.082l1.584.926a.272.272 0 0 0 .14.047c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 0 1-.023-.156.49.49 0 0 1 .201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89c-.135-.01-.27-.027-.407-.03zm-2.53 3.274c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.969-.982z\"/></svg>",
                        "text": "微信",
                        "url": "javascript:void(0)",
                        "external": False,
                        "isWechat": True
                    }
                ]
            },
            "skills": [
                {
                    "name": "前端开发",
                    "bgColor": "bg-blue-500/10 rounded-full blur-xl group-hover:bg-blue-500/20 transition-all duration-300",
                    "barColor": "bg-gradient-to-r from-blue-500 to-indigo-600",
                    "items": [
                        { "name": "Vue.js", "level": 95 },
                        { "name": "typeScript", "level": 85 },
                        { "name": "CSS/SCSS", "level": 90 }
                    ]
                },
                {
                    "name": "后端技术",
                    "bgColor": "bg-green-500/10 rounded-full blur-xl group-hover:bg-green-500/20 transition-all duration-300",
                    "barColor": "bg-gradient-to-r from-green-500 to-teal-600",
                    "items": [
                        { "name": "Python", "level": 80 },
                        { "name": "Java", "level": 80 },
                        { "name": "C/C++", "level": 75 },
                        { "name": "SpringBoot", "level": 75 },
                        { "name": "MySQL", "level": 70 }
                    ]
                },
                {
                    "name": "工具与方法",
                    "bgColor": "bg-purple-500/10 rounded-full blur-xl group-hover:bg-purple-500/20 transition-all duration-300",
                    "barColor": "bg-gradient-to-r from-purple-500 to-pink-600",
                    "items": [
                        { "name": "Git/GitHub", "level": 90 },
                        { "name": "Linux", "level": 85 },
                        { "name": "Docker/podman", "level": 85 },
                        { "name": "Maven", "level": 75 }
                    ]
                }
            ],
            "workExperience": [
                {
                    "title": "后端开发实习生",
                    "company": "武汉正奇云网络科技有限公司",
                    "period": "2024年暑期实习",
                    "description": "参与公司官网和内部管理系统的后端接口开发，学习后端技术栈和开发流程。",
                    "tags": ["Java", "SpringBoot", "MySQL"],
                    "tagClasses": "bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200",
                    "badgeColor": "bg-gradient-to-r from-purple-500 to-pink-600"
                }
            ],
            "education": [
                {
                    "degree": "计算机科学与技术 学士",
                    "institution": "中南民族大学",
                    "period": "2021年 - 2025年",
                    "description": "主修后端开发相关课程，在校期间参与多个实际项目开发，课程设计类课程均分为90，拥有很强的动手能力和工程项目实践经验。并积极参加竞赛，是学校超算实验室团队的成员。",
                    "achievements": ["GPA 3.2/5.0", "ASC24竞赛二等奖", "优秀志愿者","CET-4","蓝桥杯三等奖"],
                    "bgColor": "bg-purple-500/10",
                    "periodClass": "bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200",
                    "tagClasses": "bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200"
                }
            ],
            "projects": [
                {
                    "title": "His大健康体检系统",
                    "image": "/images/project-1.png",
                    "images": [
                        "/images/project-1.png",
                        "/images/project-2.png",
                        "/images/project-3.png",
                        "/images/project-4.png"
                    ],
                    "description": "HIS 大健康系统是为 体检中心开发并实施的体检系统。体检人可以在业务端系统购买体检套餐，并且预约体检日期，也可以下载到自己的体检报告；体检中心工作人员在MIS 端可以管理各个模块的业务数据，并且为体检人完成签到、打印引导单等服务；体检医生在 MIS 系统中可以为体检人录入体检结果。",
                    "technologies": ["SpringBoot", "MySQL集群", "Vue3","Redis","MongoDB"]
                },
                {
                    "title": "EHO互联网医疗系统",
                    "image": "/images/project2-1.png",
                    "images": [
                        "/images/project2-1.png",
                        "/images/project2-2.png",
                        "/images/project2-3.png"
                    ],
                    "description": "EHO 医疗系统采用了前后端分离的架构设计。后端项目由 Maven 工具搭建，采用MyBatis 作为持久层框架。由于医疗系统产生的数据量非常大，为了减少数据库分库分表和冷热数据归档的维护，本项目采用了 HBase 作为数据库，Phoenix 作为 SQL层，实现了单表存储百亿行记录的情况下，读写性能不输于 MySQL",
                    "technologies": ["HBase", "MyBatis", "Maven"]
                },
                {
                    "title": "ASC24世界大学生超算竞赛 团体二等奖",
                    "image": "/images/award1.jpg",
                    "images": [
                        "/images/award1.jpg"
                    ],
                    "description": "荣获团体二等奖，主要负责最后一题的优化包括：1. OpenCAEPoro的部署工作 2. 修改动态内存分配方式为一次性的静态分配，减少内存分配时间 3. 更改编译方式为O3优化 4. 平台适配工作（使用华为的Kgcc与Hmpi）",
                    "technologies": ["React Native", "Firebase"]
                }
            ],
            "contactSection": {
                "message": "如果您对我的经历项目感兴趣，或者有任何合作机会，欢迎随时与我联系。我期待能够与您一起创造出色的数字体验和价值。🎉",
                "emailLink": "mailto:brownlu0911@gmail.com",
                "buttonText": "发送邮件"
            },
            "footer": "© 2025 Brown Lu · 后端开发 · 保留所有权利"
        }
        about_page = AboutPageService.create_about_page(db, default_content)

    # 将 about_page 转换为字典
    result = {
        "id": about_page.id,
        "created_at": about_page.created_at,
        "updated_at": about_page.updated_at,
        "content": about_page.content
    }

    # 确保 content 字段包含所有必要的字段
    if "skills" not in result["content"]:
        result["content"]["skills"] = [
            {
                "name": "前端开发",
                "bgColor": "bg-blue-500/10 rounded-full blur-xl group-hover:bg-blue-500/20 transition-all duration-300",
                "barColor": "bg-gradient-to-r from-blue-500 to-indigo-600",
                "items": [
                    { "name": "Vue.js", "level": 95 },
                    { "name": "typeScript", "level": 85 },
                    { "name": "CSS/SCSS", "level": 90 }
                ]
            },
            {
                "name": "后端技术",
                "bgColor": "bg-green-500/10 rounded-full blur-xl group-hover:bg-green-500/20 transition-all duration-300",
                "barColor": "bg-gradient-to-r from-green-500 to-teal-600",
                "items": [
                    { "name": "Python", "level": 80 },
                    { "name": "Java", "level": 80 },
                    { "name": "C/C++", "level": 75 },
                    { "name": "SpringBoot", "level": 75 },
                    { "name": "MySQL", "level": 70 }
                ]
            },
            {
                "name": "工具与方法",
                "bgColor": "bg-purple-500/10 rounded-full blur-xl group-hover:bg-purple-500/20 transition-all duration-300",
                "barColor": "bg-gradient-to-r from-purple-500 to-pink-600",
                "items": [
                    { "name": "Git/GitHub", "level": 90 },
                    { "name": "Linux", "level": 85 },
                    { "name": "Docker/podman", "level": 85 },
                    { "name": "Maven", "level": 75 }
                ]
            }
        ]

    # 确保 education 字段有值
    if "education" not in result["content"] or not result["content"]["education"]:
        result["content"]["education"] = [
            {
                "degree": "计算机科学与技术 学士",
                "institution": "中南民族大学",
                "period": "2021年 - 2025年",
                "description": "主修后端开发相关课程，在校期间参与多个实际项目开发，课程设计类课程均分为90，拥有很强的动手能力和工程项目实践经验。并积极参加竞赛，是学校超算实验室团队的成员。",
                "achievements": ["GPA 3.2/5.0", "ASC24竞赛二等奖", "优秀志愿者", "CET-4", "蓝桥杯三等奖"],
                "bgColor": "bg-purple-500/10",
                "periodClass": "bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200",
                "tagClasses": "bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200"
            }
        ]

    # 确保 workExperience 字段有值
    if "workExperience" not in result["content"] or not result["content"]["workExperience"]:
        result["content"]["workExperience"] = [
            {
                "title": "后端开发实习生",
                "company": "武汉正奇云网络科技有限公司",
                "period": "2024年暑期实习",
                "description": "参与公司官网和内部管理系统的后端接口开发，学习后端技术栈和开发流程。",
                "tags": ["Java", "SpringBoot", "MySQL"],
                "tagClasses": "bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200",
                "badgeColor": "bg-gradient-to-r from-purple-500 to-pink-600"
            }
        ]

    # 确保 projects 字段有值
    if "projects" not in result["content"] or not result["content"]["projects"]:
        result["content"]["projects"] = [
            {
                "title": "His大健康体检系统",
                "image": "/images/project-1.png",
                "images": [
                    "/images/project-1.png",
                    "/images/project-2.png",
                    "/images/project-3.png",
                    "/images/project-4.png"
                ],
                "description": "HIS 大健康系统是为体检中心开发并实施的体检系统。体检人可以在业务端系统购买体检套餐，并且预约体检日期，也可以下载到自己的体检报告；体检中心工作人员在MIS 端可以管理各个模块的业务数据，并且为体检人完成签到、打印引导单等服务；体检医生在 MIS 系统中可以为体检人录入体检结果。",
                "technologies": ["SpringBoot", "MySQL集群", "Vue3", "Redis", "MongoDB"]
            },
            {
                "title": "EHO互联网医疗系统",
                "image": "/images/project2-1.png",
                "images": [
                    "/images/project2-1.png",
                    "/images/project2-2.png",
                    "/images/project2-3.png"
                ],
                "description": "EHO 医疗系统采用了前后端分离的架构设计。后端项目由 Maven 工具搭建，采用MyBatis 作为持久层框架。由于医疗系统产生的数据量非常大，为了减少数据库分库分表和冷热数据归档的维护，本项目采用了 HBase 作为数据库，Phoenix 作为 SQL层，实现了单表存储百亿行记录的情况下，读写性能不输于 MySQL",
                "technologies": ["HBase", "MyBatis", "Maven"]
            },
            {
                "title": "ASC24世界大学生超算竞赛 团体二等奖",
                "image": "/images/award1.jpg",
                "images": [
                    "/images/award1.jpg"
                ],
                "description": "荣获团体二等奖，主要负责最后一题的优化包括：1. OpenCAEPoro的部署工作 2. 修改动态内存分配方式为一次性的静态分配，减少内存分配时间 3. 更改编译方式为O3优化 4. 平台适配工作（使用华为的Kgcc与Hmpi）",
                "technologies": ["React Native", "Firebase"]
            }
        ]

    # 确保 personalInfo 字段有值
    if "personalInfo" not in result["content"] or not result["content"]["personalInfo"]:
        result["content"]["personalInfo"] = {
            "name": "陆炳任",
            "title": "后端开发",
            "avatar": "/images/image.png",
            "bio": "性格开朗、稳重、有活力，待人热情、真诚；对待工作认真负责，善于沟通、协调有较强的组织能力与团队精神；上进心强、勤于学习能不断提高自身的能力与综合素质，参与开发多个项目。",
            "contacts": []
        }

    # 确保 contacts 字段有值
    if "contacts" not in result["content"]["personalInfo"] or not result["content"]["personalInfo"]["contacts"]:
        result["content"]["personalInfo"]["contacts"] = [
            {
                "icon": '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
                "text": "Brownlu0911@gmail.com",
                "url": "mailto:Brownlu0911@gmail.com",
                "external": False
            },
            {
                "icon": '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>',
                "text": "18154521838",
                "url": "tel:+8618154521838",
                "external": False
            },
            {
                "icon": '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
                "text": "GitHub",
                "url": "https://github.com",
                "external": True
            },
            {
                "icon": '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178A1.17 1.17 0 0 1 4.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178 1.17 1.17 0 0 1-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 0 1 .598.082l1.584.926a.272.272 0 0 0 .14.047c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 0 1-.023-.156.49.49 0 0 1 .201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89c-.135-.01-.27-.027-.407-.03zm-2.53 3.274c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.969-.982z"/></svg>',
                "text": "微信",
                "url": "javascript:void(0)",
                "external": False,
                "isWechat": True
            }
        ]

    return result

@router.put("", response_model=AboutPageResponse)
async def update_about_page(
    about_data: AboutPageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    """
    更新About页面内容

    需要管理员权限
    """
    # 检查权限
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update the about page"
        )

    # 获取现有页面
    about_page = AboutPageService.get_about_page(db)

    if not about_page:
        # 如果不存在，创建新的
        return AboutPageService.create_about_page(db, about_data.content)

    # 更新现有页面
    updated_page = AboutPageService.update_about_page(db, about_page.id, about_data.content)
    if not updated_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="About page not found"
        )

    return updated_page
