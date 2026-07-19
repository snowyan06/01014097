<template>
    <div class="student-learning-stats">
        <div class="stats-container">
            <!-- 标题区域 -->
            <div class="stats-header">
                <div class="header-content">
                    <h1 class="page-title">
                        <span class="title-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9 11L12 14L22 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </span>
                        学生学习统计
                    </h1>
                    <p class="page-subtitle">全面追踪学生表现，优化教学策略</p>
                </div>
                <div v-if="selectedUserId" class="current-student">
                    <span class="current-label">当前查看：</span>
                    <div class="student-tag">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="tag-icon">
                            <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        {{ user.nickname }}
                    </div>
                </div>
            </div>

            <!-- 学生列表 -->
            <div v-if="!selectedUserId" class="students-list-container">
                <div class="list-header">
                    <div class="header-icon">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M9 11C11.2091 11 13 9.20914 13 7C13 4.79086 11.2091 3 9 3C6.79086 3 5 4.79086 5 7C5 9.20914 6.79086 11 9 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="list-title">学生列表</h3>
                        <p class="list-subtitle">点击查看详情分析学生表现</p>
                    </div>
                </div>
                <div class="students-table">
                    <DataTable :value="students" class="custom-datatable" :paginator="true" :rows="10"
                               paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                               currentPageReportTemplate="显示 {first} 到 {last} 共 {totalRecords} 名学生"
                               :rowsPerPageOptions="[5,10,20]"
                               responsiveLayout="scroll">
                        <Column field="userId" header="用户ID" :sortable="true"></Column>
                        <Column field="nickname" header="昵称" :sortable="true"></Column>
                        <Column header="操作">
                            <template #body="slotProps">
                                <button class="analysis-btn" @click="selectStudent(slotProps.data.userId)">
                                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M3 12H7L10 5L14 19L17 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                    分析报告
                                </button>
                            </template>
                        </Column>
                    </DataTable>
                </div>
            </div>

            <!-- 学生详情 -->
            <div v-else class="student-details">
                <button class="back-btn" @click="backToList">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    返回列表
                </button>

                <!-- 用户信息卡片 -->
                <div class="user-info-card">
                    <div class="card-header">
                        <div class="card-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <h3 class="card-title">用户信息</h3>
                    </div>
                    <div class="info-grid">
                        <div class="info-item">
                            <p class="info-label">用户ID</p>
                            <p class="info-value">{{ user.userId }}</p>
                        </div>
                        <div class="info-item">
                            <p class="info-label">昵称</p>
                            <p class="info-value">{{ user.nickname }}</p>
                        </div>
                        <div class="info-item">
                            <p class="info-label">总答题数</p>
                            <p class="info-value">
                                {{ correctRateTrend.reduce((sum, item) => sum + item.totalAnswers, 0) }}
                            </p>
                        </div>
                        <div class="info-item">
                            <p class="info-label">平均正确率</p>
                            <p class="info-value" :class="'rate-' + (getAverageCorrectRate() >= 70 ? 'high' : getAverageCorrectRate() >= 50 ? 'medium' : 'low')">
                                {{ getAverageCorrectRate().toFixed(1) }}%
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 数据分析区域 -->
                <div class="analysis-grid">
                    <!-- 正确率趋势 -->
                    <div class="analysis-card">
                        <div class="card-header">
                            <div class="card-icon trend-icon">
                                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M3 12H7L10 5L14 19L17 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                            <h3 class="card-title">正确率趋势分析</h3>
                        </div>
                        <div class="chart-container">
                            <Chart type="line" :data="chartData" :options="chartOptions" />
                        </div>
                        <div class="data-table-wrapper">
                            <DataTable :value="correctRateTrend" class="trend-table"
                                       :paginator="true" :rows="5" responsiveLayout="scroll">
                                <Column field="date" header="日期" :sortable="true"></Column>
                                <Column field="totalAnswers" header="答题数" :sortable="true"></Column>
                                <Column field="correctRate" header="正确率" :sortable="true">
                                    <template #body="slotProps">
                                        <div class="rate-cell">
                                            <span :class="'rate-value rate-' + (slotProps.data.correctRate >= 70 ? 'high' : slotProps.data.correctRate >= 50 ? 'medium' : 'low')">
                                                {{ slotProps.data.correctRate }}%
                                            </span>
                                            <svg v-if="slotProps.data.correctRate >= 70" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="rate-icon rate-high">
                                                <path d="M7 14L12 9L17 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            </svg>
                                            <svg v-else-if="slotProps.data.correctRate >= 50" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="rate-icon rate-medium">
                                                <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            </svg>
                                            <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="rate-icon rate-low">
                                                <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                            </svg>
                                        </div>
                                    </template>
                                </Column>
                            </DataTable>
                        </div>
                    </div>

                    <!-- 题型答题表现 -->
                    <div class="analysis-card">
                        <div class="card-header">
                            <div class="card-icon mastery-icon">
                                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4 19V5C4 4.44772 4.44772 4 5 4H9C9.55228 4 10 4.44772 10 5V19C10 19.5523 9.55228 20 9 20H5C4.44772 20 4 19.5523 4 19Z" stroke="currentColor" stroke-width="2"/>
                                    <path d="M14 19V9C14 8.44772 14.4477 8 15 8H19C19.5523 8 20 8.44772 20 9V19C20 19.5523 19.5523 20 19 20H15C14.4477 20 14 19.5523 14 19Z" stroke="currentColor" stroke-width="2"/>
                                </svg>
                            </div>
                            <h3 class="card-title">题型答题表现</h3>
                        </div>
                        <div class="chart-container">
                            <Chart type="bar" :data="masteryChartData" :options="masteryChartOptions" />
                        </div>
                        <div class="data-table-wrapper">
                            <DataTable :value="knowledgeMastery" class="mastery-table"
                                       :paginator="true" :rows="5" responsiveLayout="scroll">
                                <Column field="questionType" header="题型" :sortable="true"></Column>
                                <Column field="totalQuestions" header="题目数" :sortable="true"></Column>
                                <Column field="masteryRate" header="准确率" :sortable="true">
                                    <template #body="slotProps">
                                        <div class="mastery-cell">
                                            <div class="mastery-bar">
                                                <div class="mastery-progress"
                                                     :class="'progress-' + (slotProps.data.masteryRate >= 70 ? 'high' : slotProps.data.masteryRate >= 50 ? 'medium' : 'low')"
                                                     :style="{width: slotProps.data.masteryRate + '%'}">
                                                </div>
                                            </div>
                                            <span class="mastery-value"
                                                  :class="'rate-' + (slotProps.data.masteryRate >= 70 ? 'high' : slotProps.data.masteryRate >= 50 ? 'medium' : 'low')">
                                                {{ slotProps.data.masteryRate }}%
                                            </span>
                                        </div>
                                    </template>
                                </Column>
                            </DataTable>
                        </div>
                    </div>
                </div>

                <!-- 高频错误知识点 -->
                <div class="errors-card">
                    <div class="card-header">
                        <div class="card-icon error-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M10.29 3.86L1.82 18C1.64537 18.3024 1.55296 18.6453 1.55199 18.9945C1.55101 19.3437 1.64149 19.6871 1.81442 19.9905C1.98735 20.2939 2.23673 20.5467 2.53771 20.7238C2.83869 20.901 3.18047 20.9962 3.53 21H20.47C20.8195 20.9962 21.1613 20.901 21.4623 20.7238C21.7633 20.5467 22.0126 20.2939 22.1856 19.9905C22.3585 19.6871 22.449 19.3437 22.448 18.9945C22.447 18.6453 22.3546 18.3024 22.18 18L13.71 3.86C13.5317 3.56611 13.2807 3.32313 12.9812 3.15449C12.6817 2.98585 12.3437 2.89726 12 2.89726C11.6563 2.89726 11.3183 2.98585 11.0188 3.15449C10.7193 3.32313 10.4683 3.56611 10.29 3.86Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M12 9V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M12 17H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="card-title">高频错误知识点</h3>
                            <p class="card-subtitle">需要重点关注的薄弱环节</p>
                        </div>
                    </div>
                    <div class="errors-list">
                        <div v-for="(item, index) in frequentErrors" :key="index" class="error-item">
                            <div class="error-header">
                                <span class="error-index">错误点 {{ index + 1 }}</span>
                                <span class="error-count">错误 {{ item.errorCount }} 次</span>
                            </div>
                            <p class="error-question">{{ item.questionContent }}</p>
                            <p class="error-explanation">{{ item.explanation.replace(/^回答错误。/, '') }}</p>
                            <div class="error-tip">
                                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    <path d="M12 16V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    <path d="M12 8H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                                建议加强此知识点的讲解和练习
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Chart from 'primevue/chart'
import ProgressBar from 'primevue/progressbar'
import Tooltip from 'primevue/tooltip'

