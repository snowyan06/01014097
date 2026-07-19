<template>
    <div class="landing-page">
        <!-- 顶部导航栏 -->
        <nav class="navbar">
            <div class="container navbar-content">
                <div class="logo-section">
                    <div class="logo-simple">
                        <span class="logo-icon">智</span>
                    </div>
                    <span class="brand-name">智面未来</span>
                </div>

                <div class="nav-menu">
                    <a @click="smoothScroll('#features')" class="nav-link">核心功能</a>
                    <a @click="smoothScroll('#testimonials')" class="nav-link">客户评价</a>
                    <a @click="smoothScroll('#contact')" class="nav-link">联系我们</a>
                </div>

                <div class="nav-actions">
                    <!-- 用户头像菜单 -->
                    <div class="profile-container">
                        <button
                            type="button"
                            class="profile-toggle"
                            @click="toggleProfileMenu"
                            id="profileToggleBtn"
                        >
                            <div class="profile-avatar-wrapper">
                                <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" class="profile-avatar-img" />
                                <i v-else class="pi pi-user profile-icon"></i>
                            </div>
                        </button>

                        <!-- 菜单 - 始终渲染，用 CSS 控制显示 -->
                        <div
                            class="profile-dropdown-menu shadow-lg"
                            :class="{ 'menu-visible': showProfileMenu }"
                            id="profileMenu"
                        >
                            <div class="profile-header">
                                <div class="profile-avatar">
                                    <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" class="avatar-img" />
                                    <i v-else class="pi pi-user-circle"></i>
                                </div>
                                <div class="profile-info">
                                    <h4 class="username">欢迎你，{{ userInfo.nickname }}</h4>
                                    <p class="user-email">用户名：{{ userInfo.username }}</p>
                                </div>
                            </div>

                            <div class="profile-menu">
                                <button @click="goToAccount" class="menu-item">
                                    <i class="pi pi-user-edit"></i>
                                    <span>账号信息</span>
                                </button>
                                <button @click="goToSettings" class="menu-item">
                                    <i class="pi pi-cog"></i>
                                    <span>设置</span>
                                </button>
                            </div>

                            <div class="profile-actions">
                                <button @click="logout" class="logout-button">
                                    <i class="pi pi-sign-out"></i>
                                    <span>退出登录</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <button class="btn-primary" @click="navigateTo('login')">立即体验</button>
                </div>
            </div>
        </nav>

        <!-- 首屏 Banner 区域 -->
        <section id="hero" class="hero-section">
            <div class="hero-background">
                <div class="gradient-overlay"></div>
                <div class="data-flow-animation"></div>
            </div>

            <div class="container hero-content">
                <h1 class="hero-title">
                    <span class="title-line-1">多智知途·智能体学习平台</span>
                    <span class="title-line-2">因材施教自适应，依托多智能体打造个性化学习闭环</span>
                </h1>

                <p class="hero-subtitle">
                    对话采集学情画像  多智能体协同生成专属学习资源   数字人多模态答疑  多维学习效果测评  自动更新画像、重新优化学习方案，全链路数据互通、动态迭代，真正落地因材施教！
                </p>

                <div class="hero-cta">
                    <button class="btn-primary btn-large" @click="navigateTo('register')">
                        <span>开启个性化学习</span>
                        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </button>
                    <button class="btn-secondary btn-large" @click="navigateTo('AIMockInterview')">
                        <svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor">
                            <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                        <span>观看功能演示</span>
                    </button>
                </div>

                <div class="hero-stats">
                    <div class="stat-item">
                        <div class="stat-value">10W+</div>
                        <div class="stat-label">专属学习资源库</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">6维</div>
                        <div class="stat-label">全维度学情画像分析</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">96%</div>
                        <div class="stat-label">学习适配满意度</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 四大功能模块区 -->
        <section id="features" class="features-section">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">核心功能</h2>
                    <p class="section-subtitle">四大核心模块，全方位提升面试能力</p>
                </div>

                <div class="features-grid">
                    <!-- 模块 1：岗景引擎 -->
                    <div class="feature-card" @click="navigateTo('TeacherCenter')">
                        <div class="feature-icon-wrapper">
                            <svg class="feature-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z"/>
                            </svg>
                        </div>
                        <h3 class="feature-title">岗景引擎</h3>
                        <p class="feature-description">
                            基于岗位知识图谱的智能检索系统，一键生成真实面试场景
                        </p>
                        <ul class="feature-list">
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>岗位知识图谱</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>智能岗位检索</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>一键生成情景</span>
                            </li>
                        </ul>
                        <div class="feature-value">让备考方向更精准</div>
                        <div class="feature-action">
                            <span>立即开始</span>
                            <svg class="arrow-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                                <polyline points="12 5 19 12 12 19"></polyline>
                            </svg>
                        </div>
                    </div>

                    <!-- 模块 2：对话剧场 -->
                    <div class="feature-card" @click="navigateTo('AIMockInterview')">
                        <div class="feature-icon-wrapper">
                            <svg class="feature-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4h-4z"/>
                            </svg>
                        </div>
                        <h3 class="feature-title">对话剧场</h3>
                        <p class="feature-description">
                            沉浸式视频面试模拟，配备专业场控和智能复盘系统
                        </p>
                        <ul class="feature-list">
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>沉浸式视频窗口</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>场控控制台</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>结算与复盘入口</span>
                            </li>
                        </ul>
                        <div class="feature-value">让实战演练更沉浸</div>
                        <div class="feature-action">
                            <span>进入剧场</span>
                            <svg class="arrow-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                                <polyline points="12 5 19 12 12 19"></polyline>
                            </svg>
                        </div>
                    </div>

                    <!-- 模块 3：慧评雷达 -->
                    <div class="feature-card" @click="navigateTo('Analytics')">
                        <div class="feature-icon-wrapper">
                            <svg class="feature-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/>
                            </svg>
                        </div>
                        <h3 class="feature-title">慧评雷达</h3>
                        <p class="feature-description">
                            六维能力评估体系，精准定位优势与待改进领域
                        </p>
                        <ul class="feature-list">
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>六维能力雷达图</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>高光与待改进切片</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>历史趋势曲线</span>
                            </li>
                        </ul>
                        <div class="feature-value">让能力诊断更透彻</div>
                        <div class="feature-action">
                            <span>查看报告</span>
                            <svg class="arrow-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                                <polyline points="12 5 19 12 12 19"></polyline>
                            </svg>
                        </div>
                    </div>

                    <!-- 模块 4：成长导航仪 -->
                    <div class="feature-card" @click="navigateTo('AnalysisImprovement')">
                        <div class="feature-icon-wrapper">
                            <svg class="feature-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                            </svg>
                        </div>
                        <h3 class="feature-title">成长导航仪</h3>
                        <p class="feature-description">
                            面试知识题库，智能岗位检索，一键生成情景
                        </p>
                        <ul class="feature-list">
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>面试知识题库</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>智能岗位检索</span>
                            </li>
                            <li>
                                <svg class="check-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <span>一键生成情景</span>
                            </li>
                        </ul>
                        <div class="feature-value">让进阶路径更清晰</div>
                        <div class="feature-action">
                            <span>查看详细</span>
                            <svg class="arrow-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                                <polyline points="12 5 19 12 12 19"></polyline>
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="features-footer">
                    <p class="features-footer-text">让备考更精准 · 让实战更从容 · 让评估更科学 · 让成长更快速</p>
                </div>
            </div>
        </section>

        <!-- 客户证言区 -->
        <section id="testimonials" class="testimonials-section">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">客户评价</h2>
                    <p class="section-subtitle">听听他们怎么说</p>
                </div>

                <div class="testimonial-card">
                    <div class="quote-icon">
                        <svg class="quote-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/>
                        </svg>
                    </div>
                    <p class="testimonial-text">
                        "作为深耕教育行业数字化解决方案的先行者，锐捷网络依托自身在AI与场景融合方面的技术积累，提出构建'AI模拟面试与能力提升平台'的创新方向，直击学生准备过程中的核心痛点，助力高校人才实现从知识掌握到能力展示的关键跨越。"
                    </p>
                    <div class="client-info">
                        <div class="client-details">
                            <div class="client-name">锐捷网络股份有限公司</div>
                            <div class="client-title">行业领先的ICT基础设施及行业解决方案提供商 | 股票代码301165</div>
                        </div>
                        <div class="rating">
                            <svg class="star-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                            </svg>
                            <svg class="star-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                            </svg>
                            <svg class="star-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                            </svg>
                            <svg class="star-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                            </svg>
                            <svg class="star-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 底部联系信息 -->
        <footer id="contact" class="footer">
            <div class="container">
                <div class="footer-content">
                    <div class="footer-section">
                        <div class="footer-logo">
                            <svg viewBox="0 0 54 40" fill="none" xmlns="http://www.w3.org/2000/svg" class="footer-logo-icon">
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M17.1637 19.2467C17.1566 19.4033 17.1529 19.561 17.1529 19.7194C17.1529 25.3503 21.7203 29.915 27.3546 29.915C32.9887 29.915 37.5561 25.3503 37.5561 19.7194C37.5561 19.5572 37.5524 19.3959 37.5449 19.2355C38.5617 19.0801 39.5759 18.9013 40.5867 18.6994L40.6926 18.6782C40.7191 19.0218 40.7326 19.369 40.7326 19.7194C40.7326 27.1036 34.743 33.0896 27.3546 33.0896C19.966 33.0896 13.9765 27.1036 13.9765 19.7194C13.9765 19.374 13.9896 19.0316 14.0154 18.6927L14.0486 18.6994C15.0837 18.9062 16.1223 19.0886 17.1637 19.2467ZM33.3284 11.4538C31.6493 10.2396 29.5855 9.52381 27.3546 9.52381C25.1195 9.52381 23.0524 10.2421 21.3717 11.4603C20.0078 11.3232 18.6475 11.1387 17.2933 10.907C19.7453 8.11308 23.3438 6.34921 27.3546 6.34921C31.36 6.34921 34.9543 8.10844 37.4061 10.896C36.0521 11.1292 34.692 11.3152 33.3284 11.4538ZM43.826 18.0518C43.881 18.6003 43.9091 19.1566 43.9091 19.7194C43.9091 28.8568 36.4973 36.2642 27.3546 36.2642C18.2117 36.2642 10.8 28.8568 10.8 19.7194C10.8 19.1615 10.8276 18.61 10.8816 18.0663L7.75383 17.4411C7.66775 18.1886 7.62354 18.9488 7.62354 19.7194C7.62354 30.6102 16.4574 39.4388 27.3546 39.4388C38.2517 39.4388 47.0855 30.6102 47.0855 19.7194C47.0855 18.9439 47.0407 18.1789 46.9536 17.4267L43.826 18.0518ZM44.2613 9.54743L40.9084 10.2176C37.9134 5.95821 32.9593 3.1746 27.3546 3.1746C21.7442 3.1746 16.7856 5.96385 13.7915 10.2305L10.4399 9.56057C13.892 3.83178 20.1756 0 27.3546 0C34.5281 0 40.8075 3.82591 44.2613 9.54743Z"
                                    fill="currentColor"
                                />
                            </svg>
                            <span class="footer-brand">智面未来</span>
                        </div>
                        <p class="footer-description">专业的 AI 面试训练平台，助力每一位求职者实现职业梦想</p>
                        <div class="social-links">
                            <a href="#" class="social-link" title="微信">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="social-icon-svg">
                                    <path d="M9.5 4C5.36 4 2 6.69 2 10c0 1.89 1.08 3.56 2.78 4.66L4 17l2.5-1.18C7.47 16.27 8.47 16.5 9.5 16.5c.17 0 .33 0 .5-.02C9.68 15.99 9.5 15.51 9.5 15c0-3.04 2.69-5.5 6-5.5.17 0 .33.01.5.02C15.19 6.31 12.59 4 9.5 4zM7 9a1 1 0 110-2 1 1 0 010 2zm5 0a1 1 0 110-2 1 1 0 010 2zm3.5 3c-2.76 0-5 1.79-5 4s2.24 4 5 4c.64 0 1.25-.1 1.82-.28L19 21l-.68-2.05C19.46 18.12 20 17.1 20 16c0-2.21-2.24-4-5-4zm-1.5 5a.75.75 0 110-1.5.75.75 0 010 1.5zm3 0a.75.75 0 110-1.5.75.75 0 010 1.5z"/>
                                </svg>
                            </a>
                            <a href="#" class="social-link" title="微博">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="social-icon-svg">
                                    <path d="M10.1 18.3c-3.5.4-6.5-1.2-6.8-3.6-.3-2.4 2.3-4.8 5.8-5.2 3.5-.4 6.5 1.2 6.8 3.6.3 2.4-2.3 4.8-5.8 5.2zm6.6-9.5c-.3-.8-1.2-1.2-2-.9-.8.3-1.2 1.2-.9 2 .3.8 1.2 1.2 2 .9.8-.3 1.2-1.2.9-2zm1.3-2.5c-.2-.5-.8-.7-1.3-.5-.5.2-.7.8-.5 1.3.2.5.8.7 1.3.5.5-.2.7-.8.5-1.3zm1.5-2c-.2-.4-.6-.5-1-.4-.4.2-.5.6-.4 1 .2.4.6.5 1 .4.4-.2.5-.6.4-1zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                                </svg>
                            </a>
                            <a href="#" class="social-link" title="LinkedIn">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="social-icon-svg">
                                    <path d="M19 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h14m-.5 15.5v-5.3a3.26 3.26 0 00-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 011.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 001.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 00-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                                </svg>
                            </a>
                        </div>
                    </div>

                    <div class="footer-section">
                        <h4 class="footer-title">产品服务</h4>
                        <ul class="footer-links">
                            <li><a @click="navigateTo('TeacherCenter')">岗景引擎 - 岗位化题库</a></li>
                            <li><a @click="navigateTo('AIMockInterview')">对话剧场 - 多模态面试</a></li>
                            <li><a @click="navigateTo('Analytics')">慧评雷达 - 多维度分析</a></li>
                            <li><a @click="navigateTo('AnalysisImprovement')">成长导航仪 - 能力提升反馈</a></li>
                        </ul>
                    </div>

                    <div class="footer-section">
                        <h4 class="footer-title">关于我们</h4>
                        <ul class="footer-links">
                            <li><a href="#">公司介绍</a></li>
                            <li><a href="#">技术背景</a></li>
                            <li><a href="#">教育合作</a></li>
                            <li><a href="#">联系我们</a></li>
                        </ul>
                    </div>

                    <div class="footer-section">
                        <h4 class="footer-title">联系方式</h4>
                        <ul class="footer-contact">
                            <li>
                                <svg class="footer-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                                </svg>
                                <span>400-880-9900</span>
                            </li>
                            <li>
                                <svg class="footer-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                                </svg>
                                <span>contact@ruijie.com.cn</span>
                            </li>
                            <li>
                                <svg class="footer-icon-svg" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                                </svg>
                                <span>福建省福州市仓山区金山大道618号桔园洲工业区</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="footer-bottom">
                    <p>&copy; 2026 智面未来。All rights reserved.</p>
                    <div class="footer-legal">
                        <a href="#">隐私政策</a>
                        <a href="#">服务条款</a>
                        <a href="#">Cookie 政策</a>
                    </div>
                </div>
            </div>
        </footer>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 使用 ref
