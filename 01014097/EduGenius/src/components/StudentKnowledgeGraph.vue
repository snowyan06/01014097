<template>
    <div class="knowledge-graph-container">
        <Card>
            <template #header>
                <div class="header-container">
                    <h2 class="title">
                        知识图谱分析
                    </h2>
                    <div class="header-actions">
                        <!-- 搜索框 -->
                        <span class="p-input-icon-left">
                            <i class="pi pi-search move-left-right" />
                            <InputText
                                v-model="searchQuery"
                                placeholder="搜索知识点..."
                                @input="handleSearch"
                                class="search-input"
                                :class="{'tree-search': viewMode === 'tree'}"
                            />
                        </span>

                        <!-- 视图切换 -->
                        <SelectButton
                            v-model="viewMode"
                            :options="viewOptions"
                            optionLabel="label"
                            optionValue="value"
                            @change="switchView"
                            class="view-selector"
                        />

                        <!-- 操作按钮 -->
                        <Button
                            icon="pi pi-refresh"
                            label="刷新"
                            @click="fetchKnowledgeGraph"
                            :loading="loading"
                            severity="secondary"
                            size="small"
                            :class="{'tree-button': viewMode === 'tree'}"
                        />
                        <Button
                            icon="pi pi-download"
                            label="导出"
                            @click="exportGraph"
                            severity="info"
                            size="small"
                            :class="{'tree-button': viewMode === 'tree'}"
                        />
                    </div>
                </div>
            </template>

            <template #content>
                <!-- 加载状态 -->
                <div v-if="loading" class="loading-container" :class="{'tree-loading-bg': viewMode === 'tree'}">
                    <ProgressSpinner />
                    <p class="loading-text">正在分析知识结构...</p>
                </div>

                <!-- 错误状态 -->
                <div v-else-if="error" class="error-container" :class="{'tree-error-bg': viewMode === 'tree'}">
                    <InlineMessage severity="error">
                        {{ error }}
                    </InlineMessage>
                    <Button
                        label="重试"
                        icon="pi pi-replay"
                        @click="fetchKnowledgeGraph"
                        class="mt-3"
                        :class="{'tree-button': viewMode === 'tree'}"
                    />
                </div>

                <!-- 主内容 -->
                <div v-else class="main-content">
                    <!-- 统计信息 - 树形视图时显示在图表上方 -->
                    <div class="stats-container" :class="{'tree-mode': viewMode === 'tree'}">
                        <div class="stat-card">
                            <i class="pi pi-book stat-icon"></i>
                            <div class="stat-content">
                                <span class="stat-value">{{ nodeCount }}</span>
                                <span class="stat-label">知识点</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <i class="pi pi-link stat-icon"></i>
                            <div class="stat-content">
                                <span class="stat-value">{{ edgeCount }}</span>
                                <span class="stat-label">依赖关系</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <i class="pi pi-chart-line stat-icon"></i>
                            <div class="stat-content">
                                <span class="stat-value">{{ masteryRate }}%</span>
                                <span class="stat-label">掌握程度</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <i class="pi pi-exclamation-triangle stat-icon warning"></i>
                            <div class="stat-content">
                                <span class="stat-value">{{ weakPoints }}</span>
                                <span class="stat-label">薄弱环节</span>
                            </div>
                        </div>
                    </div>

                    <!-- 图表容器 - 添加树形视图特殊类 -->
                    <div class="chart-wrapper">
                        <div ref="chartContainer" class="chart-container" :class="{'tree-view': viewMode === 'tree'}"></div>

                        <!-- 控制面板 - 树形视图时样式不同 -->
                        <div class="control-panel" :class="{'tree-mode': viewMode === 'tree'}">
                            <h4>图形控制</h4>
                            <div class="control-item">
                                <label>节点间距</label>
                                <Slider v-model="edgeLength" :min="50" :max="300" @change="updateLayout" />
                            </div>
                            <div class="control-item">
                                <label>排斥力</label>
                                <Slider v-model="repulsion" :min="100" :max="1000" @change="updateLayout" />
                            </div>
                            <div class="control-item">
                                <label>显示标签</label>
                                <InputSwitch v-model="showLabels" @change="toggleLabels" />
                            </div>

                            <!-- 树形视图特有控制项 -->
                        </div>
                    </div>



                    <!-- 图例和说明 -->
                    <div v-if="viewMode" class="info-section">
                        <div class="legend">
                            <h4>节点说明</h4>
                            <div class="legend-items">
                                <div class="legend-item">
                                    <div class="node-icon core"></div>
                                    <div class="legend-text">
                                        <strong>核心知识点</strong>
                                        <span>基础概念，多个知识点的前置条件</span>
                                    </div>
                                </div>
                                <div class="legend-item">
                                    <div class="node-icon branch"></div>
                                    <div class="legend-text">
                                        <strong>分支知识点</strong>
                                        <span>承上启下，连接多个知识体系</span>
                                    </div>
                                </div>
                                <div class="legend-item">
                                    <div class="node-icon leaf"></div>
                                    <div class="legend-text">
                                        <strong>应用知识点</strong>
                                        <span>具体应用，需要前置知识支撑</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 学习建议 -->
                        <div class="suggestions">
                            <h4>学习建议</h4>
                            <div class="suggestion-list">
                                <div v-for="(suggestion, index) in learningSuggestions"
                                     :key="index"
                                     class="suggestion-item">
                                    <i class="pi pi-lightbulb"></i>
                                    {{ suggestion }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 树形视图的缩放控制按钮 -->
                    <div v-if="viewMode === 'tree'" class="tree-zoom-controls">
                        <div class="tree-zoom-btn" @click="zoomIn">
                            <i class="pi pi-plus"></i>
                        </div>
                        <div class="tree-zoom-btn" @click="zoomOut">
                            <i class="pi pi-minus"></i>
                        </div>
                        <div class="tree-zoom-btn" @click="zoomReset">
                            <i class="pi pi-search"></i>
                        </div>
                    </div>
                </div>
            </template>
        </Card>

        <!-- 节点详情对话框 - 树形视图时样式不同 -->
        <Dialog
            v-model:visible="showNodeDialog"
            :header="selectedNode?.name"
            :style="{width: '550px'}"
            modal
            :class="{'tree-dialog': viewMode === 'tree'}"
        >
            <div v-if="selectedNode" class="node-detail" :class="{'tree-mode': viewMode === 'tree'}">
                <!-- 基本信息 -->
                <div class="detail-section">
                    <h5><i class="pi pi-info-circle"></i> 基本信息</h5>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>知识点名称</label>
                            <span>{{ selectedNode.name }}</span>
                        </div>
                        <div class="info-item">
                            <label>节点类型</label>
                            <Tag :severity="getNodeSeverity(selectedNode.category)">
                                {{ selectedNode.category }}
                            </Tag>
                        </div>
                        <div class="info-item">
                            <label>掌握程度</label>
                            <ProgressBar
                                :value="selectedNode.mastery || 0"
                                :showValue="true"
                                :class="getMasteryClass(selectedNode.mastery)"
                            />
                        </div>
                        <div class="info-item">
                            <label>重要程度</label>
                            <Rating v-model="selectedNode.importance" :readonly="true" :stars="5" />
                        </div>
                        <!-- 树形视图特有信息 -->
                        <div v-if="viewMode === 'tree'" class="info-item">
                            <label>层级深度</label>
                            <span>第 {{ selectedNode.level + 1 }} 层</span>
                        </div>
                    </div>

                    <!-- 层级深度指示器 -->
                    <div v-if="viewMode === 'tree'" class="tree-depth-gradient"></div>
                </div>

                <Divider />

                <!-- 依赖关系 -->
                <div class="detail-section">
                    <h5><i class="pi pi-sitemap"></i> 知识点关系</h5>

                    <div v-if="nodeRelations.parents.length > 0" class="relation-group">
                        <h6>前置知识点 ({{ nodeRelations.parents.length }})</h6>
                        <div class="relation-list">
                            <div v-for="parent in nodeRelations.parents"
                                 :key="parent.name"
                                 class="relation-item"
                                 @click="navigateToNode(parent.name)">
                                <i class="pi pi-arrow-up"></i>
                                <span>{{ parent.name }}</span>
                                <Tag severity="info" class="ml-auto">
                                    {{ parent.mastery }}% 掌握
                                </Tag>
                            </div>
                        </div>
                    </div>

                    <div v-if="nodeRelations.children.length > 0" class="relation-group mt-3">
                        <h6>后续知识点 ({{ nodeRelations.children.length }})</h6>
                        <div class="relation-list">
                            <div v-for="child in nodeRelations.children"
                                 :key="child.name"
                                 class="relation-item"
                                 @click="navigateToNode(child.name)">
                                <i class="pi pi-arrow-down"></i>
                                <span>{{ child.name }}</span>
                                <Tag severity="secondary" class="ml-auto">
                                    {{ child.mastery }}% 掌握
                                </Tag>
                            </div>
                        </div>
                    </div>
                </div>

                <Divider />

                <!-- 学习路径 -->
                <div class="detail-section">
                    <h5><i class="pi pi-directions"></i> 推荐学习路径</h5>
                    <Timeline :value="learningPath" class="learning-timeline">
                        <template #content="slotProps">
                            <div class="timeline-content">
                                <strong>{{ slotProps.item.name }}</strong>
                                <p>{{ slotProps.item.description }}</p>
                            </div>
                        </template>
                    </Timeline>
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import SelectButton from 'primevue/selectbutton'
import ProgressSpinner from 'primevue/progressspinner'
import InlineMessage from 'primevue/inlinemessage'
import Dialog from 'primevue/dialog'
import Divider from 'primevue/divider'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'
import Rating from 'primevue/rating'
import Timeline from 'primevue/timeline'
import Slider from 'primevue/slider'
import InputSwitch from 'primevue/inputswitch'
import axios from 'axios'

// 响应式数据
const loading = ref(false)
const error = ref(null)
const graphData = ref({})
const chartContainer = ref(null)
const chartInstance = ref(null)
const showNodeDialog = ref(false)
const selectedNode = ref(null)
const searchQuery = ref('')
const viewMode = ref('force')
const edgeLength = ref(150)
const repulsion = ref(500)
const showLabels = ref(true)

// 视图选项
const viewOptions = ref([
    { label: '默认', value: 'force', icon: 'pi pi-share-alt' },
    { label: '层级', value: 'tree', icon: 'pi pi-sitemap' },
    { label: '圆形', value: 'circular', icon: 'pi pi-circle' }
])

// 模拟的知识点详细数据
const knowledgeDetails = ref({
    // 这里应该从后端获取，现在用模拟数据
})

// 计算属性
const nodeCount = computed(() => {
    const nodes = new Set()
    Object.keys(graphData.value).forEach(parent => {
        nodes.add(parent)
        graphData.value[parent]?.forEach(child => nodes.add(child))
    })
    return nodes.size
})

const edgeCount = computed(() => {
    return Object.values(graphData.value).reduce((sum, children) => sum + (children?.length || 0), 0)
})

const masteryRate = computed(() => {
    // 计算整体掌握率
    return 75 // 模拟数据
})

const weakPoints = computed(() => {
    // 计算薄弱知识点数量
    return 3 // 模拟数据
})

const nodeRelations = computed(() => {
    if (!selectedNode.value) return { parents: [], children: [] }

    const nodeName = selectedNode.value.name
    const parents = []
    const children = []

    // 查找父节点
    Object.entries(graphData.value).forEach(([parent, childList]) => {
        if (childList?.includes(nodeName)) {
            parents.push({
                name: parent,
                mastery: Math.floor(Math.random() * 100) // 模拟掌握度
            })
        }
    })

    // 查找子节点
    if (graphData.value[nodeName]) {
        graphData.value[nodeName].forEach(child => {
            children.push({
                name: child,
                mastery: Math.floor(Math.random() * 100) // 模拟掌握度
            })
        })
    }

    return { parents, children }
})

const learningPath = computed(() => {
    // 生成学习路径建议
    if (!selectedNode.value) return []

    return [
        { name: '复习前置知识', description: '确保掌握所有前置知识点' },
        { name: '学习当前知识点', description: '通过练习和实践加深理解' },
        { name: '拓展应用', description: '尝试更复杂的应用场景' }
    ]
})

const learningSuggestions = computed(() => {
    return [
        '建议先巩固"基础概念"相关知识点',
        '重点关注标记为红色的薄弱环节',
        '可以通过知识图谱查看学习路径'
    ]
})
const forceRefresh = () => {
    if (chartInstance.value) {
        chartInstance.value.resize()
        // 或者重新渲染
        const option = chartInstance.value.getOption()
        chartInstance.value.clear()
        chartInstance.value.setOption(option)
    }
}
// 硬编码的计算机/AI专业知识图谱数据
const hardcodedGraphData = {
    '计算机科学基础': ['数据结构', '算法设计', '计算机组成原理'],
    '数据结构': ['线性表', '树与二叉树', '图结构', '哈希表'],
    '算法设计': ['排序算法', '搜索算法', '动态规划', '贪心算法'],
    '计算机组成原理': ['CPU架构', '存储系统', '指令系统'],
    '人工智能基础': ['机器学习', '深度学习', '自然语言处理'],
    '机器学习': ['监督学习', '无监督学习', '强化学习', '特征工程'],
    '深度学习': ['神经网络基础', '卷积神经网络CNN', '循环神经网络RNN', 'Transformer'],
    '自然语言处理': ['词嵌入技术', '文本分类', '机器翻译', '大语言模型'],
    '监督学习': ['线性回归', '逻辑回归', '支持向量机SVM', '决策树'],
    '无监督学习': ['K-means聚类', '主成分分析PCA', 'DBSCAN'],
    '强化学习': ['Q-Learning', '策略梯度', 'Actor-Critic'],
    '神经网络基础': ['激活函数', '反向传播', '损失函数', '优化算法'],
    '卷积神经网络CNN': ['卷积层', '池化层', '经典CNN模型'],
    '循环神经网络RNN': ['LSTM', 'GRU', '序列建模'],
    'Transformer': ['Self-Attention', '多头注意力', 'BERT', 'GPT系列'],
    '大语言模型': ['预训练与微调', 'Prompt工程', 'Few-shot学习', 'RAG检索增强'],
    '操作系统': ['进程管理', '内存管理', '文件系统'],
    '计算机网络': ['TCP/IP协议', 'HTTP协议', '网络安全'],
    '数据库系统': ['关系型数据库', 'SQL语言', '数据库设计', 'NoSQL数据库'],
    '软件工程': ['设计模式', '敏捷开发', '版本控制Git']
};

// 硬编码的知识点掌握度数据
const hardcodedMasteryData = {
    '计算机科学基础': { mastery_score: 85, total_questions: 12, correct_count: 10 },
    '数据结构': { mastery_score: 78, total_questions: 15, correct_count: 12 },
    '算法设计': { mastery_score: 72, total_questions: 10, correct_count: 7 },
    '计算机组成原理': { mastery_score: 65, total_questions: 8, correct_count: 5 },
    '人工智能基础': { mastery_score: 80, total_questions: 10, correct_count: 8 },
    '机器学习': { mastery_score: 75, total_questions: 14, correct_count: 11 },
    '深度学习': { mastery_score: 68, total_questions: 12, correct_count: 8 },
    '自然语言处理': { mastery_score: 60, total_questions: 8, correct_count: 5 },
    '监督学习': { mastery_score: 82, total_questions: 10, correct_count: 8 },
    '无监督学习': { mastery_score: 55, total_questions: 6, correct_count: 3 },
    '强化学习': { mastery_score: 45, total_questions: 5, correct_count: 2 },
    '神经网络基础': { mastery_score: 70, total_questions: 10, correct_count: 7 },
    '卷积神经网络CNN': { mastery_score: 62, total_questions: 8, correct_count: 5 },
    '循环神经网络RNN': { mastery_score: 50, total_questions: 6, correct_count: 3 },
    'Transformer': { mastery_score: 58, total_questions: 7, correct_count: 4 },
    '大语言模型': { mastery_score: 52, total_questions: 6, correct_count: 3 },
    '操作系统': { mastery_score: 60, total_questions: 8, correct_count: 5 },
    '计算机网络': { mastery_score: 72, total_questions: 10, correct_count: 7 },
    '数据库系统': { mastery_score: 78, total_questions: 12, correct_count: 9 },
    '软件工程': { mastery_score: 85, total_questions: 8, correct_count: 7 },
    '线性表': { mastery_score: 88, total_questions: 6, correct_count: 5 },
    '树与二叉树': { mastery_score: 75, total_questions: 8, correct_count: 6 },
    '图结构': { mastery_score: 65, total_questions: 6, correct_count: 4 },
    '哈希表': { mastery_score: 80, total_questions: 5, correct_count: 4 },
    '排序算法': { mastery_score: 85, total_questions: 8, correct_count: 7 },
    '搜索算法': { mastery_score: 70, total_questions: 6, correct_count: 4 },
    '动态规划': { mastery_score: 55, total_questions: 8, correct_count: 4 },
    '贪心算法': { mastery_score: 68, total_questions: 5, correct_count: 3 },
    'CPU架构': { mastery_score: 60, total_questions: 6, correct_count: 4 },
    '存储系统': { mastery_score: 72, total_questions: 5, correct_count: 4 },
    '指令系统': { mastery_score: 58, total_questions: 4, correct_count: 2 },
    '特征工程': { mastery_score: 70, total_questions: 6, correct_count: 4 },
    '线性回归': { mastery_score: 85, total_questions: 5, correct_count: 4 },
    '逻辑回归': { mastery_score: 78, total_questions: 5, correct_count: 4 },
    '支持向量机SVM': { mastery_score: 65, total_questions: 6, correct_count: 4 },
    '决策树': { mastery_score: 80, total_questions: 5, correct_count: 4 },
    'K-means聚类': { mastery_score: 58, total_questions: 4, correct_count: 2 },
    '主成分分析PCA': { mastery_score: 50, total_questions: 4, correct_count: 2 },
    'DBSCAN': { mastery_score: 42, total_questions: 3, correct_count: 1 },
    'Q-Learning': { mastery_score: 48, total_questions: 4, correct_count: 2 },
    '策略梯度': { mastery_score: 40, total_questions: 3, correct_count: 1 },
    'Actor-Critic': { mastery_score: 35, total_questions: 3, correct_count: 1 },
    '激活函数': { mastery_score: 82, total_questions: 5, correct_count: 4 },
    '反向传播': { mastery_score: 70, total_questions: 6, correct_count: 4 },
    '损失函数': { mastery_score: 75, total_questions: 5, correct_count: 4 },
    '优化算法': { mastery_score: 65, total_questions: 6, correct_count: 4 },
    '卷积层': { mastery_score: 68, total_questions: 5, correct_count: 3 },
    '池化层': { mastery_score: 72, total_questions: 4, correct_count: 3 },
    '经典CNN模型': { mastery_score: 55, total_questions: 5, correct_count: 3 },
    'LSTM': { mastery_score: 52, total_questions: 5, correct_count: 3 },
    'GRU': { mastery_score: 48, total_questions: 4, correct_count: 2 },
    '序列建模': { mastery_score: 45, total_questions: 4, correct_count: 2 },
    'Self-Attention': { mastery_score: 62, total_questions: 5, correct_count: 3 },
    '多头注意力': { mastery_score: 55, total_questions: 4, correct_count: 2 },
    'BERT': { mastery_score: 50, total_questions: 5, correct_count: 3 },
    'GPT系列': { mastery_score: 58, total_questions: 4, correct_count: 2 },
    '预训练与微调': { mastery_score: 55, total_questions: 4, correct_count: 2 },
    'Prompt工程': { mastery_score: 60, total_questions: 3, correct_count: 2 },
    'Few-shot学习': { mastery_score: 45, total_questions: 3, correct_count: 1 },
    'RAG检索增强': { mastery_score: 40, total_questions: 3, correct_count: 1 },
    '进程管理': { mastery_score: 65, total_questions: 5, correct_count: 3 },
    '内存管理': { mastery_score: 58, total_questions: 5, correct_count: 3 },
    '文件系统': { mastery_score: 55, total_questions: 4, correct_count: 2 },
    'TCP/IP协议': { mastery_score: 75, total_questions: 6, correct_count: 5 },
    'HTTP协议': { mastery_score: 80, total_questions: 5, correct_count: 4 },
    '网络安全': { mastery_score: 62, total_questions: 5, correct_count: 3 },
    '关系型数据库': { mastery_score: 82, total_questions: 6, correct_count: 5 },
    'SQL语言': { mastery_score: 85, total_questions: 8, correct_count: 7 },
    '数据库设计': { mastery_score: 70, total_questions: 5, correct_count: 4 },
    'NoSQL数据库': { mastery_score: 55, total_questions: 4, correct_count: 2 },
    '设计模式': { mastery_score: 78, total_questions: 6, correct_count: 5 },
    '敏捷开发': { mastery_score: 82, total_questions: 4, correct_count: 3 },
    '版本控制Git': { mastery_score: 88, total_questions: 5, correct_count: 4 }
};

// 获取知识图谱数据（使用硬编码数据）
const fetchKnowledgeGraph = async () => {
    loading.value = true
    error.value = null

    try {
        // 直接使用硬编码的知识图谱数据
        graphData.value = hardcodedGraphData
        window.userMasteryData = hardcodedMasteryData

        await nextTick()
        setTimeout(() => {
            renderGraph()
        }, 100)
    } catch (err) {
        error.value = err.message || '加载知识图谱失败，请稍后重试'
        console.error('Error:', err)
    } finally {
        loading.value = false
    }
}

// 获取节点类型
const getNodeType = (nodeName) => {
    const hasParent = Object.values(graphData.value).some(children =>
        children?.includes(nodeName)
    )
    const hasChildren = graphData.value[nodeName]?.length > 0

    if (!hasParent && hasChildren) return 'core'
    if (hasParent && hasChildren) return 'branch'
    return 'leaf'
}

// 获取节点样式
const getNodeStyle = (type, nodeName, mastery = null) => {
    // 优先使用传入的掌握度，否则从全局数据获取
    const actualMastery = mastery !== null ? mastery :
        (window.userMasteryData?.[nodeName]?.mastery_score ?? 75)

    const baseColors = {
        core: '#8b5cf6',    // 紫色
        branch: '#3b82f6',  // 蓝色
        leaf: '#10b981'     // 绿色
    }

    // 根据掌握度调整颜色
    let color, borderColor
    if (actualMastery < 60) {
        color = '#ef4444'  // 红色 - 薄弱
        borderColor = '#dc2626'
    } else if (actualMastery < 80) {
        color = '#f59e0b'  // 黄色 - 一般
        borderColor = '#d97706'
    } else {
        color = baseColors[type]
        borderColor = baseColors[type]
    }

    return {
        color: color,
        opacity: actualMastery < 60 ? 0.7 : 1,
        borderColor: borderColor,
        borderWidth: actualMastery < 60 ? 3 : 1
    }
}


// 构建图表数据
const buildEChartsData = () => {
    const nodes = []
    const links = []
    const categories = [
        { name: '核心知识点', itemStyle: { color: '#8b5cf6' } },
        { name: '分支知识点', itemStyle: { color: '#3b82f6' } },
        { name: '应用知识点', itemStyle: { color: '#10b981' } }
    ]

    // 收集所有节点
    const nodeSet = new Set()
    Object.entries(graphData.value).forEach(([parent, children]) => {
        nodeSet.add(parent)
        children?.forEach(child => nodeSet.add(child))
    })

    // 创建节点
    nodeSet.forEach(nodeName => {
        const nodeType = getNodeType(nodeName)
        const categoryIndex = nodeType === 'core' ? 0 : nodeType === 'branch' ? 1 : 2

        // 获取真实掌握度
        const masteryData = window.userMasteryData?.[nodeName]
        const mastery = masteryData ? masteryData.mastery_score : Math.floor(Math.random() * 100)
        const importance = masteryData ? Math.ceil(masteryData.total_questions / 5) : Math.ceil(Math.random() * 5)

        const style = getNodeStyle(nodeType, nodeName, mastery)

        nodes.push({
            id: nodeName,
            name: nodeName,
            category: ['核心知识点', '分支知识点', '应用知识点'][categoryIndex],
            categoryIndex: categoryIndex,
            value: 30 + importance * 10,
            symbolSize: 30 + importance * 10,
            mastery: mastery,
            importance: importance,
            itemStyle: {
                color: style.color,
                opacity: style.opacity,
                borderColor: style.borderColor,
                borderWidth: style.borderWidth,
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.2)'
            },
            label: {
                show: showLabels.value,
                fontSize: 12,
                fontWeight: 'bold',
                color: '#1f2937'
            }
        })
    })

    // 创建连接
    Object.entries(graphData.value).forEach(([parent, children]) => {
        children?.forEach(child => {
            links.push({
                source: parent,
                target: child,
                lineStyle: {
                    width: 2,
                    curveness: 0.2,
                    color: '#94a3b8',
                    type: 'solid'
                },
                emphasis: {
                    lineStyle: {
                        width: 4,
                        color: '#3b82f6'
                    }
                }
            })
        })
    })

    return { nodes, links, categories }
}

