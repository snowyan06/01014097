<template>
     <div class="student-dashboard" :class="{ 'dark-mode': isDarkTheme }">
        <!-- 风景背景层 -->
        <div class="scenic-background"></div>
        <GeometricBackground />

        <!-- 第一层：顶部深蓝色通栏标题 -->
        <div class="relative overflow-hidden bg-gradient-to-r from-blue-800 via-blue-900 to-cyan-900 shadow-lg px-6 py-4 mb-4 rounded-xl">
            <div class="absolute inset-0 opacity-10 z-10">
                <div class="absolute -top-4 -right-4 w-32 h-32 bg-white rounded-full"></div>
                <div class="absolute -bottom-4 -left-4 w-24 h-24 bg-white rounded-full"></div>
            </div>
            <div class="relative flex align-items-center justify-content-between z-20">
                <div>
                    <h2 class="text-2xl font-bold text-white m-0 drop-shadow-sm" style="font-family: 'SimSun', 'STSong', 'Adobe Song Std', serif;">学生学情画像分析</h2>
                    <p class="text-white text-sm m-0 opacity-90" style="font-family: 'SimSun', 'STSong', 'Adobe Song Std', serif;">Student Profile Dialogue Collection</p>
                </div>
                <span class="banner-note">赛题强制需求 对话式采集六维动态学情画像</span>
            </div>
        </div>

        <!-- 第二层：六维学情采集进度卡片 -->
        <div class="progress-card">
            <h4 class="progress-card-title">六大学情维度采集进度</h4>
            <div class="progress-tags">
                <div v-for="(dim, idx) in dimensions" :key="idx" class="progress-tag" :class="{ completed: dim.collected }">
                    <span class="progress-tag-icon">{{ dim.collected ? '&#10003;' : (idx + 1) }}</span>
                    <span class="progress-tag-label">{{ dim.name }}</span>
                </div>
            </div>

        </div>

        <!-- Tab 切换面板 -->
        <TabView v-model:activeIndex="activeTab">
            <!-- Tab 1：学情画像分析 -->
            <TabPanel header="学情画像分析">
                <div class="ai-assistant-container">

                    <!-- 第三层：当前采集维度提示框 -->
                    <div class="dimension-prompt-card">
                        <div class="dimension-prompt-header">
                            <span class="dimension-prompt-label">当前采集维度</span>
                            <span class="dimension-prompt-name">{{ currentDimension.name }}</span>
                        </div>
                        <p class="dimension-prompt-text">{{ currentDimension.guideText }}</p>
                    </div>

                    <!-- 第四层：对话气泡容器 -->
                    <div class="chat-wrapper">
                        <div class="chat-messages" ref="chatContainer">
                            <div class="messages-list">
                                <div v-for="(message, index) in chatMessages" :key="message.id"
                                     :class="['message-row', message.type]">
                                    <!-- AI 消息 - 左侧 -->
                                    <div v-if="message.type === 'ai'" class="message-content-wrapper">
                                        <div class="avatar ai-avatar">
                                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
                                                <circle cx="9" cy="10" r="1.5" fill="currentColor"/>
                                                <circle cx="15" cy="10" r="1.5" fill="currentColor"/>
                                                <path d="M8 15C8 15 9.5 17 12 17C14.5 17 16 15 16 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                            </svg>
                                        </div>
                                        <div class="message-bubble">
                                            <div
                                                class="message-content markdown-content"
                                                v-html="renderMarkdown(message.content)"
                                            ></div>
                                            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
                                        </div>
                                    </div>

                                    <!-- 用户消息 - 右侧 -->
                                    <div v-else class="message-content-wrapper user-message">
                                        <div class="message-bubble user-bubble">
                                            <div class="message-content">
                                                {{ message.content }}
                                            </div>
                                            <div class="message-time user-time">{{ formatTime(message.timestamp) }}</div>
                                        </div>
                                        <div class="avatar user-avatar">
                                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                                <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            </svg>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="isTyping" class="message-row ai">
                                    <div class="message-content-wrapper">
                                        <div class="avatar ai-avatar">
                                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
                                                <circle cx="9" cy="10" r="1.5" fill="currentColor"/>
                                                <circle cx="15" cy="10" r="1.5" fill="currentColor"/>
                                                <path d="M8 15C8 15 9.5 17 12 17C14.5 17 16 15 16 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                            </svg>
                                        </div>
                                        <div class="message-bubble">
                                            <div class="typing-dots">
                                                <span></span>
                                                <span></span>
                                                <span></span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                     <!-- 第五层：底部输入操作栏 -->
                     <div class="input-area">
                        <div class="input-toolbar">
                            <button class="tool-btn tool-btn-outline" title="暂不采集该维度，直接进入下一个学情维度提问" @click="skipDimension">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                                跳过当前维度
                            </button>
                            <button class="tool-btn tool-btn-outline" title="保存已回答维度数据，随时可重新继续采集" @click="terminateCollection">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9l6 6M15 9l-6 6"/></svg>
                                终止本次采集
                            </button>
                            <div class="toolbar-spacer"></div>
                            <button class="tool-btn tool-btn-primary" title="采集完毕后跳转至学情测评分析页面查看六维雷达图，同步可前往学习资源中心匹配对应专项练习题库、思维导图资源" @click="completeCollection">
                                完成采集，生成六维画像
                            </button>
                        </div>
                        <div class="input-wrapper">
                            <input
                                v-model="newQuestion"
                                @keyup.enter="sendQuestion"
                                type="text"
                                placeholder="针对当前维度输入你的学情描述..."
                                class="message-input"
                                :disabled="isTyping"
                            />
                            <div class="input-actions">
                                <button
                                    @click="sendQuestion"
                                    class="send-button"
                                    :disabled="!newQuestion.trim() || isTyping"
                                >
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                        <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </button>
                            </div>
                        </div>

                    </div>
                </div>
            </TabPanel>
        </TabView>
    </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