// 学生列表数据
const students = ref([])
const selectedUserId = ref(null)
const user = ref(null)
const correctRateTrend = ref([])
const knowledgeMastery = ref([])
const frequentErrors = ref([])

// 计算平均正确率
const getAverageCorrectRate = () => {
    if (correctRateTrend.value.length === 0) return 0
    const sum = correctRateTrend.value.reduce((acc, cur) => acc + cur.correctRate, 0)
    return sum / correctRateTrend.value.length
}

// 图表数据
const chartData = computed(() => {
    return {
        labels: correctRateTrend.value.map(item => item.date),
        datasets: [
            {
                label: '正确率 (%)',
                data: correctRateTrend.value.map(item => item.correctRate),
                fill: false,
                borderColor: '#06b6d4',
                tension: 0.4,
                backgroundColor: 'rgba(6, 182, 212, 0.1)'
            }
        ]
    }
})

const chartOptions = {
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: '#475569'
            }
        }
    },
    scales: {
        x: {
            ticks: {
                color: '#64748b'
            },
            grid: {
                color: '#f1f5f9'
            }
        },
        y: {
            min: 0,
            max: 100,
            ticks: {
                color: '#64748b',
                callback: function(value) {
                    return value + '%'
                }
            },
            grid: {
                color: '#f1f5f9'
            }
        }
    }
}

