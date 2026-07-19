<template>
    <div class="qa-assistant">
        <GeometricBackground />
        <div class="scenic-background"></div>

        <!-- 蓝色渐变标题栏 -->
        <div class="page-banner">
            <div class="banner-decoration">
                <div class="deco-circle deco-circle-1"></div>
                <div class="deco-circle deco-circle-2"></div>
            </div>
            <div class="banner-content">
                <div class="banner-text">
                    <h2 class="banner-title">智能学情答疑助手</h2>
                    <p class="banner-subtitle">Multimodal Q&A Assistant</p>
                </div>
                <span class="banner-tag">赛题加分功能 讯飞STT/TTS多模态数字人答疑</span>
            </div>
        </div>

        <!-- Tab 标签栏 -->
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

        <!-- Tab1：多模态学情答疑 -->
        <div v-if="activeTab === 0">
            <div class="main-layout">
                <!-- 左栏：对话区 70% -->
                <div class="chat-panel">
                    <div class="chat-container">
                        <div class="chat-messages" ref="chatMessagesRef">
                            <div v-if="sampleMessages.length === 0" class="empty-state">
                                <div class="empty-icon">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M8 12H8.01M12 12H12.01M16 12H16.01M21 12C21 16.9706 16.9706 21 12 21C10.2307 21 8.57995 20.4884 7.19029 19.6068L3 21L4.39312 16.8097C3.51164 15.42 3 13.7693 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </div>
                                <p class="empty-text">开始学情答疑</p>
                                <p class="empty-hint">输入您在学习中遇到的问题，获取专业解答</p>
                            </div>
                            <div v-else class="messages-list">
                                <div v-for="(msg, index) in sampleMessages" :key="index" class="message-row" :class="msg.type">
                                    <!-- AI 消息 -->
                                    <div v-if="msg.type === 'ai'" class="message-content-wrapper">
                                        <div class="avatar ai-avatar">
                                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
                                                <circle cx="9" cy="10" r="1.5" fill="currentColor"/>
                                                <circle cx="15" cy="10" r="1.5" fill="currentColor"/>
                                                <path d="M8 15C8 15 9.5 17 12 17C14.5 17 16 15 16 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                            </svg>
                                        </div>
                                        <div class="message-bubble">
                                            <div v-if="msg.format === 'text'" class="message-content">{{ msg.content }}</div>
                                            <div v-else-if="msg.format === 'mindmap'" class="multimodal-card">
                                                <div class="multimodal-label">📊 思维导图</div>
                                                <div class="mindmap-container" :ref="el => mindmapContainers[index] = el"></div>
                                                <div class="multimodal-btns">
                                                    <button class="btn btn-sm btn-outline" @click="downloadMindmap(index)">下载 SVG</button>
                                                    <button class="btn btn-sm btn-primary" @click="expandMindmap(index)">全屏预览</button>
                                                </div>
                                            </div>
                                            <div v-else-if="msg.format === 'code'" class="multimodal-card">
                                                <div class="multimodal-label">💻 {{ msg.codeData?.title || '代码案例' }}</div>
                                                <div class="code-block"><pre><code>{{ msg.codeData?.code || '' }}</code></pre></div>
                                                <div v-if="msg.codeData?.description" class="code-desc-text">{{ msg.codeData.description }}</div>
                                                <div class="multimodal-btns">
                                                    <button class="btn btn-sm btn-outline" @click="copyCode(msg)">复制代码</button>
                                                </div>
                                            </div>
                                            <div v-else-if="msg.format === 'quiz'" class="multimodal-card">
                                                <div class="multimodal-label">📝 专项练习题</div>
                                                <div class="quiz-list">
                                                    <div v-for="(q, qi) in msg.quizData?.questions || []" :key="qi" class="quiz-item">
                                                        <div class="quiz-item-header">
                                                            <span class="quiz-type-tag" :class="'tag-' + q.type">{{ q.type === 'choice' ? '选择题' : q.type === 'judge' ? '判断题' : q.type === 'fill' ? '填空题' : '简答题' }}</span>
                                                            <span class="quiz-qnum">第 {{ qi + 1 }} 题</span>
                                                        </div>
                                                        <div class="quiz-q-text">{{ q.question }}</div>
                                                        <div v-if="q.options" class="quiz-options">
                                                            <div v-for="(opt, oi) in q.options" :key="oi" class="quiz-option">{{ opt }}</div>
                                                        </div>
                                                        <div v-if="msg.showAnswers" class="quiz-answer-box">
                                                            <strong>答案：</strong>{{ q.answer }}
                                                            <div v-if="q.explanation" class="quiz-explanation">解析：{{ q.explanation }}</div>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="multimodal-btns">
                                                    <button class="btn btn-sm btn-primary" @click="msg.showAnswers = !msg.showAnswers">{{ msg.showAnswers ? '隐藏全部答案' : '显示全部答案' }}</button>
                                                </div>
                                            </div>
                                            <div v-else-if="msg.format === 'report'" class="multimodal-card">
                                                <div class="multimodal-label">📄 完整文字解析报告</div>
                                                <div class="report-content" v-html="renderMarkdown(msg.content)"></div>
                                                <div class="multimodal-btns">
                                                    <button class="btn btn-sm btn-outline" @click="downloadReport(msg)">下载报告</button>
                                                </div>
                                            </div>
                                            <div v-else-if="msg.format === 'loading'" class="loading-indicator">
                                                <div class="loading-dots"><span></span><span></span><span></span></div>
                                                <span class="loading-text">{{ msg.content || 'AI 正在生成中...' }}</span>
                                            </div>
                                            <div class="message-time">{{ msg.time }}</div>
                                        </div>
                                    </div>
                                    <!-- 用户消息 -->
                                    <div v-else class="message-content-wrapper user-message">
                                        <div class="message-bubble user-bubble">
                                            <div class="message-content">{{ msg.content }}</div>
                                            <div class="message-time user-time">{{ msg.time }}</div>
                                        </div>
                                        <div class="avatar user-avatar">
                                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                                <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            </svg>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 右栏：配置面板 28% -->
                <div class="config-panel">
                    <div class="sidebar-card">
                        <h4 class="sidebar-title">多模态输出配置面板</h4>
                        <div class="config-section">
                            <label class="config-label">当前答疑话题</label>
                            <input v-model="currentTopic" type="text" placeholder="请输入学习主题，如：二叉树遍历算法" class="topic-input" />
                        </div>
                        <div class="config-section">
                            <label class="config-label">输出内容偏好</label>
                            <div class="radio-group">
                                <label class="radio-label" :class="{ active: outputPreference === 'theory' }" @click="outputPreference = 'theory'"><input type="radio" v-model="outputPreference" value="theory" class="hidden-radio" />理论文字优先</label>
                                <label class="radio-label" :class="{ active: outputPreference === 'code' }" @click="outputPreference = 'code'"><input type="radio" v-model="outputPreference" value="code" class="hidden-radio" />实操代码优先</label>
                                <label class="radio-label" :class="{ active: outputPreference === 'diagram' }" @click="outputPreference = 'diagram'"><input type="radio" v-model="outputPreference" value="diagram" class="hidden-radio" />图解导图优先</label>
                            </div>
                        </div>
                        <div class="config-section">
                            <label class="config-label">输出难度适配</label>
                            <div class="radio-group">
                                <label class="radio-label" :class="{ active: difficultyLevel === 'basic' }" @click="difficultyLevel = 'basic'"><input type="radio" v-model="difficultyLevel" value="basic" class="hidden-radio" />基础易懂</label>
                                <label class="radio-label" :class="{ active: difficultyLevel === 'standard' }" @click="difficultyLevel = 'standard'"><input type="radio" v-model="difficultyLevel" value="standard" class="hidden-radio" />标准均衡</label>
                                <label class="radio-label" :class="{ active: difficultyLevel === 'advanced' }" @click="difficultyLevel = 'advanced'"><input type="radio" v-model="difficultyLevel" value="advanced" class="hidden-radio" />拔高拓展</label>
                            </div>
                        </div>
                        <div class="model-info">
                            <span class="model-label">AI 模型</span>
                            <span class="model-name">{{ currentModelName }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 多模态快捷操作栏 -->
            <div class="multimodal-bar">
                <div class="multimodal-actions">
                    <button class="btn" :class="activeButton === 'mindmap' ? 'btn-primary' : 'btn-outline'" @click="handleButtonClick('mindmap')" :disabled="generating">{{ generating && generatingType === 'mindmap' ? '生成中...' : '生成思维导图图解' }}</button>
                    <button class="btn" :class="activeButton === 'code' ? 'btn-primary' : 'btn-outline'" @click="handleButtonClick('code')" :disabled="generating">{{ generating && generatingType === 'code' ? '生成中...' : '生成分层代码案例' }}</button>
                    <button class="btn" :class="activeButton === 'quiz' ? 'btn-primary' : 'btn-outline'" @click="handleButtonClick('quiz')" :disabled="generating">{{ generating && generatingType === 'quiz' ? '生成中...' : '生成专项练习题库' }}</button>
                    <button class="btn" :class="activeButton === 'report' ? 'btn-primary' : 'btn-outline'" @click="handleButtonClick('report')" :disabled="generating">{{ generating && generatingType === 'report' ? '生成中...' : '生成完整文字解析报告' }}</button>
                </div>
            </div>

            <!-- 底部输入栏 -->
            <div class="input-bar">
                <div class="input-wrapper">
                    <button class="mic-btn" title="语音提问">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 1C10.3431 1 9 2.34315 9 4V12C9 13.6569 10.3431 15 12 15C13.6569 15 15 13.6569 15 12V4C15 2.34315 13.6569 1 12 1Z" fill="currentColor"/><path d="M19 10V12C19 15.866 15.866 19 12 19C8.13401 19 5 15.866 5 12V10H3V12C3 16.4183 6.58172 20 11 20V23H13V20C17.4183 20 21 16.4183 21 12V10H19Z" fill="currentColor"/></svg>
                    </button>
                    <input v-model="inputText" type="text" placeholder="输入学情问题，或点击麦克风语音提问..." class="message-input" @keyup.enter="sendMessage" />
                    <button class="send-btn" title="发送" @click="sendMessage">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </button>
                    <button class="digital-human-btn" :class="{ active: digitalHumanStore.isActive && digitalHumanStore.isVisible && !digitalHumanStore.isMinimized }" @click="toggleDigitalHuman">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/><circle cx="9" cy="10" r="1.5" fill="currentColor"/><circle cx="15" cy="10" r="1.5" fill="currentColor"/><path d="M8 15C8 15 9.5 17 12 17C14.5 17 16 15 16 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Tab2：问答历史记录 -->
        <div v-if="activeTab === 1">
            <div class="content-card">
                <div class="card-header-row">
                    <h3 class="card-title" style="margin: 0;">问答历史记录</h3>
                    <button class="btn btn-outline btn-sm" @click="exportHistory">批量导出问答记录</button>
                </div>
                <div v-if="historyRecords.length === 0" class="empty-state" style="padding: 2rem;"><p class="empty-text">暂无历史记录</p></div>
                <div v-else class="history-list">
                    <div v-for="(record, index) in historyRecords" :key="index" class="history-item">
                        <div class="history-item-info">
                            <span class="history-summary">{{ record.topic }}</span>
                            <span class="history-time">{{ record.time }}</span>
                            <span class="history-tags"><span class="tag" :class="'tag-' + record.type">{{ record.typeLabel }}</span></span>
                        </div>
                        <div class="history-item-actions"><button class="btn btn-sm btn-outline" @click="replayRecord(index)">重新答疑</button></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab3：配套知识点资源库 -->
        <div v-if="activeTab === 2">
            <div class="content-card">
                <h3 class="card-title">配套知识点资源库</h3>
                <div class="resource-tabs">
                    <div v-for="(rtab, rindex) in resourceTabs" :key="rindex" class="resource-tab" :class="{ active: activeResourceTab === rindex }" @click="activeResourceTab = rindex">{{ rtab }}</div>
                </div>
                <div class="resource-grid">
                    <div v-for="(item, idx) in filteredResources" :key="idx" class="resource-item">
                        <div class="resource-item-body">
                            <span class="resource-item-title">{{ item.title }}</span>
                            <span class="resource-item-desc">{{ item.desc }}</span>
                            <span v-if="item.tag" class="resource-tag" :class="'tag-' + item.tagType">{{ item.tag }}</span>
                        </div>
                        <button class="btn btn-sm btn-outline" @click="inputText = item.question">带入提问</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive, computed, nextTick, onBeforeUnmount } from 'vue';
