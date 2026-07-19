<template>
    <Dialog
        :visible="visible"
        @update:visible="$emit('update:visible', $event)"
        :header="record && 'title' in record ? '练习详情：' + record.title : '练习详情'"
        :style="{ width: '70vw', maxWidth: '900px' }"
        :modal="true"
        :dismissableMask="true"
        class="practice-detail-dialog"
    >
        <div class="content-wrapper">
            <div v-if="questions.length === 0" class="empty-state">
                <i class="pi pi-info-circle text-2xl mb-3"></i>
                <p class="font-medium">暂无题目数据</p>
            </div>

            <div
                v-for="(question, index) in questions"
                :key="question.id || index"
                class="question-card"
                :class="{ 'question-card-not-first': index !== 0 }"
            >
                <div class="question-header">
                    <div class="question-number">
                        {{ index + 1 }}
                    </div>
                    <div class="flex-grow-1">
                        <!-- 题目内容 -->
                        <div class="question-content">
                            <p class="question-text">{{ question.content }}</p>
                        </div>

                        <!-- 用户答案 -->
                        <div class="answer-card user-answer" :class="{ 'incorrect': !question.isCorrect, 'correct': question.isCorrect }">
                            <div class="answer-label">你的答案</div>
                            <div class="answer-content">
                                <i
                                    :class="question.isCorrect ? 'pi pi-check-circle correct-icon' : 'pi pi-times-circle incorrect-icon'"
                                ></i>
                                <span class="answer-text" :class="{ 'text-correct': question.isCorrect, 'text-incorrect': !question.isCorrect }">
                                    {{ question.userAnswer || '未作答' }}
                                </span>
                            </div>
                        </div>

                        <!-- 正确答案 -->
                        <div class="answer-card correct-answer">
                            <div class="answer-label">正确答案</div>
                            <div class="answer-content">
                                <i class="pi pi-check correct-icon"></i>
                                <span class="answer-text">{{ question.correctAnswer || "无" }}</span>
                            </div>
                        </div>

                        <!-- 解析 -->
                        <div v-if="question.explanation" class="answer-card explanation">
                            <div class="answer-label">解析</div>
                            <p class="explanation-text">{{ question.explanation }}</p>
                        </div>

                        <!-- 状态标签 -->
                        <div class="status-tag-container">
                            <Tag
                                :value="question.isCorrect ? '回答正确' : '回答错误'"
                                :severity="question.isCorrect ? 'success' : 'danger'"
                                :icon="question.isCorrect ? 'pi pi-check' : 'pi pi-times'"
                                class="status-tag"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <template #footer>
            <Button
                label="关闭"
                icon="pi pi-times"
                @click="$emit('update:visible', false)"
                class="close-button p-button-text"
            />
        </template>
    </Dialog>
</template>

<script>
export default {
    name: "PracticeHistoryDetailModal",
    props: {
        visible: {
            type: Boolean,
            required: true
        },
        record: {
            type: Object,
            default: () => ({})
        },
        questions: {
            type: Array,
            default: () => []
        }
    },
    emits: ["update:visible"]
}
</script>

<style scoped>
/* 全局样式 */
.practice-detail-dialog .p-dialog-header {
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    padding: 1.5rem 2rem;
    background-color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    color: #1e293b;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.practice-detail-dialog .p-dialog-content {
    padding: 0;
    background-color: #f8fafc;
}

.practice-detail-dialog .p-dialog-footer {
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    padding: 1.25rem 2rem;
    background-color: #ffffff;
}

.content-wrapper {
    padding: 2rem;
}

/* 空状态 */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    color: #64748b;
    background-color: white;
    border-radius: 0.75rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

/* 问题卡片 */
.question-card {
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    transition: all 0.2s ease;
}

.question-card:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}

.question-card-not-first {
    padding-top: 2rem;
}

.question-header {
    display: flex;
    align-items: flex-start;
}

.question-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    margin-right: 1rem;
    font-weight: 600;
    font-size: 1.1rem;
    color: #3b82f6;
    background-color: rgba(59, 130, 246, 0.1);
    border-radius: 50%;
    box-shadow: 0 2px 5px rgba(59, 130, 246, 0.15);
}

.question-content {
    margin-bottom: 1.5rem;
}

.question-text {
    font-size: 1.1rem;
    font-weight: 500;
    color: #0f172a;
    line-height: 1.6;
    margin: 0;
}

/* 答案卡片样式 */
.answer-card {
    margin-bottom: 1rem;
    padding: 1.25rem;
    border-radius: 0.75rem;
    background-color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.answer-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.answer-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.answer-content {
    display: flex;
    align-items: center;
}

.answer-text {
    font-size: 1rem;
    color: #1e293b;
    font-weight: 500;
}

/* 用户答案 */
.user-answer {
    border-left: 4px solid #94a3b8;
}

.user-answer.correct {
    background-color: rgba(16, 185, 129, 0.08);
    border-left: 4px solid #10b981;
}

.user-answer.incorrect {
    background-color: rgba(239, 68, 68, 0.08);
    border-left: 4px solid #ef4444;
}

.correct-icon {
    color: #10b981;
    margin-right: 0.75rem;
    font-size: 1.1rem;
}

.incorrect-icon {
    color: #ef4444;
    margin-right: 0.75rem;
    font-size: 1.1rem;
}

.text-correct {
    color: #10b981;
}

.text-incorrect {
    color: #ef4444;
}

/* 正确答案 */
.correct-answer {
    background-color: rgba(16, 185, 129, 0.05);
    border-left: 4px solid #10b981;
}

/* 解析 */
.explanation {
    background-color: rgba(59, 130, 246, 0.05);
    border-left: 4px solid #3b82f6;
}

.explanation-text {
    font-size: 1rem;
    color: #334155;
    line-height: 1.6;
    margin: 0;
}

/* 状态标签 */
.status-tag-container {
    display: flex;
    justify-content: flex-end;
    margin-top: 1rem;
}

.status-tag {
    font-weight: 500;
    border-radius: 2rem;
    padding: 0.4rem 1rem;
}

/* 关闭按钮 */
.close-button {
    font-weight: 500;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
}

.close-button:hover {
    background-color: rgba(0, 0, 0, 0.05);
}
</style>
