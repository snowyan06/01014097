<template>
    <div class="teacher-dashboard">
        <GeometricBackground />
        <!-- 上蓝下白背景层 -->
        <div class="scenic-background"></div>
        <!-- 顶部导航栏 - 深蓝色系 -->
        <div class="relative overflow-hidden bg-gradient-to-r from-blue-800 via-blue-900 to-cyan-900 shadow-lg px-6 py-4 mb-6 rounded-xl">
            <!-- 装饰性气泡元素 -->
            <div class="bubble bubble-1"></div>
            <div class="bubble bubble-2"></div>
            <div class="bubble bubble-3"></div>

            <div class="relative flex align-items-center justify-content-between z-20">
                <!-- 左侧标题区域 -->
                <div class="flex align-items-center gap-3">
                    <div>
                        <h2 class="text-2xl font-bold text-white m-0 drop-shadow-sm" style="font-family: 'SimSun', 'STSong', 'Adobe Song Std', serif;">学习资源中心</h2>
                        <p class="text-white text-sm m-0" style="font-family: 'SimSun', 'STSong', 'Adobe Song Std', serif;">Learning Resource Center</p>
                    </div>
                </div>
            </div>
        </div>

      <!-- 主要功能区域 -->
        <div class="grid">
            <div class="col-12">
                <div class="card mb-4">
                    <div class="flex align-items-center justify-content-between mb-3">
                        <h3 class="text-xl font-semibold m-0">学习资源</h3>
                    </div>

                    <TabView v-model:activeIndex="activeTab">
                        <!-- Tab 1: 练习测评 -->
                        <TabPanel header="练习测评">
                            <div style="display: flex; flex-direction: column; gap: 1rem;">
                                <!-- 第一行：题目生成配置 + 练习历史 -->
                                <div style="display: grid; grid-template-columns: 75% 25%; gap: 1rem;">
                                    <!-- 左侧：题目生成配置 -->
                                    <div>
                                        <div class="card">
                                            <h4 class="text-lg font-semibold mb-3">测评题目配置</h4>

                                            <!-- 第一行：题目来源、题目数量、难度等级 -->
                                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
                                                <div>
                                                    <label class="block text-sm font-medium mb-2">题目来源</label>
                                                    <SelectButton v-model="questionSource" :options="questionSourceOptions" optionLabel="label" optionValue="value" style="width: 100%" />
                                                </div>
                                                <div>
                                                    <label class="block text-sm font-medium mb-2">题目数量</label>
                                                    <InputNumber v-model="questionCount" :min="1" :max="20" style="width: 100%" />
                                                </div>
                                                <div>
                                                    <label class="block text-sm font-medium mb-2">难度等级</label>
                                                    <SelectButton v-model="selectedDifficulty" :options="difficultyOptions" optionLabel="label" optionValue="value" style="width: 100%" />
                                                </div>
                                            </div>

                                            <!-- 第二行：题目分类、题型 -->
                                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; padding-bottom: 17rem; margin-bottom: 1rem;">
                                                <div>
                                                    <label class="block text-sm font-medium mb-2">题目分类</label>
                                                    <Dropdown
                                                        v-model="selectedQuestionCategory"
                                                        :options="questionCategoryOptions"
                                                        optionLabel="label"
                                                        optionValue="value"
                                                        placeholder="选择分类"
                                                        style="width: 100%"
                                                    />
                                                </div>
                                                <div>
                                                    <label class="block text-sm font-medium mb-2">
                                                        <i class="pi pi-file-text mr-2"></i>
                                                        题型
                                                    </label>
                                                    <Dropdown
                                                        v-model="selectedQuestionType"
                                                        :options="questionTypeOptions"
                                                        optionLabel="label"
                                                        optionValue="value"
                                                        placeholder="选择题型"
                                                        style="width: 100%"
                                                    />
                                                </div>
                                            </div>

                                            <!-- 知识点方向、知识点领域 -->
                                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; ">
                                                <div>
                                                    <label class="block text-sm font-medium mb-2">知识点方向</label>
                                                    <Dropdown
                                                        v-model="topicCategoryFilter"
                                                        :options="topicCategoryOptions"
                                                        optionLabel="label"
                                                        optionValue="value"
                                                        placeholder="选择方向"
                                                        style="width: 100%"
                                                    />
                                                </div>
                                                <div>
                                                    <label class="block text-sm font-medium mb-2">知识点领域</label>
                                                    <MultiSelect
                                                        v-model="selectedTopics"
                                                        :options="filteredTopics"
                                                        optionLabel="name"
                                                        optionValue="id"
                                                        placeholder="选择知识点"
                                                        style="width: 100%"
                                                        display="chip"
                                                        :filter="true"
                                                        filter-placeholder="搜索知识点..."
                                                        :max-selected-labels="5"
                                                    >
                                                        <template #option="slotProps">
                                                            <div class="flex align-items-center gap-2">
                                                                <span>{{ slotProps.option.name }}</span>
                                                            </div>
                                                        </template>
                                                        <template #chip="slotProps">
                                                            <div class="p-chip p-component p-chip-rounded">
                                                                <span class="p-chip-text">{{ getTopicNameById(slotProps.value) }}</span>
                                                            </div>
                                                        </template>
                                                    </MultiSelect>
                                                </div>
                                            </div>

                                            <!-- 生成按钮 -->
                                            <div style="margin-top: 17rem;">
                                                <Button label="生成题目" icon="pi pi-plus" severity="primary" style="width: 100%; background: linear-gradient(135deg, #165DFF 0%, #4080FF 100%); border-color: #165DFF;" :loading="isGenerating" @click="generateQuestions" />
                                            </div>
                                        </div>
                                    </div>

                                    <!-- 右侧：练习历史 -->
                                     <div>
                                         <div class="card h-full" style="height: 100%;">
                                             <div class="flex align-items-center justify-content-between mb-4">
                                                 <h4 class="text-xl font-bold m-0" style="color: #1D2129;">练习历史</h4>
                                                 <Button
                                                     v-if="practiceHistory.length > 0"
                                                     icon="pi pi-trash"
                                                     severity="danger"
                                                     text
                                                     rounded
                                                     size="small"
                                                     @click="clearPracticeHistory"
                                                     v-tooltip="'清除历史'"
                                                 />
                                             </div>

                                            <div class="flex flex-column gap-3 overflow-y-auto" style="max-height: 350px;">
                                                <div
                                                    v-for="record in practiceHistory"
                                                    :key="record.id"
                                                    class="history-record-item"
                                                    @click="viewHistoryDetail(record)"
                                                >
                                                    <div class="flex justify-content-between align-items-start mb-2">
                                                        <div class="font-semibold text-sm line-clamp-1" style="color: #1D2129;">{{ record.title }}</div>
                                                        <Badge :value="record.score" :severity="getScoreSeverity(record.score)" class="px-2 py-1 rounded-full text-xs font-medium flex-shrink-0" />
                                                    </div>
                                                    <div class="text-xs" style="color: #86909C;">{{ record.date }}</div>
                                                </div>
                                                <div v-if="practiceHistory.length === 0" class="text-center py-8" style="color: #86909C;">
                                                    <i class="pi pi-history text-2xl mb-2"></i>
                                                    <p class="text-sm">暂无练习记录</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- 第二行：练习题目区域（居中显示） -->
                                <div style="display: flex; justify-content: center;">
                                    <div style="width: 83.333%; padding: 0 1rem;">
                                        <div class="card">
                                            <div class="flex align-items-center justify-content-between mb-4">
                                                <h4 class="text-lg font-semibold m-0">练习题目</h4>
                                                <div v-if="currentQuestions.length > 0" class="flex align-items-center gap-2">
                                                    <span class="text-sm text-600"> {{ currentQuestionIndex + 1 }} / {{ currentQuestions.length }} </span>
                                                    <Button icon="pi pi-refresh" text rounded size="small" @click="resetPractice" v-tooltip="'重新开始'" />
                                                </div>
                                            </div>

                                            <!-- 题目展示区域 -->
                                            <div v-if="currentQuestions.length === 0" class="text-center py-8">
                                                <i class="pi pi-book text-4xl mb-3" style="color: #C9CDD4;"></i>
                                                <p style="color: #86909C;">请先配置并生成题目</p>
                                            </div>

                                            <div v-else class="question-container">
                                                <div class="question-header mb-4">
                                                    <Tag :value="getQuestionTypeLabel(currentQuestion.type)" :severity="getQuestionTypeSeverity(currentQuestion.type)" class="mr-2" />
                                                    <Tag :value="currentQuestion.difficulty" severity="info" class="mr-2" />
                                                    <span class="font-semibold">{{ currentQuestion.title }}</span>
                                                </div>

                                                <div class="question-content mb-4">
                                                    <p class="text-lg mb-3">{{ currentQuestion.content }}</p>
                                                </div>

                                                <!-- 答题区域 -->
                                                <div class="answer-section">
                                                    <!-- 单选题 -->
                                                    <div v-if="currentQuestion.type === 'choice'" class="choice-answers">
                                                        <div class="flex flex-wrap gap-2">
                                                            <Button
                                                                v-for="(option, index) in currentQuestion.options"
                                                                :key="index"
                                                                :label="`${option.key}. ${option.text}`"
                                                                :class="{
                                                                    'p-button-outlined': currentAnswer !== option.key,
                                                                    'p-button-primary': currentAnswer === option.key
                                                                }"
                                                                @click="currentAnswer = option.key"
                                                                :disabled="isAnswerSubmitted"
                                                                class="flex-1 min-w-12rem"
                                                            />
                                                        </div>
                                                    </div>

                                                    <!-- 判断题 -->
                                                    <div v-if="currentQuestion.type === 'judge'" class="judge-answers">
                                                        <div class="flex gap-4">
                                                            <div class="field-radiobutton">
                                                                <RadioButton id="judge-true" v-model="currentAnswer" value="true" :disabled="isAnswerSubmitted" />
                                                                <label for="judge-true" class="ml-2 cursor-pointer">正确</label>
                                                            </div>
                                                            <div class="field-radiobutton">
                                                                <RadioButton id="judge-false" v-model="currentAnswer" value="false" :disabled="isAnswerSubmitted" />
                                                                <label for="judge-false" class="ml-2 cursor-pointer">错误</label>
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <!-- 填空题 -->
                                                    <div v-if="currentQuestion.type === 'fill'" class="fill-answers">
                                                        <div class="flex flex-column gap-3">
                                                            <InputText
                                                                v-for="(blank, index) in currentQuestion.blanks"
                                                                :key="index"
                                                                v-model="currentAnswer[index]"
                                                                :placeholder="`请输入第 ${index + 1} 个空的答案`"
                                                                :disabled="isAnswerSubmitted"
                                                                class="w-full"
                                                            />
                                                        </div>
                                                    </div>

                                                    <!-- 简答题 -->
                                                    <div v-if="currentQuestion.type === 'essay'" class="essay-answers">
                                                        <Textarea
                                                            v-model="currentAnswer"
                                                            placeholder="请输入你的答案..."
                                                            :disabled="isAnswerSubmitted"
                                                            rows="5"
                                                            class="w-full"
                                                        />
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- 操作按钮 -->
                                            <div v-if="currentQuestions.length > 0" class="flex justify-content-between mt-4">
                                                <Button label="上一题" icon="pi pi-arrow-left" outlined :disabled="currentQuestionIndex === 0" @click="previousQuestion" />
                                                <div class="flex gap-2">
                                                    <Button v-if="!isAnswerSubmitted" label="提交答案" icon="pi pi-check" :disabled="!hasUserAnswer" :loading="isGrading" @click="submitAnswer" />
                                                    <Button v-if="currentQuestionIndex < currentQuestions.length - 1" label="下一题" icon="pi pi-arrow-right" @click="nextQuestion" />
                                                    <Button v-if="currentQuestionIndex === currentQuestions.length - 1 && isAnswerSubmitted" label="完成练习" icon="pi pi-flag" severity="success" @click="finishPractice" />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- 练习历史详情弹窗 -->
                            <PracticeHistoryDetailModal
                                v-model:visible="showHistoryModal"
                                :record="selectedHistoryRecord"
                                :questions="historyQuestions"
                            />
                        </TabPanel>

                        <!-- Tab 2: 知识网络 -->
                        <TabPanel header="知识网络">
                            <StudentKnowledgeGraph v-if="activeTab === 1" />
                        </TabPanel>

                        <!-- Tab 3: 题目库 -->
                        <TabPanel header="题目库">
                            <div class="card">
                                <div class="flex align-items-center justify-content-between mb-4">
                                    <h4 class="text-lg font-semibold m-0">题目库</h4>
                                    <Button icon="pi pi-refresh" label="刷新" @click="loadAllQuestions" :loading="isLoadingQuestions" />
                                </div>

                                <DataTable :value="allQuestions" :loading="isLoadingQuestions" paginator :rows="10" :rowsPerPageOptions="[5, 10, 20]" stripedRows responsiveLayout="scroll" v-if="allQuestions.length > 0">
                                    <Column field="id" header="ID" :sortable="true" style="min-width: 80px"></Column>
                                    <Column field="questionId" header="题目编号" :sortable="true" style="min-width: 120px"></Column>
                                    <Column field="type" header="分类" :sortable="true" style="min-width: 100px">
                                        <template #body="slotProps">
                                            <Tag :value="slotProps.data.type" :severity="getQuestionTypeSeverityForTable(slotProps.data.type)" />
                                        </template>
                                    </Column>
                                    <Column field="questionType" header="题型" :sortable="true" style="min-width: 80px">
                                        <template #body="slotProps">
                                            <Badge :value="slotProps.data.questionType" :severity="getQuestionTypeSeverityForTable(slotProps.data.questionType)" />
                                        </template>
                                    </Column>
                                    <Column field="content" header="题目内容" style="min-width: 300px">
                                        <template #body="slotProps">
                                            <div class="question-content-cell">{{ slotProps.data.content }}</div>
                                        </template>
                                    </Column>
                                    <Column field="answer" header="答案" style="min-width: 150px">
                                        <template #body="slotProps">
                                            <span class="answer-cell">{{ slotProps.data.answer }}</span>
                                        </template>
                                    </Column>
                                    <Column field="difficulty" header="难度" :sortable="true" style="min-width: 100px">
                                        <template #body="slotProps">
                                            <Badge :value="slotProps.data.difficulty" :severity="getDifficultySeverityForTable(slotProps.data.difficulty)" />
                                        </template>
                                    </Column>
                                    <Column field="knowledgePoint" header="知识点" style="min-width: 120px">
                                        <template #body="slotProps">
                                            <span class="text-sm" style="color: #4E5969;">{{ slotProps.data.knowledgePoint }}</span>
                                        </template>
                                    </Column>
                                    <Column header="操作" style="min-width: 100px">
                                        <template #body="slotProps">
                                            <div class="add-to-practice-btn" @click="addToPractice(slotProps.data)" v-tooltip="'添加到练习'">
                                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                                    <path d="M12 5v14M5 12h14" stroke-linecap="round" stroke-linejoin="round"/>
                                                </svg>
                                            </div>
                                        </template>
                                    </Column>
                                </DataTable>

                                <div v-else class="text-center py-8">
                                    <i class="pi pi-inbox text-4xl mb-3" style="color: #C9CDD4;"></i>
                                    <p style="color: #86909C;">暂无题目，请点击刷新加载</p>
                                </div>
                            </div>
                        </TabPanel>
                    </TabView>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import GeometricBackground from '@/components/GeometricBackground.vue';