import GeometricBackground from '@/components/GeometricBackground.vue';
import { useDigitalHumanStore } from '@/store/digitalHumanStore';
import { AIService } from '@/service/AIService';

export default {
    name: 'AnalyticsDashboard',
    components: { GeometricBackground },
    setup() {
        const activeTab = ref(0);
        const inputText = ref('');
        const currentTopic = ref('');
        const outputPreference = ref('theory');
        const difficultyLevel = ref('standard');
        const activeResourceTab = ref(0);
        const digitalHumanStore = useDigitalHumanStore();
        const generating = ref(false);
        const generatingType = ref('');
        const chatMessagesRef = ref(null);
        const mindmapContainers = ref([]);
        const activeButton = ref('mindmap');
        const mindmapInstances = new Map();

        const currentModelName = computed(() => {
            const provider = import.meta.env.VITE_LLM_PROVIDER || 'iflytek';
            return provider === 'iflytek' ? '讯飞星火 Spark Ultra-32K' : '通义千问 qwen-turbo';
        });

        const toggleDigitalHuman = () => {
            if (digitalHumanStore.isActive && digitalHumanStore.isVisible && !digitalHumanStore.isMinimized) {
                digitalHumanStore.minimize();
            } else {
                digitalHumanStore.expand();
            }
        };

        const tabs = ['多模态学情答疑', '问答历史记录', '配套知识点资源库'];
        const resourceTabs = ['课程文档', '思维导图', '分层题库', '代码案例', '拓展阅读', '教学动画'];

        // 硬编码的计算机/AI专业知识库资源
        const allResources = [
            // 课程文档
            { category: 0, title: '数据结构与算法导论', desc: '线性表、树、图、排序与搜索算法的系统讲解', tag: '核心基础', tagType: 'primary', question: '请讲解数据结构与算法的核心知识点' },
            { category: 0, title: '机器学习理论基础', desc: '监督学习、无监督学习、强化学习的数学原理与算法推导', tag: '重点', tagType: 'warning', question: '请详细讲解机器学习的三大范式及其区别' },
            { category: 0, title: '深度学习框架与实践', desc: '神经网络基础、CNN、RNN、Transformer架构详解', tag: '热门', tagType: 'danger', question: '请讲解深度学习中的CNN和RNN有什么区别' },
            { category: 0, title: '计算机组成原理', desc: 'CPU架构、存储系统、指令系统与总线通信', tag: '核心基础', tagType: 'primary', question: '请讲解计算机组成原理的核心概念' },
            { category: 0, title: '操作系统原理', desc: '进程管理、内存调度、文件系统与I/O系统', tag: '核心基础', tagType: 'primary', question: '请讲解操作系统中进程与线程的区别' },
            { category: 0, title: '数据库系统概论', desc: '关系代数、SQL语言、范式理论与事务管理', tag: '重点', tagType: 'warning', question: '请讲解数据库的三大范式' },
            // 思维导图
            { category: 1, title: '算法复杂度分析思维导图', desc: '时间复杂度与空间复杂度的系统梳理', tag: '高频考点', tagType: 'warning', question: '请用思维导图梳理算法复杂度分析' },
            { category: 1, title: '机器学习算法全景图', desc: '分类、回归、聚类、降维算法分类体系', tag: '热门', tagType: 'danger', question: '请用思维导图展示机器学习算法分类' },
            { category: 1, title: '深度学习网络架构导图', desc: 'CNN、RNN、GAN、Transformer对比梳理', tag: '热门', tagType: 'danger', question: '请用思维导图对比各种深度学习网络' },
            { category: 1, title: '计算机网络协议栈导图', desc: 'OSI七层与TCP/IP四层协议体系', tag: '核心基础', tagType: 'primary', question: '请用思维导图梳理计算机网络协议栈' },
            // 分层题库
            { category: 2, title: '数据结构基础题库', desc: '链表、栈、队列、树等基础题型50道', tag: '50题', tagType: 'info', question: '请给我出几道数据结构基础题' },
            { category: 2, title: '机器学习进阶题库', desc: 'SVM、决策树、集成学习等进阶题型30道', tag: '30题', tagType: 'warning', question: '请给我出几道机器学习进阶题' },
            { category: 2, title: '深度学习挑战题库', desc: '反向传播、注意力机制等难题20道', tag: '20题', tagType: 'danger', question: '请给我出几道深度学习挑战题' },
            { category: 2, title: '计算机综合题库', desc: '组成原理、操作系统、网络综合题40道', tag: '40题', tagType: 'info', question: '请给我出几道计算机综合题' },
            // 代码案例
            { category: 3, title: 'Python数据结构实现', desc: '链表、二叉树、哈希表的Python代码实现', tag: 'Python', tagType: 'success', question: '请展示用Python实现二叉树的代码' },
            { category: 3, title: 'PyTorch深度学习实战', desc: 'CNN图像分类、RNN序列建模代码案例', tag: 'PyTorch', tagType: 'danger', question: '请展示PyTorch实现CNN的代码' },
            { category: 3, title: '经典排序算法代码集', desc: '冒泡、快排、归并、堆排序的代码对比', tag: '算法', tagType: 'primary', question: '请展示快速排序的代码实现' },
            { category: 3, title: 'Scikit-learn机器学习实战', desc: '数据预处理、模型训练、评估完整流程', tag: 'sklearn', tagType: 'warning', question: '请展示sklearn完成机器学习的完整代码' },
            // 拓展阅读
            { category: 4, title: 'Transformer注意力机制详解', desc: 'Self-Attention、Multi-Head Attention原理剖析', tag: '前沿技术', tagType: 'danger', question: '请详细讲解Transformer的注意力机制' },
            { category: 4, title: '大语言模型原理与应用', desc: 'GPT、BERT、LLaMA等模型的技术演进', tag: '前沿技术', tagType: 'danger', question: '请讲解大语言模型的发展历程' },
            { category: 4, title: '计算机视觉前沿', desc: '目标检测、图像分割、生成对抗网络最新进展', tag: '前沿技术', tagType: 'warning', question: '请介绍计算机视觉的最新研究进展' },
            { category: 4, title: '自然语言处理技术演进', desc: '从Word2Vec到BERT再到GPT的技术路线', tag: '前沿技术', tagType: 'warning', question: '请讲解NLP技术的发展历程' },
            // 教学动画
            { category: 5, title: '二叉树遍历动画演示', desc: '前序、中序、后序、层序遍历的可视化过程', tag: '动画', tagType: 'primary', question: '请用动画演示二叉树的遍历过程' },
            { category: 5, title: '排序算法可视化动画', desc: '各种排序算法的执行过程动态展示', tag: '动画', tagType: 'success', question: '请动画展示快速排序的执行过程' },
            { category: 5, title: '神经网络前向传播动画', desc: '数据在网络中逐层传递的可视化', tag: '动画', tagType: 'danger', question: '请动画展示神经网络的前向传播' },
            { category: 5, title: 'TCP三次握手动画', desc: 'TCP连接建立过程的动态模拟', tag: '动画', tagType: 'info', question: '请动画展示TCP三次握手过程' },
        ];

        const filteredResources = computed(() => {
            return allResources.filter(item => item.category === activeResourceTab.value);
        });

        const sampleMessages = ref([
            { type: 'ai', content: '你好！我是你的学情答疑助手，有任何学习问题都可以向我提问。', time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }), format: 'text' }
        ]);
        const historyRecords = ref([]);

        function renderMindmap(index) {
            const msg = sampleMessages.value[index];
            if (!msg?.mindmapData) return;
            nextTick(() => {
                const container = mindmapContainers.value[index];
                if (!container) return;
                if (mindmapInstances.has(index)) { mindmapInstances.get(index).remove(); }
                container.innerHTML = '';
                const data = msg.mindmapData;
                const rootData = { name: data.root, children: data.children || [] };
                const nodeHeight = 44, levelGap = 220;
                const totalNodes = countNodes(rootData);
                const maxDepth = getMaxDepth(rootData);
                const svgWidth = Math.max(800, (maxDepth + 1) * levelGap + 200);
                const svgHeight = Math.max(400, totalNodes * nodeHeight + 80);
                const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svg.setAttribute('width', svgWidth);
                svg.setAttribute('height', svgHeight);
                svg.style.background = '#f8fafc';
                const colors = ['#165DFF', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];
                function buildTree(node, depth, startY) {
                    const x = depth * levelGap + 100;
                    const children = node.children || [];
                    if (children.length === 0) return { x, cy: startY + nodeHeight / 2, name: node.name, depth, children: [], height: nodeHeight };
                    let currentY = startY;
                    const childNodes = [];
                    children.forEach(child => { const r = buildTree(child, depth + 1, currentY); childNodes.push(r); currentY += r.height; });
                    const cy = (childNodes[0].cy + childNodes[childNodes.length - 1].cy) / 2;
                    return { x, cy, name: node.name, depth, children: childNodes, height: Math.max(nodeHeight, currentY - startY) };
                }
                const tree = buildTree(rootData, 0, 40);
                function drawLines(t) {
                    t.children.forEach(child => {
                        const line = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                        const mx = (t.x + child.x) / 2;
                        line.setAttribute('d', `M${t.x + 8},${t.cy} C${mx},${t.cy} ${mx},${child.cy} ${child.x - 8},${child.cy}`);
                        line.setAttribute('fill', 'none');
                        line.setAttribute('stroke', '#94a3b8');
                        line.setAttribute('stroke-width', '1.5');
                        svg.appendChild(line);
                        drawLines(child);
                    });
                }
                function drawNodes(t) {
                    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    circle.setAttribute('cx', t.x); circle.setAttribute('cy', t.cy);
                    circle.setAttribute('r', t.depth === 0 ? 8 : 5);
                    circle.setAttribute('fill', colors[t.depth % colors.length]);
                    circle.setAttribute('stroke', '#fff'); circle.setAttribute('stroke-width', '2');
                    g.appendChild(circle);
                    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    text.setAttribute('x', t.x + (t.depth === 0 ? 0 : 14));
                    text.setAttribute('y', t.cy + 4);
                    text.setAttribute('font-size', t.depth === 0 ? '14' : '12');
                    text.setAttribute('font-weight', t.depth <= 1 ? '600' : '400');
                    text.setAttribute('fill', '#1e293b');
                    text.setAttribute('text-anchor', t.depth === 0 ? 'middle' : 'start');
                    text.textContent = t.name;
                    g.appendChild(text);
                    svg.appendChild(g);
                    t.children.forEach(drawNodes);
                }
                drawLines(tree); drawNodes(tree);
                container.appendChild(svg);
                mindmapInstances.set(index, svg);
            });
        }

        function countNodes(node) { let count = 1; if (node.children) node.children.forEach(c => { count += countNodes(c); }); return count; }
        function getMaxDepth(node, depth) { depth = depth || 0; if (!node.children || node.children.length === 0) return depth; return Math.max(...node.children.map(c => getMaxDepth(c, depth + 1))); }
        function getTime() { return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }); }

        function parseJSONFromResponse(text) {
            if (!text) return null;
            let s = String(text).trim();
            try { return JSON.parse(s); } catch (e) {}
            s = s.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '');
            try { return JSON.parse(s.trim()); } catch (e) {}
            const m = s.match(/\{[\s\S]*\}/);
            if (m) { let j = m[0].replace(/(?<!\\)\n/g, '\\n').replace(/(?<!\\)\r/g, '\\r').replace(/(?<!\\)\t/g, '\\t'); try { return JSON.parse(j); } catch (e) {} }
            let partial = s.match(/\{[\s\S]*/);
            if (partial) {
                let j = partial[0].replace(/(?<!\\)\n/g, '\\n').replace(/(?<!\\)\r/g, '\\r').replace(/(?<!\\)\t/g, '\\t');
                if (j.match(/"[^"\\]*(?:\\.[^"\\]*)*$/)) j += '"';
                while (j.split('{').length > j.split('}').length) j += '}';
                try { return JSON.parse(j); } catch (e) {}
            }
            const codeMatch = s.match(/"code"\s*:\s*"([\s\S]*?)"/);
            if (codeMatch) {
                const code = codeMatch[1].replace(/\\n/g, '\n').replace(/\\"/g, '"').replace(/\\\\/g, '\\');
                const titleMatch = s.match(/"title"\s*:\s*"([^"]*)"/);
                const descMatch = s.match(/"description"\s*:\s*"([^"]*)"/);
                const langMatch = s.match(/"language"\s*:\s*"([^"]*)"/);
                return { title: titleMatch ? titleMatch[1] : '代码示例', description: descMatch ? descMatch[1] : '', code, language: langMatch ? langMatch[1] : 'text' };
            }
            return null;
        }

        async function sendMessage() {
            if (!inputText.value.trim()) return;
            const userMsg = { type: 'user', content: inputText.value, time: getTime(), format: 'text' };
            sampleMessages.value.push(userMsg);
            inputText.value = '';
            await nextTick(); scrollToBottom();
            const loadingMsg = reactive({ type: 'ai', content: 'AI 正在思考中...', time: getTime(), format: 'loading' });
            sampleMessages.value.push(loadingMsg); scrollToBottom();
            try {
                const res = await AIService.askQuestion(userMsg.content, currentTopic.value);
                loadingMsg.format = 'text';
                loadingMsg.content = res.data?.data?.answer || res.data?.message || '抱歉，暂时无法回答该问题。';
                loadingMsg.time = getTime();
            } catch (e) {
                loadingMsg.format = 'text';
                loadingMsg.content = '提问失败：' + (e.response?.data?.detail || e.message || '未知错误');
            } finally { scrollToBottom(); }
        }

        async function callMultimodalAPI(type) {
            if (!currentTopic.value.trim()) { alert('请先输入答疑话题！'); return; }
            generating.value = true; generatingType.value = type;
            const loadingMsg = reactive({ type: 'ai', content: '正在生成中，请稍候...', time: getTime(), format: 'loading' });
            sampleMessages.value.push(loadingMsg); scrollToBottom();
            try {
                let res;
                switch (type) {
                    case 'mindmap': res = await AIService.generateMindmap(currentTopic.value, difficultyLevel.value, outputPreference.value); break;
                    case 'code': res = await AIService.generateCodeExamples(currentTopic.value, difficultyLevel.value, outputPreference.value); break;
                    case 'quiz': res = await AIService.generatePracticeQuestions(currentTopic.value, difficultyLevel.value, outputPreference.value); break;
                    case 'report': res = await AIService.generateAnalysisReport(currentTopic.value, difficultyLevel.value, outputPreference.value); break;
                }
                loadingMsg.time = getTime();
                let raw = res.data?.data ?? res.data?.message ?? '';
                const answerText = typeof raw === 'string' ? raw : (raw?.answer ?? JSON.stringify(raw));
                switch (type) {
                    case 'mindmap': {
                        const mindmapData = parseJSONFromResponse(answerText);
                        loadingMsg.format = 'mindmap';
                        loadingMsg.mindmapData = mindmapData || { root: currentTopic.value, children: [{ name: '解析中...' }] };
                        const idx = sampleMessages.value.indexOf(loadingMsg);
                        if (idx !== -1) renderMindmap(idx);
                        break;
                    }
                    case 'code': {
                        let codeData;
                        if (typeof raw === 'object' && raw !== null && raw.code) { codeData = raw; }
                        else { codeData = parseJSONFromResponse(answerText); }
                        loadingMsg.format = 'code';
                        if (codeData && codeData.code) { loadingMsg.codeData = codeData; }
                        else if (codeData && (codeData.basic || codeData.intermediate || codeData.advanced || codeData.standard)) {
                            const levelKey = difficultyLevel.value === 'advanced' ? 'advanced' : difficultyLevel.value === 'standard' ? 'intermediate' : 'basic';
                            loadingMsg.codeData = codeData[levelKey] || codeData.basic || codeData.intermediate || codeData.advanced || codeData.standard;
                        } else if (codeData) {
                            loadingMsg.codeData = { title: codeData.title || '代码示例', description: codeData.description || '', code: JSON.stringify(codeData), language: 'text' };
                        } else {
                            loadingMsg.codeData = { title: '代码示例', description: 'JSON解析失败', code: answerText, language: 'text' };
                        }
                        break;
                    }
                    case 'quiz': { const quizData = parseJSONFromResponse(answerText); loadingMsg.format = 'quiz'; loadingMsg.quizData = quizData || { questions: [] }; loadingMsg.showAnswers = false; break; }
                    case 'report': { loadingMsg.format = 'report'; loadingMsg.content = answerText; break; }
                }
                const typeLabels = { mindmap: '思维导图', code: '代码案例', quiz: '练习题库', report: '解析报告' };
                historyRecords.value.unshift({ topic: currentTopic.value, time: new Date().toLocaleString('zh-CN'), type, typeLabel: typeLabels[type] });
            } catch (e) {
                loadingMsg.format = 'text';
                loadingMsg.content = '生成失败：' + (e.response?.data?.detail || e.message || '未知错误');
            } finally { generating.value = false; generatingType.value = ''; scrollToBottom(); }
        }

        function handleButtonClick(type) { activeButton.value = type; callMultimodalAPI(type); }
        function copyCode(msg) { navigator.clipboard.writeText(msg.codeData?.code || '').then(() => alert('代码已复制！')); }

        function downloadMindmap(index) {
            const msg = sampleMessages.value[index]; if (!msg?.mindmapData) return;
            const data = msg.mindmapData; const rootData = { name: data.root, children: data.children || [] };
            function countN(node) { let c = 1; if (node.children) node.children.forEach(ch => { c += countN(ch); }); return c; }
            function maxD(node, d) { d = d || 0; if (!node.children || node.children.length === 0) return d; return Math.max(...node.children.map(ch => maxD(ch, d + 1))); }
            const nodeHeight = 44, levelGap = 220; const totalNodes = countN(rootData), maxDepth = maxD(rootData);
            const svgWidth = Math.max(800, (maxDepth + 1) * levelGap + 200), svgHeight = Math.max(400, totalNodes * nodeHeight + 80);
            const colors = ['#165DFF', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];
            function buildTree(node, depth, startY) {
                const x = depth * levelGap + 100; const children = node.children || [];
                if (children.length === 0) return { x, cy: startY + nodeHeight / 2, name: node.name, depth, children: [], height: nodeHeight };
                let currentY = startY; const childNodes = [];
                children.forEach(child => { const r = buildTree(child, depth + 1, currentY); childNodes.push(r); currentY += r.height; });
                const cy = (childNodes[0].cy + childNodes[childNodes.length - 1].cy) / 2;
                return { x, cy, name: node.name, depth, children: childNodes, height: Math.max(nodeHeight, currentY - startY) };
            }
            const tree = buildTree(rootData, 0, 40); let linesSvg = '', nodesSvg = '';
            function drawLines(t) { t.children.forEach(child => { const mx = (t.x + child.x) / 2; linesSvg += `<path d="M${t.x + 8},${t.cy} C${mx},${t.cy} ${mx},${child.cy} ${child.x - 8},${child.cy}" fill="none" stroke="#94a3b8" stroke-width="1.5"/>`; drawLines(child); }); }
            function drawNodes(t) { const r = t.depth === 0 ? 10 : 6; const color = colors[t.depth % colors.length]; nodesSvg += `<g><circle cx="${t.x}" cy="${t.cy}" r="${r}" fill="${color}" stroke="#fff" stroke-width="2"/><text x="${t.x + (t.depth === 0 ? 0 : 16)}" y="${t.cy + 5}" font-size="${t.depth === 0 ? 16 : 13}" font-weight="${t.depth <= 1 ? 600 : 400}" fill="#1e293b" text-anchor="${t.depth === 0 ? 'middle' : 'start'}">${t.name}</text></g>`; t.children.forEach(drawNodes); }
            drawLines(tree); drawNodes(tree);
            const svgContent = `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${svgWidth}" height="${svgHeight}" viewBox="0 0 ${svgWidth} ${svgHeight}"><rect width="${svgWidth}" height="${svgHeight}" fill="#f8fafc"/>${linesSvg}${nodesSvg}</svg>`;
            const blob = new Blob([svgContent], { type: 'image/svg+xml;charset=utf-8' }); const url = URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url; a.download = `${data.root || 'mindmap'}.svg`; a.click(); URL.revokeObjectURL(url);
        }

        function expandMindmap(index) {
            const msg = sampleMessages.value[index]; if (!msg?.mindmapData) return;
            const win = window.open('', '_blank'); if (!win) return;
            const data = msg.mindmapData; const rootData = { name: data.root, children: data.children || [] };
            function countN(node) { let c = 1; if (node.children) node.children.forEach(ch => { c += countN(ch); }); return c; }
            function maxD(node, d) { d = d || 0; if (!node.children || node.children.length === 0) return d; return Math.max(...node.children.map(ch => maxD(ch, d + 1))); }
            const nodeHeight = 44, levelGap = 220; const totalNodes = countN(rootData), maxDepth = maxD(rootData);
            const svgWidth = Math.max(800, (maxDepth + 1) * levelGap + 200), svgHeight = Math.max(400, totalNodes * nodeHeight + 80);
            const colors = ['#165DFF', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];
            function buildTree(node, depth, startY) {
                const x = depth * levelGap + 100; const children = node.children || [];
                if (children.length === 0) return { x, cy: startY + nodeHeight / 2, name: node.name, depth, children: [], height: nodeHeight };
                let currentY = startY; const childNodes = [];
                children.forEach(child => { const r = buildTree(child, depth + 1, currentY); childNodes.push(r); currentY += r.height; });
                const cy = (childNodes[0].cy + childNodes[childNodes.length - 1].cy) / 2;
                return { x, cy, name: node.name, depth, children: childNodes, height: Math.max(nodeHeight, currentY - startY) };
            }
            const tree = buildTree(rootData, 0, 40); let linesSvg = '', nodesSvg = '';
            function drawLines(t) { t.children.forEach(child => { const mx = (t.x + child.x) / 2; linesSvg += `<path d="M${t.x + 8},${t.cy} C${mx},${t.cy} ${mx},${child.cy} ${child.x - 8},${child.cy}" fill="none" stroke="#94a3b8" stroke-width="1.5"/>`; drawLines(child); }); }
            function drawNodes(t) { const r = t.depth === 0 ? 10 : 6; const color = colors[t.depth % colors.length]; nodesSvg += `<g><circle cx="${t.x}" cy="${t.cy}" r="${r}" fill="${color}" stroke="#fff" stroke-width="2"/><text x="${t.x + (t.depth === 0 ? 0 : 16)}" y="${t.cy + 5}" font-size="${t.depth === 0 ? 16 : 13}" font-weight="${t.depth <= 1 ? 600 : 400}" fill="#1e293b" text-anchor="${t.depth === 0 ? 'middle' : 'start'}">${t.name}</text></g>`; t.children.forEach(drawNodes); }
            drawLines(tree); drawNodes(tree);
            const html = `<!DOCTYPE html><html><head><title>思维导图 - ${data.root}</title><style>body{margin:0;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#f8fafc;font-family:sans-serif;}svg{max-width:100%;height:auto;}</style></head><body><svg xmlns="http://www.w3.org/2000/svg" width="${svgWidth}" height="${svgHeight}" viewBox="0 0 ${svgWidth} ${svgHeight}"><rect width="${svgWidth}" height="${svgHeight}" fill="#f8fafc"/>${linesSvg}${nodesSvg}</svg></body></html>`;
            win.document.write(html); win.document.close();
        }

        function downloadReport(msg) { const blob = new Blob([msg.content], { type: 'text/plain;charset=utf-8' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `解析报告_${currentTopic.value}.txt`; a.click(); URL.revokeObjectURL(url); }
        function replayRecord(index) { const record = historyRecords.value[index]; if (record) { currentTopic.value = record.topic; activeTab.value = 0; } }
        function exportHistory() { const blob = new Blob([JSON.stringify(historyRecords.value, null, 2)], { type: 'application/json' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = '答疑历史记录.json'; a.click(); URL.revokeObjectURL(url); }
        function renderMarkdown(text) { if (!text) return ''; return text.replace(/^### (.*$)/gim, '<h3>$1</h3>').replace(/^## (.*$)/gim, '<h2>$1</h2>').replace(/^# (.*$)/gim, '<h1>$1</h1>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\*(.*?)\*/g, '<em>$1</em>').replace(/`(.*?)`/g, '<code>$1</code>').replace(/\n/g, '<br>'); }
        function scrollToBottom() { nextTick(() => { if (chatMessagesRef.value) chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight; }); }
        onBeforeUnmount(() => { mindmapInstances.forEach(svg => svg.remove()); mindmapInstances.clear(); });

        return {
            activeTab, inputText, currentTopic, outputPreference, difficultyLevel,
            activeResourceTab, digitalHumanStore, toggleDigitalHuman,
            tabs, resourceTabs, allResources, filteredResources, sampleMessages, historyRecords,
            generating, generatingType, chatMessagesRef, mindmapContainers,
            currentModelName, activeButton,
            sendMessage, handleButtonClick, renderMindmap,
            renderMarkdown, copyCode, downloadMindmap, expandMindmap,
            downloadReport, replayRecord, exportHistory
        };
    }
}
</script>

<style scoped lang="scss">
.scenic-background {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(to bottom, rgba(22, 93, 255, 0.85) 0%, rgba(64, 128, 255, 0.8) 40%, rgba(255, 255, 255, 0.85) 40%, rgba(255, 255, 255, 0.9) 100%);
    background-size: cover; background-position: center; background-attachment: fixed;
    z-index: -2; pointer-events: none;
}

.qa-assistant { padding: 24px; background-color: transparent; min-height: 100vh; }

/* 蓝色渐变标题栏 */
.page-banner {
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #0e7490 100%);
    border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;
    box-shadow: 0 4px 16px rgba(30, 58, 138, 0.25);
}
.banner-decoration { position: absolute; inset: 0; opacity: 0.1; z-index: 1; pointer-events: none; }
.deco-circle { position: absolute; border-radius: 50%; background: #fff; }
.deco-circle-1 { width: 128px; height: 128px; top: -16px; right: -16px; }
.deco-circle-2 { width: 96px; height: 96px; bottom: -16px; left: -16px; }
.banner-content { position: relative; z-index: 2; display: flex; align-items: center; justify-content: space-between; }
.banner-title { font-size: 1.5rem; font-weight: 700; color: #fff; margin: 0; font-family: 'SimSun', serif; text-shadow: 0 1px 3px rgba(0,0,0,0.15); }
.banner-subtitle { font-size: 0.875rem; color: #fff; margin: 0.25rem 0 0; opacity: 0.9; font-family: 'SimSun', serif; }
.banner-tag { font-size: 0.75rem; color: rgba(255,255,255,0.55); white-space: nowrap; }

/* Tab 标签栏 */
.tab-bar { display: flex; gap: 0; margin-bottom: 1.5rem; border-bottom: 2px solid #e5e7eb; }
.tab-item { padding: 0.75rem 1.5rem; font-size: 0.9375rem; font-weight: 500; color: #64748b; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px; transition: all 0.2s; }
.tab-item:hover { color: #165DFF; }
.tab-item.active { color: #165DFF; border-bottom-color: #165DFF; font-weight: 600; }

/* 主体双栏 */
.main-layout { display: flex; gap: 1.5rem; margin-bottom: 1.5rem; }
.chat-panel { flex: 0 0 70%; }
.config-panel { flex: 0 0 28%; }

/* 对话容器 */
.chat-container { background: #fff; border-radius: 8px; border: 1px solid #e5e7eb; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.chat-messages { height: 520px; overflow-y: auto; padding: 1.5rem; }
.empty-state { text-align: center; padding: 3rem 1rem; color: #86909C; }
.empty-icon { width: 80px; height: 80px; margin: 0 auto 1rem; color: #C9CDD4; }
.empty-text { font-size: 1.125rem; font-weight: 500; margin-bottom: 0.5rem; }
.empty-hint { font-size: 0.875rem; color: #86909C; }
.messages-list { display: flex; flex-direction: column; gap: 1.25rem; }
.message-row { display: flex; width: 100%; }
.message-row.ai { justify-content: flex-start; }
.message-row.user { justify-content: flex-end; }
.message-content-wrapper { display: flex; align-items: flex-end; gap: 0.75rem; max-width: 85%; }
.avatar { flex-shrink: 0; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.avatar svg { width: 24px; height: 24px; }
.ai-avatar { background: linear-gradient(135deg, #059669, #047857); color: white; }
.user-avatar { background: linear-gradient(135deg, #165DFF, #0E42D2); color: white; }
.message-bubble { padding: 1rem 1.25rem; border-radius: 18px; background: #F7F8FA; color: #1D2129; max-width: 100%; word-wrap: break-word; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.message-row.ai .message-bubble { border-bottom-left-radius: 4px; }
.user-bubble { background: linear-gradient(135deg, #165DFF, #4080FF); color: white; border-bottom-right-radius: 4px; }
.message-content { font-size: 0.9375rem; line-height: 1.6; margin-bottom: 0.5rem; }
.message-content:last-child { margin-bottom: 0; }
.message-time { font-size: 0.7rem; color: #86909C; text-align: right; margin-top: 0.25rem; display: block; }
.user-time { color: rgba(255,255,255,0.8); }

/* 多模态消息卡片 */
.multimodal-card { background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem; }
.multimodal-label { font-size: 0.75rem; font-weight: 600; color: #165DFF; margin-bottom: 0.5rem; }
.multimodal-btns { display: flex; gap: 0.5rem; margin-top: 0.5rem; }
.mindmap-container { min-height: 200px; max-height: 500px; background: #fff; border-radius: 6px; border: 1px dashed #e2e8f0; overflow: auto; margin-bottom: 0.5rem; }
.code-block { background: #1e293b; border-radius: 6px; padding: 0.75rem; margin-bottom: 0.5rem; overflow-x: auto; }
.code-block pre { margin: 0; font-family: 'Consolas', monospace; font-size: 0.8125rem; color: #e2e8f0; line-height: 1.5; }
.code-desc-text { font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem; }
.quiz-list { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 0.5rem; }
.quiz-item { font-size: 0.8125rem; color: #374151; padding: 0.5rem 0.75rem; background: #fff; border-radius: 6px; border: 1px solid #f1f5f9; }
.quiz-item-header { display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.375rem; }
.quiz-type-tag { padding: 0.125rem 0.5rem; border-radius: 4px; font-size: 0.6875rem; font-weight: 600; }
.tag-choice { background: rgba(22,93,255,0.1); color: #165DFF; }
.tag-judge { background: rgba(245,158,11,0.1); color: #f59e0b; }
.tag-fill { background: rgba(139,92,246,0.1); color: #8b5cf6; }
.tag-essay { background: rgba(16,185,129,0.1); color: #10b981; }
.quiz-qnum { font-size: 0.75rem; color: #94a3b8; }
.quiz-q-text { font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; }
.quiz-options { display: flex; flex-direction: column; gap: 0.25rem; }
.quiz-option { font-size: 0.8125rem; color: #475569; padding: 0.25rem 0; }
.quiz-answer-box { margin-top: 0.5rem; padding: 0.5rem; background: #f0fdf4; border-radius: 6px; font-size: 0.8125rem; }
.quiz-explanation { margin-top: 0.25rem; color: #64748b; }
.report-content { font-size: 0.875rem; line-height: 1.8; color: #1e293b; }
.report-content :deep(h1) { font-size: 1.25rem; margin: 1rem 0 0.5rem; }
.report-content :deep(h2) { font-size: 1.125rem; margin: 0.75rem 0 0.5rem; }
.report-content :deep(h3) { font-size: 1rem; margin: 0.5rem 0 0.25rem; }
.report-content :deep(code) { background: #f1f5f9; padding: 0.125rem 0.375rem; border-radius: 4px; font-size: 0.8125rem; }

/* 加载中 */
.loading-indicator { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; }
.loading-dots { display: flex; gap: 4px; }
.loading-dots span { width: 8px; height: 8px; border-radius: 50%; background: #165DFF; animation: bounce 1.4s infinite ease-in-out both; }
.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
.loading-text { font-size: 0.8125rem; color: #64748b; }

/* 侧边配置卡片 */
.sidebar-card { background: #fff; border-radius: 8px; border: 1px solid #e5e7eb; padding: 1.25rem; box-shadow: 0 1px 4px rgba(0,0,0,0.04); position: sticky; top: 24px; }
.sidebar-title { font-size: 1rem; font-weight: 700; color: #1e293b; margin: 0 0 1rem; }
.config-section { margin-bottom: 1.25rem; }
.config-label { display: block; font-size: 0.8125rem; font-weight: 600; color: #475569; margin-bottom: 0.5rem; }
.topic-input { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.875rem; outline: none; transition: border-color 0.2s; box-sizing: border-box; }
.topic-input:focus { border-color: #165DFF; box-shadow: 0 0 0 2px rgba(22,93,255,0.1); }
.radio-group { display: flex; flex-direction: column; gap: 0.375rem; }
.radio-label { display: inline-flex; align-items: center; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.8125rem; color: #475569; cursor: pointer; transition: all 0.2s; }
.radio-label:hover { border-color: #165DFF; color: #165DFF; }
.radio-label.active { background: #165DFF; color: #fff; border-color: #165DFF; }
.hidden-radio { display: none; }
.model-info { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0.75rem; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; margin-top: 0.75rem; }
.model-label { font-size: 0.75rem; color: #64748b; }
.model-name { font-size: 0.8125rem; font-weight: 600; color: #16a34a; }

/* 多模态操作栏 */
.multimodal-bar { margin-bottom: 0; }
.multimodal-actions { background: #fff; border-radius: 8px 8px 0 0; border: 1px solid #e5e7eb; border-bottom: none; padding: 1rem 1.25rem; display: flex; gap: 1rem; flex-wrap: wrap; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }

/* 底部输入栏 */
.input-bar { background: #fff; border-radius: 0 0 8px 8px; border: 1px solid #e5e7eb; border-top: none; padding: 1rem 1.25rem; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.input-wrapper { display: flex; align-items: center; gap: 0.5rem; background: #F7F8FA; border-radius: 9999px; padding: 0.375rem 0.75rem; border: 2px solid transparent; transition: all 0.3s; }
.input-wrapper:focus-within { background: white; border-color: #165DFF; box-shadow: 0 0 0 3px rgba(22,93,255,0.1); }
.mic-btn { width: 36px; height: 36px; border-radius: 50%; background: #f1f5f9; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #64748b; transition: all 0.2s; flex-shrink: 0; }
.mic-btn:hover { background: #e2e8f0; color: #165DFF; }
.mic-btn svg { width: 18px; height: 18px; }
.message-input { flex: 1; border: none; outline: none; font-size: 0.9375rem; background: transparent; color: #1D2129; min-width: 0; }
.message-input::placeholder { color: #86909C; }
.send-btn { width: 36px; height: 36px; border-radius: 50%; background: #165DFF; color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; flex-shrink: 0; }
.send-btn:hover { background: #0e4fd9; box-shadow: 0 4px 12px rgba(22,93,255,0.3); }
.send-btn svg { width: 18px; height: 18px; }
.digital-human-btn { width: 36px; height: 36px; border-radius: 50%; background: #165DFF; color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; flex-shrink: 0; }
.digital-human-btn:hover { background: #0e4fd9; }
.digital-human-btn.active { background: #10b981; box-shadow: 0 0 8px rgba(16,185,129,0.4); }
.digital-human-btn svg { width: 18px; height: 18px; }

/* 按钮 */
.btn { padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.8125rem; font-weight: 600; text-align: center; cursor: pointer; transition: all 0.3s; border: 1px solid transparent; white-space: nowrap; }
.btn-primary { background: #165DFF; color: #fff; border-color: #165DFF; box-shadow: 0 2px 8px rgba(22,93,255,0.3); }
.btn-primary:hover:not(:disabled) { background: #0e4fd9; box-shadow: 0 4px 12px rgba(22,93,255,0.4); }
.btn-outline { background: #fff; color: #165DFF; border-color: #165DFF; }
.btn-outline:hover:not(:disabled) { background: rgba(22,93,255,0.05); }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-sm { padding: 0.375rem 0.75rem; font-size: 0.75rem; }

/* 内容卡片 */
.content-card { background: #fff; border-radius: 8px; padding: 1.5rem; border: 1px solid #e5e7eb; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.card-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.card-title { font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0; }
.history-list { display: flex; flex-direction: column; gap: 0.75rem; }
.history-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; }
.history-item:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.history-item-info { display: flex; align-items: center; gap: 1rem; }
.history-summary { font-size: 0.875rem; color: #1e293b; font-weight: 500; }
.history-time { font-size: 0.75rem; color: #94a3b8; }
.tag { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.6875rem; font-weight: 600; }
.tag-mindmap { background: rgba(22,93,255,0.1); color: #165DFF; }
.tag-code { background: rgba(139,92,246,0.1); color: #8b5cf6; }
.tag-quiz { background: rgba(245,158,11,0.1); color: #f59e0b; }
.tag-report { background: rgba(16,185,129,0.1); color: #10b981; }
.resource-tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; }
.resource-tab { padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.75rem; cursor: pointer; background: #f1f5f9; color: #64748b; transition: all 0.2s; }
.resource-tab.active { background: #165DFF; color: #fff; }
.resource-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
.resource-item { display: flex; justify-content: space-between; align-items: center; padding: 1rem; border: 1px solid #e2e8f0; border-radius: 8px; }
.resource-item:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.resource-item-body { flex: 1; }
.resource-item-title { display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.25rem; }
.resource-item-desc { font-size: 0.75rem; color: #94a3b8; }
.resource-tag { display: inline-block; padding: 0.125rem 0.5rem; border-radius: 4px; font-size: 0.6875rem; font-weight: 600; margin-top: 0.375rem; }
.tag-primary { background: rgba(22,93,255,0.1); color: #165DFF; }
.tag-warning { background: rgba(245,158,11,0.1); color: #f59e0b; }
.tag-danger { background: rgba(239,68,68,0.1); color: #ef4444; }
.tag-info { background: rgba(100,116,139,0.1); color: #64748b; }
.tag-success { background: rgba(16,185,129,0.1); color: #10b981; }

@media (max-width: 1024px) {
    .main-layout { flex-direction: column; }
    .chat-panel, .config-panel { flex: 1 1 auto; }
}
</style>
