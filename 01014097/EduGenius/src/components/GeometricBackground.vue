<template>
    <div class="geometric-background">
        <div
            v-for="(shape, index) in shapes"
            :key="index"
            class="geometric-shape"
            :class="`shape-${index + 1}`"
            :style="{
        'width': shape.size,
        'height': shape.size,
        'background': shape.gradient,
        'top': shape.position.top,
        'left': shape.position.left,
        'right': shape.position.right,
        'bottom': shape.position.bottom,
        'animation-delay': shape.animation.delay,
        'filter': `blur(${shape.blur})`,
        'animation-duration': animationDuration
      }"
        ></div>

        <!-- 添加网格纹理 -->
        <div class="grid-overlay"></div>

        <!-- 添加光晕效果 -->
        <div class="glow-effect"></div>
    </div>
</template>

<script>
export default {
    name: 'GeometricBackground',
    props: {
        shapes: {
            type: Array,
            default: () => [
                {
                    size: '320px',
                    gradient: 'linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(99, 102, 241, 0.25))',
                    position: { top: '-160px', left: '-160px' },
                    animation: { delay: '0s' },
                    blur: '80px'
                },
                {
                    size: '280px',
                    gradient: 'linear-gradient(45deg, rgba(16, 185, 129, 0.18), rgba(5, 150, 105, 0.28))',
                    position: { top: '20%', right: '-140px' },
                    animation: { delay: '-8s' },
                    blur: '60px'
                },
                {
                    size: '400px',
                    gradient: 'linear-gradient(225deg, rgba(245, 158, 11, 0.12), rgba(217, 119, 6, 0.22))',
                    position: { bottom: '-200px', left: '30%' },
                    animation: { delay: '-15s' },
                    blur: '100px'
                },
                {
                    size: '240px',
                    gradient: 'linear-gradient(315deg, rgba(236, 72, 153, 0.14), rgba(190, 24, 93, 0.24))',
                    position: { top: '60%', left: '-120px' },
                    animation: { delay: '-22s' },
                    blur: '70px'
                },
                {
                    size: '180px',
                    gradient: 'linear-gradient(180deg, rgba(59, 130, 246, 0.16), rgba(37, 99, 235, 0.26))',
                    position: { top: '10%', left: '70%' },
                    animation: { delay: '-30s' },
                    blur: '50px'
                },
                {
                    size: '350px',
                    gradient: 'linear-gradient(90deg, rgba(168, 85, 247, 0.13), rgba(126, 34, 206, 0.23))',
                    position: { bottom: '20%', right: '-175px' },
                    animation: { delay: '-12s' },
                    blur: '90px'
                }
            ]
        },
        animationDuration: {
            type: String,
            default: '25s'
        },
        opacity: {
            type: Number,
            default: 0.7
        }
    }
}
</script>

<style scoped>
.geometric-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    overflow: hidden;
    background: linear-gradient(135deg,
    rgba(249, 250, 251, 0.4) 0%,
    rgba(243, 244, 246, 0.6) 50%,
    rgba(229, 231, 235, 0.4) 100%
    );
}

.geometric-shape {
    position: absolute;
    border-radius: 50%;
    animation: elegantFloat var(--animation-duration, 25s) ease-in-out infinite;
    transform-origin: center;
    opacity: v-bind(opacity);
    will-change: transform;
}

/* 不同形状的特殊效果 */
.shape-1 {
    border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
    animation: elegantFloat 25s ease-in-out infinite, morphShape1 15s ease-in-out infinite alternate;
}

.shape-2 {
    border-radius: 40% 60% 70% 30% / 40% 70% 30% 60%;
    animation: elegantFloat 25s ease-in-out infinite, morphShape2 18s ease-in-out infinite alternate;
}

.shape-3 {
    border-radius: 70% 30% 40% 60% / 30% 60% 40% 70%;
    animation: elegantFloat 25s ease-in-out infinite, morphShape3 20s ease-in-out infinite alternate;
}

.shape-4 {
    border-radius: 50% 50% 30% 70% / 50% 30% 70% 50%;
    animation: elegantFloat 25s ease-in-out infinite, morphShape4 22s ease-in-out infinite alternate;
}