import PracticeHistoryDetailModal from '@/components/PracticeHistoryDetailModal.vue';
import StudentKnowledgeGraph from '@/components/StudentKnowledgeGraph.vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api';
const router = useRouter();

// ========== 练习测评相关 ==========
const activeTab = ref(0);

const loadPracticeHistory = async () => {
    try {
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth'));
        const userId = authData?.id;
        if (!userId) { console.error('未获取到用户 ID，请重新登录'); return; }
        const res = await axios.get(`${API_BASE_URL}/practice-sessions/by-user/${userId}`);
        practiceHistory.value = res.data.map((item) => ({
            id: item.id,
            title: item.title,
            score: `${item.score}分`,
            date: item.createdAt.split('T')[0],
            sessionId: item.sessionId
        }));
    } catch (error) { console.error('加载练习历史失败:', error); }
};

const clearPracticeHistory = async () => {
    if (!confirm('确定要清除所有练习历史记录吗？此操作不可恢复！')) return;
    try {
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth'));
        const userId = authData?.id;
        if (!userId) { alert('未获取到用户 ID，请重新登录'); return; }
        const res = await axios.get(`${API_BASE_URL}/practice-sessions/by-user/${userId}`);
        for (const session of res.data) { await axios.delete(`${API_BASE_URL}/practice-sessions/${session.id}`); }
        await loadPracticeHistory();
        alert('练习历史已清除！');
    } catch (error) { console.error('清除练习历史失败:', error); alert('清除失败，请重试'); }
};

