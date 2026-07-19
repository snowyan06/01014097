<template>
    <div class="teaching-efficiency-container">
        <div class="header">
            <div class="title-section">
                <div class="title-icon">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 13H5L7 9L9 13L11 11L13 15L15 11L17 13L19 9L21 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="12" cy="5" r="2" fill="currentColor"/>
                    </svg>
                </div>
                <h2 class="page-title">教学效率指数</h2>
            </div>
            <div class="filters">
                <div class="teacher-selector">
                    <Dropdown
                        v-model="selectedTeacher"
                        :options="teachers"
                        optionLabel="nickname"
                        optionValue="teacherId"
                        placeholder="选择教师"
                        filter
                        @change="fetchEfficiencyData"
                        class="custom-dropdown"
                    />
                </div>
                <div class="date-range-selector">
                    <Calendar
                        v-model="dateRange"
                        selectionMode="range"
                        :manualInput="false"
                        dateFormat="yy-mm-dd"
                        showIcon
                        @date-select="fetchEfficiencyData"
                        class="custom-calendar"
                    />
                </div>
            </div>
        </div>

        <div v-if="selectedTeacher" class="efficiency-content">
            <div class="efficiency-index-card">
                <div class="card-header">
                    <div class="index-main">
                        <span class="index-label">教学效率指数</span>
                        <span class="index-value">{{ efficiencyData.efficiencyIndex || '--' }}</span>
                    </div>
                    <div class="index-indicator">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="currentColor" opacity="0.2"/>
                            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                </div>
                <div class="index-metrics">
                    <div class="metric-item">
                        <div class="metric-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                                <path d="M12 7V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div class="metric-content">
                            <span class="metric-label">平均备课时间</span>
                            <span class="metric-value">{{ efficiencyData.avgPrepTime || '--' }} <span class="metric-unit">分钟</span></span>
                        </div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M4 7V4C4 3.44772 4.44772 3 5 3H9L12 6L15 3H19C19.5523 3 20 3.44772 20 4V7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M4 7H20V19C20 19.5523 19.5523 20 19 20H5C4.44772 20 4 19.5523 4 19V7Z" stroke="currentColor" stroke-width="2"/>
                                <path d="M9 11H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                <path d="M9 15H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div class="metric-content">
                            <span class="metric-label">平均备课修正次数</span>
                            <span class="metric-value">{{ efficiencyData.avgPrepRevisions || '--' }}</span>
                        </div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9 11L12 14L22 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <div class="metric-content">
                            <span class="metric-label">优化建议数量</span>
                            <span class="metric-value">{{ efficiencyData.optimizationCount || '--' }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="efficiency-details">
                <div class="detail-section prep-time-section">
                    <div class="section-header">
                        <h3 class="section-title">备课与修正耗时</h3>
                        <div class="section-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
                                <path d="M9 9H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                <path d="M9 13H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                <path d="M9 17H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>
                    </div>
                    <div class="chart-container">
                        <div v-if="dailyData.length > 0" class="prep-time-table">
                            <div class="table-wrapper">
                                <table class="custom-table">
                                    <thead>
                                    <tr>
                                        <th>日期</th>
                                        <th>备课时间<span class="th-unit">(分钟)</span></th>
                                        <th>备课修正次数</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr v-for="(data, index) in dailyData" :key="index">
                                        <td>
                                            <div class="date-cell">
                                                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="date-icon">
                                                    <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.5"/>
                                                    <path d="M3 10H21" stroke="currentColor" stroke-width="1.5"/>
                                                    <path d="M8 2V6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                                                    <path d="M16 2V6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                                                </svg>
                                                {{ data.date }}
                                            </div>
                                        </td>
                                        <td>
                                            <div class="time-cell">
                                                <span class="time-value">{{ data.prepTime || '--' }}</span>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="revision-cell">
                                                <div class="revision-indicator">
                                                    <span class="revision-value">{{ data.prepRevisions || '--' }}</span>
                                                    <span v-if="data.prepRevisions > 0" class="revision-badge">次</span>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div v-else class="no-data">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="no-data-icon">
                                <path d="M9 10H9.01M15 10H15.01M9.5 15.5C10.0606 16.3861 11.0292 17 12.125 17C13.2208 17 14.1894 16.3861 14.75 15.5M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            <span>暂无备课数据</span>
                        </div>
                    </div>
                </div>

                <div class="detail-section optimization-section">
                    <div class="section-header">
                        <h3 class="section-title">课程优化方向</h3>
                        <div class="section-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 2L13.09 8.26L19 9L14 13.14L15.18 20.18L12 17L8.82 20.18L10 13.14L5 9L10.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                    </div>
                    <div class="optimization-notes">
                        <div v-if="optimizationNotes.length > 0" class="notes-list">
                            <Chip
                                v-for="(note, index) in optimizationNotes"
                                :key="index"
                                :label="note"
                                class="note-tag"
                            />
                        </div>
                        <div v-else class="no-data">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="no-data-icon">
                                <path d="M12 8V12M12 16H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            <span>暂无优化建议</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-else class="select-teacher-prompt">
            <div class="empty-state">
                <div class="empty-icon">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" stroke-width="2"/>
                        <path d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <h3 class="empty-title">选择教师查看数据</h3>
                <p class="empty-description">请从上方下拉菜单中选择一位教师<br>查看其教学效率指数和相关数据</p>
            </div>
        </div>

        <Toast />
    </div>
</template>

<script>
import axios from 'axios';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Chip from 'primevue/chip';
import Toast from 'primevue/toast';

export default {
    name: 'TeachingEfficiency',
    components: {
        Dropdown,
        Calendar,
        DataTable,
        Column,
        Chip,
        Toast
    },
    data() {
        return {
            dateRange: [this.getFirstDayOfMonth(), this.getLastDayOfMonth()],
            teachers: [],
            selectedTeacher: null,
            efficiencyData: {},
            dailyData: [],
            optimizationNotes: []
        }
    },
    created() {
        this.fetchTeachers();
    },
    methods: {
        getFirstDayOfMonth() {
            const date = new Date();
            return new Date(date.getFullYear(), date.getMonth(), 1);
        },
        getLastDayOfMonth() {
            const date = new Date();
            return new Date(date.getFullYear(), date.getMonth() + 1, 0);
        },
        async fetchTeachers() {
            try {
                const response = await axios.get('http://localhost:8080/api/teaching-efficiency/teachers-and-admins');//这里如果是不想要管理员工，就换成/teachers
                this.teachers = response.data;

                if (this.teachers.length > 0) {
                    this.selectedTeacher = this.teachers[0].teacherId;
                    this.fetchEfficiencyData();
                }
            } catch (error) {
                console.error('获取教师列表失败:', error);
                this.$toast.add({
                    severity: 'error',
                    summary: '错误',
                    detail: '获取教师列表失败',
                    life: 3000
                });
            }
        },
        async fetchEfficiencyData() {
            if (!this.selectedTeacher || !this.dateRange || this.dateRange.length !== 2) return;

            const formatDate = (date) => {
                return date.toISOString().split('T')[0];
            };

            const startDate = formatDate(this.dateRange[0]);
            const endDate = formatDate(this.dateRange[1]);

            try {
                // 获取效率指数
                const indexResponse = await axios.get('http://localhost:8080/api/teaching-efficiency/index', {
                    params: {
                        teacherId: this.selectedTeacher,
                        startDate,
                        endDate
                    }
                });
                this.efficiencyData = indexResponse.data;

                // 获取每日数据
                const dailyResponse = await axios.get('http://localhost:8080/api/teaching-efficiency/range', {
                    params: {
                        teacherId: this.selectedTeacher,
                        startDate,
                        endDate
                    }
                });
                this.dailyData = dailyResponse.data;

                // 提取优化建议
                this.optimizationNotes = this.dailyData
                    .filter(item => item.optimizationNotes)
                    .flatMap(item => item.optimizationNotes.split(';').filter(note => note.trim()));
            } catch (error) {
                console.error('获取教学效率数据失败:', error);
                this.$toast.add({
                    severity: 'error',
                    summary: '错误',
                    detail: '获取教学效率数据失败',
                    life: 3000
                });
            }
        }
    }
}
</script>

<style scoped>
/* 引入高级字体 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

.teaching-efficiency-container {
    padding: 32px;
    max-width: 1320px;
    margin: 0 auto;
    font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(180deg, #fafbfc 0%, #f5f7fa 100%);
    min-height: 100vh;
}

/* 头部样式 */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    padding: 24px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.title-section {
    display: flex;
    align-items: center;
    gap: 16px;
}

.title-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
}