const masteryChartData = computed(() => {
    return {
        labels: knowledgeMastery.value.map(item => item.questionType),
        datasets: [
            {
                label: '准确率 (%)',
                data: knowledgeMastery.value.map(item => item.masteryRate),
                backgroundColor: knowledgeMastery.value.map(item =>
                    item.masteryRate >= 70 ? '#10b981' :
                        item.masteryRate >= 50 ? '#06b6d4' : '#64748b'
                )
            }
        ]
    }
})

const masteryChartOptions = {
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: '#475569'
            }
        }
    },
    scales: {
        x: {
            ticks: {
                color: '#64748b'
            },
            grid: {
                color: '#f1f5f9'
            }
        },
        y: {
            min: 0,
            max: 100,
            ticks: {
                color: '#64748b',
                callback: function(value) {
                    return value + '%'
                }
            },
            grid: {
                color: '#f1f5f9'
            }
        }
    }
}

// 获取所有学生列表
const fetchStudents = async () => {
    try {
        const res = await axios.get('http://localhost:8080/api/user-answers/with-nickname')
        const uniqueUsers = Object.values(
            res.data.reduce((acc, cur) => {
                acc[cur.userId] = cur
                return acc
            }, {})
        )
        students.value = uniqueUsers
    } catch (error) {
        console.error('获取学生列表失败:', error)
    }
}