// 渲染图形


// 构建树形数据
const buildTreeData = () => {
    // 找到根节点 - 没有被任何节点指向的节点
    const allNodes = new Set()
    const hasParentNodes = new Set()
    const nodeChildren = new Map() // 缓存子节点映射

    // 收集所有节点和有父节点的节点
    Object.entries(graphData.value).forEach(([parent, children]) => {
        allNodes.add(parent)
        nodeChildren.set(parent, children || [])
        children?.forEach(child => {
            allNodes.add(child)
            hasParentNodes.add(child)
        })
    })

    // 找出根节点
    const roots = Array.from(allNodes).filter(node => !hasParentNodes.has(node))

    // 全局visited集合，防止重复构建
    const globalVisited = new Set()

    // 递归构建树节点 - 修复版本
    const buildNode = (name, level = 0) => {
        // 防止循环依赖和重复构建
        if (globalVisited.has(name)) {
            return null
        }
        globalVisited.add(name)

        const nodeType = getNodeType(name)
        const mastery = Math.floor(Math.random() * 100)
        const importance = Math.ceil(Math.random() * 5)

        // 构建子节点
        const children = []
        const childNames = nodeChildren.get(name) || []

        childNames.forEach(childName => {
            if (!globalVisited.has(childName)) { // 只处理未访问的节点
                const childNode = buildNode(childName, level + 1)
                if (childNode) {
                    children.push(childNode)
                }
            }
        })

        const node = {
            name: name,
            value: importance,
            category: nodeType,
            mastery: mastery,
            importance: importance,
            level: level,
            // 确保所有层级都有合适的大小
            symbolSize: Math.max(15, 40 - level * 3),
            itemStyle: {
                color: nodeType === 'core' ? '#8b5cf6' : nodeType === 'branch' ? '#3b82f6' : '#10b981',
                borderColor: mastery < 60 ? '#ef4444' : '#ffffff',
                borderWidth: 2,
                shadowBlur: 6,
                shadowColor: 'rgba(0, 0, 0, 0.1)',
                opacity: mastery < 60 ? 0.7 : 1
            },
            label: {
                show: true,
                fontSize: Math.max(9, 14 - level * 0.8), // 渐进式字体大小
                fontWeight: level === 0 ? 'bold' : level === 1 ? '500' : 'normal',
                color: '#1f2937',
                // 添加背景以提高可读性
                backgroundColor: level > 2 ? 'rgba(255, 255, 255, 0.8)' : 'transparent',
                padding: level > 2 ? [2, 4] : [0, 0],
                borderRadius: 2
            }
        }

        // 只有在有子节点时才添加children属性
        if (children.length > 0) {
            node.children = children
        }

        return node
    }

    // 如果没有找到根节点，选择度数最高的节点作为根
    if (roots.length === 0 && allNodes.size > 0) {
        // 找到出度最大的节点作为根节点
        let maxDegreeNode = Array.from(allNodes)[0]
        let maxDegree = 0

        Array.from(allNodes).forEach(node => {
            const degree = (nodeChildren.get(node) || []).length
            if (degree > maxDegree) {
                maxDegree = degree
                maxDegreeNode = node
            }
        })

        return [buildNode(maxDegreeNode)].filter(node => node !== null)
    }

    return roots.map(root => buildNode(root)).filter(node => node !== null)
}