import { AIService } from '@/service/AIService';
import GeometricBackground from '@/components/GeometricBackground.vue';
import { useDigitalHumanStore } from '@/store/digitalHumanStore';
import { voiceNavigationService } from '@/service/voiceNavigationService';
import { marked } from 'marked';
import { useLayout } from '@/layout/composables/layout';
import { TabView, TabPanel } from 'primevue';

marked.setOptions({
    breaks: true,
    gfm: true,
    highlight: function(code, lang) { return code; }
});

export default {
    name: 'StudentDashboard',
    components: {
        GeometricBackground,
        TabView,
        TabPanel
    },
    setup() {
        const activeTab = ref(0);
        const { isDarkTheme } = useLayout();
        const newQuestion = ref('');
        const digitalHumanStore = useDigitalHumanStore();
        const isTyping = ref(false);
        const chatContainer = ref(null);
        const currentDimensionIndex = ref(0);
        const router = useRouter();

        const AI_SERVICE_URL = import.meta.env.VITE_AI_SERVICE_URL || 'http://localhost:8000';

        // 六大学情维度定义（赛题核心需求）
        const dimensions = ref([
            { name: '知识基础', collected: false, guideText: '请描述你的专业基础、掌握的编程与计算机核心知识点，便于评估知识储备水平。' },
            { name: '认知风格', collected: false, guideText: '你更偏向阅读文档理论学习，还是动手实操代码练习？日常学习节奏偏好是什么？' },
            { name: '易错短板', collected: false, guideText: '平时做题、写代码最容易出错的知识点、题型有哪些？' },
            { name: '学习目标', collected: false, guideText: '你的学习目标是期末考核、岗位求职还是竞赛拔高？' },
            { name: '学习节奏', collected: false, guideText: '你每日稳定学习时长、自主复盘习惯如何？' },
            { name: '兴趣偏好', collected: false, guideText: '你更感兴趣前端/后端/AI算法/网络安全哪类技术方向？' }
        ]);

        const currentDimension = computed(() => dimensions.value[currentDimensionIndex.value]);

        // ====== 每个维度的问题题库 ======
        const dimensionQuestions = {
            '知识基础': [
                '请描述你的专业背景和已掌握的核心编程语言（如Python/Java/C++等），以及你对数据结构、算法、操作系统、计算机网络等计算机基础知识的了解程度。',
                '你在机器学习或深度学习方面有哪些前置知识？是否熟悉线性代数、概率统计、微积分等数学基础？',
                '请列举你最熟悉的3-5个技术栈或框架，并说明你在项目中实际使用过哪些。'
            ],
            '认知风格': [
                '在学习新的AI概念时，你更倾向于先阅读理论文档和论文，还是直接上手写代码做实验？',
                '面对一个复杂的算法问题，你通常会先画流程图理清思路，还是直接在IDE里调试？',
                '你平时学习新技术时，更喜欢看视频教程、读官方文档，还是通过开源项目实战来掌握？'
            ],
            '易错短板': [
                '在机器学习中，你是否容易混淆过拟合和欠拟合的概念？能否解释它们的区别和解决方法？',
                '你在编写代码时最常犯的错误类型是什么？（如边界条件处理、内存泄漏、并发问题等）',
                '对于反向传播、梯度下降等深度学习核心算法，你觉得最难理解的部分是什么？'
            ],
            '学习目标': [
                '你学习AI的主要目的是什么？（学术研究/工程应用/竞赛比赛/转行求职）',
                '你希望在AI领域达到什么样的水平？（入门了解/能独立开发模型/成为领域专家）',
                '完成本次学习后，你最想实现的AI项目或应用场景是什么？'
            ],
            '学习节奏': [
                '你每周大约花多少时间在AI相关的学习上？是否有固定的学习计划？',
                '你通常通过什么方式跟进AI领域的最新进展？（论文/博客/课程/开源社区）',
                '遇到难以理解的AI概念时，你会如何处理？（反复阅读/请教他人/实践验证/暂时跳过）'
            ],
            '兴趣偏好': [
                '在AI的各个方向中（NLP/计算机视觉/强化学习/大模型/推荐系统），你最感兴趣的是哪个？为什么？',
                '你更关注AI的理论研究还是工程落地？对AI伦理和安全问题有何看法？',
                '如果让你选择一个AI应用场景深入钻研，你会选择哪个领域？（医疗/金融/教育/自动驾驶/智能客服等）'
            ]
        };

        // 初始对话消息
        const chatMessages = ref([
            {
                id: 1,
                type: 'ai',
                content: '你好！我将分6个维度依次向你提问，完成全部对话后即可生成专属六维学情画像。你可以随时点击「终止采集」保存当前进度，全部答完后跳转学情测评页面查看雷达图、前往学习资源中心配套练习。\n\n现在让我们开始第一个维度：**知识基础**。',
                timestamp: new Date()
            },
            {
                id: 2,
                type: 'ai',
                content: dimensionQuestions['知识基础'][0],
                timestamp: new Date()
            }
        ]);

        onMounted(async () => {
            const route = useRoute();
        });

        const renderMarkdown = (content) => {
            try { return marked(content); }
            catch (error) { console.error('Markdown 渲染错误:', error); return content; }
        };

        const formatTime = (timestamp) => {
            const date = new Date(timestamp);
            return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
        };

        const scrollToBottom = () => {
            if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        };

        // ====== 推进到下一维度 ======
        const advanceToNextDimension = (previousReply) => {
            currentDimensionIndex.value++;

            if (currentDimensionIndex.value >= dimensions.value.length) {
                chatMessages.value.push({
                    id: Date.now(),
                    type: 'ai',
                    content: '🎉 恭喜！你已完成全部6个维度的学情采集。现在为你生成六维学情画像雷达图，即将跳转到学情测评分析页面...',
                    timestamp: new Date()
                });
                setTimeout(() => {
                    router.push('/AnalysisImprovement');
                }, 3000);
                return;
            }

            const nextDim = dimensions.value[currentDimensionIndex.value];
            const questions = dimensionQuestions[nextDim.name];
            const randomQuestion = questions[Math.floor(Math.random() * questions.length)];

            chatMessages.value.push({
                id: Date.now() + 1,
                type: 'ai',
                content: `接下来是第 ${currentDimensionIndex.value + 1} 个维度：**${nextDim.name}**。\n\n${randomQuestion}`,
                timestamp: new Date()
            });
        };

        // ====== 发送问题/回答 ======
        const sendQuestion = async () => {
            const userQuestion = newQuestion.value.trim();
            if (!userQuestion || isTyping.value) return;
            newQuestion.value = '';

            chatMessages.value.push({ id: Date.now(), type: 'user', content: userQuestion, timestamp: new Date() });
            isTyping.value = true;
            await nextTick();
            scrollToBottom();

            try {
                const response = await AIService.askQuestion(userQuestion, `当前采集维度：${currentDimension.value.name}`);
                const aiAnswer = response.data.success ? response.data.data?.answer || response.data.data?.content || '抱歉，暂时无法回答这个问题。' : '抱歉，暂时无法回答这个问题。';
                chatMessages.value.push({ id: Date.now() + 1, type: 'ai', content: aiAnswer, timestamp: new Date() });
                if (digitalHumanStore.isActive) digitalHumanStore.setTextToSpeak(aiAnswer);

                dimensions.value[currentDimensionIndex.value].collected = true;
                setTimeout(() => {
                    advanceToNextDimension(aiAnswer);
                }, 1000);
            } catch (error) {
                console.error('请求失败:', error);
                chatMessages.value.push({ id: Date.now() + 1, type: 'ai', content: '网络错误，请稍后再试。但你的回答已记录，继续下一维度。', timestamp: new Date() });
                dimensions.value[currentDimensionIndex.value].collected = true;
                setTimeout(() => {
                    advanceToNextDimension('');
                }, 1000);
            } finally {
                isTyping.value = false;
                await nextTick();
                scrollToBottom();
            }
        };

        // ====== 跳过当前维度 ======
        const skipDimension = () => {
            dimensions.value[currentDimensionIndex.value].collected = true;
            advanceToNextDimension('已跳过');
        };

        // ====== 终止采集 ======
        const terminateCollection = () => {
            if (!confirm('确定要终止本次采集吗？已完成的维度数据将保留。')) return;
            chatMessages.value.push({
                id: Date.now(),
                type: 'ai',
                content: `采集已终止。你已完成 ${dimensions.value.filter(d => d.collected).length} / ${dimensions.value.length} 个维度的采集。可随时重新开始。`,
                timestamp: new Date()
            });
        };

        // ====== 完成采集 ======
        const completeCollection = () => {
            const completed = dimensions.value.filter(d => d.collected).length;
            if (completed < dimensions.value.length) {
                if (!confirm(`你还有 ${dimensions.value.length - completed} 个维度未完成，确定要直接生成画像吗？`)) return;
            }
            dimensions.value.forEach(d => { d.collected = true; });
            chatMessages.value.push({
                id: Date.now(),
                type: 'ai',
                content: '🎉 六维学情画像生成完毕！即将跳转到学情测评分析页面...',
                timestamp: new Date()
            });
            setTimeout(() => { router.push('/AnalysisImprovement'); }, 2000);
        };

        return {
            activeTab,
            isDarkTheme,
            newQuestion,
            chatMessages,
            digitalHumanStore,
            isTyping,
            sendQuestion,
            skipDimension,
            terminateCollection,
            completeCollection,
            renderMarkdown,
            formatTime,
            chatContainer,
            scrollToBottom,
            dimensions,
            currentDimension
        };
    }
};
</script>