onMounted(async () => {
    loadPracticeHistory();
    questionSource.value = 'AI生成';
    selectedQuestionType.value = 'all';
    selectedQuestionCategory.value = 'all';
    selectedDifficulty.value = '中等';
    questionCount.value = 5;
    await loadQuestionsFromDatabase(false);
    loadAllQuestions();
});

const questionSourceOptions = ref([
    { label: '智能生成', value: 'AI生成' },
    { label: '企业面试真题', value: '企业面试真题' }
]);
const questionSource = ref('企业面试真题');

const questionTypeOptions = ref([
    { label: '全部题型', value: 'all' },
    { label: '单选题', value: '单选题' },
    { label: '判断题', value: '判断题' },
    { label: '填空题', value: '填空题' },
    { label: '简答题', value: '简答题' }
]);

const questionCategoryOptions = ref([
    { label: '全部分类', value: 'all' },
    { label: '技术知识', value: '技术知识' },
    { label: '项目经历深挖', value: '项目经历深挖' },
    { label: '场景题', value: '场景题' },
    { label: '行为题', value: '行为题' }
]);

const topicCategoryOptions = ref([
    { label: '全部方向', value: 'all' },
    { label: '前端开发', value: 'frontend' },
    { label: '后端开发', value: 'backend' },
    { label: '全栈开发', value: 'fullstack' },
    { label: '数据分析', value: 'data' },
    { label: '人工智能', value: 'ai' },
    { label: '产品经理', value: 'product' },
    { label: '通用技能', value: 'common' }
]);