// 获取学习统计数据
const fetchStats = async (userId) => {
    try {
        const [trendRes, masteryRes, errorsRes] = await Promise.all([
            axios.get(`http://localhost:8080/api/user-answers/stats/correct-rate-trend/${userId}`),
            axios.get(`http://localhost:8080/api/user-answers/stats/knowledge-mastery/${userId}`),
            axios.get(`http://localhost:8080/api/user-answers/stats/frequent-errors/${userId}`)
        ])

        correctRateTrend.value = trendRes.data
        knowledgeMastery.value = masteryRes.data
        frequentErrors.value = errorsRes.data
        console.log(errorsRes.data)
    } catch (error) {
        console.error('获取统计数据失败:', error)
    }
}

// 设置当前选中的学生并加载数据
const selectStudent = async (userId) => {
    selectedUserId.value = userId
    try {
        user.value = null;
        const res = await axios.get(`http://localhost:8080/api/user-answers/user/${userId}/with-nickname`)
        if (res.data && res.data.length > 0) {
            const userData = res.data[0]
            user.value = {
                userId: userData.userId,
                nickname: userData.nickname
            }
        }
        await fetchStats(userId)
    } catch (error) {
        console.error('获取用户数据失败:', error)
    }
}

// 返回学生列表
const backToList = () => {
    selectedUserId.value = null
    user.value = null
    correctRateTrend.value = []
    knowledgeMastery.value = []
    frequentErrors.value = []
}