<style scoped>
.scenic-background {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(to bottom, rgba(22, 93, 255, 0.85) 0%, rgba(64, 128, 255, 0.8) 40%, rgba(255, 255, 255, 0.85) 40%, rgba(255, 255, 255, 0.9) 100%), url('/src/assets/backgrounds/landscape-3.jpg');
    background-size: cover; background-position: center; background-attachment: fixed; z-index: -2; pointer-events: none;
}

.student-dashboard { padding: 1.5rem; min-height: 100vh; background-color: transparent; }

.ai-assistant-container { max-width: 1200px; margin: 0 auto; }

/* ===== 横幅右下角标注 ===== */
.banner-note {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.55);
    white-space: nowrap;
    font-family: 'SimSun', 'STSong', 'Adobe Song Std', serif;
}

/* ===== 六维采集进度卡片 ===== */
.progress-card {
    background: #fff;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.progress-card-title {
    font-size: 0.9375rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 0.875rem;
}

.progress-tags {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
}

.progress-tag {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.375rem 0.875rem;
    border-radius: 6px;
    border: 1px solid #e5e7eb;
    background: #f8fafc;
    font-size: 0.8125rem;
    color: #94a3b8;
    transition: all 0.2s;
}

.progress-tag.completed {
    background: #165DFF;
    border-color: #165DFF;
    color: #fff;
}