.shape-5 {
    border-radius: 30% 70% 50% 50% / 70% 50% 50% 30%;
    animation: elegantFloat 25s ease-in-out infinite, morphShape5 16s ease-in-out infinite alternate;
}

.shape-6 {
    border-radius: 80% 20% 60% 40% / 20% 80% 40% 60%;
    animation: elegantFloat 25s ease-in-out infinite, morphShape6 24s ease-in-out infinite alternate;
}

/* 网格纹理覆盖 */
.grid-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        linear-gradient(rgba(156, 163, 175, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(156, 163, 175, 0.1) 1px, transparent 1px);
    background-size: 50px 50px;
    opacity: 0.5;
}

/* 光晕效果 */
.glow-effect {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 80%;
    height: 80%;
    transform: translate(-50%, -50%);
    background: radial-gradient(
        circle at center,
        rgba(229, 231, 235, 0.3) 0%,
        rgba(209, 213, 219, 0.5) 30%,
        transparent 70%
    );
    border-radius: 50%;
    animation: glowPulse 30s ease-in-out infinite;
}

/* 动画定义 */
@keyframes elegantFloat {
    0%, 100% {
        transform: translateY(0) translateX(0) rotate(0deg) scale(1);
    }
    25% {
        transform: translateY(-15px) translateX(10px) rotate(90deg) scale(1.05);
    }
    50% {
        transform: translateY(-25px) translateX(0) rotate(180deg) scale(1.1);
    }
    75% {
        transform: translateY(-10px) translateX(-10px) rotate(270deg) scale(1.05);
    }
}

@keyframes morphShape1 {
    0% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
    100% { border-radius: 30% 70% 60% 40% / 40% 60% 30% 70%; }
}

@keyframes morphShape2 {
    0% { border-radius: 40% 60% 70% 30% / 40% 70% 30% 60%; }
    100% { border-radius: 70% 30% 40% 60% / 60% 40% 70% 30%; }
}

@keyframes morphShape3 {
    0% { border-radius: 70% 30% 40% 60% / 30% 60% 40% 70%; }
    100% { border-radius: 40% 60% 30% 70% / 70% 40% 60% 30%; }
}

@keyframes morphShape4 {
    0% { border-radius: 50% 50% 30% 70% / 50% 30% 70% 50%; }
    100% { border-radius: 30% 70% 50% 50% / 70% 50% 50% 30%; }
}

@keyframes morphShape5 {
    0% { border-radius: 30% 70% 50% 50% / 70% 50% 50% 30%; }
    100% { border-radius: 50% 50% 70% 30% / 50% 70% 30% 50%; }
}

@keyframes morphShape6 {
    0% { border-radius: 80% 20% 60% 40% / 20% 80% 40% 60%; }
    100% { border-radius: 60% 40% 80% 20% / 40% 60% 20% 80%; }
}

@keyframes glowPulse {
    0%, 100% {
        opacity: 0.3;
        transform: translate(-50%, -50%) scale(1);
    }
    50% {
        opacity: 0.1;
        transform: translate(-50%, -50%) scale(1.1);
    }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .geometric-shape {
        transform: scale(0.7);
    }

    .grid-overlay {
        background-size: 30px 30px;
    }
}

@media (max-width: 480px) {
    .geometric-shape {
        transform: scale(0.5);
    }

    .grid-overlay {
        background-size: 20px 20px;
        opacity: 0.1;
    }
}

/* 深色主题支持 */
@media (prefers-color-scheme: dark) {
    .geometric-background {
        background: linear-gradient(135deg,
        rgba(0, 0, 0, 0.02) 0%,
        rgba(15, 23, 42, 0.05) 50%,
        rgba(30, 41, 59, 0.03) 100%
        );
    }

    .grid-overlay {
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.01) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.01) 1px, transparent 1px);
    }

    .glow-effect {
        background: radial-gradient(
            circle at center,
            rgba(255, 255, 255, 0.01) 0%,
            rgba(248, 250, 252, 0.02) 30%,
            transparent 70%
        );
    }
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
    .geometric-shape {
        animation: none;
    }

    .glow-effect {
        animation: none;
    }
}

/* 性能优化 */
.geometric-shape {
    backface-visibility: hidden;
    transform-style: preserve-3d;
}
</style>
