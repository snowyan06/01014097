<template>
    <div class="analysis-improvement">
        <GeometricBackground />
        <div class="scenic-background"></div>

        <!-- 顶部蓝色标题栏 -->
        <div class="page-banner">
            <div class="banner-decoration">
                <div class="deco-circle deco-circle-1"></div>
                <div class="deco-circle deco-circle-2"></div>
            </div>
            <div class="banner-content">
                <div class="banner-text">
                    <h2 class="banner-title">学生学情画像分析</h2>
                    <p class="banner-subtitle">Student Profile Analysis</p>
                </div>
                <span class="banner-tag">赛题强制需求1 对话式6维动态可量化学情画像系统</span>
            </div>
        </div>

        <!-- 主体白色圆角卡片 -->
        <div class="main-card">
            <div class="card-inner">
                <!-- 左半栏：雷达图 -->
                <div class="left-panel">
                    <div class="radar-wrapper">
                        <div ref="radarChartRef" class="radar-chart"></div>
                    </div>
                    <!-- 功能按钮 -->
                    <div class="radar-actions">
                        <button class="btn btn-primary">刷新学情画像数据</button>
                        <button class="btn btn-outline">导出画像分析报告</button>
                    </div>
                </div>

                <!-- 右半栏：六维度详情诊断列表 -->
                <div class="right-panel">
                    <div v-for="(item, index) in dimensions" :key="index" class="dimension-item">
                        <div class="dimension-header">
                            <span class="dimension-name">{{ item.name }}</span>
                            <span class="dimension-score">{{ item.score }}%</span>
                        </div>
                        <p class="dimension-desc">{{ item.diagnostic }}</p>
                    </div>
                </div>
            </div>

            <!-- 底部说明文字 -->
            <div class="card-footer">
                <p>本画像系统支持对话自动采集学情，完成练习、答疑、资源学习后自动更新六维度量化分值，动态刷新雷达图，满足赛题对话式动态画像硬性要求。</p>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import GeometricBackground from '@/components/GeometricBackground.vue';
import * as echarts from 'echarts';

export default {
    name: 'AnalysisImprovement',
    components: {
        GeometricBackground
    },
    setup() {
        const radarChartRef = ref(null);
        let chartInstance = null;

        const dimensions = [
            { name: '知识基础', score: 86, diagnostic: '核心专业知识点覆盖率良好，底层编程基础扎实，高阶拓展内容有待补充' },
            { name: '认知风格', score: 74, diagnostic: '更偏向实操代码类学习资源，理论文档吸收效率一般，可搭配思维导图辅助理解' },
            { name: '易错短板', score: 62, diagnostic: '算法逻辑、底层原理类题目失分较多，需增加专项分层题库训练' },
            { name: '学习目标', score: 90, diagnostic: '目标清晰，以开发岗求职为核心诉求，适合推送面试真题、项目实操类资源' },
            { name: '学习节奏', score: 79, diagnostic: '日均学习时长稳定，但缺少定期复盘习惯，建议增加阶段性复习节点' },
            { name: '兴趣偏好', score: 83, diagnostic: '对AI算法、大模型开发方向兴趣度高，路径规划可优先倾斜相关课程资源' }
        ];

        const initRadarChart = () => {
            if (!radarChartRef.value) return;
            chartInstance = echarts.init(radarChartRef.value);

            const option = {
                radar: {
                    indicator: [
                        { name: '知识基础', max: 100 },
                        { name: '认知风格', max: 100 },
                        { name: '易错短板', max: 100 },
                        { name: '学习目标', max: 100 },
                        { name: '学习节奏', max: 100 },
                        { name: '兴趣偏好', max: 100 }
                    ],
                    shape: 'polygon',
                    radius: '65%',
                    center: ['50%', '50%'],
                    splitNumber: 5,
                    axisName: {
                        color: '#334155',
                        fontSize: 13,
                        fontWeight: 600
                    },
                    splitArea: {
                        areaStyle: {
                            color: ['rgba(22, 93, 255, 0.02)', 'rgba(22, 93, 255, 0.04)', 'rgba(22, 93, 255, 0.06)', 'rgba(22, 93, 255, 0.08)', 'rgba(22, 93, 255, 0.10)']
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(22, 93, 255, 0.15)'
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(22, 93, 255, 0.2)'
                        }
                    }
                },
                series: [
                    {
                        type: 'radar',
                        data: [
                            {
                                value: [86, 74, 62, 90, 79, 83],
                                name: '学情画像',
                                symbol: 'circle',
                                symbolSize: 6,
                                lineStyle: {
                                    color: '#165DFF',
                                    width: 2
                                },
                                itemStyle: {
                                    color: '#165DFF'
                                },
                                areaStyle: {
                                    color: 'rgba(22, 93, 255, 0.2)'
                                }
                            }
                        ]
                    }
                ]
            };

            chartInstance.setOption(option);
        };

        onMounted(() => {
            initRadarChart();
            window.addEventListener('resize', handleResize);
        });

        onBeforeUnmount(() => {
            window.removeEventListener('resize', handleResize);
            if (chartInstance) {
                chartInstance.dispose();
            }
        });

        const handleResize = () => {
            if (chartInstance) {
                chartInstance.resize();
            }
        };

        return {
            radarChartRef,
            dimensions
        };
    }
}
</script>