.progress-tag-icon {
    font-size: 0.75rem;
    font-weight: 600;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.06);
}

.progress-tag.completed .progress-tag-icon {
    background: rgba(255, 255, 255, 0.25);
}

.progress-tag-label {
    font-weight: 500;
}

.progress-card-hint {
    font-size: 0.75rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.5;
}

/* ===== 当前采集维度提示框 ===== */
.dimension-prompt-card {
    background: #fff;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    border-left: 3px solid #165DFF;
    padding: 0.875rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.dimension-prompt-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.375rem;
}

.dimension-prompt-label {
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 500;
}

.dimension-prompt-name {
    font-size: 0.875rem;
    font-weight: 700;
    color: #165DFF;
}

.dimension-prompt-text {
    font-size: 0.8125rem;
    color: #475569;
    margin: 0;
    line-height: 1.6;
}

/* ===== 对话容器 ===== */
.chat-wrapper { background: #fff; border-radius: 8px; border: 1px solid #E5E6EB; overflow: hidden; transition: transform 0.2s ease; }
.chat-messages { height: 500px; overflow-y: auto; padding: 1.5rem; }

.messages-list { display: flex; flex-direction: column; gap: 1.5rem; }
.message-row { display: flex; width: 100%; }
.message-row.ai { justify-content: flex-start; }
.message-row.user { justify-content: flex-end; }
.message-content-wrapper { display: flex; align-items: flex-end; gap: 0.75rem; max-width: 80%; }
.message-row.ai .avatar { order: 1; }
.message-row.ai .message-bubble { order: 2; }

.avatar { flex-shrink: 0; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.avatar svg { width: 24px; height: 24px; }
.ai-avatar { background: linear-gradient(135deg, #165DFF 0%, #0E42D2 100%); color: white; }
.user-avatar { background: linear-gradient(135deg, #4080FF 0%, #165DFF 100%); color: white; }

.message-bubble { padding: 1rem 1.25rem; border-radius: 18px; position: relative; background: #F7F8FA; color: #1D2129; max-width: 100%; word-wrap: break-word; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); }
.message-row.ai .message-bubble { border-bottom-left-radius: 4px; }
.message-row.user .message-bubble { background: linear-gradient(135deg, #165DFF 0%, #4080FF 100%); color: white; border-bottom-right-radius: 4px; }

.message-content { font-size: 0.9375rem; line-height: 1.6; margin-bottom: 0.5rem; }
.message-content:last-child { margin-bottom: 0; }
.markdown-content { word-wrap: break-word; }
.markdown-content :deep(p) { margin-bottom: 0.5rem; }
.markdown-content :deep(pre) { background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 0.5rem 0; }
.markdown-content :deep(code) { font-family: 'Consolas', 'Monaco', monospace; font-size: 0.875rem; }
.user-bubble .message-content :deep(pre) { background: rgba(0, 0, 0, 0.2); color: white; }

.message-time { font-size: 0.7rem; color: #86909C; text-align: right; margin-top: 0.25rem; display: block; }
.user-time { color: rgba(255, 255, 255, 0.8); }

.typing-dots { display: flex; gap: 4px; }
.typing-dots span { width: 6px; height: 6px; background: #86909C; border-radius: 50%; animation: typing 1.4s infinite; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.7; }
    30% { transform: translateY(-10px); opacity: 1; }
}

/* ===== 底部输入操作栏 ===== */
.input-area { margin-top: 1rem; padding: 1.5rem; background: #fff; border-radius: 8px; border: 1px solid #E5E6EB; }

.input-toolbar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.toolbar-spacer {
    flex: 1;
}

.tool-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.4375rem 1rem;
    border-radius: 6px;
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    white-space: nowrap;
}

.tool-btn-outline {
    background: #fff;
    border: 1px solid #d1d5db;
    color: #475569;
}

.tool-btn-outline:hover {
    background: #f1f5f9;
    border-color: #165DFF;
    color: #165DFF;
}

.tool-btn-primary {
    background: #165DFF;
    color: #fff;
    border: 1px solid #165DFF;
}

.tool-btn-primary:hover {
    background: #0e4fd9;
    box-shadow: 0 4px 12px rgba(22, 93, 255, 0.3);
}

.input-wrapper { display: flex; align-items: center; gap: 0.75rem; background: #F7F8FA; border-radius: 9999px; padding: 0.5rem 1rem; border: 2px solid transparent; transition: all 0.3s; }
.input-wrapper:focus-within { background: white; border-color: #165DFF; box-shadow: 0 0 0 3px rgba(22, 93, 255, 0.1); }

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
:deep(.p-tabview-nav li.p-highlight .p-tabview-nav-link span) {
    border-bottom-color: #87CEEB !important;
}
.message-input { flex: 1; border: none; outline: none; font-size: 0.9375rem; background: transparent; color: #1D2129; }
.message-input::placeholder { color: #86909C; }

.input-actions { display: flex; gap: 0.5rem; align-items: center; }

.send-button { width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #165DFF 0%, #0E42D2 100%); color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.send-button:hover:not(:disabled) { transform: scale(1.05); box-shadow: 0 4px 12px rgba(22, 93, 255, 0.3); }
.send-button:disabled { opacity: 0.5; cursor: not-allowed; }
.send-button svg { width: 20px; height: 20px; }

.input-hint { text-align: center; font-size: 0.75rem; color: #94a3b8; margin-top: 0.75rem; line-height: 1.5; }

@media (max-width: 768px) {
    .message-bubble { max-width: 85%; }
    .progress-tags { flex-direction: column; }
    .input-toolbar { flex-direction: column; align-items: stretch; }
    .toolbar-spacer { display: none; }
}

.dark-mode .student-dashboard { background-color: transparent; }
.dark-mode .card,
.dark-mode .ai-assistant-container,
.dark-mode .chat-wrapper,
.dark-mode .input-area,
.dark-mode .progress-card,
.dark-mode .dimension-prompt-card { background-color: rgba(30, 41, 59, 0.95); color: #f1f5f9; }
</style>
