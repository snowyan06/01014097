<template>
    <div class="dashboard-overview">
        <div class="stats-container">
            <!-- 教师统计板块 -->
            <div class="stats-section teacher-stats">
                <div class="section-header">
                    <div class="section-icon teacher-icon">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M17 10H7V12H17V10Z" fill="currentColor"/>
                            <path d="M17 14H7V16H17V14Z" fill="currentColor"/>
                            <path d="M14 6H10V8H14V6Z" fill="currentColor"/>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M3 5C3 3.89543 3.89543 3 5 3H19C20.1046 3 21 3.89543 21 5V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5ZM5 5H19V19H5V5Z" fill="currentColor"/>
                        </svg>
                    </div>
                    <h2 class="section-title">教师使用统计</h2>
                </div>

                <div class="stats-cards">
                    <StatsCard
                        title="当日出题数量"
                        :value="teacherDaily.total"
                        :details="teacherDaily.teachers"
                        type="teacher"
                        @show-more="showTeacherDetail('daily')"
                    />

                    <StatsCard
                        title="本周出题数量"
                        :value="teacherWeekly.total"
                        :details="teacherWeekly.teachers"
                        type="teacher"
                        @show-more="showTeacherDetail('weekly')"
                    />

                    <StatsCard
                        title="累计出题总数"
                        :value="teacherTotal.total"
                        :details="teacherTotal.teachers"
                        type="teacher"
                        @show-more="showTeacherDetail('total')"
                    />
                </div>
            </div>

            <!-- 学生统计板块 -->
            <div class="stats-section student-stats">
                <div class="section-header">
                    <div class="section-icon student-icon">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 4C13.1046 4 14 4.89543 14 6C14 7.10457 13.1046 8 12 8C10.8954 8 10 7.10457 10 6C10 4.89543 10.8954 4 12 4Z" fill="currentColor"/>
                            <path d="M12 10C14.2091 10 16 11.7909 16 14V20H14V14C14 12.8954 13.1046 12 12 12C10.8954 12 10 12.8954 10 14V20H8V14C8 11.7909 9.79086 10 12 10Z" fill="currentColor"/>
                            <path d="M17 13C17 12.4477 17.4477 12 18 12C18.5523 12 19 12.4477 19 13V20H17V13Z" fill="currentColor"/>
                            <path d="M5 13C5 12.4477 5.44772 12 6 12C6.55228 12 7 12.4477 7 13V20H5V13Z" fill="currentColor"/>
                            <path d="M18 10C18.5523 10 19 9.55228 19 9C19 8.44772 18.5523 8 18 8C17.4477 8 17 8.44772 17 9C17 9.55228 17.4477 10 18 10Z" fill="currentColor"/>
                            <path d="M6 10C6.55228 10 7 9.55228 7 9C7 8.44772 6.55228 8 6 8C5.44772 8 5 8.44772 5 9C5 9.55228 5.44772 10 6 10Z" fill="currentColor"/>
                        </svg>
                    </div>
                    <h2 class="section-title">学生使用统计</h2>
                </div>

                <div class="stats-cards">
                    <StatsCard
                        title="当日活跃用户"
                        :value="studentDaily.activeUsers"
                        :secondary-value="studentDaily.totalAnswers"
                        secondary-label="答题次数"
                        :details="studentDaily.users"
                        type="student"
                        @show-more="showStudentDetail('daily')"
                    />

                    <StatsCard
                        title="本周活跃用户"
                        :value="studentWeekly.activeUsers"
                        :secondary-value="studentWeekly.totalAnswers"
                        secondary-label="答题次数"
                        :details="studentWeekly.users"
                        type="student"
                        @show-more="showStudentDetail('weekly')"
                    />

                    <StatsCard
                        title="总使用次数"
                        :value="studentTotal.totalUsage"
                        :details="studentTotal.users"
                        type="student"
                        @show-more="showStudentDetail('total')"
                    />
                </div>
            </div>
        </div>

        <!-- 详情弹窗 -->
        <DetailModal
            v-if="showDetail"
            :title="detailTitle"
            :items="detailItems"
            :type="detailType"
            @close="showDetail = false"
        />
    </div>
</template>

<script>
import axios from 'axios';
import StatsCard from './StatsCard.vue';
import DetailModal from './DetailModal.vue';

