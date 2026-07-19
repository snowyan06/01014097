<template>
    <div class="homepage-container">
        <!-- 动态背景层 -->
        <div class="animated-background"></div>

        <!-- 装饰性光晕 -->
        <div class="solid-color-orb orb-1"></div>
        <div class="solid-color-orb orb-2"></div>
        <div class="solid-color-orb orb-3"></div>

        <!-- 主内容区 - 三个页面 -->
        <main class="main-content">
            <!-- Page 1: 大标题页 -->
            <section class="page page-1" :class="{ 'active': currentPage === 1 }">
                <div class="page-content page-1-content">
                    <div class="page-1-top">
                        <div class="banner banner-style-1">
                            <div class="banner-circle banner-circle-left"></div>
                            <div class="banner-content">
                                <h2 class="banner-title">智面未来</h2>
                                <p class="banner-subtitle">AI Mock Interview Platform</p>
                            </div>
                            <div class="banner-circle banner-circle-right"></div>
                        </div>
                    </div>
                    <div class="page-1-middle">
                        <div class="page-1-title-container">
                            <h1 class="mega-title mega-title-light">
                                <span class="title-text">智面未来 · AI 面试教练平台</span>
                            </h1>
                            <p class="mega-subtitle mega-subtitle-light">从紧张到从容，让每一次开口都更有底气</p>
                        </div>
                        <div class="split-line"></div>
                    </div>
                    <div class="page-1-bottom"></div>
                </div>
            </section>

            <!-- Page 2: 功能模块页 -->
            <section class="page page-2" :class="{ 'active': currentPage === 2 }">
                <div class="page-content">
                    <div class="scrolled-header">
                        <div class="banner banner-style-2">
                            <div class="banner-circle banner-circle-left"></div>
                            <div class="banner-content">
                                <h2 class="banner-title">功能模块</h2>
                                <p class="banner-subtitle">Feature Modules</p>
                            </div>
                            <div class="banner-circle banner-circle-right"></div>
                        </div>
                    </div>

                    <div class="features-carousel">
                        <div class="feature-card feature-card-light"
                             :class="{ 'active': activeCardIndex === 0 }"
                             @click="navigateTo('TeacherCenter')"
                             @mouseenter="activeCardIndex = 0"
                             @mouseleave="activeCardIndex = null">
                            <div class="card-inner">
                                <div class="icon-wrapper" style="background-color: #064e3b;">
                                    <i class="fas fa-briefcase"></i>
                                </div>
                                <h3 class="text-dark">岗景引擎</h3>
                                <p class="feature-description feature-description-dark">
                                    岗位知识图谱<br>
                                    智能岗位检索<br>
                                    一键生成情景
                                </p>
                                <div class="highlight-text highlight-text-dark">让备考方向更精准</div>
                                <div class="card-footer card-footer-dark">
                                    <span>立即开始</span>
                                    <i class="fas fa-arrow-right"></i>
                                </div>
                            </div>
                        </div>

                        <div class="feature-card feature-card-light"
                             :class="{ 'active': activeCardIndex === 1 }"
                             @click="navigateTo('AIMockInterview')"
                             @mouseenter="activeCardIndex = 1"
                             @mouseleave="activeCardIndex = null">
                            <div class="card-inner">
                                <div class="icon-wrapper" style="background-color: #065f46;">
                                    <i class="fas fa-film"></i>
                                </div>
                                <h3 class="text-dark">对话剧场</h3>
                                <p class="feature-description feature-description-dark">
                                    沉浸式视频窗口<br>
                                    场控控制台<br>
                                    结算与复盘入口
                                </p>
                                <div class="highlight-text highlight-text-dark">让实战演练更沉浸</div>
                                <div class="card-footer card-footer-dark">
                                    <span>进入剧场</span>
                                    <i class="fas fa-arrow-right"></i>
                                </div>
                            </div>
                        </div>

                        <div class="feature-card feature-card-light"
                             :class="{ 'active': activeCardIndex === 2 }"
                             @click="navigateTo('Analytics')"
                             @mouseenter="activeCardIndex = 2"
                             @mouseleave="activeCardIndex = null">
                            <div class="card-inner">
                                <div class="icon-wrapper" style="background-color: #047857;">
                                    <i class="fas fa-chart-line"></i>
                                </div>
                                <h3 class="text-dark">慧评雷达</h3>
                                <p class="feature-description feature-description-dark">
                                    六维能力雷达图<br>
                                    高光与待改进切片<br>
                                    历史趋势曲线
                                </p>
                                <div class="highlight-text highlight-text-dark">让能力诊断更透彻</div>
                                <div class="card-footer card-footer-dark">
                                    <span>查看报告</span>
                                    <i class="fas fa-arrow-right"></i>
                                </div>
                            </div>
                        </div>

                        <div class="feature-card feature-card-light"
                             :class="{ 'active': activeCardIndex === 3 }"
                             @click="navigateTo('AnalysisImprovement')"
                             @mouseenter="activeCardIndex = 3"
                             @mouseleave="activeCardIndex = null">
                            <div class="card-inner">
                                <div class="icon-wrapper" style="background-color: #059669;">
                                    <i class="fas fa-map-marked-alt"></i>
                                </div>
                                <h3 class="text-dark">成长导航仪</h3>
                                <p class="feature-description feature-description-dark">
                                    面试知识题库<br>
                                    智能岗位检索<br>
                                    一键生成情景
                                </p>
                                <div class="highlight-text highlight-text-dark">让进阶路径更清晰</div>
                                <div class="card-footer card-footer-dark">
                                    <span>查看详细</span>
                                    <i class="fas fa-arrow-right"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Page 3: 客户评价页 -->
            <section class="page page-3" :class="{ 'active': currentPage === 3 }">
                <div class="page-content">
                    <div class="page-3-top">
                        <div class="banner banner-style-3">
                            <div class="banner-circle banner-circle-left"></div>
                            <div class="banner-content">
                                <h2 class="banner-title">慧评雷达</h2>
                                <p class="banner-subtitle">Intelligent Evaluation Radar</p>
                            </div>
                            <div class="banner-circle banner-circle-right"></div>
                        </div>

                        <div class="testimonial-card testimonial-card-light">
                            <div class="quote-icon quote-icon-light">
                                <i class="fas fa-quote-left"></i>
                            </div>
                            <p class="testimonial-text testimonial-text-light">
                                "AI 面试教练的最佳实践平台，帮助我们提升了<strong>85%</strong>的面试通过率，学员满意度达到<strong>96%</strong>以上"
                            </p>
                            <div class="client-info">
                                <div class="client-avatar">🎯</div>
                                <div class="client-details">
                                    <div class="client-name client-name-light">某知名人力资源机构</div>
                                    <div class="client-title client-title-light">战略合作伙伴</div>
                                </div>
                                <div class="rating">
                                    <i class="fas fa-star" v-for="i in 5" :key="i"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="page-3-bottom">
                        <div class="cta-container">
                            <button class="cta-button" @click="navigateTo('login')">
                                <div class="button-content">
                                    <i class="fas fa-rocket"></i>
                                    <span>立即开始面试训练</span>
                                </div>
                            </button>

                            <div class="support-info">
                                <div class="support-contact support-contact-light">
                                    <i class="fas fa-phone"></i>
                                    <span>咨询热线：400-800-9000</span>
                                </div>
                                <div class="support-contact support-contact-light">
                                    <i class="fas fa-envelope"></i>
                                    <span>contact@zhimian.com</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <!-- 页面指示器 -->
        <div class="page-indicator">
            <div class="indicator-dot"
                 :class="{ 'active': currentPage === 1 }"
                 @click="scrollToPage(1)"></div>
            <div class="indicator-dot"
                 :class="{ 'active': currentPage === 2 }"
                 @click="scrollToPage(2)"></div>
            <div class="indicator-dot"
                 :class="{ 'active': currentPage === 3 }"
                 @click="scrollToPage(3)"></div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
    name: 'Dashboard',
    setup() {
        const router = useRouter();
        const currentPage = ref(1);
        const activeCardIndex = ref(null);

        return {
            currentPage,
            activeCardIndex
        };
    },
    data() {
        return {
            particles: [],
            isScrolling: false,
            wheelLock: false
        };
    },
    mounted() {
        this.generateParticles();
        window.addEventListener('wheel', this.handleWheel, { passive: false });
    },
    beforeUnmount() {
        window.removeEventListener('wheel', this.handleWheel);
    },
    methods: {
        getParticleStyle(index) {
            const particle = this.particles[index - 1];
            if (!particle) return {};
            return {
                left: `${particle.x}%`,
                top: `${particle.y}%`,
                width: `${particle.size}px`,
                height: `${particle.size}px`,
                opacity: particle.opacity,
                animationDelay: `${particle.delay}s`,
                animationDuration: `${particle.duration}s`
            };
        },
        generateParticles() {
            this.particles = Array(40).fill().map(() => ({
                x: Math.random() * 100,
                y: Math.random() * 100,
                size: Math.random() * 6 + 2,
                opacity: Math.random() * 0.6 + 0.2,
                delay: Math.random() * 5,
                duration: Math.random() * 10 + 15
            }));
        },
        handleWheel(event) {
            if (this.wheelLock || this.isScrolling) return;

            this.wheelLock = true;

            if (event.deltaY > 0) {
                if (this.currentPage < 3) {
                    this.scrollToPage(this.currentPage + 1);
                }
            } else {
                if (this.currentPage > 1) {
                    this.scrollToPage(this.currentPage - 1);
                }
            }

            setTimeout(() => {
                this.wheelLock = false;
            }, 800);
        },
        scrollToPage(pageNum) {
            if (this.isScrolling || this.currentPage === pageNum) return;

            this.isScrolling = true;
            const targetPage = document.querySelector(`.page-${pageNum}`);

            if (targetPage) {
                targetPage.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                this.currentPage = pageNum;

                setTimeout(() => {
                    this.isScrolling = false;
                }, 800);
            }
        },
        navigateTo(route) {
            console.log(`导航到：${route}`);
            this.$router.push(`/${route}`);
        }
    }
};
</script>

