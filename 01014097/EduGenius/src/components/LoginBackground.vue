<template>
    <div class="background-container" @mousemove="handleMouseMove">
        <!-- 主背景SVG -->
        <svg class="background-svg" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">
            <defs>
                <!-- 科技感渐变背景 -->
                <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#2193b0" />  <!-- 深蓝绿色 -->
                    <stop offset="50%" stop-color="#00b4d8" /> <!-- 中等蓝绿色 -->
                    <stop offset="100%" stop-color="#90e0ef" /> <!-- 浅蓝绿色 -->
                </linearGradient>

                <!-- 教育主题图标 -->
                <symbol id="icon-book" viewBox="0 0 24 24">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 18H4V4h16v16zM8 6h4v4l-2-2-2 2V6z"/>
                </symbol>

                <symbol id="icon-cap" viewBox="0 0 24 24">
                    <path d="M12 3L1 9l11 6 9-4.91V17h2V9M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/>
                </symbol>

                <symbol id="icon-brain" viewBox="0 0 24 24">
                    <path d="M12 4c2.21 0 4 1.79 4 4s-1.79 4-4 4-4-1.79-4-4 1.79-4 4-4m0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m0 7c2.67 0 8 1.33 8 4v3H4v-3c0-2.67 5.33-4 8-4m0 1.9c-3 0-6.1 1.46-6.1 2.1v1.1h12.2V17c0-.64-3.1-2.1-6.1-2.1z"/>
                </symbol>

                <symbol id="icon-chart" viewBox="0 0 24 24">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7zm4-3h2v10h-2zm4 6h2v4h-2z"/>
                </symbol>

                <!-- 数据流路径 -->
                <path id="data-path-1" d="M0,100 C200,50 400,150 600,100 C800,50 1000,150 1200,100 C1400,50 1600,150 1800,100" />
                <path id="data-path-2" d="M0,300 C200,250 400,350 600,300 C800,250 1000,350 1200,300 C1400,250 1600,350 1800,300" />
                <path id="data-path-3" d="M0,500 C200,450 400,550 600,500 C800,450 1000,550 1200,500 C1400,450 1600,550 1800,500" />

                <!-- 高级视觉效果 -->
                <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>

                <filter id="noise">
                    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" />
                    <feColorMatrix type="saturate" values="0" />
                    <feComposite in="SourceGraphic" operator="in" />
                </filter>
            </defs>

            <!-- 背景矩形 -->
            <rect width="100%" height="100%" fill="url(#bgGradient)" />

            <!-- 数据流动画 -->
            <use href="#data-path-1" class="data-path" x="-200" y="0" stroke="rgba(255,255,255,0.1)" stroke-width="2" fill="none" />
            <use href="#data-path-2" class="data-path" x="-200" y="0" stroke="rgba(255,255,255,0.1)" stroke-width="2" fill="none" />
            <use href="#data-path-3" class="data-path" x="-200" y="0" stroke="rgba(255,255,255,0.1)" stroke-width="2" fill="none" />

            <!-- 动态几何形状 -->
            <polygon class="shape shape-1" points="100,100 150,150 100,200 50,150" />
            <rect class="shape shape-2" x="1200" y="200" width="100" height="100" rx="10" />
            <circle class="shape shape-3" cx="300" cy="700" r="60" />
            <path class="shape shape-4" d="M1100,700 L1150,650 L1200,700 L1150,750 Z" />

            <!-- 教育主题图标 -->
            <use href="#icon-book" class="icon icon-1" x="20%" y="25%" width="70" height="70" />
            <use href="#icon-cap" class="icon icon-2" x="75%" y="15%" width="80" height="80" />
            <use href="#icon-brain" class="icon icon-3" x="10%" y="70%" width="90" height="90" />
            <use href="#icon-chart" class="icon icon-4" x="80%" y="65%" width="60" height="60" />

            <!-- 鼠标跟随效果 -->
            <circle class="mouse-follower" :cx="mouseX" :cy="mouseY" r="50" />
            <circle class="mouse-follower-2" :cx="mouseX" :cy="mouseY" r="30" />
        </svg>

        <!-- 高级粒子系统 -->
        <div class="particles">
            <div v-for="(particle, index) in particles" :key="index"
                 class="particle"
                 :class="'particle-' + particle.type"
                 :style="{
                     left: particle.x + 'vw',
                     top: particle.y + 'vh',
                     width: particle.size + 'px',
                     height: particle.size + 'px',
                     animationDelay: particle.delay + 's',
                     opacity: particle.opacity,
                     transform: 'rotate(' + particle.rotation + 'deg)',
                     backgroundColor: particle.color
                 }"></div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'EduPlatformBackground',
    data() {
        return {
            mouseX: -100,
            mouseY: -100,
            particles: Array.from({ length: 30 }, (_, i) => ({
                x: Math.random() * 100,
                y: Math.random() * 100,
                size: Math.random() * 10 + 5,
                delay: Math.random() * 15,
                opacity: Math.random() * 0.6 + 0.2,
                rotation: Math.random() * 360,
                color: this.getRandomColor(),
                type: Math.floor(Math.random() * 3) + 1
            }))
        }
    },
    methods: {
        handleMouseMove(e) {
            const rect = e.target.getBoundingClientRect()
            this.mouseX = ((e.clientX - rect.left) / rect.width) * 1440
            this.mouseY = ((e.clientY - rect.top) / rect.height) * 900
        },
        getRandomColor() {
            const colors = [
                'rgba(106, 17, 203, 0.7)',
                'rgba(74, 0, 224, 0.7)',
                'rgba(37, 117, 252, 0.7)',
                'rgba(100, 255, 218, 0.7)',
                'rgba(255, 255, 255, 0.7)'
            ]
            return colors[Math.floor(Math.random() * colors.length)]
        }
    }
}
</script>