export default {
    name: 'DashboardOverview',
    components: { StatsCard, DetailModal },
    data() {
        return {
            teacherDaily: { total: 0, teachers: [] },
            teacherWeekly: { total: 0, teachers: [] },
            teacherTotal: { total: 0, teachers: [] },
            studentDaily: { activeUsers: 0, totalAnswers: 0, users: [] },
            studentWeekly: { activeUsers: 0, totalAnswers: 0, users: [] },
            studentTotal: { totalUsage: 0, users: [] },
            refreshInterval: null,
            showDetail: false,
            detailTitle: '',
            detailItems: [],
            detailType: ''
        }
    },
    created() {
        this.fetchData();
        this.refreshInterval = setInterval(this.fetchData, 5 * 60 * 1000);
    },
    beforeDestroy() {
        clearInterval(this.refreshInterval);
    },
    methods: {
        async fetchData() {
            try {
                const [dailyRes, weeklyRes, totalRes] = await Promise.all([
                    axios.get('http://localhost:8080/api/questions/daily'),
                    axios.get('http://localhost:8080/api/questions/weekly'),
                    axios.get('http://localhost:8080/api/questions/total')
                ]);

                this.teacherDaily = this.processTeacherData(dailyRes.data);
                this.teacherWeekly = this.processTeacherData(weeklyRes.data);
                this.teacherTotal = this.processTeacherData(totalRes.data);

                const [dailyActiveRes, weeklyActiveRes, totalUsageRes] = await Promise.all([
                    axios.get('http://localhost:8080/api/user-answers/stats/daily-active'),
                    axios.get('http://localhost:8080/api/user-answers/stats/weekly-active'),
                    axios.get('http://localhost:8080/api/user-answers/stats/total-usage')
                ]);

                this.studentDaily = this.processStudentData(dailyActiveRes.data);
                this.studentWeekly = this.processStudentData(weeklyActiveRes.data);
                this.studentTotal = this.processTotalUsageData(totalUsageRes.data);
            } catch (error) {
                console.error('获取统计数据失败:', error);
            }
        },
        processTeacherData(data) {
            const teachers = Array.isArray(data) ? data : [];
            const total = teachers.reduce((sum, t) => sum + (t.questionCount || 0), 0);
            return { total, teachers };
        },
        processStudentData(data) {
            const users = Array.isArray(data) ? data : [];
            const totalAnswers = users.reduce((sum, u) => sum + (u.count || 0), 0);
            return { activeUsers: users.length, totalAnswers, users };
        },
        processTotalUsageData(data) {
            const users = Array.isArray(data) ? data : [];
            const totalUsage = users.reduce((sum, u) => sum + (u.count || 0), 0);
            return { totalUsage, users };
        },
        showTeacherDetail(type) {
            this.detailType = 'teacher';
            this.detailItems = this[`teacher${type.charAt(0).toUpperCase() + type.slice(1)}`].teachers;
            this.detailTitle = `${this.getTitle(type)}教师出题详情`;
            this.showDetail = true;
        },
        showStudentDetail(type) {
            this.detailType = 'student';
            this.detailItems = this[`student${type.charAt(0).toUpperCase() + type.slice(1)}`].users;
            this.detailTitle = `${this.getTitle(type)}学生答题详情`;
            this.showDetail = true;
        },
        getTitle(type) {
            const map = { daily: '当日', weekly: '本周', total: '累计' };
            return map[type] || '';
        }
    }
}
</script>

<style scoped>
/* 高级字体系统 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

.dashboard-overview {
    padding: 32px;
    max-width: 1280px;
    margin: 0 auto;
    font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #f0f2f5 100%);
    min-height: 100vh;
    position: relative;
}

.dashboard-overview::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 300px;
    background: linear-gradient(180deg, rgba(255,255,255,0.5) 0%, transparent 100%);
    pointer-events: none;
}

.stats-container {
    display: flex;
    flex-direction: column;
    gap: 36px;
    position: relative;
    z-index: 1;
}

.stats-section {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    box-shadow:
        0 2px 8px rgba(0, 0, 0, 0.04),
        0 8px 24px rgba(0, 0, 0, 0.08);
    padding: 32px;
    transition: all 0.4s cubic-bezier(0.215, 0.610, 0.355, 1.000);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.7);
}

.stats-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--theme-color) 0%, var(--theme-color-light) 100%);
    opacity: 0.9;
}

.stats-section::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, var(--theme-color) 0%, transparent 70%);
    opacity: 0.03;
    pointer-events: none;
}

.teacher-stats {
    --theme-color: #4a69bd;
    --theme-color-light: #6c7fd8;
}

.student-stats {
    --theme-color: #27ae60;
    --theme-color-light: #52c77a;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
    position: relative;
}

.section-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.teacher-icon {
    background: linear-gradient(135deg, #4a69bd 0%, #6c7fd8 100%);
}

.student-icon {
    background: linear-gradient(135deg, #27ae60 0%, #52c77a 100%);
}

.section-icon svg {
    width: 24px;
    height: 24px;
    color: white;
}

.section-title {
    margin: 0;
    color: #1a202c;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.8px;
    position: relative;
    background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

/* 高级悬浮效果 */
.stats-section:hover {
    transform: translateY(-4px);
    box-shadow:
        0 4px 12px rgba(0, 0, 0, 0.08),
        0 12px 32px rgba(0, 0, 0, 0.12);
}

/* 平滑动画 */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stats-section {
    animation: slideInUp 0.6s cubic-bezier(0.215, 0.610, 0.355, 1.000) forwards;
}

.stats-section:nth-child(2) {
    animation-delay: 0.1s;
}

/* 响应式优化 */
@media (max-width: 768px) {
    .dashboard-overview {
        padding: 20px;
    }

    .stats-section {
        padding: 24px;
    }

    .section-title {
        font-size: 22px;
    }

    .section-icon {
        width: 40px;
        height: 40px;
    }

    .stats-cards {
        grid-template-columns: 1fr;
    }
}

/* 精细化文字渲染 */
* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

/* 优雅的选择效果 */
::selection {
    background-color: rgba(74, 105, 189, 0.15);
    color: #2d3748;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #f1f3f5;
    border-radius: 8px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #cbd5e0 0%, #a0aec0 100%);
    border-radius: 8px;
    border: 2px solid #f1f3f5;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #a0aec0 0%, #718096 100%);
}

/* 加载状态优化 */
.stats-cards > * {
    opacity: 0;
    animation: slideInUp 0.5s cubic-bezier(0.215, 0.610, 0.355, 1.000) forwards;
}

.stats-cards > *:nth-child(1) {
    animation-delay: 0.15s;
}

.stats-cards > *:nth-child(2) {
    animation-delay: 0.25s;
}

.stats-cards > *:nth-child(3) {
    animation-delay: 0.35s;
}
</style>