.title-icon svg {
    width: 24px;
    height: 24px;
    color: white;
}

.page-title {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    color: #1f2937;
    letter-spacing: -0.8px;
}

.filters {
    display: flex;
    gap: 16px;
}

.teacher-selector,
.date-range-selector {
    min-width: 280px;
}

/* 自定义下拉框和日历样式 */
.custom-dropdown,
.custom-calendar {
    font-family: inherit;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    transition: all 0.3s ease;
    background: white;
}

.custom-dropdown:hover,
.custom-calendar:hover {
    border-color: #22c55e;
    box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.08);
}

/* 效率指数卡片 */
.efficiency-index-card {
    background: white;
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.efficiency-index-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(34, 197, 94, 0.03) 0%, transparent 70%);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    position: relative;
}

.index-main {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.index-label {
    font-size: 16px;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 0.5px;
}

.index-value {
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

.index-indicator {
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.index-indicator svg {
    width: 100%;
    height: 100%;
    color: #22c55e;
}

/* 指标项目 */
.index-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    position: relative;
}

.metric-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: #f9fafb;
    border-radius: 16px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.metric-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    border-color: rgba(34, 197, 94, 0.2);
}

.metric-icon {
    width: 48px;
    height: 48px;
    background: white;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.metric-icon svg {
    width: 24px;
    height: 24px;
    color: #22c55e;
}

.metric-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.metric-label {
    font-size: 14px;
    color: #6b7280;
    font-weight: 500;
}

.metric-value {
    font-size: 24px;
    font-weight: 700;
    color: #1f2937;
}

.metric-unit {
    font-size: 14px;
    font-weight: 400;
    color: #9ca3af;
}

/* 详情区域 */
.efficiency-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 24px;
}

.detail-section {
    background: white;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    min-height: 400px;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #f3f4f6;
}

.section-title {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: #1f2937;
    letter-spacing: -0.3px;
}

.section-icon {
    width: 40px;
    height: 40px;
    background: #f9fafb;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.section-icon svg {
    width: 20px;
    height: 20px;
    color: #22c55e;
}

/* 美化的表格样式 */
.table-wrapper {
    overflow-x: auto;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.custom-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-family: inherit;
}

.custom-table thead {
    background: #f9fafb;
}

.custom-table th {
    padding: 16px 20px;
    text-align: left;
    font-weight: 600;
    color: #374151;
    font-size: 14px;
    letter-spacing: 0.3px;
    border-bottom: 1px solid #e5e7eb;
}

.custom-table th:first-child {
    border-top-left-radius: 11px;
}

.custom-table th:last-child {
    border-top-right-radius: 11px;
}

.th-unit {
    font-size: 12px;
    font-weight: 400;
    color: #9ca3af;
    margin-left: 4px;
}

.custom-table tbody tr {
    transition: all 0.2s ease;
}

.custom-table tbody tr:hover {
    background: #fafbfc;
}

.custom-table td {
    padding: 16px 20px;
    border-bottom: 1px solid #f3f4f6;
}

.custom-table tbody tr:last-child td {
    border-bottom: none;
}

.date-cell {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
    color: #374151;
}

.date-icon {
    width: 16px;
    height: 16px;
    color: #9ca3af;
}

.time-cell {
    display: flex;
    align-items: center;
}

.time-value {
    font-weight: 600;
    color: #1f2937;
    font-size: 15px;
}

.revision-cell {
    display: flex;
    align-items: center;
}

.revision-indicator {
    display: flex;
    align-items: baseline;
    gap: 4px;
}

.revision-value {
    font-weight: 600;
    color: #1f2937;
    font-size: 15px;
}

.revision-badge {
    font-size: 12px;
    color: #6b7280;
    font-weight: 400;
}

/* 优化建议标签 */
.notes-list {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.note-tag {
    background: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
    padding: 8px 16px;
    font-weight: 500;
    border-radius: 20px;
    font-size: 14px;
    transition: all 0.3s ease;
}

.note-tag:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
    background: #dcfce7;
}

/* 空状态 */
.no-data {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #9ca3af;
    gap: 16px;
}

.no-data-icon {
    width: 48px;
    height: 48px;
    opacity: 0.5;
}

.select-teacher-prompt {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 500px;
}

.empty-state {
    text-align: center;
    padding: 60px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.empty-icon {
    width: 120px;
    height: 120px;
    margin: 0 auto 24px;
    background: #f9fafb;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.empty-icon svg {
    width: 60px;
    height: 60px;
    color: #9ca3af;
}

.empty-title {
    margin: 0 0 12px;
    font-size: 24px;
    font-weight: 600;
    color: #374151;
}

.empty-description {
    margin: 0;
    font-size: 16px;
    color: #6b7280;
    line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 1024px) {
    .efficiency-details {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .header {
        flex-direction: column;
        gap: 20px;
    }

    .filters {
        flex-direction: column;
        width: 100%;
    }

    .teacher-selector,
    .date-range-selector {
        min-width: 100%;
    }

    .index-metrics {
        grid-template-columns: 1fr;
    }

    .page-title {
        font-size: 24px;
    }

    .index-value {
        font-size: 36px;
    }

    .custom-table {
        font-size: 14px;
    }

    .custom-table th,
    .custom-table td {
        padding: 12px 16px;
    }
}

/* 文字渲染优化 */
* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

/* 过渡动画 */
.efficiency-content > * {
    animation: fadeIn 0.5s ease-out forwards;
}

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

/* 自定义滚动条 */
.table-wrapper::-webkit-scrollbar {
    height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
    background: #f9fafb;
    border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
    background: #9ca3af;
}

</style>
