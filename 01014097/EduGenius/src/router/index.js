import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const routes = [
    {
        path: '/',
        component: AppLayout,
        children: [
            {
                path: '',
                name: 'dashboard',
                component: () => import('@/views/pages/Landing.vue')
            },

            {
                path: '/TeacherCenter',
                name: 'TeacherCenter',
                component: () => import('@/views/pages/edu/TeacherCenter.vue')
            },

            {
                path: '/StudentAssistant',
                name: 'StudentAssistant',
                component: () => import('@/views/pages/edu/StudentAssistant.vue')
            },

            {
                path: '/AIMockInterview',
                name: 'AIMockInterview',
                component: () => import('@/views/pages/AIMockInterview.vue')
            },

            {
                path: '/AnalysisImprovement',
                name: 'AnalysisImprovement',
                component: () => import('@/views/pages/AnalysisImprovement.vue')
            },

            {
                path: '/Analytics',
                name: 'Analytics',
                component: () => import('@/views/pages/edu/AnalyticsDashboard.vue')
            },

            {
                path: '/documentation',
                name: 'documentation',
                component: () => import('@/views/pages/Documentation.vue')
            },
            {
                path: '/account',
                name: 'account',
                component: () => import('@/views/pages/Account.vue')
            },
            {
                path: '/settings',
                name: 'settings',
                component: () => import('@/views/pages/Settings.vue')
            },
        ]
    },
    {
        path: '/landing',
        name: 'landing',
        component: () => import('@/views/pages/Landing.vue')
    },
    {
        path: '/pages/notfound',
        name: 'notfound',
        component: () => import('@/views/pages/NotFound.vue')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('@/views/pages/auth/Login.vue')
    },
    {
        path: '/auth/login',
        name: 'auth-login',
        component: () => import('@/views/pages/auth/Login.vue')
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('@/views/pages/register.vue')
    },
    {
        path: '/auth/access',
        name: 'accessDenied',
        component: () => import('@/views/pages/auth/Access.vue')
    },
    {
        path: '/auth/error',
        name: 'error',
        component: () => import('@/views/pages/auth/Error.vue')
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
