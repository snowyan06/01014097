<template>
    <div class="student-exercises">
        <!-- 标题区域 -->
        <div class="header-section">
            <div class="header-content">
                <div class="title-group">
                    <div class="icon-wrapper">
                        <i class="pi pi-chart-line"></i>
                    </div>
                    <div>
                        <h3 class="section-title">学生练习分析</h3>
                        <p class="section-subtitle">跟踪和分析学生的练习表现数据</p>
                    </div>
                </div>
                <div class="header-decoration">
                    <div class="decoration-circle circle-1"></div>
                    <div class="decoration-circle circle-2"></div>
                    <div class="decoration-circle circle-3"></div>
                </div>
            </div>
        </div>

        <!-- 控制区域 -->
        <div class="control-section">
            <div class="control-content">
                <!-- 学生选择 -->
                <div class="student-selector">
                    <label class="control-label">
                        <i class="pi pi-user label-icon"></i>
                        选择学生
                    </label>
                    <div class="selector-group">
                        <Dropdown
                            v-model="selectedUserId"
                            :options="userOptions"
                            optionLabel="nickname"
                            optionValue="userId"
                            placeholder="请选择学生..."
                            class="custom-dropdown"
                            @change="fetchExercises"
                        />
                        <Button
                            icon="pi pi-list"
                            class="list-button"
                            @click="fetchAllExercises"
                            :disabled="loading"
                            v-tooltip.top="'查看全部学生数据'"
                        />
                    </div>
                </div>

                <!-- 统计摘要 -->
                <div class="stats-summary" v-if="exercises.length > 0">
                    <div class="stat-item">
                        <div class="stat-icon total-icon">
                            <i class="pi pi-book"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">总练习数</div>
                            <div class="stat-value">{{ stats.total }}</div>
                        </div>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat-item">
                        <div class="stat-icon accuracy-icon">
                            <i class="pi pi-check-circle"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">正确率</div>
                            <div class="stat-value">{{ stats.accuracy }}%</div>
                        </div>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat-item">
                        <div class="stat-icon difficulty-icon">
                            <i class="pi pi-star"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">平均难度</div>
                            <div class="stat-value">{{ stats.avgDifficulty }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
            <div class="loading-content">
                <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="3" />
                <p class="loading-text">正在加载数据...</p>
            </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="error-container">
            <Message severity="error" class="custom-error" :closable="false">
                <div class="error-content">
                    <i class="pi pi-exclamation-triangle error-icon"></i>
                    <span>{{ error }}</span>
                </div>
            </Message>
        </div>

        <!-- 数据区域 -->
        <div v-if="exercises.length > 0" class="data-section">
            <!-- 统计卡片 (移动端显示) -->
            <div class="mobile-stats">
                <div class="mobile-stat-card">
                    <div class="mobile-stat-icon total-bg">
                        <i class="pi pi-book"></i>
                    </div>
                    <div class="mobile-stat-info">
                        <div class="mobile-stat-label">总练习数</div>
                        <div class="mobile-stat-value">{{ stats.total }}</div>
                    </div>
                </div>
                <div class="mobile-stat-card">
                    <div class="mobile-stat-icon accuracy-bg">
                        <i class="pi pi-check-circle"></i>
                    </div>
                    <div class="mobile-stat-info">
                        <div class="mobile-stat-label">正确率</div>
                        <div class="mobile-stat-value">{{ stats.accuracy }}%</div>
                    </div>
                </div>
                <div class="mobile-stat-card">
                    <div class="mobile-stat-icon difficulty-bg">
                        <i class="pi pi-star"></i>
                    </div>
                    <div class="mobile-stat-info">
                        <div class="mobile-stat-label">平均难度</div>
                        <div class="mobile-stat-value">{{ stats.avgDifficulty }}</div>
                    </div>
                </div>
            </div>

            <!-- 数据表格 -->
            <div class="table-card">
                <div class="table-header">
                    <div class="table-title-group">
                        <div class="table-icon">
                            <i class="pi pi-table"></i>
                        </div>
                        <div>
                            <h4 class="table-title">
                                {{ selectedUserId ? `${selectedUserNickname} 的练习记录` : '所有学生练习记录' }}
                            </h4>
                            <p class="table-subtitle">共 {{ exercises.length }} 条记录</p>
                        </div>
                    </div>
                    <Button
                        icon="pi pi-download"
                        class="export-button"
                        label="导出数据"
                        @click="exportData"
                    />
                </div>

                <div class="table-content">
                    <DataTable
                        :value="exercises"
                        :paginator="true"
                        :rows="10"
                        :rowsPerPageOptions="[10, 20, 50]"
                        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                        currentPageReportTemplate="显示 {first} 到 {last} / 共 {totalRecords} 条记录"
                        responsiveLayout="scroll"
                        class="custom-table"
                    >
                        <Column field="nickname" header="学生昵称" v-if="!selectedUserId" class="font-medium">
                            <template #body="{ data }">
                                <div class="student-cell">
                                    <div class="student-avatar">
                                        <i class="pi pi-user"></i>
                                    </div>
                                    <span class="student-name">{{ data.nickname }}</span>
                                </div>
                            </template>
                        </Column>
                        <Column field="questionContent" header="题目内容" style="width: 40%">
                            <template #body="{ data }">
                                <div class="question-content">
                                    {{ data.questionContent }}
                                </div>
                            </template>
                        </Column>
                        <Column field="difficulty" header="难度" style="width: 120px">
                            <template #body="{ data }">
                                <Tag :value="data.difficulty"
                                     :class="getDifficultyClass(data.difficulty)"
                                     class="difficulty-tag">
                                    <i :class="getDifficultyIcon(data.difficulty)" class="tag-icon"></i>
                                    {{ data.difficulty }}
                                </Tag>
                            </template>
                        </Column>
                        <Column header="结果" style="width: 100px">
                            <template #body="{ data }">
                                <Tag :class="data.isCorrect ? 'result-correct' : 'result-wrong'"
                                     class="result-tag">
                                    <i :class="data.isCorrect ? 'pi pi-check' : 'pi pi-times'" class="tag-icon"></i>
                                    {{ data.isCorrect ? '正确' : '错误' }}
                                </Tag>
                            </template>
                        </Column>
                        <Column header="练习时间" style="width: 160px">
                            <template #body="{ data }">
                                <div class="time-cell">
                                    <i class="pi pi-clock time-icon"></i>
                                    <span class="time-text">{{ formatDate(data.answeredAt) }}</span>
                                </div>
                            </template>
                        </Column>
                    </DataTable>
                </div>

            <!-- 图表区域 -->
            <div class="chart-section">
                <!-- 正确率趋势图 -->
                <div class="chart-card trend-card">
                    <div class="chart-header">
                        <div class="chart-title-group">
                            <div class="chart-icon trend-icon">
                                <i class="pi pi-chart-line"></i>
                            </div>
                            <h4 class="chart-title">正确率趋势</h4>
                        </div>
                        <div class="chart-decoration"></div>
                    </div>
                    <div class="chart-content">
                        <Chart
                            type="line"
                            :data="accuracyTrendData"
                            :options="accuracyTrendOptions"
                            height="300px"
                        />
                    </div>
                </div>

                <!-- 难度分布图 -->
                <div class="chart-card distribution-card">
                    <div class="chart-header">
                        <div class="chart-title-group">
                            <div class="chart-icon distribution-icon">
                                <i class="pi pi-chart-pie"></i>
                            </div>
                            <h4 class="chart-title">题目难度分布</h4>
                        </div>
                        <div class="chart-decoration"></div>
                    </div>
                    <div class="chart-content">
                        <Chart
                            type="pie"
                            :data="difficultyDistributionData"
                            :options="difficultyDistributionOptions"
                            height="300px"
                        />
                    </div>
                </div>

                <!-- 正确率与难度关系图 -->
                <div class="chart-card analysis-card full-width">
                    <div class="chart-header">
                        <div class="chart-title-group">
                            <div class="chart-icon analysis-icon">
                                <i class="pi pi-chart-bar"></i>
                            </div>
                            <h4 class="chart-title">各难度正确率分析</h4>
                        </div>
                        <div class="chart-decoration"></div>
                    </div>
                    <div class="chart-content">
                        <Chart
                            type="bar"
                            :data="accuracyByDifficultyData"
                            :options="accuracyByDifficultyOptions"
                            height="300px"
                        />
                    </div>
                </div>
            </div>

            </div>
        </div>

        <!-- 无数据提示 -->
        <div v-else-if="!loading && !error" class="empty-state">
            <div class="empty-content">
                <div class="empty-icon">
                    <i class="pi pi-inbox"></i>
                </div>
                <h3 class="empty-title">暂无练习记录</h3>
                <p class="empty-description">当前没有找到任何练习数据</p>
                <Button
                    label="刷新数据"
                    icon="pi pi-refresh"
                    class="refresh-button"
                    @click="selectedUserId ? fetchExercises() : fetchAllExercises()"
                />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Chart from 'primevue/chart';

export default {
    name: 'StudentExercises',
    components: {
        Chart
    },
    data() {
        return {
            selectedUserId: null,
            selectedUserNickname: '',
            userOptions: [],
            exercises: [],
            loading: true,
            error: null,
            stats: {
                total: 0,
                accuracy: 0,
                avgDifficulty: '-'
            },
            // 图表数据
            accuracyTrendData: null,
            accuracyTrendOptions: null,
            difficultyDistributionData: null,
            difficultyDistributionOptions: null,
            accuracyByDifficultyData: null,
            accuracyByDifficultyOptions: null
        };
    },
    async created() {
        try {
            await Promise.all([
                this.fetchUserList(),
                this.fetchAllExercises()
            ]);
        } catch (err) {
            this.error = '初始化数据加载失败';
            console.error(err);
        } finally {
            this.loading = false;
        }
    },
    methods: {
        async fetchUserList() {
            try {
                const res = await axios.get('http://localhost:8080/api/user-answers/user-stats-with-nickname');
                this.userOptions = [
                    { userId: null, nickname: '选择学生...' },
                    ...res.data
                ];
            } catch (err) {
                console.error('获取学生列表失败:', err);
                throw err;
            }
        },

        async fetchExercises() {
            if (!this.selectedUserId) {
                await this.fetchAllExercises();
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const res = await axios.get(`http://localhost:8080/api/user-answers/user/${this.selectedUserId}/with-nickname`);
                this.exercises = res.data;
                console.log(res.data)
                const selectedUser = this.userOptions.find(u => u.userId === this.selectedUserId);
                this.selectedUserNickname = selectedUser ? selectedUser.nickname : '';
                this.calculateStats();
            } catch (err) {
                this.error = '获取练习数据失败，请检查网络或 ID 是否存在。';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        async fetchAllExercises() {
            this.loading = true;
            this.error = null;
            this.selectedUserId = null;
            this.selectedUserNickname = '';

            try {
                const res = await axios.get('http://localhost:8080/api/user-answers/with-nickname');
                this.exercises = res.data;
                this.calculateStats();
            } catch (err) {
                this.error = '获取全部练习数据失败';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        calculateStats() {
            if (this.exercises.length === 0) {
                this.stats = { total: 0, accuracy: 0, avgDifficulty: '-' };
                return;
            }

            this.stats.total = this.exercises.length;

            const correctCount = this.exercises.filter(e => e.isCorrect).length;
            this.stats.accuracy = ((correctCount / this.stats.total) * 100).toFixed(1);

            const difficulties = {
                '简单': 1,
                '中等': 2,
                '困难': 3
            };

            const totalScore = this.exercises.reduce((sum, ex) => sum + (difficulties[ex.difficulty] || 0), 0);
            const avgScore = totalScore / this.stats.total;

            if (avgScore < 1.5) {
                this.stats.avgDifficulty = '简单';
            } else if (avgScore < 2.5) {
                this.stats.avgDifficulty = '中等';
            } else {
                this.stats.avgDifficulty = '困难';
            }

            // 准备图表数据
            this.prepareChartData();
        },

        prepareChartData() {
            this.prepareAccuracyTrendData();
            this.prepareDifficultyDistributionData();
            this.prepareAccuracyByDifficultyData();
        },

        prepareAccuracyTrendData() {
            // 按日期分组数据
            const dateGroups = {};
            this.exercises.forEach(ex => {
                const date = new Date(ex.answeredAt).toLocaleDateString();
                if (!dateGroups[date]) {
                    dateGroups[date] = {
                        total: 0,
                        correct: 0
                    };
                }
                dateGroups[date].total++;
                if (ex.isCorrect) dateGroups[date].correct++;
            });

            // 准备图表数据
            const sortedDates = Object.keys(dateGroups).sort();
            const accuracyRates = sortedDates.map(date => {
                const group = dateGroups[date];
                return (group.correct / group.total * 100).toFixed(1);
            });

            this.accuracyTrendData = {
                labels: sortedDates,
                datasets: [
                    {
                        label: '正确率 (%)',
                        data: accuracyRates,
                        fill: false,
                        borderColor: '#5B9BD5',
                        backgroundColor: 'rgba(91, 155, 213, 0.1)',
                        tension: 0.4,
                        borderWidth: 3,
                        pointBackgroundColor: '#5B9BD5',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    }
                ]
            };

            this.accuracyTrendOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        titleColor: '#374151',
                        bodyColor: '#6B7280',
                        borderColor: '#E5E7EB',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return `正确率: ${context.raw}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        grid: {
                            color: '#F3F4F6',
                            borderColor: '#E5E7EB'
                        },
                        ticks: {
                            color: '#6B7280',
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#6B7280'
                        }
                    }
                }
            };
        },

        prepareDifficultyDistributionData() {
            const difficultyCounts = {
                '简单': 0,
                '中等': 0,
                '困难': 0
            };

            this.exercises.forEach(ex => {
                difficultyCounts[ex.difficulty]++;
            });

            this.difficultyDistributionData = {
                labels: Object.keys(difficultyCounts),
                datasets: [
                    {
                        data: Object.values(difficultyCounts),
                        backgroundColor: [
                            '#A3E4D7', // 简单 - 浅绿色
                            '#F9E79F', // 中等 - 浅黄色
                            '#F5B7B1'  // 困难 - 浅红色
                        ],
                        borderColor: [
                            '#52C3A3',
                            '#F1C40F',
                            '#E74C3C'
                        ],
                        borderWidth: 2,
                        hoverBackgroundColor: [
                            '#85E0C7',
                            '#F7DC6F',
                            '#F1948A'
                        ]
                    }
                ]
            };

            this.difficultyDistributionOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#374151',
                            padding: 20,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        titleColor: '#374151',
                        bodyColor: '#6B7280',
                        borderColor: '#E5E7EB',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const value = context.raw;
                                const percentage = Math.round((value / total) * 100);
                                return `${context.label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            };
        },

        prepareAccuracyByDifficultyData() {
            const difficultyGroups = {
                '简单': { total: 0, correct: 0 },
                '中等': { total: 0, correct: 0 },
                '困难': { total: 0, correct: 0 }
            };

            this.exercises.forEach(ex => {
                difficultyGroups[ex.difficulty].total++;
                if (ex.isCorrect) difficultyGroups[ex.difficulty].correct++;
            });

            const labels = Object.keys(difficultyGroups);
            const accuracyData = labels.map(difficulty => {
                const group = difficultyGroups[difficulty];
                return group.total > 0 ? (group.correct / group.total * 100).toFixed(1) : 0;
            });

            this.accuracyByDifficultyData = {
                labels: labels,
                datasets: [
                    {
                        label: '正确率 (%)',
                        data: accuracyData,
                        backgroundColor: [
                            'rgba(163, 228, 215, 0.8)', // 简单
                            'rgba(249, 231, 159, 0.8)',  // 中等
                            'rgba(245, 183, 177, 0.8)'   // 困难
                        ],
                        borderColor: [
                            '#52C3A3', // 简单
                            '#F1C40F', // 中等
                            '#E74C3C'  // 困难
                        ],
                        borderWidth: 2,
                        borderRadius: 4
                    }
                ]
            };

            this.accuracyByDifficultyOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        titleColor: '#374151',
                        bodyColor: '#6B7280',
                        borderColor: '#E5E7EB',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                const difficulty = context.label;
                                const group = difficultyGroups[difficulty];
                                return `${difficulty}: ${context.raw}% (${group.correct}/${group.total})`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        grid: {
                            color: '#F3F4F6',
                            borderColor: '#E5E7EB'
                        },
                        ticks: {
                            color: '#6B7280',
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#6B7280'
                        }
                    }
                }
            };
        },

        getDifficultySeverity(difficulty) {
            switch (difficulty) {
                case '简单':
                    return 'success';
                case '中等':
                    return 'warning';
                case '困难':
                    return 'danger';
                default:
                    return 'info';
            }
        },

        getDifficultyClass(difficulty) {
            switch (difficulty) {
                case '简单':
                    return 'difficulty-easy';
                case '中等':
                    return 'difficulty-medium';
                case '困难':
                    return 'difficulty-hard';
                default:
                    return 'difficulty-unknown';
            }
        },

        getDifficultyIcon(difficulty) {
            switch (difficulty) {
                case '简单':
                    return 'pi pi-circle';
                case '中等':
                    return 'pi pi-circle-fill';
                case '困难':
                    return 'pi pi-star-fill';
                default:
                    return 'pi pi-circle';
            }
        },

        formatDate(dateString) {
            if (!dateString) return '-';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        },

        exportData() {
            this.$toast.add({
                severity: 'info',
                summary: '导出功能',
                detail: '数据导出功能将在后续版本中提供',
                life: 3000
            });
        }
    }
};
</script>

<style scoped>
/* 全局样式 */
.student-exercises {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
    background: linear-gradient(135deg, #f9f9f9 0%, #fafafa 100%);
    min-height: 100vh;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 标题区域 */
.header-section {
    margin-bottom: 2rem;
}

.header-content {
    position: relative;
    background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(91, 155, 213, 0.1);
    border: 1px solid #e8f2ff;
    overflow: hidden;
}

.title-group {
    display: flex;
    align-items: center;
    gap: 1rem;
    position: relative;
    z-index: 2;
}

.icon-wrapper {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #5B9BD5, #4A90C2);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(91, 155, 213, 0.3);
}

.icon-wrapper i {
    color: white;
    font-size: 24px;
}

.section-title {
    font-size: 2rem;
    font-weight: 700;
    color: #2c3e50;
    margin: 0;
    background: linear-gradient(135deg, #2c3e50, #34495e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section-subtitle {
    font-size: 1rem;
    color: #7f8c8d;
    margin: 0.25rem 0 0 0;
}

.header-decoration {
    position: absolute;
    top: -50px;
    right: -50px;
    pointer-events: none;
}

.decoration-circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
}

.circle-1 {
    width: 120px;
    height: 120px;
    background: #5B9BD5;
    top: 0;
    right: 0;
}

.circle-2 {
    width: 80px;
    height: 80px;
    background: #4A90C2;
    top: 40px;
    right: 40px;
}

.circle-3 {
    width: 40px;
    height: 40px;
    background: #357ABD;
    top: 80px;
    right: 80px;
}

/* 控制区域 */
.control-section {
    background: linear-gradient(135deg, #ffffff 0%, #fafbff 100%);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 16px rgba(91, 155, 213, 0.08);
    border: 1px solid #e8f2ff;
    margin-bottom: 2rem;
}

.control-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

@media (min-width: 768px) {
    .control-content {
        flex-direction: row;
        align-items: flex-end;
        justify-content: space-between;
    }
}

/* 学生选择器 */
.student-selector {
    flex: 1;
    max-width: 400px;
}

.control-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 0.5rem;
}

.label-icon {
    color: #5B9BD5;
    font-size: 14px;
}

.selector-group {
    display: flex;
    gap: 0.75rem;
    align-items: center;
}

/* 自定义下拉框 */
:deep(.custom-dropdown) {
    flex: 1;
    min-width: 200px;
}

:deep(.custom-dropdown .p-dropdown) {
    background: white;
    border: 2px solid #e8f2ff;
    border-radius: 12px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(91, 155, 213, 0.05);
}

:deep(.custom-dropdown .p-dropdown:hover) {
    border-color: #d1e7ff;
    box-shadow: 0 4px 12px rgba(91, 155, 213, 0.1);
}

:deep(.custom-dropdown .p-dropdown.p-focus) {
    border-color: #5B9BD5;
    box-shadow: 0 0 0 3px rgba(91, 155, 213, 0.1);
}

:deep(.custom-dropdown .p-dropdown-label) {
    color: #374151;
    font-weight: 500;
}

.list-button {
    background: linear-gradient(135deg, #f8faff, #e8f2ff) !important;
    border: 2px solid #e8f2ff !important;
    color: #5B9BD5 !important;
    border-radius: 12px !important;
    width: 48px;
    height: 48px;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(91, 155, 213, 0.05) !important;
}

.list-button:hover {
    background: linear-gradient(135deg, #e8f2ff, #d1e7ff) !important;
    border-color: #5B9BD5 !important;
    box-shadow: 0 4px 12px rgba(91, 155, 213, 0.15) !important;
    transform: translateY(-1px);
}

/* 统计摘要 */
.stats-summary {
    display: none;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: linear-gradient(135deg, #ffffff, #f8faff);
    border-radius: 12px;
    border: 1px solid #e8f2ff;
    box-shadow: 0 2px 8px rgba(91, 155, 213, 0.05);
}

@media (min-width: 768px) {
    .stats-summary {
        display: flex;
    }
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 16px;
}

.total-icon {
    background: linear-gradient(135deg, #5B9BD5, #4A90C2);
}

.accuracy-icon {
    background: linear-gradient(135deg, #52C3A3, #48B396);
}

.difficulty-icon {
    background: linear-gradient(135deg, #F1C40F, #E6B800);
}

.stat-content {
    text-align: left;
}

.stat-label {
    font-size: 0.75rem;
    color: #6b7280;
    font-weight: 500;
    margin-bottom: 2px;
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2c3e50;
}

.stat-divider {
    height: 40px;
    width: 1px;
    background: #e5e7eb;
}

/* 移动端统计卡片 */
.mobile-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
    .mobile-stats {
        display: none;
    }
}

.mobile-stat-card {
    background: linear-gradient(135deg, #ffffff, #f8faff);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #e8f2ff;
    box-shadow: 0 2px 8px rgba(91, 155, 213, 0.05);
    text-align: center;
    transition: all 0.3s ease;
}

.mobile-stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(91, 155, 213, 0.1);
}

.mobile-stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem;
    color: white;
    font-size: 14px;
}

.total-bg {
    background: linear-gradient(135deg, #5B9BD5, #4A90C2);
}

.accuracy-bg {
    background: linear-gradient(135deg, #52C3A3, #48B396);
}

.difficulty-bg {
    background: linear-gradient(135deg, #F1C40F, #E6B800);
}

.mobile-stat-info {
    text-align: center;
}

.mobile-stat-label {
    font-size: 0.75rem;
    color: #6b7280;
    font-weight: 500;
    margin-bottom: 4px;
}

.mobile-stat-value {
    font-size: 1rem;
    font-weight: 700;
    color: #2c3e50;
}

/* 加载状态 */
.loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #ffffff, #f8faff);
    border-radius: 16px;
    box-shadow: 0 2px 16px rgba(91, 155, 213, 0.08);
    border: 1px solid #e8f2ff;
}

.loading-content {
    text-align: center;
}

.loading-text {
    margin-top: 1rem;
    color: #6b7280;
    font-weight: 500;
}

/* 错误提示 */
.error-container {
    margin-bottom: 2rem;
}

:deep(.custom-error) {
    border-radius: 12px;
    border: 1px solid #fecaca;
    background: linear-gradient(135deg, #fef2f2, #fef7f7);
}

.error-content {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.error-icon {
    color: #ef4444;
    font-size: 18px;
}

/* 图表区域 */
.chart-section {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

@media (min-width: 1024px) {
    .chart-section {
        grid-template-columns: repeat(2, 1fr);
    }
}

.chart-card {
    background: linear-gradient(135deg, #ffffff, #fafbff);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(91, 155, 213, 0.08);
    border: 1px solid #e8f2ff;
    overflow: hidden;
    transition: all 0.3s ease;
}

.chart-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(91, 155, 213, 0.12);
}

.full-width {
    grid-column: 1 / -1;
}

.chart-header {
    position: relative;
    padding: 1.5rem;
    background: linear-gradient(135deg, #f8faff, #ffffff);
    border-bottom: 1px solid #e8f2ff;
}

.chart-title-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.chart-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 16px;
}

.trend-icon {
    background: linear-gradient(135deg, #5B9BD5, #4A90C2);
}

.distribution-icon {
    background: linear-gradient(135deg, #52C3A3, #48B396);
}

.analysis-icon {
    background: linear-gradient(135deg, #F1C40F, #E6B800);
}

.chart-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.chart-decoration {
    position: absolute;
    top: 10px;
    right: 15px;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, #5B9BD5, #52C3A3, #F1C40F);
    border-radius: 2px;
    opacity: 0.3;
}

.chart-content {
    padding: 1.5rem;
}

/* 表格区域 */
.table-card {
    background: linear-gradient(135deg, #ffffff, #fafbff);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(91, 155, 213, 0.08);
    border: 1px solid #e8f2ff;
    overflow: hidden;
}

.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #f8faff, #ffffff);
    border-bottom: 1px solid #e8f2ff;
}

.table-title-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.table-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #5B9BD5, #4A90C2);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 16px;
}

.table-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
}

.table-subtitle {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0.25rem 0 0 0;
}

.export-button {
    background: linear-gradient(135deg, #f8faff, #e8f2ff) !important;
    border: 2px solid #e8f2ff !important;
    color: #5B9BD5 !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(91, 155, 213, 0.05) !important;
}

.export-button:hover {
    background: linear-gradient(135deg, #e8f2ff, #d1e7ff) !important;
    border-color: #5B9BD5 !important;
    box-shadow: 0 4px 12px rgba(91, 155, 213, 0.15) !important;
    transform: translateY(-1px);
}

.table-content {
    overflow: hidden;
}

/* 表格样式 */
:deep(.custom-table) {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    border: none;
}

:deep(.custom-table .p-datatable-thead > tr > th) {
    background: linear-gradient(135deg, #f8faff, #f1f7ff);
    color: #374151;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    border: none;
    border-bottom: 2px solid #e8f2ff;
    padding: 1rem;
}

:deep(.custom-table .p-datatable-tbody > tr > td) {
    padding: 1rem;
    border: none;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
}

:deep(.custom-table .p-datatable-tbody > tr:hover > td) {
    background: linear-gradient(135deg, #fafbff, #f8faff);
}

:deep(.custom-table .p-datatable-tbody > tr:nth-child(even) > td) {
    background: rgba(248, 250, 255, 0.3);
}

/* 学生头像单元格 */
.student-cell {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.student-avatar {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #5B9BD5, #4A90C2);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 12px;
}

.student-name {
    font-weight: 500;
    color: #2c3e50;
}

/* 题目内容 */
.question-content {
    max-width: 300px;
    line-height: 1.5;
    color: #374151;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* 难度标签 */
.difficulty-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.375rem 0.75rem;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.difficulty-easy {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    color: #047857;
    border-color: #a7f3d0;
}

.difficulty-medium {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    color: #92400e;
    border-color: #fde68a;
}

.difficulty-hard {
    background: linear-gradient(135deg, #fecaca, #fca5a5);
    color: #dc2626;
    border-color: #fca5a5;
}

.difficulty-unknown {
    background: linear-gradient(135deg, #e5e7eb, #d1d5db);
    color: #4b5563;
    border-color: #d1d5db;
}

/* 结果标签 */
.result-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.375rem 0.75rem;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.result-correct {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    color: #047857;
    border-color: #a7f3d0;
}

.result-wrong {
    background: linear-gradient(135deg, #fecaca, #fca5a5);
    color: #dc2626;
    border-color: #fca5a5;
}

.tag-icon {
    font-size: 10px;
}

/* 时间单元格 */
.time-cell {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
}

.time-icon {
    font-size: 12px;
    color: #9ca3af;
}

.time-text {
    font-size: 0.75rem;
}

/* 分页样式 */
:deep(.custom-table .p-paginator) {
    background: linear-gradient(135deg, #fafbff, #f8faff);
    border: none;
    border-top: 1px solid #e8f2ff;
    padding: 1rem 1.5rem;
}

:deep(.custom-table .p-paginator .p-paginator-pages .p-paginator-page) {
    background: transparent;
    border: 1px solid #e8f2ff;
    color: #6b7280;
    border-radius: 6px;
    margin: 0 2px;
    transition: all 0.2s ease;
}

:deep(.custom-table .p-paginator .p-paginator-pages .p-paginator-page:hover) {
    background: #f8faff;
    border-color: #d1e7ff;
}

:deep(.custom-table .p-paginator .p-paginator-pages .p-paginator-page.p-highlight) {
    background: linear-gradient(135deg, #5B9BD5, #4A90C2);
    color: white;
    border-color: #5B9BD5;
}

/* 空状态 */
.empty-state {
    background: linear-gradient(135deg, #ffffff, #f8faff);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(91, 155, 213, 0.08);
    border: 1px solid #e8f2ff;
    padding: 4rem 2rem;
    text-align: center;
}

.empty-content {
    max-width: 400px;
    margin: 0 auto;
}

.empty-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    font-size: 32px;
}

.empty-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0 0 0.5rem 0;
}

.empty-description {
    color: #6b7280;
    margin: 0 0 1.5rem 0;
    line-height: 1.5;
}

.refresh-button {
    background: linear-gradient(135deg, #5B9BD5, #4A90C2) !important;
    border: none !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 16px rgba(91, 155, 213, 0.3) !important;
}

.refresh-button:hover {
    background: linear-gradient(135deg, #4A90C2, #357ABD) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(91, 155, 213, 0.4) !important;
}

/* 动画效果 */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.data-section {
    animation: fadeIn 0.6s ease-out;
}

.chart-section {
    animation: fadeIn 0.8s ease-out;
}

.table-card {
    animation: fadeIn 1s ease-out;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .student-exercises {
        padding: 1rem;
    }

    .header-content {
        padding: 1.5rem;
    }

    .section-title {
        font-size: 1.5rem;
    }

    .icon-wrapper {
        width: 50px;
        height: 50px;
    }

    .icon-wrapper i {
        font-size: 20px;
    }

    .control-section {
        padding: 1rem;
    }

    .chart-content {
        padding: 1rem;
    }

    .table-header {
        flex-direction: column;
        gap: 1rem;
        align-items: flex-start;
    }

    .table-title-group {
        width: 100%;
    }

    .export-button {
        width: 100%;
        justify-content: center;
    }
}

/* 打印样式 */
@media print {
    .student-exercises {
        background: white;
        box-shadow: none;
    }

    .chart-card,
    .table-card,
    .control-section {
        box-shadow: none;
        border: 1px solid #e5e7eb;
    }

    .export-button,
    .list-button,
    .refresh-button {
        display: none;
    }
}

</style>