// 修复后的渲染树形视图函数
const renderTreeView = () => {
    const treeData = buildTreeData()
    console.log('Tree data structure:', JSON.stringify(treeData, null, 2)) // 调试用

    const option = {
        backgroundColor: '#ffffff',
        title: {
            text: '知识结构层次图',
            subtext: '从基础到应用的学习路径',
            left: 'center',
            top: 20,
            textStyle: {
                fontSize: 20,
                fontWeight: 'bold',
                color: '#1f2937'
            },
            subtextStyle: {
                fontSize: 14,
                color: '#6b7280'
            }
        },
        tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderColor: '#e5e7eb',
            borderWidth: 1,
            borderRadius: 8,
            textStyle: {
                color: '#1f2937'
            },
            formatter: (params) => {
                const data = params.data
                return `
                    <div style="padding: 12px; min-width: 200px;">
                        <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px;">
                            ${data.name}
                        </div>
                        <div style="border-bottom: 1px solid #e5e7eb; margin-bottom: 8px;"></div>
                        <div style="margin-bottom: 4px;">
                            <span style="color: #6b7280;">层级:</span>
                            <span style="color: #3b82f6; font-weight: bold;">第${data.level + 1}层</span>
                        </div>
                        <div style="margin-bottom: 4px;">
                            <span style="color: #6b7280;">类型:</span>
                            <span style="color: #10b981;">${data.category === 'core' ? '核心知识点' : data.category === 'branch' ? '分支知识点' : '应用知识点'}</span>
                        </div>
                        <div style="margin-bottom: 4px;">
                            <span style="color: #6b7280;">掌握度:</span>
                            <span style="color: ${data.mastery >= 80 ? '#10b981' : data.mastery >= 60 ? '#f59e0b' : '#ef4444'}; font-weight: bold;">
                                ${data.mastery}%
                            </span>
                        </div>
                        <div>
                            <span style="color: #6b7280;">重要度:</span>
                            <span style="color: #f59e0b;">${'★'.repeat(data.importance)}</span>
                        </div>
                    </div>
                `
            }
        },
        series: [{
            type: 'tree',
            data: treeData,
            left: '10%',
            right: '10%',
            top: '15%',
            bottom: '5%',
            layout: 'orthogonal',
            orient: 'LR', // 从左到右
            symbol: 'circle',
            symbolSize: (value, params) => params.data.symbolSize || 25,

            // 修复线条样式 - 确保所有层级都显示
            lineStyle: {
                color: '#94a3b8',
                width: 2,
                type: 'solid',
                shadowColor: 'rgba(0, 0, 0, 0.1)',
                shadowBlur: 2,
                // 添加渐变效果
                opacity: 0.8
            },

            // 节点标签样式
            label: {
                show: true,
                position: 'right',
                verticalAlign: 'middle',
                align: 'left',
                fontSize: 12,
                fontWeight: 'normal',
                color: '#1f2937',
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                padding: [4, 8],
                borderRadius: 4,
                shadowColor: 'rgba(0, 0, 0, 0.1)',
                shadowBlur: 2,
                // 确保深层标签也显示
                rich: {
                    level0: { fontSize: 14, fontWeight: 'bold' },
                    level1: { fontSize: 12, fontWeight: '500' },
                    level2: { fontSize: 11, fontWeight: 'normal' },
                    level3: { fontSize: 10, fontWeight: 'normal' }
                }
            },

            // 叶子节点样式 - 确保显示
            leaves: {
                label: {
                    show: true,
                    position: 'right',
                    fontSize: 10,
                    color: '#4b5563',
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    padding: [2, 6],
                    borderRadius: 3
                },
                // 叶子节点连线样式
                lineStyle: {
                    color: '#94a3b8',
                    width: 2,
                    type: 'solid',
                    opacity: 0.8
                }
            },

            // 关键修复：展开/收缩配置
            expandAndCollapse: false, // 禁用展开/收缩
            initialTreeDepth: -1, // 展开所有层级（-1表示全部展开）

            // 动画配置
            animationDuration: 1000,
            animationEasing: 'cubicOut',
            animationDelay: (idx) => idx * 10, // 渐进式动画

            // 强调样式 - 包括深层级
            emphasis: {
                focus: 'descendant',
                itemStyle: {
                    borderWidth: 3,
                    borderColor: '#3b82f6',
                    shadowBlur: 15,
                    shadowColor: 'rgba(59, 130, 246, 0.4)'
                },
                lineStyle: {
                    color: '#3b82f6',
                    width: 3,
                    shadowColor: 'rgba(59, 130, 246, 0.3)',
                    shadowBlur: 8,
                    opacity: 1
                },
                label: {
                    show: true,
                    fontSize: 13,
                    fontWeight: 'bold'
                }
            },

            // 确保所有节点都被渲染
            silent: false,

            // 添加层级配置
            levels: [
                {
                    itemStyle: { color: '#8b5cf6' },
                    lineStyle: { color: '#8b5cf6', width: 3 }
                },
                {
                    itemStyle: { color: '#3b82f6' },
                    lineStyle: { color: '#3b82f6', width: 2 }
                },
                {
                    itemStyle: { color: '#10b981' },
                    lineStyle: { color: '#10b981', width: 2 }
                },
                {
                    itemStyle: { color: '#f59e0b' },
                    lineStyle: { color: '#f59e0b', width: 2 }
                }
            ]
        }]
    }

    return option
}