const showProfileMenu = ref(false);
const userInfo = ref({
    nickname: '',
    username: '',
    avatar: ''
});

function smoothScroll(id) {
    document.body.click();
    const element = document.querySelector(id);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

function navigateTo(route) {
    router.push({ name: route });
}

function toggleProfileMenu() {
    console.log('=== 头像点击开始 ===');
    console.log('点击前 showProfileMenu:', showProfileMenu.value);
    showProfileMenu.value = !showProfileMenu.value;
    console.log('点击后 showProfileMenu:', showProfileMenu.value);
    console.log('userInfo:', userInfo.value);
    console.log('=== 头像点击结束 ===');
}

function goToAccount() {
    showProfileMenu.value = false;
    router.push({ name: 'account' });
}

function goToSettings() {
    showProfileMenu.value = false;
    router.push({ name: 'settings' });
}

function logout() {
    localStorage.removeItem('auth');
    sessionStorage.removeItem('auth');
    localStorage.removeItem('isLoggedIn');
    sessionStorage.removeItem('isLoggedIn');
    showProfileMenu.value = false;
    router.push({ name: 'login' });
}

function fetchUserInfo() {
    const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
    if (authData) {
        userInfo.value = {
            nickname: authData.nickname || authData.username || '用户',
            username: authData.username || '未知',
            avatar: authData.avatar || ''
        };
    }
}

function handleClickOutside(event) {
    console.log('=== 点击外部检测 ===');
    console.log('点击目标:', event.target);
    console.log('点击目标 ID:', event.target.id);
    console.log('点击目标类名:', event.target.className);

    // 获取相关元素
    const profileToggle = document.querySelector('#profileToggleBtn');
    const profileMenu = document.querySelector('#profileMenu');
    const profileContainer = document.querySelector('.profile-container');

    console.log('头像按钮:', profileToggle);
    console.log('菜单:', profileMenu);
    console.log('容器:', profileContainer);

    // 检查点击是否在头像按钮上（包括其所有子元素）
    const isClickOnToggle = profileToggle && (
        profileToggle.contains(event.target) ||
        event.target === profileToggle ||
        event.target.closest('#profileToggleBtn')
    );

    // 检查点击是否在菜单上（包括其所有子元素）
    const isClickOnMenu = profileMenu && (
        profileMenu.contains(event.target) ||
        event.target === profileMenu ||
        event.target.closest('#profileMenu')
    );

    // 检查点击是否在容器内
    const isClickInContainer = profileContainer && (
        profileContainer.contains(event.target) ||
        event.target.closest('.profile-container')
    );

    console.log('是否点击头像按钮:', isClickOnToggle);
    console.log('是否点击菜单:', isClickOnMenu);
    console.log('是否点击容器内:', isClickInContainer);

    if (!isClickOnToggle && !isClickOnMenu && !isClickInContainer) {
        console.log('点击外部，关闭菜单');
        showProfileMenu.value = false;
    } else {
        console.log('点击有效区域，保持菜单打开');
    }
}

// 组件挂载时获取用户信息
onMounted(() => {
    fetchUserInfo();
    console.log('组件已挂载，初始状态:', showProfileMenu.value);

    // 监听跨窗口 storage 事件
    window.addEventListener('storage', (e) => {
        if (e.key === 'auth' && e.newValue) {
            try {
                const authData = JSON.parse(e.newValue);
                fetchUserInfo();
            } catch (error) {
                console.error('storage 事件解析失败:', error);
            }
        }
    });

    // 监听头像更新自定义事件
    window.addEventListener('avatar-updated', (e) => {
        console.log('Landing.vue 收到头像更新事件:', e.detail);
        if (e.detail) {
            fetchUserInfo();
        }
    });

    // 添加点击外部关闭菜单的监听器
    document.addEventListener('click', handleClickOutside);
});

// 组件卸载时清理监听器
onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* 全局字体设置 - 宋体系列 */
* {
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif !important;
}

/* CSS 变量定义 */
.landing-page {
    --primary-dark: #0E42D2;
    --primary-medium: #165DFF;
    --primary-light: #4080FF;
    --text-dark: #1f2937;
    --text-gray: #6b7280;
    --text-light: #9ca3af;
    --bg-white: #ffffff;
    --bg-light: #f9fafb;
    --bg-gray: #f3f4f6;
    --border-color: #e5e7eb;
}

/* 容器工具类 - 添加前缀避免污染全局 */
.landing-page .container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 2rem;
}