const selectedQuestionType = ref('all');
const selectedQuestionCategory = ref('all');
const questionCount = ref(5);
const selectedDifficulty = ref('medium');
const selectedTopics = ref([]);
const isGenerating = ref(false);
const isGrading = ref(false);
const difficultyOptions = ref([
    { label: '简单', value: '简单' },
    { label: '中等', value: '中等' },
    { label: '困难', value: '困难' }
]);

const availableTopics = ref([
    { id: 1, name: '机器学习基础', category: 'ai', icon: 'pi pi-brain' },
    { id: 2, name: '深度学习理论', category: 'ai', icon: 'pi pi-network' },
    { id: 3, name: '神经网络基础', category: 'ai', icon: 'pi pi-sitemap' },
    { id: 4, name: '卷积神经网络 (CNN)', category: 'ai', icon: 'pi pi-eye' },
    { id: 5, name: '循环神经网络 (RNN)', category: 'ai', icon: 'pi pi-refresh' },
    { id: 6, name: 'Transformer架构', category: 'ai', icon: 'pi pi-lightbulb' },
    { id: 7, name: '注意力机制', category: 'ai', icon: 'pi pi-search' },
    { id: 8, name: '自然语言处理 (NLP)', category: 'ai', icon: 'pi pi-comments' },
    { id: 9, name: '计算机视觉 (CV)', category: 'ai', icon: 'pi pi-eye' },
    { id: 10, name: '大语言模型 (LLM)', category: 'ai', icon: 'pi pi-globe' },
    { id: 11, name: '生成式AI (AIGC)', category: 'ai', icon: 'pi pi-star' },
    { id: 12, name: '预训练模型', category: 'ai', icon: 'pi pi-box' },
    { id: 13, name: '迁移学习', category: 'ai', icon: 'pi pi-share-alt' },
    { id: 14, name: '强化学习', category: 'ai', icon: 'pi pi-trophy' },
    { id: 15, name: '词嵌入技术', category: 'ai', icon: 'pi pi-tag' },
    { id: 16, name: 'PyTorch/TensorFlow', category: 'ai', icon: 'pi pi-microchip' },
    { id: 17, name: '模型训练与优化', category: 'ai', icon: 'pi pi-cog' },
    { id: 18, name: '损失函数', category: 'ai', icon: 'pi pi-chart-line' },
    { id: 19, name: '梯度下降', category: 'ai', icon: 'pi pi-arrow-down' },
    { id: 20, name: '正则化技术', category: 'ai', icon: 'pi pi-shield' },
    { id: 21, name: '模型评估', category: 'ai', icon: 'pi pi-check-circle' },
    { id: 22, name: '模型部署与优化', category: 'ai', icon: 'pi pi-rocket' },
    { id: 23, name: '数据预处理', category: 'ai', icon: 'pi pi-filter' },
    { id: 24, name: '特征工程', category: 'ai', icon: 'pi pi-sliders-h' },
    { id: 25, name: 'HTML/CSS 基础', category: 'frontend', icon: 'pi pi-code' },
    { id: 26, name: 'JavaScript 核心', category: 'frontend', icon: 'pi pi-bolt' },
    { id: 27, name: 'ES6+ 新特性', category: 'frontend', icon: 'pi pi-star' },
    { id: 28, name: 'Vue.js 框架', category: 'frontend', icon: 'pi pi-thumbs-up' },
    { id: 29, name: 'React 框架', category: 'frontend', icon: 'pi pi-bookmark' },
    { id: 30, name: '响应式布局', category: 'frontend', icon: 'pi pi-desktop' },
    { id: 31, name: 'Webpack/Vite', category: 'frontend', icon: 'pi pi-cog' },
    { id: 32, name: 'TypeScript', category: 'frontend', icon: 'pi pi-shield' },
    { id: 33, name: 'Java 编程基础', category: 'backend', icon: 'pi pi-coffee' },
    { id: 34, name: 'Python 编程', category: 'backend', icon: 'pi pi-palette' },
    { id: 35, name: 'Spring Boot 框架', category: 'backend', icon: 'pi pi-sitemap' },
    { id: 36, name: 'MySQL 数据库', category: 'backend', icon: 'pi pi-database' },
    { id: 37, name: 'Redis 缓存技术', category: 'backend', icon: 'pi pi-flash' },
    { id: 38, name: '微服务架构', category: 'backend', icon: 'pi pi-cloud' },
    { id: 39, name: 'RESTful API 设计', category: 'backend', icon: 'pi pi-link' },
    { id: 40, name: '消息队列 (MQ)', category: 'backend', icon: 'pi pi-envelope' },
    { id: 41, name: 'Node.js 开发', category: 'fullstack', icon: 'pi pi-server' },
    { id: 42, name: 'MongoDB NoSQL', category: 'fullstack', icon: 'pi pi-folder' },
    { id: 43, name: 'Docker 容器化', category: 'fullstack', icon: 'pi pi-box' },
    { id: 44, name: 'CI/CD 流程', category: 'fullstack', icon: 'pi pi-refresh' },
    { id: 45, name: 'Linux 系统管理', category: 'fullstack', icon: 'pi pi-cog' },
    { id: 46, name: 'Git 版本控制', category: 'fullstack', icon: 'pi pi-code-branch' },
    { id: 47, name: 'Python/R 语言', category: 'data', icon: 'pi pi-chart-line' },
    { id: 48, name: 'SQL 高级查询', category: 'data', icon: 'pi pi-search' },
    { id: 49, name: '统计学原理', category: 'data', icon: 'pi pi-calculator' },
    { id: 50, name: '数据可视化', category: 'data', icon: 'pi pi-chart-bar' },
    { id: 51, name: 'Tableau/Echarts', category: 'data', icon: 'pi pi-chart-pie' },
    { id: 52, name: 'Pandas/NumPy', category: 'data', icon: 'pi pi-table' },
    { id: 53, name: '产品设计方法论', category: 'product', icon: 'pi pi-lightbulb' },
    { id: 54, name: '需求分析与规划', category: 'product', icon: 'pi pi-list' },
    { id: 55, name: '原型设计工具', category: 'product', icon: 'pi pi-paint-brush' },
    { id: 56, name: '用户体验 (UX)', category: 'product', icon: 'pi pi-smile' },
    { id: 57, name: '敏捷开发流程', category: 'product', icon: 'pi pi-sync' },
    { id: 58, name: '数据分析与决策', category: 'product', icon: 'pi pi-chart-line' },
    { id: 59, name: '数据结构与算法', category: 'common', icon: 'pi pi-sitemap' },
    { id: 60, name: '操作系统原理', category: 'common', icon: 'pi pi-hdd' },
    { id: 61, name: '计算机网络', category: 'common', icon: 'pi pi-globe' },
    { id: 62, name: '常用设计模式', category: 'common', icon: 'pi pi-sitemap' },
    { id: 63, name: '系统设计能力', category: 'common', icon: 'pi pi-sitemap' },
    { id: 64, name: '沟通表达能力', category: 'common', icon: 'pi pi-comments' },
    { id: 65, name: '项目管理基础', category: 'common', icon: 'pi pi-briefcase' }
]);