<style scoped>
* {
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif !important;
}

.homepage-container {
    position: relative;
    height: 100vh;
    overflow: hidden;
    background: #ffffff;
}

.layout-topbar {
    z-index: 1000 !important;
    position: relative !important;
}

.menu-button, .layout-menu-button {
    z-index: 1001 !important;
    pointer-events: auto !important;
    cursor: pointer !important;
}

.animated-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #065f46 100%);
}

.solid-color-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.2;
    animation: float 20s ease-in-out infinite;
}

.orb-1 {
    width: 400px;
    height: 400px;
    background-color: #064e3b;
    top: -100px;
    left: -100px;
    animation-delay: 0s;
}

.orb-2 {
    width: 300px;
    height: 300px;
    background-color: #10b981;
    top: 50%;
    right: -100px;
    animation-delay: -7s;
}

.orb-3 {
    width: 350px;
    height: 350px;
    background-color: #059669;
    bottom: -100px;
    left: 30%;
    animation-delay: -14s;
}

.main-content {
    position: relative;
    z-index: 1;
    height: 100vh;
    overflow: hidden;
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

.page {
    height: 100vh;
    width: 100%;
    scroll-snap-align: start;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 80px 20px 40px;
    transition: opacity 0.6s ease;
}

.page.active {
    opacity: 1;
}

.page:not(.active) {
    opacity: 0;
}

.page-content {
    max-width: 1600px;
    width: 100%;
    margin: 0 auto;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.page-1 {
    background-image:
        linear-gradient(to bottom, rgba(255, 255, 255, 0.85) 0%, rgba(255, 255, 255, 0.7) 30%, rgba(6, 78, 59, 0.85) 30%, rgba(6, 78, 59, 0.9) 70%, rgba(255, 255, 255, 0.85) 70%, rgba(255, 255, 255, 0.9) 100%),
        url('/src/assets/backgrounds/landscape-1.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.page-1-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.page-1-top {
    flex: 0 0 30%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
}

.page-1-middle {
    flex: 0 0 40%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.page-1-title-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    width: 100%;
}

.page-1-bottom {
    flex: 0 0 30%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.split-line {
    display: none;
}

.banner {
    width: 100%;
    max-width: 1200px;
    height: 100px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    transition: all 0.4s ease;
    background: linear-gradient(135deg, rgba(6, 78, 59, 0.95) 0%, rgba(4, 120, 87, 0.9) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.banner:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
}

.banner-circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.15;
    pointer-events: none;
}

.banner-circle-left {
    width: 120px;
    height: 120px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
    left: -40px;
    top: 50%;
    transform: translateY(-50%);
}

.banner-circle-right {
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.25) 0%, transparent 70%);
    right: -50px;
    top: 50%;
    transform: translateY(-50%);
}

.banner-content {
    flex: 1;
    text-align: left;
    z-index: 1;
    padding-left: 20px;
}

.banner-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: #ffffff;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    letter-spacing: 2px;
}

.banner-subtitle {
    font-size: 1rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.85);
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
    letter-spacing: 1px;
}