/* 导航栏样式 */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    z-index: 999;
    transition: all 0.3s ease;
}

.navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    position: relative;
    z-index: 1000;
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.logo-simple {
    width: 45px !important;
    height: 45px !important;
    border-radius: 12px;
    background: linear-gradient(135deg, #0E42D2 0%, #4080FF 100%) !important;
    display: flex !important;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(14, 66, 210, 0.3);
    transition: all 0.3s ease;
}

.logo-simple:hover {
    transform: rotate(-5deg) scale(1.05);
    box-shadow: 0 6px 20px rgba(14, 66, 210, 0.5);
}

.logo-icon {
    font-size: 1.8rem;
    font-weight: 700;
    color: white !important;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.brand-name {
    font-size: 1.5rem;
    font-weight: 600;
    color: #165DFF !important;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
    letter-spacing: 2px;
}

.nav-menu {
    display: flex;
    gap: 2rem;
}

.nav-link {
    font-size: 1rem;
    color: var(--text-dark);
    text-decoration: none;
    transition: color 0.3s ease;
    cursor: pointer;
}

.nav-link:hover {
    color: var(--primary-medium);
}

/* 导航栏动作区 */
.landing-page .nav-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* 头像容器 */
.landing-page .profile-container {
    position: relative;
    z-index: 1000;
}

/* 头像切换按钮 */
.landing-page .profile-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 50%;
    position: relative;
    z-index: 1001;
    pointer-events: auto;
}

.landing-page .profile-toggle:hover {
    background-color: rgba(22, 93, 255, 0.1);
}

/* 头像包装器 */
.landing-page .profile-avatar-wrapper {
    width: 40px;
    height: 40px;
    min-width: 40px;
    min-height: 40px;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--primary-medium), var(--primary-light));
    flex-shrink: 0;
    position: relative;
    z-index: 1002;
}