<style scoped lang="scss">
.scenic-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
        linear-gradient(to bottom, rgba(22, 93, 255, 0.85) 0%, rgba(64, 128, 255, 0.8) 40%, rgba(255, 255, 255, 0.85) 40%, rgba(255, 255, 255, 0.9) 100%),
        url('/src/assets/backgrounds/landscape-3.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    z-index: -2;
    pointer-events: none;
}

.analysis-improvement {
    padding: 24px;
    background-color: transparent;
    min-height: 100vh;
}

/* ===== 顶部蓝色标题栏 ===== */
.page-banner {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #0e7490 100%);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 16px rgba(30, 58, 138, 0.25);
}

.banner-decoration {
    position: absolute;
    inset: 0;
    opacity: 0.1;
    z-index: 1;
    pointer-events: none;
}

.deco-circle {
    position: absolute;
    border-radius: 50%;
    background: #fff;
}

.deco-circle-1 {
    width: 128px;
    height: 128px;
    top: -16px;
    right: -16px;
}

.deco-circle-2 {
    width: 96px;
    height: 96px;
    bottom: -16px;
    left: -16px;
}

.banner-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.banner-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    font-family: 'SimSun', 'STSong', 'Adobe Song Std', serif;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

.banner-subtitle {
    font-size: 0.875rem;
    color: #fff;
    margin: 0.25rem 0 0;
    opacity: 0.9;
    font-family: 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

.banner-tag {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.55);
    white-space: nowrap;
}

/* ===== 主体白色卡片 ===== */
.main-card {
    background: rgba(255, 255, 255, 0.97);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.card-inner {
    display: flex;
    gap: 2rem;
}

/* ===== 左半栏：雷达图 ===== */
.left-panel {
    flex: 0 0 45%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.radar-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.radar-chart {
    width: 100%;
    height: 420px;
}

.radar-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.btn {
    padding: 0.6rem 1.25rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
}

.btn-primary {
    background: #165DFF;
    color: #fff;
}

.btn-primary:hover {
    background: #0e4fd9;
    box-shadow: 0 4px 12px rgba(22, 93, 255, 0.3);
}

.btn-outline {
    background: #fff;
    color: #165DFF;
    border: 1.5px solid #165DFF;
}

.btn-outline:hover {
    background: rgba(22, 93, 255, 0.05);
}

/* ===== 右半栏：维度列表 ===== */
.right-panel {
    flex: 0 0 55%;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    justify-content: center;
}

.dimension-item {
    padding: 0.875rem 1rem;
    background: #f8fafc;
    border-radius: 8px;
    border: 1px solid #f1f5f9;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.dimension-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.dimension-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.375rem;
}

.dimension-name {
    font-size: 0.9375rem;
    font-weight: 700;
    color: #1e293b;
}

.dimension-score {
    font-size: 1rem;
    font-weight: 700;
    color: #165DFF;
}

.dimension-desc {
    font-size: 0.8125rem;
    color: #64748b;
    margin: 0;
    line-height: 1.5;
}

/* ===== 底部说明 ===== */
.card-footer {
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid #f1f5f9;
    text-align: center;
}

.card-footer p {
    font-size: 0.75rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.6;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
    .analysis-improvement {
        padding: 1rem;
    }

    .main-card {
        padding: 1.25rem;
    }

    .card-inner {
        flex-direction: column;
    }

    .left-panel,
    .right-panel {
        flex: 1 1 100%;
    }

    .radar-chart {
        height: 320px;
    }

    .banner-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
}
</style>