// 添加树形视图的缩放控制方法
const zoomIn = () => {
    if (chartInstance.value && viewMode.value === 'tree') {
        chartInstance.value.dispatchAction({
            type: 'dataZoom',
            start: 10,
            end: 90
        })
    }
}

const zoomOut = () => {
    if (chartInstance.value && viewMode.value === 'tree') {
        chartInstance.value.dispatchAction({
            type: 'dataZoom',
            start: 0,
            end: 100
        })
    }
}

const zoomReset = () => {
    if (chartInstance.value && viewMode.value === 'tree') {
        chartInstance.value.dispatchAction({
            type: 'restore'
        })
    }
}

const renderGraph = () => {
    if (!chartContainer.value) {
        setTimeout(() => {
            if (chartContainer.value) renderGraph()
        }, 200)
        return
    }

    if (chartInstance.value) {
        chartInstance.value.dispose()
    }

    try {
        chartInstance.value = echarts.init(chartContainer.value, null, {
            renderer: 'svg'
        })

        let option = {}

        if (viewMode.value === 'tree') {
            // 使用修复后的树形视图配置
            option = renderTreeView()
        } else {
            // 原有的力导向和圆形布局配置保持不变
            const { nodes, links, categories } = buildEChartsData()

            option = {
                backgroundColor: '#f8fafc',
                title: {
                    text: '知识结构网络',
                    subtext: '点击节点查看详情 • 拖拽调整布局',
                    left: 'center',
                    top: 20,
                    textStyle: {
                        fontSize: 20,
                        fontWeight: 'bold',
                        color: '#1f2937'
                    },
                    subtextStyle: {
                        fontSize: 14,
                        color: '#6b7280'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    borderColor: '#e5e7eb',
                    borderWidth: 1,
                    textStyle: {
                        color: '#1f2937'
                    },
                    formatter: (params) => {
                        if (params.dataType === 'node') {
                            return `
                                <div style="padding: 12px;">
                                    <strong style="font-size: 16px;">${params.data.name}</strong><br/>
                                    <div style="margin-top: 8px;">
                                        <span style="color: #6b7280;">类型:</span> ${params.data.category}<br/>
                                        <span style="color: #6b7280;">掌握度:</span> ${params.data.mastery}%<br/>
                                        <span style="color: #6b7280;">重要度:</span> ${'★'.repeat(params.data.importance)}
                                    </div>
                                </div>
                            `
                        }
                        return `${params.data.source} → ${params.data.target}`
                    }
                },
                legend: [{
                    data: categories.map(c => c.name),
                    left: 30,
                    top: 80,
                    orient: 'vertical',
                    itemGap: 15,
                    textStyle: {
                        fontSize: 14,
                        color: '#4b5563'
                    }
                }],
                animationDuration: 1500,
                animationEasingUpdate: 'quinticInOut',
                series: [{
                    name: '知识图谱',
                    type: 'graph',
                    layout: viewMode.value,
                    data: nodes,
                    links: links,
                    categories: categories,
                    roam: true,
                    force: {
                        repulsion: repulsion.value,
                        gravity: 0.1,
                        edgeLength: edgeLength.value,
                        layoutAnimation: true
                    },
                    circular: {
                        rotateLabel: true
                    },
                    label: {
                        position: 'right',
                        formatter: '{b}',
                        fontSize: 12,
                        color: '#374151'
                    },
                    lineStyle: {
                        color: 'source',
                        curveness: 0.3
                    },
                    emphasis: {
                        focus: 'adjacency',
                        lineStyle: {
                            width: 4
                        },
                        itemStyle: {
                            shadowBlur: 20,
                            shadowColor: 'rgba(0, 0, 0, 0.3)'
                        }
                    }
                }]
            }
        }

        chartInstance.value.setOption(option)

        // 添加交互事件
        chartInstance.value.on('click', (params) => {
            if (params.dataType === 'node' || params.data.name) {
                selectedNode.value = params.data
                showNodeDialog.value = true
            }
        })

        window.addEventListener('resize', handleResize)
    } catch (error) {
        console.error('Error rendering chart:', error)
    }
}


// 搜索处理
const handleSearch = () => {
    if (!chartInstance.value) return

    const option = chartInstance.value.getOption()
    const nodes = option.series[0].data

    nodes.forEach(node => {
        if (searchQuery.value && !node.name.includes(searchQuery.value)) {
            node.itemStyle = {
                ...node.itemStyle,
                opacity: 0.2
            }
        } else {
            node.itemStyle = {
                ...node.itemStyle,
                opacity: 1
            }
        }
    })

    chartInstance.value.setOption(option)
}

// 切换视图
const switchView = () => {
    renderGraph()

    // 如果切换到树形视图，添加特殊动画效果
    // if (viewMode.value === 'tree') {
    //     setTimeout(() => {
    //         addTreeAnimations()
    //     }, 500)
    // }
}

// 更新布局
const updateLayout = () => {
    if (!chartInstance.value) return

    const option = chartInstance.value.getOption()
    option.series[0].force.edgeLength = edgeLength.value
    option.series[0].force.repulsion = repulsion.value
    chartInstance.value.setOption(option)
}

// 切换标签显示
const toggleLabels = () => {
    if (!chartInstance.value) return

    const option = chartInstance.value.getOption()
    option.series[0].label.show = showLabels.value
    chartInstance.value.setOption(option)
    fetchKnowledgeGraph()
}

// 导航到节点
const navigateToNode = (nodeName) => {
    showNodeDialog.value = false

    // 在图中高亮该节点
    if (chartInstance.value) {
        chartInstance.value.dispatchAction({
            type: 'highlight',
            seriesIndex: 0,
            name: nodeName
        })
    }
}

// 获取节点标签样式
const getNodeSeverity = (category) => {
    const severityMap = {
        '核心知识点': 'danger',
        '分支知识点': 'info',
        '应用知识点': 'success'
    }
    return severityMap[category] || 'secondary'
}

// 获取掌握度样式
const getMasteryClass = (mastery) => {
    if (mastery < 60) return 'mastery-low'
    if (mastery < 80) return 'mastery-medium'
    return 'mastery-high'
}

// 处理窗口大小变化
const handleResize = () => {
    if (chartInstance.value) {
        chartInstance.value.resize()
    }
}

// 导出图片
const exportGraph = () => {
    if (!chartInstance.value) return

    const url = chartInstance.value.getDataURL({
        pixelRatio: 2,
        backgroundColor: '#fff'
    })

    const link = document.createElement('a')
    link.download = `knowledge-graph-${new Date().toISOString().slice(0, 10)}.png`
    link.href = url
    link.click()
}

// 生命周期
onMounted(async () => {
    await nextTick()
    setTimeout(() => {
        fetchKnowledgeGraph()
        setTimeout(() => {
            forceRefresh()
        }, 1000)
    }, 200)
})

onUnmounted(() => {
    if (chartInstance.value) {
        chartInstance.value.dispose()
    }
    window.removeEventListener('resize', handleResize)
})

// 监听搜索
watch(searchQuery, () => {
    handleSearch()
})
</script>

<style scoped>
.knowledge-graph-container {
    padding: 20px;
    max-width: 1600px;
    margin: 0 auto;
    background-color: #f3f4f6;
    min-height: 100vh;
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.title {
    margin: 0;
    color: #1f2937;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 28px;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.search-input {
    width: 250px;
}

.loading-container,
.error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 600px;
}

.loading-text {
    margin-top: 20px;
    color: #6b7280;
    font-size: 16px;
}

.main-content {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 统计卡片 */
.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-icon {
    font-size: 32px;
    color: #3b82f6;
    background: #eff6ff;
    width: 64px;
    height: 64px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stat-icon.warning {
    color: #f59e0b;
    background: #fef3c7;
}

.stat-content {
    display: flex;
    flex-direction: column;
}

.stat-value {
    font-size: 28px;
    font-weight: bold;
    color: #1f2937;
}

.stat-label {
    font-size: 14px;
    color: #6b7280;
    margin-top: 4px;
}

/* 图表区域 */
.chart-wrapper {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 20px;
    margin-bottom: 30px;
}

.chart-container {
    width: 100%;
    height: 700px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.control-panel {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    height: fit-content;
}

.control-panel h4 {
    margin: 0 0 20px 0;
    color: #1f2937;
    font-size: 18px;
}

.control-item {
    margin-bottom: 24px;
}

.control-item label {
    display: block;
    margin-bottom: 8px;
    color: #4b5563;
    font-size: 14px;
    font-weight: 500;
}

/* 信息区域 */
.info-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.legend,
.suggestions {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.legend h4,
.suggestions h4 {
    margin: 0 0 20px 0;
    color: #1f2937;
    font-size: 18px;
}

.legend-items {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 16px;
}

.node-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    flex-shrink: 0;
}

.node-icon.core {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
}

.node-icon.branch {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.node-icon.leaf {
    background: linear-gradient(135deg, #10b981, #059669);
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.legend-text strong {
    display: block;
    color: #1f2937;
    margin-bottom: 4px;
}

.legend-text span {
    color: #6b7280;
    font-size: 14px;
}

.suggestion-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.suggestion-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    background: #f9fafb;
    border-radius: 8px;
    font-size: 14px;
    color: #4b5563;
}

.suggestion-item i {
    color: #f59e0b;
    flex-shrink: 0;
    margin-top: 2px;
}

/* 节点详情对话框 */
.node-detail {
    padding: 8px;
}

.detail-section {
    margin-bottom: 24px;
}

.detail-section h5 {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 16px 0;
    color: #1f2937;
    font-size: 16px;
}

.detail-section h5 i {
    color: #3b82f6;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.info-item label {
    font-size: 12px;
    color: #6b7280;
    font-weight: 500;
}

.info-item span {
    font-size: 14px;
    color: #1f2937;
    font-weight: 600;
}

.relation-group h6 {
    margin: 0 0 12px 0;
    color: #4b5563;
    font-size: 14px;
    font-weight: 600;
}

.relation-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.relation-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #f9fafb;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.relation-item:hover {
    background: #f3f4f6;
    transform: translateX(4px);
}

.relation-item i {
    color: #6b7280;
}

.relation-item span {
    flex: 1;
    font-size: 14px;
    color: #1f2937;
}

.learning-timeline {
    margin-top: 16px;
}

.timeline-content {
    margin-bottom: 16px;
}

.timeline-content strong {
    display: block;
    margin-bottom: 4px;
    color: #1f2937;
}

.timeline-content p {
    margin: 0;
    color: #6b7280;
    font-size: 14px;
}

/* 掌握度进度条样式 */
.mastery-low :deep(.p-progressbar-value) {
    background: #ef4444;
}

.mastery-medium :deep(.p-progressbar-value) {
    background: #f59e0b;
}

.mastery-high :deep(.p-progressbar-value) {
    background: #10b981;
}

/* 工具类 */
.mt-3 { margin-top: 1rem; }
.ml-auto { margin-left: auto; }

/* 响应式设计 */
@media (max-width: 1024px) {
    .chart-wrapper {
        grid-template-columns: 1fr;
    }

    .control-panel {
        order: -1;
    }

    .chart-container {
        height: 500px;
    }
}

@media (max-width: 768px) {
    .header-container {
        flex-direction: column;
        align-items: flex-start;
    }

    .header-actions {
        width: 100%;
        justify-content: flex-start;
    }

    .info-section {
        grid-template-columns: 1fr;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .stats-container {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 480px) {
    .stats-container {
        grid-template-columns: 1fr;
    }

    .search-input {
        width: 100%;
    }
}

.title {
    font-family: 'Helvetica Neue', Helvetica, 'Arial Rounded MT Bold', sans-serif;
    font-size: 2rem;
    font-weight: 700; /* 加粗 */
    color: #111; /* 深黑色 */
    text-align: left;
    margin: 20px 0 20px 50px;
    position: relative;
    transition: all 0.3s ease-in-out;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    max-width: 300px;

    /* 可选：字体渲染优化，让文字更圆润清晰 */
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

.move-left-right {
    margin-right: 4px;
}

/* 层级视图特殊样式 */
.chart-container.tree-view {
    background: rgba(189, 189, 189, 0.33);
    border: none;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
}

.chart-container.tree-view::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    z-index: 1;
}

.chart-container.tree-view canvas,
.chart-container.tree-view svg {
    position: relative;
    z-index: 2;
}

/* 视图模式按钮样式增强 */
.p-selectbutton .p-button {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.p-selectbutton .p-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.p-selectbutton .p-button:hover::before {
    left: 100%;
}

.p-selectbutton .p-button.p-highlight {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* 控制面板在树形视图时的样式调整 */
.control-panel.tree-mode {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.control-panel.tree-mode h4 {
    background: #48517c;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 2px solid #e5e7eb;
}

/* 树形视图专用的图例样式 */
.tree-legend {
    position: absolute;
    top: 100px;
    left: 30px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    z-index: 10;
    min-width: 200px;
}

.tree-legend h4 {
    margin: 0 0 12px 0;
    color: #1f2937;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
    padding-bottom: 8px;
    border-bottom: 1px solid #e5e7eb;
}

.tree-legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
    padding: 6px;
    border-radius: 6px;
    transition: background-color 0.2s;
}

.tree-legend-item:hover {
    background: rgba(102, 126, 234, 0.1);
}

.tree-level-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
}

.tree-level-indicator.level-0 {
    background: linear-gradient(135deg, #667eea, #764ba2);
    box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

.tree-level-indicator.level-1 {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.tree-level-indicator.level-2 {
    background: linear-gradient(135deg, #10b981, #059669);
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.tree-legend-text {
    font-size: 12px;
    color: #4b5563;
    font-weight: 500;
}

/* 层级视图的加载动画 */
.tree-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 20;
}

.tree-loading-circle {
    width: 60px;
    height: 60px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top: 3px solid #667eea;
    border-radius: 50%;
    animation: tree-spin 1s linear infinite;
}

@keyframes tree-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 节点详情对话框在树形视图时的特殊样式 */
.node-detail.tree-mode {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
    backdrop-filter: blur(10px);
}

.node-detail.tree-mode .detail-section h5 {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* 层级路径指示器 */
.tree-path-indicator {
    position: absolute;
    top: 80px;
    right: 30px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 12px 16px;
    border-radius: 25px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    z-index: 10;
    font-size: 12px;
    color: #4b5563;
}

.tree-path-indicator .path-item {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.tree-path-indicator .path-arrow {
    color: #9ca3af;
    margin: 0 6px;
}

/* 统计卡片在树形视图时的样式调整 */
.stats-container.tree-mode .stat-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.stats-container.tree-mode .stat-icon {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    color: #667eea;
}

/* 树形视图的缩放控制 */
.tree-zoom-controls {
    position: absolute;
    bottom: 30px;
    right: 30px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 10;
}

.tree-zoom-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tree-zoom-btn:hover {
    background: #667eea;
    color: white;
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* 响应式调整 */
@media (max-width: 1024px) {
    .tree-legend {
        position: relative;
        top: auto;
        left: auto;
        margin-bottom: 20px;
    }

    .tree-path-indicator {
        position: relative;
        top: auto;
        right: auto;
        margin-bottom: 20px;
        text-align: center;
    }

    .tree-zoom-controls {
        position: fixed;
        bottom: 20px;
        right: 20px;
        flex-direction: row;
    }
}

@media (max-width: 768px) {
    .chart-container.tree-view {
        height: 400px;
        margin-bottom: 20px;
    }

    .tree-zoom-btn {
        width: 35px;
        height: 35px;
    }
}

/* 树形节点连接线的特殊效果 */
@keyframes tree-line-pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

.tree-connection-highlight {
    animation: tree-line-pulse 2s ease-in-out infinite;
}

/* 层级深度渐变效果 */
.tree-depth-gradient {
    background: linear-gradient(
        to right,
        rgba(102, 126, 234, 0.8) 0%,
        rgba(59, 130, 246, 0.6) 33%,
        rgba(16, 185, 129, 0.4) 66%,
        rgba(245, 158, 11, 0.2) 100%
    );
    height: 4px;
    width: 100%;
    margin-top: 10px;
    border-radius: 2px;
}

/* 悬浮提示的特殊样式 */
.tree-tooltip-enhanced {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}
</style>