/* 头像图片 */
.landing-page .profile-avatar-img {
    width: 100%;
    height: 100%;
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
}

/* 头像图标 */
.landing-page .profile-icon {
    font-size: 20px;
    color: white;
}

/* 头像下拉菜单 */
.landing-page .profile-dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    width: 280px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    z-index: 9999;
    margin-top: 0.5rem;
    pointer-events: auto;

    /* 默认隐藏 */
    display: none;
}

/* 显示菜单的类 */
.landing-page .profile-dropdown-menu.menu-visible {
    display: block !important;
}

/* 头像头部 */
.landing-page .profile-header {
    display: flex;
    align-items: center;
    padding: 16px;
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-medium));
    color: white;
}

/* 头像区域 */
.landing-page .profile-avatar {
    font-size: 40px;
    margin-right: 12px;
    color: white;
    width: 60px;
    height: 60px;
    min-width: 60px;
    min-height: 60px;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
}

/* 头像图片 */
.landing-page .avatar-img {
    width: 100%;
    height: 100%;
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
}

/* 用户信息 */
.landing-page .profile-info .username {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: white;
}

.landing-page .profile-info .user-email {
    margin: 4px 0 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 12px;
}

/* 菜单项 */
.landing-page .profile-menu {
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
}

.landing-page .menu-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: none;
    border: none;
    color: #333;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.landing-page .menu-item:hover {
    background-color: #f5f5f5;
}

