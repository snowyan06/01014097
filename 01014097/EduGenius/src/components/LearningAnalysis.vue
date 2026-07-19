<template>
    <div class="learning-analysis">
        <!-- 标题区域 -->
        <div class="header-section mb-6">
            <h3 class="section-title">学情分析系统</h3>
            <p class="section-subtitle">生成试卷、答案及学情分析报告</p>
        </div>

        <!-- 控制区域 -->
        <div class="control-section bg-white p-4 rounded-lg shadow-sm border border-gray-100 mb-6">
            <div class="flex flex-col md:flex-row gap-6">
                <!-- 试卷生成配置 -->
                <div class="flex-1">
                    <h4 class="text-lg font-semibold mb-4">试卷生成配置</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">试卷名称</label>
                            <InputText v-model="paperConfig.paperName" class="w-full" />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">试卷难度</label>
                            <Dropdown
                                v-model="paperConfig.difficulty"
                                :options="difficultyOptions"
                                optionLabel="label"
                                optionValue="value"
                                class="w-full"
                            />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">题目数量</label>
                            <InputNumber v-model="paperConfig.questionCount" :min="5" :max="50" class="w-full" />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">考试时长(分钟)</label>
                            <InputNumber v-model="paperConfig.duration" :min="30" :max="180" class="w-full" />
                        </div>
                    </div>
                </div>

                <!-- 学生选择 -->
                <div class="flex-1">
                    <h4 class="text-lg font-semibold mb-4">学生选择</h4>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">选择班级</label>
                        <Dropdown
                            v-model="selectedClassId"
                            :options="classOptions"
                            optionLabel="className"
                            optionValue="classId"
                            placeholder="选择班级"
                            class="w-full mb-3"
                            @change="fetchStudentsByClass"
                        />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">选择学生</label>
                        <MultiSelect
                            v-model="selectedStudents"
                            :options="studentOptions"
                            optionLabel="name"
                            optionValue="studentId"
                            placeholder="选择学生"
                            class="w-full"
                            :disabled="!selectedClassId"
                        />
                    </div>
                </div>
            </div>

            <div class="mt-6 flex justify-end gap-3">
                <Button
                    label="生成试卷"
                    icon="pi pi-file"
                    @click="generatePaper"
                    :disabled="generatingPaper"
                />
                <Button
                    label="生成分析报告"
                    icon="pi pi-chart-bar"
                    severity="success"
                    @click="generateAnalysisReport"
                    :disabled="!paperGenerated || analyzing"
                />
            </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="flex justify-center items-center p-8">
            <ProgressSpinner style="width: 40px; height: 40px" strokeWidth="4" />
            <span class="ml-3">{{ loadingMessage }}</span>
        </div>

        <!-- 错误提示 -->
        <Message v-if="error" severity="error" class="mb-4" :closable="false">{{ error }}</Message>

        <!-- 试卷预览 -->
        <div v-if="paperGenerated" class="paper-preview mb-6">
            <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                <div class="p-4 border-b border-gray-100 flex justify-between items-center">
                    <h4 class="text-base font-semibold text-gray-800">
                        试卷预览: {{ generatedPaper.paperName }}
                        <span class="text-xs text-gray-500 ml-2">(共 {{ generatedPaper.questions.length }} 题)</span>
                    </h4>
                    <div class="flex gap-2">
                        <Button
                            icon="pi pi-download"
                            class="p-button-text p-button-sm p-button-plain"
                            label="导出试卷"
                            @click="exportPaper"
                        />
                        <Button
                            icon="pi pi-download"
                            class="p-button-text p-button-sm p-button-plain"
                            label="导出答案"
                            @click="exportAnswerKey"
                        />
                    </div>
                </div>

                <div class="p-4">
                    <div class="paper-header mb-6 text-center">
                        <h2 class="text-2xl font-bold">{{ generatedPaper.paperName }}</h2>
                        <p class="text-gray-600">考试时长: {{ generatedPaper.duration }}分钟</p>
                        <p class="text-gray-600">难度: {{ generatedPaper.difficulty }}</p>
                    </div>

                    <div class="questions-list">
                        <div v-for="(question, index) in generatedPaper.questions" :key="question.id" class="mb-6">
                            <div class="question-item p-3 border border-gray-100 rounded">
                                <p class="font-medium mb-2">{{ index + 1 }}. {{ question.content }}</p>
                                <div v-if="question.type === 'choice'" class="options ml-4">
                                    <div v-for="(option, optIndex) in question.options" :key="optIndex" class="flex items-center mb-1">
                                        <span class="mr-2">{{ String.fromCharCode(65 + optIndex) }}.</span>
                                        <span>{{ option }}</span>
                                    </div>
                                </div>
                                <div v-else class="answer-space h-20 border border-gray-200 rounded mt-2 p-2 text-gray-400">
                                    答题区域
                                </div>
                                <div class="mt-2 text-sm text-gray-500">
                                    分值: {{ question.score }}分 | 难度: {{ question.difficulty }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 分析报告 -->
        <div v-if="analysisReport" class="analysis-report">
            <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                <div class="p-4 border-b border-gray-100 flex justify-between items-center">
                    <h4 class="text-base font-semibold text-gray-800">
                        学情分析报告
                        <span class="text-xs text-gray-500 ml-2">({{ selectedStudents.length }}名学生)</span>
                    </h4>
                    <Button
                        icon="pi pi-download"
                        class="p-button-text p-button-sm p-button-plain"
                        label="导出分析报告"
                        @click="exportAnalysisReport"
                    />
                </div>

                <div class="p-4">
                    <!-- 总体统计 -->
                    <div class="overall-stats mb-6 p-4 border border-gray-100 rounded">
                        <h5 class="text-lg font-semibold mb-3">总体统计</h5>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div class="stat-item text-center p-3 bg-blue-50 rounded">
                                <div class="text-sm text-gray-600">平均分</div>
                                <div class="text-2xl font-bold">{{ analysisReport.overall.averageScore.toFixed(1) }}</div>
                            </div>
                            <div class="stat-item text-center p-3 bg-green-50 rounded">
                                <div class="text-sm text-gray-600">最高分</div>
                                <div class="text-2xl font-bold">{{ analysisReport.overall.highestScore }}</div>
                            </div>
                            <div class="stat-item text-center p-3 bg-yellow-50 rounded">
                                <div class="text-sm text-gray-600">最低分</div>
                                <div class="text-2xl font-bold">{{ analysisReport.overall.lowestScore }}</div>
                            </div>
                            <div class="stat-item text-center p-3 bg-red-50 rounded">
                                <div class="text-sm text-gray-600">及格率</div>
                                <div class="text-2xl font-bold">{{ analysisReport.overall.passRate }}%</div>
                            </div>
                        </div>
                    </div>

                    <!-- 成绩分布图 -->
                    <div class="score-distribution mb-6">
                        <h5 class="text-lg font-semibold mb-3">成绩分布</h5>
                        <Chart
                            type="bar"
                            :data="scoreDistributionData"
                            :options="scoreDistributionOptions"
                            height="300px"
                        />
                    </div>

                    <!-- 题目分析 -->
                    <div class="question-analysis mb-6">
                        <h5 class="text-lg font-semibold mb-3">题目分析</h5>
                        <DataTable
                            :value="analysisReport.questionAnalysis"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20, 50]"
                            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                            currentPageReportTemplate="显示 {first} 到 {last} / 共 {totalRecords} 题"
                            responsiveLayout="scroll"
                            class="text-sm border-none"
                        >
                            <Column field="questionId" header="题号" sortable></Column>
                            <Column field="content" header="题目内容" style="width: 40%">
                                <template #body="{ data }">
                                    <div class="line-clamp-2">{{ data.content }}</div>
                                </template>
                            </Column>
                            <Column field="difficulty" header="难度" sortable>
                                <template #body="{ data }">
                                    <Tag :value="data.difficulty"
                                         :severity="getDifficultySeverity(data.difficulty)"
                                         class="px-2 py-1 rounded text-xs font-medium w-full text-center">
                                    </Tag>
                                </template>
                            </Column>
                            <Column field="averageScore" header="平均得分" sortable>
                                <template #body="{ data }">
                                    {{ data.averageScore.toFixed(1) }}/{{ data.fullScore }}
                                </template>
                            </Column>
                            <Column field="correctRate" header="正确率" sortable>
                                <template #body="{ data }">
                                    <ProgressBar :value="data.correctRate" :showValue="false" />
                                    <span class="ml-2">{{ data.correctRate }}%</span>
                                </template>
                            </Column>
                        </DataTable>
                    </div>

                    <!-- 学生成绩详情 -->
                    <div class="student-scores">
                        <h5 class="text-lg font-semibold mb-3">学生成绩详情</h5>
                        <DataTable
                            :value="analysisReport.studentScores"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20, 50]"
                            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                            currentPageReportTemplate="显示 {first} 到 {last} / 共 {totalRecords} 名学生"
                            responsiveLayout="scroll"
                            class="text-sm border-none"
                            sortField="totalScore"
                            :sortOrder="-1"
                        >
                            <Column field="rank" header="排名" sortable></Column>
                            <Column field="studentName" header="学生姓名" sortable></Column>
                            <Column field="totalScore" header="总分" sortable>
                                <template #body="{ data }">
                  <span :class="{'text-green-600 font-bold': data.totalScore >= analysisReport.overall.averageScore}">
                    {{ data.totalScore }}
                  </span>
                                </template>
                            </Column>
                            <Column field="scoreRate" header="得分率" sortable>
                                <template #body="{ data }">
                                    <ProgressBar :value="data.scoreRate" :showValue="false" />
                                    <span class="ml-2">{{ data.scoreRate }}%</span>
                                </template>
                            </Column>
                            <Column header="操作">
                                <template #body="{ data }">
                                    <Button
                                        icon="pi pi-eye"
                                        class="p-button-text p-button-sm"
                                        @click="viewStudentDetail(data.studentId)"
                                        v-tooltip.top="'查看详情'"
                                    />
                                </template>
                            </Column>
                        </DataTable>
                    </div>
                </div>
            </div>
        </div>

        <!-- 学生详情对话框 -->
        <Dialog
            v-model:visible="showStudentDetail"
            header="学生答题详情"
            :style="{ width: '800px' }"
            :modal="true"
        >
            <div v-if="selectedStudentDetail">
                <div class="student-info mb-4 p-3 bg-gray-50 rounded">
                    <h4 class="font-semibold">{{ selectedStudentDetail.studentName }}</h4>
                    <p>总分: {{ selectedStudentDetail.totalScore }} (排名: {{ selectedStudentDetail.rank }})</p>
                </div>

                <div class="question-responses">
                    <div v-for="(response, index) in selectedStudentDetail.responses" :key="index" class="mb-4 p-3 border border-gray-100 rounded">
                        <div class="flex justify-between mb-2">
                            <span class="font-medium">第{{ response.questionId }}题</span>
                            <span :class="{
                'text-green-600': response.score === response.fullScore,
                'text-yellow-600': response.score > 0 && response.score < response.fullScore,
                'text-red-600': response.score === 0
              }">
                {{ response.score }}/{{ response.fullScore }}
              </span>
                        </div>
                        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">题目:</span> {{ response.questionContent }}</p>
                        <p class="text-sm text-gray-600 mb-1"><span class="font-medium">学生答案:</span> {{ response.studentAnswer || '未作答' }}</p>
                        <p class="text-sm text-gray-600"><span class="font-medium">正确答案:</span> {{ response.correctAnswer }}</p>
                    </div>
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script>
import axios from 'axios';
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';

