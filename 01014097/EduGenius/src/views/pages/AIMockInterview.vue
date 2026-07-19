<template>
    <div class="adaptive-learning-path">
        <GeometricBackground />
        <div class="scenic-background"></div>

        <!-- 第一层：顶部深青蓝渐变通栏标题块 -->
        <div class="page-banner">
            <div class="banner-decoration">
                <div class="deco-circle deco-circle-1"></div>
                <div class="deco-circle deco-circle-2"></div>
            </div>
            <div class="banner-content">
                <div class="banner-text">
                    <h2 class="banner-title">自适应学习路径规划</h2>
                    <p class="banner-subtitle">Adaptive Learning Path Planning</p>
                </div>
                <span class="banner-tag">赛题强制核心需求3</span>
            </div>
        </div>

        <!-- 第二层：Tab 标签栏 -->
        <div class="tab-bar">
            <div
                v-for="(tab, index) in tabs"
                :key="index"
                class="tab-item"
                :class="{ active: activeTab === index }"
                @click="activeTab = index"
            >
                {{ tab }}
            </div>
        </div>

        <!-- 第三层：主体内容区域（左大右窄双栏） -->
        <div class="main-layout">
            <!-- 左侧大卡片（75%） -->
            <div class="left-panel">

                <!-- Tab1：路径生成配置 -->
                <div v-if="activeTab === 0" class="content-card">
                    <h3 class="card-title">路径生成参数配置</h3>

                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">绑定学生学情画像</label>
                            <select class="form-select" v-model="selectedStudentId">
                                <option value="">请选择学生</option>
                                <option v-for="s in students" :key="s.id" :value="s.id">
                                    {{ s.avatar }} {{ s.nickname }}（{{ s.grade }} · {{ s.major }}）
                                </option>
                            </select>
                            <div v-if="selectedStudent" class="student-profile-card">
                                <div class="profile-header">
                                    <span class="profile-avatar">{{ selectedStudent.avatar }}</span>
                                    <div class="profile-info">
                                        <span class="profile-name">{{ selectedStudent.nickname }}</span>
                                        <span class="profile-meta">{{ selectedStudent.grade }} · {{ selectedStudent.major }} · {{ selectedStudent.username }}</span>
                                    </div>
                                </div>
                                <p class="profile-summary">{{ selectedStudent.summary }}</p>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">目标专业课程</label>
                            <select class="form-select" v-model="selectedCourse">
                                <option value="">请选择课程</option>
                                <option v-for="c in courses" :key="c.name" :value="c.name">
                                    {{ c.name }}
                                </option>
                            </select>
                            <div v-if="selectedCourseObj" class="course-desc-card">
                                <span class="course-desc-text">{{ selectedCourseObj.desc }}</span>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">学习难度规划</label>
                            <div class="radio-group">
                                <label class="radio-label" :class="{ active: selectedDifficulty === 'short' }" @click="selectedDifficulty = 'short'">
                                    <input type="radio" v-model="selectedDifficulty" value="short" class="hidden-radio" />
                                    短期夯实基础
                                </label>
                                <label class="radio-label" :class="{ active: selectedDifficulty === 'standard' }" @click="selectedDifficulty = 'standard'">
                                    <input type="radio" v-model="selectedDifficulty" value="standard" class="hidden-radio" />
                                    标准均衡规划
                                </label>
                                <label class="radio-label" :class="{ active: selectedDifficulty === 'long' }" @click="selectedDifficulty = 'long'">
                                    <input type="radio" v-model="selectedDifficulty" value="long" class="hidden-radio" />
                                    长期拔高进阶
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="form-row two-col">
                        <div class="form-group">
                            <label class="form-label">知识点筛选</label>
                            <select class="form-select" v-model="selectedFilter">
                                <option value="all">全知识点</option>
                                <option v-for="kp in knowledgePointList" :key="kp" :value="kp">{{ kp }}</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">学习周期偏好</label>
                            <select class="form-select" v-model="selectedCycle">
                                <option value="general">通用周期规划</option>
                                <option value="weekly">按周规划</option>
                                <option value="monthly">按月规划</option>
                            </select>
                        </div>
                    </div>

                    <div class="action-buttons">
                        <div class="action-item">
                            <button class="btn btn-primary" @click="generateLearningPath" :disabled="loading">
                                {{ loading ? '生成中...' : '生成自适应分层学习路线' }}
                            </button>
                        </div>
                        <div class="action-item">
                            <button class="btn btn-outline" @click="replanLearningPath" :disabled="loading">
                                {{ loading ? '重新规划中...' : '重新动态规划路径' }}
                            </button>
                        </div>
                        <div class="action-item">
                            <button class="btn btn-outline" @click="resetConfig">清空全部配置参数</button>
                        </div>
                    </div>

                    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
                </div>

                <!-- Tab2：分层学习路线可视化 -->
                <div v-if="activeTab === 1" class="content-card">
                    <div class="route-flow-container">
                        <h4 class="section-subtitle">学习路线流程图</h4>

                        <div v-if="graphLoading" class="loading-placeholder">
                            <span>加载知识图谱中...</span>
                        </div>
                        <div v-else-if="!hasGraphData" class="empty-placeholder">
                            <p>暂无知识图谱数据，请先在"路径生成配置"中选择学生并生成路径</p>
                        </div>
                        <template v-else>
                            <div ref="visNetworkContainer" class="vis-network-container"></div>

                            <div class="flow-legend">
                                <span class="legend-item"><span class="legend-dot learned-dot"></span> 已掌握（≥70分）</span>
                                <span class="legend-item"><span class="legend-dot learning-dot"></span> 学习中（30-69分）</span>
                                <span class="legend-item"><span class="legend-dot unlearned-dot"></span> 未学习（＜30分）</span>
                            </div>

                            <div v-if="selectedNodeInfo" class="node-detail-card">
                                <h5 class="node-detail-title">{{ selectedNodeInfo.name }}</h5>
                                <div class="node-detail-stats">
                                    <span>掌握度：<strong :style="{ color: selectedNodeInfo.color }">{{ selectedNodeInfo.score }}分</strong></span>
                                    <span>答题数：{{ selectedNodeInfo.total }}次</span>
                                    <span>正确数：{{ selectedNodeInfo.correct }}次</span>
                                </div>
                            </div>
                        </template>
                    </div>

                    <div class="resource-tabs-section">
                        <h4 class="section-subtitle">配套多模态学习资源</h4>
                        <div class="resource-tabs">
                            <div
                                v-for="(rtab, rindex) in resourceTabs"
                                :key="rindex"
                                class="resource-tab"
                                :class="{ active: activeResourceTab === rindex }"
                                @click="activeResourceTab = rindex"
                            >
                                {{ rtab }}
                            </div>
                        </div>
                        <div class="resource-cards-grid">
                            <div v-for="(res, ri) in currentResources" :key="ri" class="resource-card">
                                <div class="resource-card-body">
                                    <span class="resource-card-title">{{ res.title }}</span>
                                    <span class="resource-card-desc">{{ res.desc }}</span>
                                </div>
                                <div class="resource-card-actions">
                                    <button class="btn btn-sm btn-outline">预览</button>
                                    <button class="btn btn-sm btn-primary">跳转学习</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card-bottom-actions">
                        <button class="btn btn-primary" @click="refreshGraph">刷新路径状态</button>
                        <button class="btn btn-outline" @click="exportPath">导出当前路径方案</button>
                    </div>
                </div>

                <!-- Tab3：历史学习路径管理 -->
                <div v-if="activeTab === 2" class="content-card">
                    <div class="card-header-row">
                        <h3 class="card-title" style="margin: 0;">历史保存学习路径记录</h3>
                        <button class="btn btn-outline btn-sm" @click="exportAllPaths">批量导出全部历史路径记录</button>
                    </div>
                    <div v-if="learningPaths.length === 0" class="empty-placeholder">
                        <p>暂无历史路径记录，请先生成学习路径</p>
                    </div>
                    <div v-else class="history-scroll">
                        <div v-for="(path, index) in learningPaths" :key="index" class="history-card">
                            <div class="history-card-info">
                                <span class="history-date">{{ path.date }}</span>
                                <span class="history-course">{{ path.course }}</span>
                                <span class="history-difficulty" :class="path.difficultyClass">
                                    {{ path.difficultyLabel }}
                                </span>
                                <span class="history-kp-count">知识点：{{ path.knowledgePoints?.length || 0 }}个</span>
                            </div>
                            <div class="history-card-actions">
                                <button class="btn btn-sm btn-outline" @click="viewPath(index)">切换查看</button>
                                <button class="btn btn-sm btn-danger" @click="deletePath(index)">删除记录</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 右侧固定侧边窄卡片（23%，所有Tab全程显示） -->
            <div class="right-panel">
                <div class="sidebar-card">
                    <h4 class="sidebar-title">路径配套资源快捷入口</h4>
                    <button class="btn btn-primary btn-full" @click="goToResourceCenter">跳转至学习资源中心页面</button>
                    <div v-if="hasGraphData" class="sidebar-stats">
                        <div class="sidebar-stat-item">
                            <span class="stat-label">知识点总数</span>
                            <span class="stat-value">{{ knowledgePointList.length }}</span>
                        </div>
                        <div class="sidebar-stat-item">
                            <span class="stat-label">已掌握</span>
                            <span class="stat-value" style="color:#16a34a">{{ masteredCount }}</span>
                        </div>
                        <div class="sidebar-stat-item">
                            <span class="stat-label">学习中</span>
                            <span class="stat-value" style="color:#2563eb">{{ learningCount }}</span>
                        </div>
                        <div class="sidebar-stat-item">
                            <span class="stat-label">未学习</span>
                            <span class="stat-value" style="color:#9ca3af">{{ unlearnedCount }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { Network } from 'vis-network';
import GeometricBackground from '@/components/GeometricBackground.vue';
import { AIService } from '@/service/AIService';

export default {
    name: 'AIMockInterview',
    components: {
        GeometricBackground
    },
    setup() {
        const router = useRouter();
        const activeTab = ref(0);
        const selectedDifficulty = ref('standard');
        const activeResourceTab = ref(0);
        const tabs = ['路径生成配置', '分层学习路线可视化', '历史学习路径管理'];
        const resourceTabs = ['课程文档', '知识点思维导图', '分层练习题库', '代码实操案例', '拓展阅读材料', '教学动画脚本'];

        const selectedStudentId = ref('');
        const selectedCourse = ref('');
        const selectedFilter = ref('all');
        const selectedCycle = ref('general');
        const loading = ref(false);
        const graphLoading = ref(false);
        const errorMsg = ref('');

        const students = ref([
            {
                id: '5',
                username: 'student1',
                nickname: '小明',
                grade: '2022级',
                major: '计算机科学与技术',
                avatar: '🧑‍💻',
                summary: '已完成嵌入式系统基础模块学习，对硬件接口和底层驱动有较好理解，需加强通信协议和内核开发方面的练习。'
            }
        ]);
        const courses = ref([
            { name: '嵌入式系统', desc: '涵盖ARM架构、Linux内核驱动、RTOS实时系统等核心知识', userId: '5' },
            { name: '计算机组成原理', desc: '数据表示、运算器、存储系统、指令系统、CPU、总线与I/O', userId: '30' },
            { name: '计算机基础', desc: '计算机组成原理、数据结构与算法、操作系统基础', userId: '25' },
            { name: 'Linux系统开发', desc: 'Linux环境编程、Shell脚本、系统调用与进程管理', userId: '26' }
        ]);

        // 计算机组成原理示例知识图谱（后端无数据时使用）
        const sampleKnowledgeGraphs = {
            '30': {
                graph: {
                    '计算机系统概述': ['数据表示与运算', '存储系统', '指令系统'],
                    '数据表示与运算': ['定点数表示', '浮点数表示', '运算器结构'],
                    '存储系统': ['主存储器', '高速缓存Cache', '虚拟存储器'],
                    '指令系统': ['指令格式', '寻址方式', 'CISC与RISC'],
                    '中央处理器CPU': ['CPU功能与结构', '指令执行过程', '数据通路', '控制器设计'],
                    '总线与输入输出': ['总线结构', 'I/O接口', '中断系统', 'DMA方式'],
                    '指令执行过程': ['取指周期', '译码周期', '执行周期', '中断处理']
                },
                mastery: {
                    '计算机系统概述': { mastery_score: 85, total_questions: 10, correct_count: 8 },
                    '数据表示与运算': { mastery_score: 72, total_questions: 15, correct_count: 11 },
                    '定点数表示': { mastery_score: 65, total_questions: 12, correct_count: 8 },
                    '浮点数表示': { mastery_score: 40, total_questions: 20, correct_count: 8 },
                    '运算器结构': { mastery_score: 30, total_questions: 8, correct_count: 2 },
                    '存储系统': { mastery_score: 55, total_questions: 18, correct_count: 10 },
                    '主存储器': { mastery_score: 70, total_questions: 10, correct_count: 7 },
                    '高速缓存Cache': { mastery_score: 35, total_questions: 14, correct_count: 5 },
                    '虚拟存储器': { mastery_score: 20, total_questions: 10, correct_count: 2 },
                    '指令系统': { mastery_score: 60, total_questions: 12, correct_count: 7 },
                    '指令格式': { mastery_score: 75, total_questions: 8, correct_count: 6 },
                    '寻址方式': { mastery_score: 50, total_questions: 10, correct_count: 5 },
                    'CISC与RISC': { mastery_score: 45, total_questions: 6, correct_count: 3 },
                    '中央处理器CPU': { mastery_score: 25, total_questions: 15, correct_count: 4 },
                    'CPU功能与结构': { mastery_score: 30, total_questions: 10, correct_count: 3 },
                    '指令执行过程': { mastery_score: 15, total_questions: 12, correct_count: 2 },
                    '数据通路': { mastery_score: 10, total_questions: 8, correct_count: 1 },
                    '控制器设计': { mastery_score: 5, total_questions: 10, correct_count: 0 },
                    '总线与输入输出': { mastery_score: 40, total_questions: 14, correct_count: 6 },
                    '总线结构': { mastery_score: 55, total_questions: 8, correct_count: 4 },
                    'I/O接口': { mastery_score: 35, total_questions: 10, correct_count: 4 },
                    '中断系统': { mastery_score: 25, total_questions: 12, correct_count: 3 },
                    'DMA方式': { mastery_score: 15, total_questions: 6, correct_count: 1 },
                    '取指周期': { mastery_score: 20, total_questions: 8, correct_count: 2 },
                    '译码周期': { mastery_score: 10, total_questions: 6, correct_count: 1 },
                    '执行周期': { mastery_score: 5, total_questions: 8, correct_count: 0 },
                    '中断处理': { mastery_score: 18, total_questions: 10, correct_count: 2 }
                }
            }
        };

        // 计算机组成原理示例资源
        const sampleResources = {
            '课程文档': [
                { title: '计算机组成原理概述', desc: '冯·诺依曼体系结构、计算机硬件五大部件详解' },
                { title: '数据表示与编码', desc: '原码、反码、补码、移码及IEEE754浮点数标准' },
                { title: '存储系统层次结构', desc: '寄存器-Cache-主存-辅存四级存储体系' }
            ],
            '知识点思维导图': [
                { title: '运算器知识导图', desc: 'ALU结构、定点运算、浮点运算完整脉络' },
                { title: 'CPU数据通路导图', desc: '单总线、双总线、三总线数据通路对比' },
                { title: '存储系统导图', desc: 'Cache映射方式、虚拟存储页表机制' }
            ],
            '分层练习题库': [
                { title: '基础题：数据表示', desc: '原码/补码转换、浮点数范围计算（10题）' },
                { title: '提高题：Cache设计', desc: '直接映射/全相联/组相联命中率分析（8题）' },
                { title: '拓展题：流水线优化', desc: '冒险检测、分支预测、超标量设计（6题）' }
            ],
            '代码实操案例': [
                { title: 'ALU Verilog实现', desc: '32位算术逻辑单元设计与仿真' },
                { title: 'Cache模拟器', desc: 'Python实现三种映射方式的Cache模拟' },
                { title: '指令译码器', desc: 'MIPS指令集译码逻辑硬件描述' }
            ],
            '拓展阅读材料': [
                { title: 'RISC-V架构演进', desc: '从伯克利到开源指令集的设计哲学' },
                { title: '摩尔定律与芯片制造', desc: '从14nm到3nm的工艺演进与挑战' },
                { title: '量子计算基础', desc: '量子比特、量子门与传统计算的对比' }
            ],
            '教学动画脚本': [
                { title: '指令执行流程动画', desc: '取指-译码-执行-访存-写回五段流水线演示' },
                { title: 'Cache替换过程动画', desc: 'LRU/FIFO替换算法可视化对比' },
                { title: '中断处理流程动画', desc: '中断请求-响应-处理-返回完整过程' }
            ]
        };

        const currentResources = computed(() => {
            const tabName = resourceTabs[activeResourceTab.value];
            return sampleResources[tabName] || [];
        });

        const knowledgeGraph = ref({});
        const masteryData = ref({});
        const knowledgePointList = ref([]);
        const learningPaths = ref([]);
        const visNetworkContainer = ref(null);
        let networkInstance = null;
        const selectedNodeInfo = ref(null);

        const hasGraphData = computed(() => Object.keys(knowledgeGraph.value).length > 0);

        const selectedStudent = computed(() => students.value.find(s => s.id === selectedStudentId.value));
        const selectedCourseObj = computed(() => courses.value.find(c => c.name === selectedCourse.value));

        const masteredCount = computed(() => knowledgePointList.value.filter(kp => getMasteryLevel(kp).level === 'learned').length);
        const learningCount = computed(() => knowledgePointList.value.filter(kp => getMasteryLevel(kp).level === 'learning').length);
        const unlearnedCount = computed(() => knowledgePointList.value.filter(kp => getMasteryLevel(kp).level === 'unlearned').length);

        onMounted(() => {
            loadLearningPaths();
        });

        onUnmounted(() => {
            if (networkInstance) networkInstance.destroy();
        });

        function getMasteryLevel(kpName) {
            const data = masteryData.value[kpName];
            if (!data) return { level: 'unlearned', color: '#9ca3af', label: '未学习', score: 0 };
            const score = data.mastery_score || 0;
            if (score >= 70) return { level: 'learned', color: '#16a34a', label: '已掌握', score: Math.round(score) };
            if (score >= 30) return { level: 'learning', color: '#2563eb', label: '学习中', score: Math.round(score) };
            return { level: 'unlearned', color: '#9ca3af', label: '未学习', score: Math.round(score) };
        }

        async function fetchKnowledgeGraph(userId) {
            graphLoading.value = true;
            try {
                const [graphRes, masteryRes] = await Promise.all([
                    AIService.getKnowledgeGraph(userId),
                    AIService.getUserKnowledgeMastery(userId)
                ]);
                knowledgeGraph.value = graphRes.data.graph || {};
                masteryData.value = masteryRes.data.mastery || {};

                // 后端无数据时使用本地示例
                if (Object.keys(knowledgeGraph.value).length === 0 && sampleKnowledgeGraphs[userId]) {
                    knowledgeGraph.value = { ...sampleKnowledgeGraphs[userId].graph };
                    masteryData.value = { ...sampleKnowledgeGraphs[userId].mastery };
                }

                const kpSet = new Set();
                Object.entries(knowledgeGraph.value).forEach(([parent, children]) => {
                    kpSet.add(parent);
                    children.forEach(c => kpSet.add(c));
                });
                knowledgePointList.value = Array.from(kpSet);
            } catch (e) {
                console.error('获取知识图谱失败:', e);
                // 请求失败时也尝试使用本地示例
                if (sampleKnowledgeGraphs[userId]) {
                    knowledgeGraph.value = { ...sampleKnowledgeGraphs[userId].graph };
                    masteryData.value = { ...sampleKnowledgeGraphs[userId].mastery };
                    const kpSet = new Set();
                    Object.entries(knowledgeGraph.value).forEach(([parent, children]) => {
                        kpSet.add(parent);
                        children.forEach(c => kpSet.add(c));
                    });
                    knowledgePointList.value = Array.from(kpSet);
                    errorMsg.value = '';
                } else {
                    errorMsg.value = '获取知识图谱失败，请确认Python后端服务已启动（端口8000）';
                }
            } finally {
                graphLoading.value = false;
            }
        }

        async function generateLearningPath() {
            errorMsg.value = '';
            if (!selectedStudentId.value) {
                errorMsg.value = '请先选择学生';
                return;
            }
            if (!selectedCourse.value) {
                errorMsg.value = '请先选择目标课程';
                return;
            }
            loading.value = true;
            try {
                const courseObj = courses.value.find(c => c.name === selectedCourse.value);
                const graphUserId = courseObj ? courseObj.userId : selectedStudentId.value;
                await fetchKnowledgeGraph(graphUserId);
                if (!hasGraphData.value) {
                    errorMsg.value = '该课程暂无知识图谱数据';
                    loading.value = false;
                    return;
                }

                const path = {
                    date: new Date().toLocaleDateString('zh-CN'),
                    course: selectedCourse.value,
                    difficulty: selectedDifficulty.value,
                    difficultyLabel: { short: '短期夯实基础', standard: '标准均衡规划', long: '长期拔高进阶' }[selectedDifficulty.value],
                    difficultyClass: { short: 'tag-short', standard: 'tag-standard', long: 'tag-long' }[selectedDifficulty.value],
                    studentId: selectedStudentId.value,
                    knowledgePoints: [...knowledgePointList.value],
                    graph: { ...knowledgeGraph.value },
                    mastery: { ...masteryData.value }
                };
                learningPaths.value.unshift(path);
                saveLearningPaths();
                activeTab.value = 1;
                await nextTick();
                renderKnowledgeGraph();
            } catch (e) {
                console.error(e);
                errorMsg.value = '生成失败：' + e.message;
            } finally {
                loading.value = false;
            }
        }

        function renderKnowledgeGraph() {
            if (!visNetworkContainer.value || !hasGraphData.value) return;
            if (networkInstance) { networkInstance.destroy(); networkInstance = null; }

            const nodes = [];
            const edges = [];
            const nodeIds = new Set();

            Object.entries(knowledgeGraph.value).forEach(([parent, children]) => {
                if (!nodeIds.has(parent)) {
                    const m = getMasteryLevel(parent);
                    nodes.push({
                        id: parent, label: parent,
                        color: { background: m.color, border: m.color, highlight: { background: m.color, border: '#165DFF' } },
                        font: { color: '#fff', size: 13, bold: true },
                        shape: 'box', margin: 10, borderWidth: 2
                    });
                    nodeIds.add(parent);
                }
                children.forEach(child => {
                    if (!nodeIds.has(child)) {
                        const m = getMasteryLevel(child);
                        nodes.push({
                            id: child, label: child,
                            color: { background: m.color, border: m.color, highlight: { background: m.color, border: '#165DFF' } },
                            font: { color: '#fff', size: 13, bold: true },
                            shape: 'box', margin: 10, borderWidth: 2
                        });
                        nodeIds.add(child);
                    }
                    edges.push({ from: parent, to: child, arrows: 'to', color: { color: '#94a3b8', highlight: '#165DFF' } });
                });
            });

            const data = { nodes, edges };
            const options = {
                layout: { hierarchical: { enabled: true, direction: 'UD', sortMethod: 'directed', nodeSpacing: 160, levelSeparation: 100 } },
                physics: { enabled: false },
                interaction: { hover: true, tooltipDelay: 200 },
                edges: { smooth: { type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.4 } }
            };

            networkInstance = new Network(visNetworkContainer.value, data, options);
            networkInstance.on('click', (params) => {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    const m = getMasteryLevel(nodeId);
                    const md = masteryData.value[nodeId];
                    selectedNodeInfo.value = {
                        name: nodeId, score: m.score, color: m.color, label: m.label,
                        total: md?.total_questions || 0,
                        correct: md?.correct_count || 0
                    };
                } else {
                    selectedNodeInfo.value = null;
                }
            });
        }

        function refreshGraph() {
            if (selectedStudentId.value) fetchKnowledgeGraph(selectedStudentId.value).then(() => renderKnowledgeGraph());
        }

        async function replanLearningPath() {
            errorMsg.value = '';
            if (!selectedStudentId.value || !selectedCourse.value) {
                errorMsg.value = '请先选择学生和课程';
                return;
            }
            loading.value = true;
            try {
                const courseObj = courses.value.find(c => c.name === selectedCourse.value);
                const graphUserId = courseObj ? courseObj.userId : selectedStudentId.value;
                await fetchKnowledgeGraph(graphUserId);
                if (!hasGraphData.value) {
                    errorMsg.value = '该课程暂无知识图谱数据';
                    loading.value = false;
                    return;
                }
                const path = {
                    date: new Date().toLocaleDateString('zh-CN'),
                    course: selectedCourse.value,
                    difficulty: selectedDifficulty.value,
                    difficultyLabel: { short: '短期夯实基础', standard: '标准均衡规划', long: '长期拔高进阶' }[selectedDifficulty.value],
                    difficultyClass: { short: 'tag-short', standard: 'tag-standard', long: 'tag-long' }[selectedDifficulty.value],
                    studentId: selectedStudentId.value,
                    knowledgePoints: [...knowledgePointList.value],
                    graph: { ...knowledgeGraph.value },
                    mastery: { ...masteryData.value }
                };
                learningPaths.value.unshift(path);
                saveLearningPaths();
                activeTab.value = 1;
                await nextTick();
                renderKnowledgeGraph();
            } catch (e) {
                console.error(e);
                errorMsg.value = '重新规划失败：' + e.message;
            } finally {
                loading.value = false;
            }
        }

        function resetConfig() {
            selectedStudentId.value = '';
            selectedCourse.value = '';
            selectedDifficulty.value = 'standard';
            selectedFilter.value = 'all';
            selectedCycle.value = 'general';
            errorMsg.value = '';
        }

        function loadLearningPaths() {
            try {
                const saved = localStorage.getItem('learning_paths');
                if (saved) learningPaths.value = JSON.parse(saved);
            } catch (e) { console.error(e); }
        }

        function saveLearningPaths() {
            localStorage.setItem('learning_paths', JSON.stringify(learningPaths.value));
        }

        function viewPath(index) {
            const path = learningPaths.value[index];
            if (path) {
                selectedStudentId.value = path.studentId || '';
                selectedCourse.value = path.course || '';
                selectedDifficulty.value = path.difficulty || 'standard';
                if (path.graph) knowledgeGraph.value = path.graph;
                if (path.mastery) masteryData.value = path.mastery;
                if (path.knowledgePoints) knowledgePointList.value = path.knowledgePoints;
                activeTab.value = 1;
                nextTick(() => renderKnowledgeGraph());
            }
        }

        function deletePath(index) {
            learningPaths.value.splice(index, 1);
            saveLearningPaths();
        }

        function exportAllPaths() {
            const data = JSON.stringify(learningPaths.value, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'learning_paths.json'; a.click();
            URL.revokeObjectURL(url);
        }

        function exportPath() {
            const data = { graph: knowledgeGraph.value, mastery: masteryData.value, points: knowledgePointList.value };
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'learning_path.json'; a.click();
            URL.revokeObjectURL(url);
        }

        function goToResourceCenter() {
            router.push('/TeacherCenter');
        }

        return {
            activeTab, selectedDifficulty, activeResourceTab, tabs, resourceTabs,
            selectedStudentId, selectedCourse, selectedFilter, selectedCycle,
            students, courses, knowledgePointList, learningPaths, currentResources,
            loading, graphLoading, errorMsg,
            visNetworkContainer, selectedNodeInfo,
            hasGraphData, masteredCount, learningCount, unlearnedCount,
            generateLearningPath, replanLearningPath, renderKnowledgeGraph, refreshGraph, resetConfig,
            viewPath, deletePath, exportAllPaths, exportPath, goToResourceCenter
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

.adaptive-learning-path {
    padding: 24px;
    background-color: transparent;
    min-height: 100vh;
}

/* ===== 顶部深青蓝渐变标题块 ===== */
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

/* ===== Tab 标签栏 ===== */
.tab-bar {
    display: flex;
    gap: 0;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #e5e7eb;
}

.tab-item {
    padding: 0.75rem 1.5rem;
    font-size: 0.9375rem;
    font-weight: 500;
    color: #64748b;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s ease;
    user-select: none;
}

.tab-item:hover {
    color: #165DFF;
}

.tab-item.active {
    color: #165DFF;
    border-bottom-color: #165DFF;
    font-weight: 600;
}

/* ===== 主体左右双栏 ===== */
.main-layout {
    display: flex;
    gap: 1.5rem;
}

.left-panel {
    flex: 0 0 75%;
}

.right-panel {
    flex: 0 0 23%;
}

/* ===== 白色圆角卡片 ===== */
.content-card {
    background: #fff;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    padding: 1.5rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.card-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 1.25rem;
}

.card-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.25rem;
}

/* ===== 表单控件 ===== */
.form-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.form-row.two-col {
    .form-group {
        flex: 1;
    }
}

.form-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
}

.form-label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: #475569;
}

.form-select {
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 0.875rem;
    color: #374151;
    background: #fff;
    outline: none;
    transition: border-color 0.2s;
    appearance: auto;
}

.form-select:focus {
    border-color: #165DFF;
    box-shadow: 0 0 0 2px rgba(22, 93, 255, 0.1);
}

.student-profile-card {
    margin-top: 0.5rem;
    padding: 0.75rem;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 1px solid #bae6fd;
    border-radius: 8px;
}

.profile-header {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    margin-bottom: 0.5rem;
}

.profile-avatar {
    font-size: 1.75rem;
}

.profile-info {
    display: flex;
    flex-direction: column;
}

.profile-name {
    font-size: 0.9375rem;
    font-weight: 700;
    color: #0c4a6e;
}

.profile-meta {
    font-size: 0.75rem;
    color: #0369a1;
}

.profile-summary {
    font-size: 0.8125rem;
    color: #475569;
    line-height: 1.5;
    margin: 0;
}

.course-desc-card {
    margin-top: 0.5rem;
    padding: 0.625rem 0.75rem;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
}

.course-desc-text {
    font-size: 0.8125rem;
    color: #166534;
    line-height: 1.4;
}

/* 单选难度标签 */
.radio-group {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.radio-label {
    display: inline-flex;
    align-items: center;
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.8125rem;
    color: #475569;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
}

.radio-label:hover {
    border-color: #165DFF;
    color: #165DFF;
}

.radio-label.active {
    background: #165DFF;
    color: #fff;
    border-color: #165DFF;
}

.hidden-radio {
    display: none;
}

/* ===== 按钮组 ===== */
.action-buttons {
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
    margin-top: 1.25rem;
    padding-top: 1rem;
    border-top: 1px solid #f1f5f9;
    flex-wrap: wrap;
}

.action-item {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.btn {
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    white-space: nowrap;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: #165DFF;
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
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

.btn-danger {
    background: #fff;
    color: #ef4444;
    border: 1.5px solid #ef4444;
}

.btn-danger:hover {
    background: rgba(239, 68, 68, 0.05);
}

.btn-sm {
    padding: 0.375rem 0.875rem;
    font-size: 0.8125rem;
}

.btn-full {
    width: 100%;
}

/* ===== 错误提示 ===== */
.error-msg {
    margin-top: 1rem;
    padding: 0.625rem 1rem;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 6px;
    color: #ef4444;
    font-size: 0.8125rem;
}

/* ===== 加载/空状态占位 ===== */
.loading-placeholder,
.empty-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 160px;
    background: #f8fafc;
    border-radius: 8px;
    border: 1px dashed #e2e8f0;
    color: #94a3b8;
    font-size: 0.875rem;
}

/* ===== Tab2：vis-network 知识图谱容器 ===== */
.vis-network-container {
    width: 100%;
    height: 400px;
    background: #f8fafc;
    border-radius: 8px;
    border: 1px solid #f1f5f9;
}

.route-flow-container {
    margin-bottom: 1.5rem;
}

.section-subtitle {
    font-size: 1rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0 0 1rem;
}

.flow-legend {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    font-size: 0.75rem;
    color: #64748b;
}

.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.learned-dot { background: #16a34a; }
.learning-dot { background: #2563eb; }
.unlearned-dot { background: #9ca3af; }

/* ===== 节点详情卡片 ===== */
.node-detail-card {
    margin-top: 1rem;
    padding: 1rem;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
}

.node-detail-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 0.5rem;
}

.node-detail-stats {
    display: flex;
    gap: 1.5rem;
    font-size: 0.8125rem;
    color: #475569;
}

/* ===== Tab2：资源Tab组 ===== */
.resource-tabs-section {
    margin-top: 1.5rem;
}

.resource-tabs {
    display: flex;
    gap: 0;
    border-bottom: 2px solid #e5e7eb;
    margin-bottom: 1rem;
    overflow-x: auto;
}

.resource-tab {
    padding: 0.5rem 1rem;
    font-size: 0.8125rem;
    color: #64748b;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
    white-space: nowrap;
    user-select: none;
}

.resource-tab:hover {
    color: #165DFF;
}

.resource-tab.active {
    color: #165DFF;
    border-bottom-color: #165DFF;
    font-weight: 600;
}

.resource-cards-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
}

.resource-card {
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.resource-card-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: #1e293b;
}

.resource-card-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.25rem;
}

.card-bottom-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.25rem;
    padding-top: 1rem;
    border-top: 1px solid #f1f5f9;
}

/* ===== Tab3：历史路径 ===== */
.history-scroll {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.history-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    border-radius: 8px;
    transition: transform 0.2s;
}

.history-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.history-card-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.history-date {
    font-size: 0.8125rem;
    color: #64748b;
}

.history-course {
    font-size: 0.875rem;
    font-weight: 600;
    color: #1e293b;
}

.history-difficulty {
    font-size: 0.75rem;
    padding: 0.25rem 0.625rem;
    border-radius: 4px;
}

.history-kp-count {
    font-size: 0.75rem;
    color: #94a3b8;
}

.tag-short {
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
}

.tag-standard {
    color: #165DFF;
    background: rgba(22, 93, 255, 0.1);
}

.tag-long {
    color: #8b5cf6;
    background: rgba(139, 92, 246, 0.1);
}

.history-card-actions {
    display: flex;
    gap: 0.5rem;
}

/* ===== 右侧边栏卡片 ===== */
.sidebar-card {
    background: #fff;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    padding: 1.25rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    position: sticky;
    top: 24px;
}

.sidebar-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 0.75rem;
}

.sidebar-stats {
    margin-top: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.sidebar-stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f1f5f9;
}

.stat-label {
    font-size: 0.8125rem;
    color: #64748b;
}

.stat-value {
    font-size: 1.125rem;
    font-weight: 700;
    color: #1e293b;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
    .adaptive-learning-path {
        padding: 1rem;
    }

    .main-layout {
        flex-direction: column;
    }

    .left-panel,
    .right-panel {
        flex: 1 1 100%;
    }

    .form-row {
        flex-direction: column;
    }

    .resource-cards-grid {
        grid-template-columns: 1fr;
    }

    .banner-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
}
</style>