.landing-page .menu-item i {
    font-size: 16px;
    color: var(--primary-medium);
}

/* 退出按钮区域 */
.landing-page .profile-actions {
    padding: 12px;
    background-color: #f8f9fa;
}

/* 退出按钮 */
.landing-page .logout-button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px;
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 14px;
    font-weight: 500;
}

.landing-page .logout-button:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
}

.landing-page .logout-button i {
    font-size: 16px;
}

/* 淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

/* 按钮样式 */
.btn-primary {
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-medium));
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(22, 93, 255, 0.2);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(22, 93, 255, 0.3);
}

.btn-secondary {
    background: white;
    color: var(--primary-dark);
    border: 2px solid var(--primary-medium);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-secondary:hover {
    background: var(--bg-light);
    transform: translateY(-2px);
}

.btn-large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
}

.btn-icon {
    width: 1.125rem;
    height: 1.125rem;
    display: inline-block;
    vertical-align: middle;
    margin-left: 0.5rem;
}

.feature-icon-svg {
    width: 2.5rem;
    height: 2.5rem;
    display: block;
}

.check-icon-svg {
    width: 0.875rem;
    height: 0.875rem;
    margin-right: 0.5rem;
    color: var(--primary-light);
}

.arrow-icon-svg {
    width: 1rem;
    height: 1rem;
    margin-left: 0.25rem;
}