<style scoped>
.background-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
}

.background-svg {
    width: 100%;
    height: 100%;
    opacity: 0.9;
}

.data-path {
    stroke-dasharray: 10, 5;
    animation: dataFlow 30s linear infinite;
}

@keyframes dataFlow {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(200px);
    }
}

.shape {
    fill: none;
    stroke: rgba(255, 255, 255, 0.1);
    stroke-width: 1;
}

.shape-1 {
    animation: float 15s ease-in-out infinite;
    stroke-dasharray: 5, 5;
}

.shape-2 {
    animation: float 18s ease-in-out infinite reverse;
    stroke-dasharray: 10, 5;
}

.shape-3 {
    animation: float 12s ease-in-out infinite;
    stroke-dasharray: 15, 10;
}

.shape-4 {
    animation: float 20s ease-in-out infinite reverse;
    stroke-dasharray: 8, 4;
}

@keyframes float {
    0%, 100% {
        transform: translate(0, 0);
    }
    25% {
        transform: translate(20px, 20px);
    }
    50% {
        transform: translate(0, 40px);
    }
    75% {
        transform: translate(-20px, 20px);
    }
}

.icon {
    fill: rgba(255, 255, 255, 0.8);
    filter: url(#glow);
    transition: all 0.5s ease;
    opacity: 0.9;
}

.icon-1 {
    animation: floatIcon1 12s ease-in-out infinite;
}

.icon-2 {
    animation: floatIcon2 15s ease-in-out infinite reverse;
}

.icon-3 {
    animation: floatIcon3 18s ease-in-out infinite;
}

.icon-4 {
    animation: floatIcon4 14s ease-in-out infinite reverse;
}

@keyframes floatIcon1 {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg);
    }
    50% {
        transform: translate(15px, 15px) rotate(5deg);
    }
}

@keyframes floatIcon2 {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg);
    }
    50% {
        transform: translate(-20px, 10px) rotate(-8deg);
    }
}

@keyframes floatIcon3 {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg);
    }
    50% {
        transform: translate(10px, -15px) rotate(10deg);
    }
}

@keyframes floatIcon4 {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg);
    }
    50% {
        transform: translate(-15px, 20px) rotate(-5deg);
    }
}

.mouse-follower {
    fill: rgba(255, 255, 255, 0.05);
    stroke: rgba(255, 255, 255, 0.3);
    stroke-width: 1;
    transition: all 0.1s ease-out;
    pointer-events: none;
}

.mouse-follower-2 {
    fill: rgba(255, 255, 255, 0.03);
    stroke: rgba(255, 255, 255, 0.2);
    stroke-width: 1;
    transition: all 0.15s ease-out;
    pointer-events: none;
}

.particles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.particle {
    position: absolute;
    animation: floatParticle 15s ease-in-out infinite;
    filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
}

.particle-1 {
    border-radius: 50%;
}

.particle-2 {
    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
}

.particle-3 {
    clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
}

@keyframes floatParticle {
    0%, 100% {
        transform: translate(0, 0) scale(1) rotate(0deg);
    }
    25% {
        transform: translate(10px, 10px) scale(1.1) rotate(90deg);
    }
    50% {
        transform: translate(0, 20px) scale(0.9) rotate(180deg);
    }
    75% {
        transform: translate(-10px, 10px) scale(1.05) rotate(270deg);
    }
}

.icon:hover {
    fill: rgba(255, 255, 255, 1);
    transform: scale(1.15);
    filter: url(#glow);
    opacity: 1;
    cursor: pointer;
}

/* 响应式调整 */
@media (max-width: 768px) {
    .icon {
        width: 40px !important;
        height: 40px !important;
    }

    .shape {
        display: none;
    }
}
</style>