.feature-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 8px;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    border: 2px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    min-height: 340px;
    width: 100%;
    max-width: 340px;
    margin: 0 auto;
}

.feature-card-light {
    background: rgba(255, 255, 255, 0.95);
}

.feature-card:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
    border-color: rgba(6, 78, 59, 0.3);
}

.feature-card.active {
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    border-color: rgba(6, 78, 59, 0.2);
}

.feature-card.active h3 {
    color: #064e3b;
    transform: scale(1.05);
}

.feature-card.active .highlight-text {
    color: #047857;
    transform: scale(1.08);
}

.card-inner {
    padding: 28px 22px;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.icon-wrapper {
    width: 60px;
    height: 60px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    color: white;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feature-card h3 {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 14px;
    transition: all 0.3s ease;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.text-dark {
    color: #064e3b;
}

.feature-description {
    font-size: 0.95rem;
    line-height: 1.8;
    margin-bottom: 14px;
    font-weight: 300;
    flex: 1;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.feature-description-dark {
    color: rgba(6, 78, 59, 0.75);
}

.highlight-text {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 18px;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.highlight-text-dark {
    color: #047857;
}

.card-footer {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    font-size: 0.95rem;
    padding-top: 14px;
    border-top: 1px solid rgba(6, 78, 59, 0.15);
    width: 100%;
    justify-content: center;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.card-footer-dark {
    color: #064e3b;
}

.card-footer i {
    transition: transform 0.3s ease;
}

.feature-card:hover .card-footer i {
    transform: translateX(10px);
}

.page-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 15px;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.page-title-light {
    color: #ffffff;
}

.page-subtitle {
    font-size: 1.2rem;
    font-weight: 300;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.page-subtitle-light {
    color: rgba(255, 255, 255, 0.8);
}

.page-2 {
    background-image:
        linear-gradient(135deg, rgba(6, 78, 59, 0.95) 0%, rgba(4, 120, 87, 0.9) 100%),
        url('/src/assets/backgrounds/landscape-2.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.page-2 .page-content {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.scrolled-header {
    text-align: center;
    margin-bottom: 50px;
}

.page-3 {
    background-image:
        linear-gradient(to bottom, rgba(6, 78, 59, 0.95) 0%, rgba(6, 78, 59, 0.9) 50%, rgba(255, 255, 255, 0.9) 50%, rgba(255, 255, 255, 0.95) 100%),
        url('/src/assets/backgrounds/landscape-3.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.page-3 .page-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.page-3-top {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 20px 0;
    box-sizing: border-box;
}

.page-3-bottom {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 20px 0;
    box-sizing: border-box;
}

.testimonial-card {
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 50px;
    max-width: 900px;
    margin-bottom: 40px;
    opacity: 0;
    transform: translateY(40px);
    transition: all 0.8s ease 0.2s;
}

.testimonial-card-light {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid rgba(255, 255, 255, 0.8);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.page-3.active .testimonial-card {
    opacity: 1;
    transform: translateY(0);
}

.quote-icon {
    font-size: 40px;
    margin-bottom: 20px;
}

.quote-icon-light {
    color: #064e3b;
}

.testimonial-text {
    font-size: 1.3rem;
    line-height: 1.8;
    text-align: center;
    margin-bottom: 30px;
    font-style: italic;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.testimonial-text-light {
    color: rgba(6, 78, 59, 0.8);
}

.client-info {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
}

.client-avatar {
    font-size: 48px;
}

.client-name {
    font-size: 1.1rem;
    font-weight: 600;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.client-name-light {
    color: #064e3b;
}

.client-title {
    font-size: 0.9rem;
    font-weight: 300;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.client-title-light {
    color: rgba(6, 78, 59, 0.6);
}

.rating {
    display: flex;
    gap: 4px;
}

.rating i {
    color: #fbbf24;
}

.cta-container {
    text-align: center;
}

.cta-button {
    background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
    color: white;
    border: none;
    padding: 20px 50px;
    border-radius: 16px;
    font-size: 1.2rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.cta-button:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.button-content {
    display: flex;
    align-items: center;
    gap: 12px;
}

.button-content i {
    font-size: 1.4rem;
}

.support-info {
    margin-top: 30px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
}

.support-contact {
    font-size: 1rem;
    font-weight: 500;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.support-contact-light {
    color: rgba(6, 78, 59, 0.7);
}

.support-contact i {
    margin-right: 8px;
    color: #064e3b;
}

.features-carousel {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    width: 100%;
}

.page-indicator {
    position: fixed;
    right: 30px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 16px;
    z-index: 100;
}

.indicator-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: rgba(6, 78, 59, 0.3);
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid rgba(6, 78, 59, 0.2);
}

.indicator-dot:hover {
    transform: scale(1.2);
    background: rgba(6, 78, 59, 0.5);
}

.indicator-dot.active {
    background: #064e3b;
    border-color: #064e3b;
    transform: scale(1.3);
}

@keyframes float {
    0%, 100% {
        transform: translate(0, 0);
    }
    25% {
        transform: translate(20px, -20px);
    }
    50% {
        transform: translate(-10px, 15px);
    }
    75% {
        transform: translate(15px, 10px);
    }
}

@keyframes shimmer {
    0%, 100% {
        opacity: 0.3;
    }
    50% {
        opacity: 0.6;
    }
}

@media (max-width: 1200px) {
    .features-carousel {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .features-carousel {
        grid-template-columns: 1fr;
    }

    .page {
        padding: 60px 15px 30px;
    }

    .mega-title {
        font-size: 3rem;
    }

    .mega-subtitle {
        font-size: 1.2rem;
    }
}
</style>