.quote-icon-svg {
    width: 2rem;
    height: 2rem;
    color: var(--primary-medium);
    margin-bottom: 1.5rem;
}

.star-icon-svg {
    width: 1.125rem;
    height: 1.125rem;
    color: #fbbf24;
}

.star-icon-svg:not(:first-child) {
    margin-left: 0.25rem;
}

.social-icon-svg {
    width: 1.25rem;
    height: 1.25rem;
}

.footer-icon-svg {
    width: 1rem;
    height: 1rem;
    margin-right: 0.75rem;
    color: var(--primary-medium);
}

/* Hero 区域 */
.hero-section {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding-top: 80px;
    background:
        linear-gradient(135deg, rgba(240, 245, 255, 0.85) 0%, rgba(236, 245, 253, 0.8) 50%, rgba(240, 245, 255, 0.85) 100%),
        url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    overflow: hidden;
}

.hero-background {
    position: absolute;
    inset: 0;
    overflow: hidden;
}

.gradient-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 70% 30%, rgba(22, 93, 255, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 30% 70%, rgba(64, 128, 255, 0.08) 0%, transparent 50%);
}

.data-flow-animation {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(22, 93, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(22, 93, 255, 0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    animation: flowAnimation 20s linear infinite;
}

@keyframes flowAnimation {
    0% { transform: translate(0, 0); }
    100% { transform: translate(50px, 50px); }
}

.hero-content {
    position: relative;
    z-index: 1;
    text-align: center;
    max-width: 900px;
}

.hero-title {
    margin-bottom: 1.5rem;
}

.title-line-1 {
    display: block;
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-medium));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 1rem;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.title-line-2 {
    display: block;
    font-size: 2rem;
    font-weight: 300;
    color: var(--text-gray);
    line-height: 1.4;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: var(--text-gray);
    line-height: 1.8;
    margin-bottom: 2.5rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 3rem;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 4rem;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.stat-label {
    font-size: 1rem;
    color: var(--text-gray);
    margin-top: 0.5rem;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

/* 功能模块区 */
.features-section {
    padding: 6rem 0;
    background: var(--bg-white);
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 1rem;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.section-subtitle {
    font-size: 1.25rem;
    color: var(--text-gray);
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
}

.feature-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 2rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    border-color: var(--primary-medium);
}

.feature-icon-wrapper {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-medium));
    color: white;
}

.feature-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 1rem;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.feature-description {
    font-size: 1rem;
    color: var(--text-gray);
    line-height: 1.6;
    margin-bottom: 1.5rem;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.feature-list {
    list-style: none;
    padding: 0;
    margin-bottom: 1.5rem;
}

.feature-list li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-dark);
}

