import router from '@/router';

export const voiceNavigationService = {
    async handleVoiceCommand(text, confidence) {
        const commandMap = [
            { keywords: ['首页', '主页'], path: '/' },
            { keywords: ['教师', '教师中心'], path: '/TeacherCenter' },
            { keywords: ['学生助手', '答疑', '学生'], path: '/StudentAssistant' },
            { keywords: ['面试', '模拟面试'], path: '/AIMockInterview' },
            { keywords: ['分析', '学情分析', '改进'], path: '/AnalysisImprovement' },
            { keywords: ['仪表盘', '分析面板', 'analytics'], path: '/Analytics' },
            { keywords: ['文档', '帮助文档'], path: '/documentation' },
            { keywords: ['设置'], path: '/settings' },
        ];

        const lowerText = text.toLowerCase();
        for (const cmd of commandMap) {
            if (cmd.keywords.some(kw => lowerText.includes(kw))) {
                if (router.currentRoute.value.path !== cmd.path) {
                    router.push(cmd.path);
                }
                return { type: 'navigation', path: cmd.path };
            }
        }

        throw new Error('未命中导航指令');
    }
};