const topicCategoryFilter = ref('all');
const filteredTopics = computed(() => {
    if (topicCategoryFilter.value === 'all') return availableTopics.value;
    return availableTopics.value.filter(topic => topic.category === topicCategoryFilter.value);
});
const getTopicNameById = (id) => {
    const topic = availableTopics.value.find(t => t.id === id);
    return topic ? topic.name : '';
};

const currentQuestions = ref([]);
const currentQuestionIndex = ref(0);
const userAnswers = ref({});
const currentAnswer = ref('');
const questionFeedbacks = ref({});
const practiceHistory = ref([]);
const allQuestions = ref([]);
const isLoadingQuestions = ref(false);

const currentQuestion = computed(() => currentQuestions.value[currentQuestionIndex.value] || null);

watch(currentQuestion, (newQ) => {
    if (newQ) {
        if (!userAnswers.value[newQ.id]) {
            userAnswers.value[newQ.id] = newQ.type === 'fill' ? new Array(newQ.blanks.length).fill('') : '';
        }
        currentAnswer.value = userAnswers.value[newQ.id];
    }
}, { immediate: true });

watch(currentAnswer, (newVal) => {
    if (currentQuestion.value) userAnswers.value[currentQuestion.value.id] = newVal;
});

const isAnswerSubmitted = computed(() => currentQuestion.value ? !!questionFeedbacks.value[currentQuestion.value.id] : false);
const hasUserAnswer = computed(() => {
    if (!currentQuestion.value) return false;
    const answer = userAnswers.value[currentQuestion.value.id];
    if (currentQuestion.value.type === 'fill') return answer && answer.some((a) => a && a.trim());
    return answer && answer.toString().trim();
});

