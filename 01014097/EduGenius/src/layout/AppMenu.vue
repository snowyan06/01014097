<script setup>
   import { computed } from 'vue';
    import AppMenuItem from './AppMenuItem.vue';

    const getAuthData = () => {
        try {
            return JSON.parse(localStorage.getItem('auth')) ||
                JSON.parse(sessionStorage.getItem('auth'));
        } catch (e) {
            console.error('解析 auth 数据失败:', e);
            return null;
        }
    };

    const authData = getAuthData();
    const userRole = authData?.role || 'user';

    const model = computed(() => {
        const commonItems = [
            {
                label: '首页',
                items: [{ label: '首页', icon: 'pi pi-fw pi-home', to: '/' }]
            }
        ];

        const userItems = [
            {
                label: '学习模块',
                items: [
                    {
                        label: '学生学情画像分析',
                        icon: 'pi pi-fw pi-user',
                        to: '/StudentAssistant'
                    },
                    {
                        label: '个性化学习资源中心',
                        icon: 'pi pi-fw pi-bookmark',
                        to: '/TeacherCenter'
                    },
                    {
                        label: '自适应学习路径规划',
                        icon: 'pi pi-fw pi-route',
                        to: '/AIMockInterview'
                    },
                    {
                        label: '智能学情答疑助手',
                        icon: 'pi pi-fw pi-comments',
                        to: '/Analytics'
                    },
                    {
                        label: '学情综合测评分析',
                        icon: 'pi pi-fw pi-chart-line',
                        to: '/AnalysisImprovement'
                    }
                ]
            }
        ];

        const footerItems = [
            {
                label: '使用手册',
                items: [
                    {
                       label: '文档',
                        icon: 'pi pi-fw pi-book',
                        to: '/documentation'
                   }
                ]
            }
        ];

        return [...commonItems, ...userItems, ...footerItems];
    });
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped>
</style>