.feature-list i {
    color: var(--primary-light);
}

.feature-value {
    font-size: 1rem;
    font-weight: 600;
    color: var(--primary-dark);
    padding: 0.75rem;
    background: rgba(22, 93, 255, 0.05);
    border-radius: 8px;
    margin-bottom: 1rem;
    text-align: center;
}

.feature-action {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--primary-medium);
}

.feature-action i {
    transition: transform 0.3s ease;
}

.feature-card:hover .feature-action i {
    transform: translateX(4px);
}

.features-footer {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(14, 66, 210, 0.02), rgba(22, 93, 255, 0.02));
    border-radius: 12px;
}

.features-footer-text {
    font-size: 1.125rem;
    color: var(--text-gray);
    font-weight: 500;
}

/* 客户证言区 */
.testimonials-section {
    padding: 6rem 0;
    background: var(--bg-light);
}

.testimonial-card {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.quote-icon {
    font-size: 2.5rem;
    color: var(--primary-medium);
    margin-bottom: 1.5rem;
}

.testimonial-text {
    font-size: 1.25rem;
    line-height: 1.8;
    color: var(--text-dark);
    margin-bottom: 2rem;
}

.client-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.client-logos {
    display: flex;
    gap: 1rem;
    font-size: 2rem;
}

.client-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-dark);
}