const loadQuestionsFromDatabase = async (showAlerts = false) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/questions`);
        let questions = response.data;
        if (questionSource.value && questionSource.value !== 'all') questions = questions.filter(q => q.source === questionSource.value);
        if (selectedTopics.value && selectedTopics.value.length > 0) {
            const names = selectedTopics.value.map(id => { const t = availableTopics.value.find(tp => tp.id === id); return t ? t.name : null; }).filter(n => n);
            questions = questions.filter(q => { const dbPoint = (q.knowledge_point || '').trim(); return names.some(name => name.includes(dbPoint) || dbPoint.includes(name)); });
        }
        if (selectedQuestionCategory.value !== 'all') questions = questions.filter(q => q.type === selectedQuestionCategory.value);
        if (selectedQuestionType.value !== 'all') questions = questions.filter(q => q.questionType === selectedQuestionType.value);
        if (selectedDifficulty.value && selectedDifficulty.value !== 'all') questions = questions.filter(q => q.difficulty === selectedDifficulty.value);
        if (questions.length === 0) { if (showAlerts) alert('未找到符合条件的题目，请调整筛选条件'); return; }
        const shuffled = questions.sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, Math.min(questionCount.value, questions.length));
        const parsedQuestions = selected.map(q => {
            let type = 'choice';
            if (q.questionType === '单选题') type = 'choice';
            else if (q.questionType === '判断题') type = 'judge';
            else if (q.questionType === '填空题') type = 'fill';
            else if (q.questionType === '简答题') type = 'essay';
            let options = [];
            if (type === 'choice') {
                const matchA = q.content.match(/A\.\s*([^A-D]+)[\n|]?B\.\s*([^A-D]+)[\n|]?C\.\s*([^A-D]+)[\n|]?D\.\s*([^A-D]+)/);
                if (matchA) { options = [{ key: 'A', text: matchA[1].trim() }, { key: 'B', text: matchA[2].trim() }, { key: 'C', text: matchA[3].trim() }, { key: 'D', text: matchA[4].trim() }]; }
                else {
                    const lines = q.content.split('\n').filter(l => l.trim());
                    const optLines = lines.filter(l => /^[A-D][\.\、]/.test(l.trim()));
                    if (optLines.length === 4) { options = optLines.map(line => { const m = line.trim().match(/^([A-D])[\.\、]\s*(.+)/); return m ? { key: m[1], text: m[2].trim() } : null; }).filter(o => o !== null); }
                }
            }
            let blanks = [];
            if (type === 'fill') { const matches = q.content.match(/_{2,}|——+/g); blanks = matches ? matches.map(m => m.length) : [1]; }
            return { id: q.questionId || q.id, type, content: q.content, options, correctAnswer: q.answer, explanation: q.explanation || '暂无解析', difficulty: q.difficulty, topic: q.knowledgePoint || '通用', blanks };
        });
        currentQuestions.value = parsedQuestions;
        currentQuestionIndex.value = 0;
        userAnswers.value = {};
        questionFeedbacks.value = {};
        currentQuestions.value.forEach(q => { if (q.type === 'fill') userAnswers.value[q.id] = new Array(q.blanks.length).fill(''); });
        if (showAlerts) alert('成功生成 ' + currentQuestions.value.length + ' 道题目！');
    } catch (error) { console.error('加载题目失败:', error); if (showAlerts) alert('加载题目失败，请检查后端服务是否正常运行'); }
};

const generateQuestions = async () => { isGenerating.value = true; try { await loadQuestionsFromDatabase(true); } finally { isGenerating.value = false; } };

const submitAnswer = async () => {
    if (!currentQuestion.value || !hasUserAnswer.value) return;
    isGrading.value = true;
    try {
        await new Promise(resolve => setTimeout(resolve, 500));
        if (currentQuestion.value) userAnswers.value[currentQuestion.value.id] = currentAnswer.value;
        const question = currentQuestion.value;
        const userAnswer = currentAnswer.value;
        let isCorrect = false, correctAnswer = question.correctAnswer, explanation = question.explanation || '暂无解析';
        if (question.type === 'choice' || question.type === 'judge') { isCorrect = userAnswer === correctAnswer; }
        else if (question.type === 'fill') { const answers = userAnswer.filter(a => a && a.trim()); const ca = correctAnswer.split('|'); isCorrect = answers.length === ca.length && answers.every((a, i) => a.trim().toLowerCase() === ca[i].trim().toLowerCase()); }
        else if (question.type === 'essay') { isCorrect = null; correctAnswer = '待人工评分'; explanation = '简答题需要根据评分标准进行人工评阅'; }
        questionFeedbacks.value[question.id] = { isCorrect, correctAnswer, explanation };
    } catch (error) { console.error('评分失败:', error); } finally { isGrading.value = false; }
};

const nextQuestion = () => { if (currentQuestionIndex.value < currentQuestions.value.length - 1) currentQuestionIndex.value++; };
const previousQuestion = () => { if (currentQuestionIndex.value > 0) currentQuestionIndex.value--; };
const resetPractice = () => { currentQuestionIndex.value = 0; userAnswers.value = {}; questionFeedbacks.value = {}; };

const finishPractice = async () => {
    const answeredCount = Object.keys(userAnswers.value).length;
    const correctCount = Object.values(questionFeedbacks.value).filter(f => f && f.isCorrect).length;
    const score = Math.round((correctCount / answeredCount) * 100) || 0;
    try {
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth'));
        const userId = authData?.id;
        if (!userId) { alert('未获取到用户 ID，请重新登录'); return; }
        const title = `${currentQuestions.value.length > 0 ? getQuestionTypeLabel(currentQuestions.value[0].type) : '练习'}练习`;
        const sessionId = 'session_' + Date.now();
        await axios.post(`${API_BASE_URL}/practice-sessions`, { userId: parseInt(userId), title, score, totalQuestions: currentQuestions.value.length, correctCount, sessionId });
        for (const question of currentQuestions.value) {
            const ua = userAnswers.value[question.id]; const feedback = questionFeedbacks.value[question.id];
            let answerText = Array.isArray(ua) ? ua.join(',') : typeof ua === 'string' ? ua : typeof ua === 'boolean' ? (ua ? '正确' : '错误') : '';
            await axios.post(`${API_BASE_URL}/user-answers`, { questionType: getQuestionTypeLabel(question.type), questionContent: question.content, difficulty: question.difficulty, userAnswer: answerText, correctAnswer: question.correctAnswer, explanation: question.explanation, isCorrect: feedback ? feedback.isCorrect : false, sessionId, userId: parseInt(userId) });
        }
        alert(`练习完成！\n答题数：${answeredCount}\n正确数：${correctCount}\n得分：${score}分`);
        await loadPracticeHistory(); resetPractice();
    } catch (error) { console.error('保存练习记录失败:', error); alert(`练习完成！得分：${score}分（保存历史记录失败）`); resetPractice(); }
};

const getQuestionTypeLabel = (type) => ({ 'choice': '单选题', 'judge': '判断题', 'fill': '填空题', 'essay': '简答题' }[type] || type);
const getQuestionTypeSeverity = (type) => ({ 'choice': 'primary', 'judge': 'success', 'fill': 'warning', 'essay': 'info' }[type] || 'info');
const getQuestionTypeSeverityForTable = (type) => getQuestionTypeSeverity(type === '单选题' ? 'choice' : type === '判断题' ? 'judge' : type === '填空题' ? 'fill' : 'essay');
const getDifficultySeverityForTable = (difficulty) => ({ '简单': 'success', '中等': 'warning', '困难': 'danger' }[difficulty] || 'info');
const getScoreSeverity = (score) => { const n = parseInt(score); if (n >= 90) return 'success'; if (n >= 70) return 'info'; if (n >= 60) return 'warning'; return 'danger'; };

const showHistoryModal = ref(false);
const selectedHistoryRecord = ref(null);
const historyQuestions = ref([]);
const viewHistoryDetail = async (record) => {
    selectedHistoryRecord.value = record;
    try { const res = await axios.get(`${API_BASE_URL}/user-answers/by-session/${record.sessionId}`); historyQuestions.value = res.data; showHistoryModal.value = true; }
    catch (error) { console.error('加载历史记录题目失败:', error); historyQuestions.value = []; showHistoryModal.value = true; }
};

const loadAllQuestions = async () => {
    isLoadingQuestions.value = true;
    try { const response = await axios.get(`${API_BASE_URL}/questions`); allQuestions.value = response.data; }
    catch (error) { console.error('加载题库失败:', error); alert('加载题库失败，请检查后端服务是否正常运行'); }
    finally { isLoadingQuestions.value = false; }
};

const addToPractice = (question) => {
    const pq = convertToPracticeQuestion(question);
    if (currentQuestions.value.some(q => q.id === pq.id)) { alert('该题目已在练习列表中'); return; }
    currentQuestions.value.push(pq);
    alert(`已成功添加题目到练习列表！\n当前练习题目数：${currentQuestions.value.length}`);
};

const convertToPracticeQuestion = (q) => {
    let type = 'essay';
    switch (q.questionType) { case '单选题': type = 'choice'; break; case '判断题': type = 'judge'; break; case '填空题': type = 'fill'; break; case '简答题': type = 'essay'; break; }
    let options = [], content = q.content;
    if (type === 'choice') {
        const pattern = /([A-D])\.\s*([^A-D]+)(?=\s*[A-D]\.|$)/g; let match; const matches = [];
        while ((match = pattern.exec(content)) !== null) matches.push({ key: match[1], text: match[2].trim() });
        if (matches.length > 0) { options = matches; content = content.replace(pattern, '').replace(/^\s*\n+/, ''); }
        else { options = [{ key: 'A', text: '选项 A' }, { key: 'B', text: '选项 B' }, { key: 'C', text: '选项 C' }, { key: 'D', text: '选项 D' }]; }
    }
    return { id: q.id, questionId: q.questionId, type, title: `题目 ${currentQuestions.value.length + 1}`, content, options, blanks: type === 'fill' ? [1] : [], difficulty: q.difficulty, topic: q.knowledgePoint, correctAnswer: q.answer, explanation: q.explanation || '' };
};
</script>

<style scoped>
.scenic-background {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(to bottom, rgba(22, 93, 255, 0.85) 0%, rgba(64, 128, 255, 0.8) 40%, rgba(255, 255, 255, 0.85) 40%, rgba(255, 255, 255, 0.9) 100%), url('/src/assets/backgrounds/landscape-3.jpg');
    background-size: cover; background-position: center; background-attachment: fixed; z-index: -2; pointer-events: none;
}

/* 气泡装饰效果 */
.bubble {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.15);
    animation: float-bubble 6s ease-in-out infinite;
    pointer-events: none;
}

.bubble-1 {
    width: 80px;
    height: 80px;
    top: -20px;
    right: 10%;
    animation-delay: 0s;
}

.bubble-2 {
    width: 50px;
    height: 50px;
    top: 20px;
    right: 25%;
    animation-delay: 1s;
}

.bubble-3 {
    width: 120px;
    height: 120px;
    bottom: -40px;
    right: 5%;
    animation-delay: 2s;
}

@keyframes float-bubble {
    0%, 100% {
        transform: translateY(0) scale(1);
        opacity: 0.15;
    }
    50% {
        transform: translateY(-15px) scale(1.1);
        opacity: 0.25;
    }
}
.teacher-dashboard { padding: 1rem; background-color: transparent; min-height: 100vh; }
.card { background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.card:hover { transform: scale(1.005); }

/* 练习测评样式 */
.question-container { padding: 1rem; }
.question-header { padding-bottom: 1rem; border-bottom: 2px solid #E5E6EB; }
.question-content { padding: 1.5rem 0; font-size: 1.0625rem; line-height: 1.7; color: #4E5969; }
.answer-section { padding: 1.5rem 0; }
.choice-answers { display: grid; gap: 1rem; }
.judge-answers { padding: 1rem 0; }
.fill-answers { display: flex; flex-direction: column; gap: 1rem; }
.essay-answers { padding: 0.5rem 0; }

.p-multiselect .p-multiselect-label { padding: 0.5rem 1rem; }
.p-chip { border-radius: 9999px; background-color: #eff6ff; color: #1d4ed8; padding: 0.25rem 0.75rem; font-size: 0.75rem; font-weight: 500; }
.p-chip i { margin-right: 0.375rem; }

.history-record-item { padding: 0.75rem; border-radius: 8px; border: 1px solid #E5E6EB; background: #fff; cursor: pointer; transition: all 0.2s ease; }
.history-record-item:hover { background: #E8F3FF; border-color: #165DFF; transform: scale(1.01); }

.add-to-practice-btn { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border: 1.5px solid #165DFF; border-radius: 4px; background-color: white; cursor: pointer; transition: all 0.2s ease; position: relative; }
.add-to-practice-btn:hover { background-color: #165DFF; transform: scale(1.05); box-shadow: 0 2px 6px rgba(22, 93, 255, 0.3); }
.add-to-practice-btn svg { width: 14px; height: 14px; stroke: #165DFF; transition: stroke 0.2s ease; }
.add-to-practice-btn:hover svg { stroke: white; }

/* PrimeVue 组件主题颜色覆盖 - 改为蓝色系 */
:deep(.p-tag.p-tag-success),
:deep(.p-badge.p-badge-success) {
    background-color: #165DFF !important;
    color: white !important;
}

:deep(.p-button.p-button-success) {
    background: linear-gradient(135deg, #165DFF 0%, #4080FF 100%) !important;
    border-color: #165DFF !important;
    color: white !important;
}

:deep(.p-button.p-button-outlined.p-button-success) {
    background: transparent !important;
    border-color: #165DFF !important;
    color: #165DFF !important;
}

:deep(.p-button.p-button-outlined.p-button-success:hover) {
    background: rgba(22, 93, 255, 0.1) !important;
}

/* TabView 标签页下划线改为淡天蓝色 */
:deep(.p-tabview-nav) {
    border-bottom: 2px solid #E5E6EB !important;
}
:deep(.p-tabview-nav li.p-highlight .p-tabview-nav-link) {
    color: #165DFF !important;
    border-color: #87CEEB !important;
}
:deep(.p-tabview-nav li .p-tabview-nav-link:hover) {
    color: #165DFF !important;
}
:deep(.p-tabview-nav li.p-highlight .p-tabview-nav-link::before),
:deep(.p-tabview-nav li.p-highlight .p-tabview-nav-link::after) {
    background-color: #87CEEB !important;
}
/* PrimeVue TabView 激活指示器 - 强制覆盖为淡天蓝色 */
:deep(.p-tabview-nav li.p-highlight .p-tabview-nav-link span) {
    border-bottom-color: #87CEEB !important;
}

@media (max-width: 768px) {
    .flex.flex-wrap.gap-2.mb-3 { justify-content: center; }
}

:deep(.p-dropdown-panel) {
    z-index: 1100 !important;
}
:deep(.p-multiselect-panel) {
    z-index: 1100 !important;
}
 </style>