export default {
    name: 'LearningAnalysis',
    data() {
        return {
            // 配置数据
            paperConfig: {
                paperName: '数学期中测试卷',
                difficulty: 'medium',
                questionCount: 20,
                duration: 90
            },
            difficultyOptions: [
                { label: '简单', value: 'easy' },
                { label: '中等', value: 'medium' },
                { label: '困难', value: 'hard' }
            ],

            // 班级和学生数据
            classOptions: [],
            selectedClassId: null,
            studentOptions: [],
            selectedStudents: [],

            // 生成状态
            generatingPaper: false,
            analyzing: false,
            loading: false,
            loadingMessage: '',
            error: null,

            // 生成结果
            paperGenerated: false,
            generatedPaper: null,
            analysisReport: null,

            // 学生详情
            showStudentDetail: false,
            selectedStudentDetail: null
        };
    },
    computed: {
        // 成绩分布图表数据
        scoreDistributionData() {
            if (!this.analysisReport) return null;

            const scoreRanges = [
                { range: '0-59', min: 0, max: 59 },
                { range: '60-69', min: 60, max: 69 },
                { range: '70-79', min: 70, max: 79 },
                { range: '80-89', min: 80, max: 89 },
                { range: '90-100', min: 90, max: 100 }
            ];

            const counts = scoreRanges.map(range => {
                return this.analysisReport.studentScores.filter(s =>
                    s.totalScore >= range.min && s.totalScore <= range.max
                ).length;
            });

            return {
                labels: scoreRanges.map(r => r.range),
                datasets: [
                    {
                        label: '学生人数',
                        data: counts,
                        backgroundColor: '#3B82F6'
                    }
                ]
            };
        },
        scoreDistributionOptions() {
            return {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.parsed.y}名学生`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            };
        }
    },
    async created() {
        await this.fetchClasses();
    },
    methods: {
        // 获取班级列表
        async fetchClasses() {
            try {
                this.loading = true;
                this.loadingMessage = '正在加载班级数据...';
                const res = await axios.get('/api/classes');
                this.classOptions = res.data;
            } catch (err) {
                this.error = '获取班级列表失败';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        // 根据班级获取学生
        async fetchStudentsByClass() {
            if (!this.selectedClassId) return;

            try {
                this.loading = true;
                this.loadingMessage = '正在加载学生数据...';
                const res = await axios.get(`/api/classes/${this.selectedClassId}/students`);
                this.studentOptions = res.data;
                this.selectedStudents = [];
            } catch (err) {
                this.error = '获取学生列表失败';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        // 生成试卷
        async generatePaper() {
            if (!this.selectedClassId || this.selectedStudents.length === 0) {
                this.error = '请先选择班级和学生';
                return;
            }

            try {
                this.generatingPaper = true;
                this.loading = true;
                this.loadingMessage = '正在生成试卷...';

                const payload = {
                    ...this.paperConfig,
                    studentIds: this.selectedStudents
                };

                const res = await axios.post('/api/papers/generate', payload);
                this.generatedPaper = res.data;
                this.paperGenerated = true;
                this.analysisReport = null;
                this.error = null;

                this.$toast.add({
                    severity: 'success',
                    summary: '试卷生成成功',
                    detail: '试卷已生成，可以导出或继续生成分析报告',
                    life: 3000
                });
            } catch (err) {
                this.error = '试卷生成失败';
                console.error(err);
            } finally {
                this.generatingPaper = false;
                this.loading = false;
            }
        },

        // 生成分析报告
        async generateAnalysisReport() {
            try {
                this.analyzing = true;
                this.loading = true;
                this.loadingMessage = '正在生成分析报告...';

                const res = await axios.get(`/api/papers/${this.generatedPaper.paperId}/analysis`);
                this.analysisReport = res.data;
                this.error = null;

                this.$toast.add({
                    severity: 'success',
                    summary: '分析报告生成成功',
                    detail: '可以查看详细分析或导出报告',
                    life: 3000
                });
            } catch (err) {
                this.error = '分析报告生成失败';
                console.error(err);
            } finally {
                this.analyzing = false;
                this.loading = false;
            }
        },

        // 导出试卷
        exportPaper() {
            if (!this.generatedPaper) return;

            const docContent = this.generatePaperDocument(this.generatedPaper);
            const blob = new Blob([docContent], { type: 'text/plain;charset=utf-8' });
            saveAs(blob, `${this.generatedPaper.paperName}.txt`);
        },

        // 生成试卷文档内容
        generatePaperDocument(paper) {
            let content = `试卷名称: ${paper.paperName}\n`;
            content += `考试时长: ${paper.duration}分钟\n`;
            content += `难度: ${this.getDifficultyLabel(paper.difficulty)}\n\n`;

            content += '试题部分:\n\n';
            paper.questions.forEach((q, index) => {
                content += `${index + 1}. ${q.content}\n`;
                if (q.options && q.options.length > 0) {
                    q.options.forEach((opt, optIndex) => {
                        content += `   ${String.fromCharCode(65 + optIndex)}. ${opt}\n`;
                    });
                }
                content += `   [分值: ${q.score}分 | 难度: ${q.difficulty}]\n\n`;
            });

            return content;
        },

        // 导出答案
        exportAnswerKey() {
            if (!this.generatedPaper) return;

            let content = `试卷答案: ${this.generatedPaper.paperName}\n\n`;
            this.generatedPaper.questions.forEach((q, index) => {
                content += `${index + 1}. ${q.correctAnswer}\n`;
            });

            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            saveAs(blob, `${this.generatedPaper.paperName}-答案.txt`);
        },

        // 导出分析报告
        exportAnalysisReport() {
            if (!this.analysisReport) return;

            // 创建工作簿
            const wb = XLSX.utils.book_new();

            // 添加总体统计表
            const overallData = [
                ['统计项', '值'],
                ['平均分', this.analysisReport.overall.averageScore.toFixed(1)],
                ['最高分', this.analysisReport.overall.highestScore],
                ['最低分', this.analysisReport.overall.lowestScore],
                ['及格率', `${this.analysisReport.overall.passRate}%`],
                ['参考人数', this.analysisReport.studentScores.length]
            ];
            const overallWS = XLSX.utils.aoa_to_sheet(overallData);
            XLSX.utils.book_append_sheet(wb, overallWS, '总体统计');

            // 添加学生成绩表
            const studentData = [
                ['排名', '学号', '姓名', '总分', '得分率']
            ].concat(
                this.analysisReport.studentScores.map(s => [
                    s.rank,
                    s.studentId,
                    s.studentName,
                    s.totalScore,
                    `${s.scoreRate}%`
                ])
            );
            const studentWS = XLSX.utils.aoa_to_sheet(studentData);
            XLSX.utils.book_append_sheet(wb, studentWS, '学生成绩');

            // 添加题目分析表
            const questionData = [
                ['题号', '题目内容', '难度', '满分', '平均得分', '正确率']
            ].concat(
                this.analysisReport.questionAnalysis.map(q => [
                    q.questionId,
                    q.content,
                    q.difficulty,
                    q.fullScore,
                    q.averageScore.toFixed(1),
                    `${q.correctRate}%`
                ])
            );
            const questionWS = XLSX.utils.aoa_to_sheet(questionData);
            XLSX.utils.book_append_sheet(wb, questionWS, '题目分析');

            // 导出Excel文件
            XLSX.writeFile(wb, `${this.generatedPaper.paperName}-学情分析.xlsx`);
        },

        // 查看学生详情
        async viewStudentDetail(studentId) {
            try {
                this.loading = true;
                const res = await axios.get(`/api/papers/${this.generatedPaper.paperId}/students/${studentId}/details`);
                this.selectedStudentDetail = res.data;
                this.showStudentDetail = true;
            } catch (err) {
                this.error = '获取学生详情失败';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        // 辅助方法
        getDifficultyLabel(difficulty) {
            const map = {
                easy: '简单',
                medium: '中等',
                hard: '困难'
            };
            return map[difficulty] || difficulty;
        },

        getDifficultySeverity(difficulty) {
            switch (difficulty) {
                case '简单': return 'success';
                case '中等': return 'warning';
                case '困难': return 'danger';
                default: return 'info';
            }
        }
    }
};
</script>

<style scoped>
.learning-analysis {
    max-width: 1400px;
    margin: 0 auto;
    padding: 1.5rem;
}

.header-section {
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 1rem;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.25rem;
}

.section-subtitle {
    font-size: 0.875rem;
    color: #6b7280;
}

.control-section {
    background-color: #ffffff;
}

.paper-preview, .analysis-report {
    animation: fadeIn 0.3s ease-in-out;
}

.stat-item {
    transition: all 0.2s ease;
}

.stat-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.question-item:hover {
    background-color: #f9fafb;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