onMounted(async () => {
    await fetchStudents()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.student-learning-stats {
    min-height: 100vh;
    background: linear-gradient(180deg, #f8fffd 0%, #fdfdfd 50%, #f0f9ff 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stats-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

/* 标题区域 */
.stats-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3rem;
    padding: 2.5rem;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    border: 1px solid rgba(6, 182, 212, 0.1);
}

.page-title {
    font-size: 2rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.title-icon {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.title-icon svg {
    width: 24px;
    height: 24px;
    color: white;
}

.page-subtitle {
    color: #64748b;
    margin-top: 0.5rem;
    font-size: 1rem;
}

.current-student {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.current-label {
    color: #64748b;
    font-size: 0.875rem;
}

.student-tag {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    background: #e0f2fe;
    color: #0369a1;
    border-radius: 100px;
    font-weight: 500;
    font-size: 0.875rem;
}

.tag-icon {
    width: 16px;
    height: 16px;
}

/* 学生列表 */
.students-list-container {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(6, 182, 212, 0.1);
}

.list-header {
    padding: 2rem 2.5rem;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.header-icon {
    width: 56px;
    height: 56px;
    background: #f0fdfa;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-icon svg {
    width: 28px;
    height: 28px;
    color: #06b6d4;
}

.list-title {
    font-size: 1.375rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
}

.list-subtitle {
    color: #64748b;
    margin: 0.25rem 0 0 0;
    font-size: 0.875rem;
}

.students-table {
    padding: 1.5rem;
}

.analysis-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    background: #06b6d4;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.analysis-btn:hover {
    background: #0891b2;
    transform: translateY(-1px);
}

.analysis-btn svg {
    width: 16px;
    height: 16px;
}

/* 返回按钮 */
.back-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: white;
    color: #475569;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 2rem;
}

.back-btn:hover {
    border-color: #06b6d4;
    color: #06b6d4;
    transform: translateX(-2px);
}

.back-btn svg {
    width: 18px;
    height: 18px;
}

/* 用户信息卡片 */
.user-info-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(6, 182, 212, 0.1);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
}

.card-icon {
    width: 44px;
    height: 44px;
    background: #f0fdfa;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card-icon svg {
    width: 22px;
    height: 22px;
    color: #06b6d4;
}

.card-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
}

.card-subtitle {
    color: #64748b;
    font-size: 0.875rem;
    margin: 0.25rem 0 0 0;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
}

.info-item {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid #f1f5f9;
}

.info-label {
    color: #64748b;
    font-size: 0.875rem;
    margin: 0;
    font-weight: 500;
}

.info-value {
    font-size: 1.625rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0.5rem 0 0 0;
}

.rate-high { color: #10b981; }
.rate-medium { color: #06b6d4; }
.rate-low { color: #64748b; }

/* 分析卡片 */
.analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.analysis-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 2.5rem;
    border: 1px solid rgba(6, 182, 212, 0.1);
}

.trend-icon {
    background: #e0f2fe;
}

.trend-icon svg {
    color: #0284c7;
}

.mastery-icon {
    background: #f0fdf4;
}

.mastery-icon svg {
    color: #10b981;
}

.chart-container {
    height: 320px;
    margin-bottom: 2rem;
}

.data-table-wrapper {
    background: #f8fafc;
    border-radius: 16px;
    padding: 1rem;
}

/* 表格样式 */
.rate-cell {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.rate-value {
    font-weight: 600;
    font-size: 0.875rem;
}

.rate-icon {
    width: 16px;
    height: 16px;
}

/* 掌握度进度条 */
.mastery-cell {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.mastery-bar {
    width: 120px;
    height: 6px;
    background: #f1f5f9;
    border-radius: 3px;
    overflow: hidden;
}

.mastery-progress {
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease;
}

.progress-high { background: #10b981; }
.progress-medium { background: #06b6d4; }
.progress-low { background: #94a3b8; }

.mastery-value {
    font-weight: 600;
    font-size: 0.875rem;
}

/* 错误卡片 */
.errors-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 2.5rem;
    border: 1px solid rgba(6, 182, 212, 0.1);
}

.error-icon {
    background: #fef3c7;
}

.error-icon svg {
    color: #f59e0b;
}

.errors-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.error-item {
    padding: 1.75rem;
    background: #fffbeb;
    border: 1px solid #fef3c7;
    border-radius: 16px;
    transition: all 0.2s ease;
}

.error-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}

.error-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.error-index {
    font-weight: 600;
    color: #92400e;
}

.error-count {
    padding: 0.375rem 0.875rem;
    background: #f59e0b;
    color: white;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 500;
}

.error-question {
    font-weight: 500;
    color: #1e293b;
    margin: 0 0 0.75rem 0;
    line-height: 1.6;
}

.error-explanation {
    color: #64748b;
    line-height: 1.6;
    margin: 0 0 1rem 0;
    font-size: 0.875rem;
}

.error-tip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: rgba(251, 191, 36, 0.1);
    border-radius: 10px;
    color: #92400e;
    font-size: 0.875rem;
}

.error-tip svg {
    width: 18px;
    height: 18px;
    color: #f59e0b;
}

/* DataTable自定义样式 */
:deep(.custom-datatable) {
    font-size: 0.875rem;
}

:deep(.p-datatable-thead > tr > th) {
    background: #f8fafc;
    color: #475569;
    font-weight: 600;
    padding: 1rem;
    border-bottom: 1px solid #f1f5f9;
}

:deep(.p-datatable-tbody > tr) {
    transition: all 0.2s ease;
}

:deep(.p-datatable-tbody > tr:hover) {
    background: #f8fafc;
}

:deep(.p-datatable-tbody > tr > td) {
    padding: 1rem;
    border-bottom: 1px solid #f8fafc;
    color: #334155;
}

:deep(.p-paginator) {
    background: transparent;
    border: none;
    padding: 1rem 0;
}

:deep(.p-paginator .p-paginator-element) {
    color: #64748b;
}

:deep(.p-paginator .p-paginator-element:hover) {
    background: #f1f5f9;
}

:deep(.p-paginator .p-highlight) {
    background: #06b6d4;
    color: white;
}

/* 响应式设计 */
@media (max-width: 1200px) {
    .analysis-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .stats-header {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }

    .info-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .page-title {
        font-size: 1.5rem;
    }
}
</style>