.client-title {
    font-size: 1rem;
    color: var(--text-gray);
}

.rating {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 0.25rem;
    color: #FBBF24;
    font-size: 1.25rem;
}

/* 页脚 */
.footer {
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-medium));
    color: white;
    padding: 4rem 0 2rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 3rem;
    margin-bottom: 3rem;
}

.footer-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.footer-logo-icon {
    width: 40px;
    height: 40px;
}

.footer-brand {
    font-size: 1.5rem;
    font-weight: 600;
}

.footer-description {
    font-size: 0.875rem;
    line-height: 1.6;
    opacity: 0.9;
    margin-bottom: 1.5rem;
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-link {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    text-decoration: none;
    transition: all 0.3s ease;
}

.social-link:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

.footer-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

.footer-links {
    list-style: none;
    padding: 0;
}

.footer-links li {
    margin-bottom: 0.5rem;
}

.footer-links a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    font-size: 0.875rem;
    transition: color 0.3s ease;
    cursor: pointer;
}

.footer-links a:hover {
    color: white;
}

.footer-contact {
    list-style: none;
    padding: 0;
}

.footer-contact li {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
}

.footer-contact i {
    width: 20px;
}

.footer-bottom {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.footer-bottom p {
    font-size: 0.875rem;
    opacity: 0.8;
}

.footer-legal {
    display: flex;
    gap: 1.5rem;
}

.footer-legal a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    font-size: 0.875rem;
    transition: color 0.3s ease;
}

.footer-legal a:hover {
    color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        padding: 0 1rem;
    }

    .navbar-content {
        flex-direction: column;
        gap: 1rem;
    }

    .nav-menu {
        gap: 1rem;
    }

    .title-line-1 {
        font-size: 2rem;
    }

    .title-line-2 {
        font-size: 1.25rem;
    }

    .hero-cta {
        flex-direction: column;
    }

    .hero-stats {
        flex-direction: column;
        gap: 2rem;
    }

    .features-grid {
        grid-template-columns: 1fr;
    }

    .footer-content {
        grid-template-columns: 1fr;
    }

    .footer-bottom {
        flex-direction: column;
        text-align: center;
    }
}
</style>
