<script setup>
    import { useLayout } from '@/layout/composables/layout';
    import { ref, onMounted, watch, computed, onUnmounted } from 'vue';
    import { useRouter, useRoute } from 'vue-router';

    const router = useRouter();
    const route = useRoute();
    const showProfileMenu = ref(false);
    const { onMenuToggle, toggleDarkMode, isDarkTheme } = useLayout();

    // 获取用户角色（用于显示对应菜单）
    const getUserRole = () => {
        try {
            const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
            return authData.role || 'student';
        } catch (e) {
            return 'student';
        }
    };

    const userRole = getUserRole();

    // 核心菜单项（学习模块的 5 个按钮）
    const coreMenuItems = computed(() => {
        return [
            { label: '学情画像分析', icon: '', to: '/StudentAssistant' },
            { label: '学习资源中心', icon: '', to: '/TeacherCenter' },
            { label: '学习路径规划', icon: '', to: '/AIMockInterview' },
            { label: '学情答疑助手', icon: '', to: '/Analytics' },
            { label: '学情测评分析', icon: '', to: '/AnalysisImprovement' }
        ];
    });

    // 获取本地存储的用户头像
    const getLocalAvatar = () => {
        try {
            const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
            return authData.avatar || '';
        } catch (e) {
            return '';
        }
    };

    // 用户信息响应式数据
    const userInfo = ref({
        username: '',
        nickname: '用户',
        email: '',
        role: '',
        avatar: getLocalAvatar()
    });

    // 获取用户信息
    async function fetchUserInfo() {
        try {
            const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
            const userId = authData?.id;

            if (!userId) {
                console.warn('未找到用户 ID');
                return;
            }

            const response = await fetch(`/api/users/${userId}`);

            if (!response.ok) {
                throw new Error('获取用户信息失败');
            }

            const data = await response.json();
            userInfo.value = {
                username: data.username,
                nickname: data.nickname || data.username,
                email: `${data.username}@edu.com`,
                role: data.role,
                avatar: data.avatar || getLocalAvatar()
            };
        } catch (error) {
            console.error('获取用户信息出错:', error);
        }
    }

    // 切换用户菜单显示
    function toggleProfileMenu() {
        showProfileMenu.value = !showProfileMenu.value;
    }

    // 关闭菜单
    function closeProfileMenu() {
        showProfileMenu.value = false;
    }

    // 退出登录
    function logout() {
        localStorage.removeItem('auth');
        sessionStorage.removeItem('auth');
        localStorage.removeItem('isLoggedIn');
        router.push({ name: 'login' });
    }

    // 跳转到账号页面
    function goToAccount() {
        router.push({ name: 'account' });
    }

    // 跳转到设置页面
    function goToSettings() {
        router.push({ name: 'settings' });
    }

    // 导航到指定路由
    function navigateTo(route) {
        router.push({ name: route });
        closeProfileMenu();
    }

    // 监听本地存储变化
    let lastAvatar = getLocalAvatar();
    watch(() => localStorage.getItem('auth'), (newVal) => {
        try {
            const authData = JSON.parse(newVal || '{}');
            if (authData.avatar !== undefined && authData.avatar !== lastAvatar) {
                userInfo.value.avatar = authData.avatar || '';
                lastAvatar = authData.avatar || '';
                console.log('头像已更新:', userInfo.value.avatar);
            }
        } catch (e) {
            console.error('解析用户数据失败:', e);
        }
    });

    // 点击外部关闭菜单
    function handleClickOutside(event) {
        // 关闭头像菜单
        const profileContainer = document.querySelector('.profile-container');
        if (profileContainer && !profileContainer.contains(event.target) && showProfileMenu.value) {
            closeProfileMenu();
        }
    }

    // 组件挂载时获取用户信息
    onMounted(() => {
        fetchUserInfo();

        // 监听跨窗口 storage 事件
        window.addEventListener('storage', (e) => {
            if (e.key === 'auth' && e.newValue) {
                try {
                    const authData = JSON.parse(e.newValue);
                    if (authData.avatar !== undefined && authData.avatar !== lastAvatar) {
                        userInfo.value.avatar = authData.avatar || '';
                        lastAvatar = authData.avatar || '';
                    }
                } catch (error) {
                    console.error('storage 事件解析失败:', error);
                }
            }
        });

        // 监听头像更新自定义事件
        window.addEventListener('avatar-updated', (e) => {
            if (e.detail) {
                userInfo.value.avatar = e.detail.avatar || '';
                lastAvatar = e.detail.avatar || '';
                console.log('收到头像更新事件:', userInfo.value.avatar);
            }
        });

        // 添加点击外部关闭菜单的监听器
        document.addEventListener('click', handleClickOutside);
    });

    // 组件卸载时清理监听器
    onUnmounted(() => {
        document.removeEventListener('click', handleClickOutside);
    });
</script>

<template>
    <div class="layout-topbar homepage-topbar">
        <div class="layout-topbar-logo-container">
            <!-- 菜单按钮（移动端显示） -->
            <button type="button" class="layout-menu-button pi pi-bars" @click="onMenuToggle()" aria-label="Menu"></button>

            <router-link to="/" class="layout-topbar-logo">
                <div class="logo-simple">
                    <span class="logo-icon">智</span>
                </div>
                <span class="logo-text">智学自适应育人引擎</span>
            </router-link>
        </div>

        <!-- 核心菜单（学习模块的 5 个按钮） -->
        <div class="layout-topbar-core-menu hidden lg:flex">
            <router-link
                v-for="item in coreMenuItems"
                :key="item.label"
                :to="item.to"
                class="layout-topbar-core-menu-item"
            >
                <i :class="item.icon"></i>
                <span>{{ item.label }}</span>
            </router-link>
        </div>

        <div class="layout-topbar-actions">
            <!-- 深浅色模式切换 -->
            <button type="button" class="layout-topbar-action" @click="toggleDarkMode" aria-label="Toggle Dark Mode">
                <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
            </button>

            <!-- 用户头像菜单 -->
            <div class="profile-container">
                <button
                    type="button"
                    class="layout-topbar-action profile-toggle"
                    @click="toggleProfileMenu"
                    aria-label="Profile"
                >
                    <div class="profile-avatar-wrapper">
                        <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" class="profile-avatar-img" />
                        <i v-else class="pi pi-user profile-icon"></i>
                    </div>
                </button>

                <transition name="fade">
                    <div v-if="showProfileMenu" class="layout-topbar-menu profile-dropdown-menu">
                        <div class="profile-header">
                            <div class="profile-avatar">
                                <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" class="avatar-img" />
                                <i v-else class="pi pi-user-circle"></i>
                            </div>
                            <div class="profile-info">
                                <h4 class="username">欢迎你，{{ userInfo.nickname }}</h4>
                                <p class="user-email">用户名：{{ userInfo.username }}</p>
                            </div>
                        </div>

                        <div class="profile-menu">
                            <button @click="goToAccount" class="menu-item">
                                <i class="pi pi-user-edit"></i>
                                <span>账号信息</span>
                            </button>
                            <button @click="goToSettings" class="menu-item">
                                <i class="pi pi-cog"></i>
                                <span>设置</span>
                            </button>
                        </div>

                        <div class="profile-actions">
                            <button @click="logout" class="logout-button">
                                <i class="pi pi-sign-out"></i>
                                <span>退出登录</span>
                            </button>
                        </div>
                    </div>
                </transition>
            </div>

            <!-- 移动端菜单按钮 -->
            <button
                class="layout-topbar-menu-button layout-topbar-action hidden lg:hidden"
                v-styleclass="{ selector: '@next', enterFromClass: 'hidden', enterActiveClass: 'animate-scalein', leaveToClass: 'hidden', leaveActiveClass: 'animate-fadeout', hideOnOutsideClick: true }"
            >
                <i class="pi pi-ellipsis-v"></i>
            </button>

            <!-- 移动端菜单 -->
            <div class="layout-topbar-menu-mobile hidden lg:hidden">
                <div class="layout-topbar-menu-content">
                    <router-link
                        v-for="item in coreMenuItems"
                        :key="item.label"
                        :to="item.to"
                        class="layout-topbar-core-menu-item"
                    >
                        <i :class="item.icon"></i>
                        <span>{{ item.label }}</span>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.layout-topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    padding: 0.75rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
}

.layout-topbar-logo-container {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.layout-menu-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #333;
    font-size: 1.25rem;
}

.layout-menu-button:hover {
    background-color: rgba(22, 93, 255, 0.1);
    color: #165DFF;
}

.layout-topbar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    transition: all 0.3s ease;
}

.logo-simple {
    width: 45px !important;
    height: 45px !important;
    border-radius: 12px;
    background: linear-gradient(135deg, #0E42D2, #165DFF) !important;
    display: flex !important;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(22, 93, 255, 0.3);
    transition: all 0.3s ease;
}

.logo-simple:hover {
    transform: rotate(-5deg) scale(1.05);
    box-shadow: 0 6px 20px rgba(22, 93, 255, 0.5);
}

.logo-icon {
    font-size: 1.8rem;
    font-weight: 700;
    color: white !important;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
}

.logo-text {
    font-size: 1.25rem;
    font-weight: 600;
    color: #165DFF !important;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', 'STSong', serif !important;
    letter-spacing: 2px;
}

.layout-topbar-logo:hover {
    transform: translateY(-2px);
}

.layout-topbar-logo:hover .logo-text {
    color: #2E8B6F !important;
}

/* 核心菜单样式 */
.layout-topbar-core-menu {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    margin-left: 5rem;
}

.layout-topbar-core-menu-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    color: #333;
    text-decoration: none;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-size: 0.95rem;
    font-weight: 500;
    white-space: nowrap;
}

.layout-topbar-core-menu-item:hover {
    background-color: rgba(22, 93, 255, 0.1);
    color: #165DFF;
}

.layout-topbar-core-menu-item i {
    font-size: 1rem;
}

.layout-topbar-actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.profile-container {
    position: relative;
}

.profile-toggle {
    border-radius: 50%;
}

.profile-avatar-wrapper {
    width: 40px;
    height: 40px;
    min-width: 40px;
    min-height: 40px;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #165DFF, #4080FF);
    flex-shrink: 0;
}

.profile-avatar-img {
    width: 100%;
    height: 100%;
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
}

.profile-icon {
    font-size: 20px;
    color: white;
}

.layout-topbar-menu {
    position: absolute;
    top: 100%;
    right: 0;
    width: 280px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    z-index: 9999;
    margin-top: 0.5rem;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.profile-header {
    display: flex;
    align-items: center;
    padding: 16px;
    background: linear-gradient(135deg, #165DFF, #4080FF);
    color: white;
}

.profile-avatar {
    font-size: 40px;
    margin-right: 12px;
    color: white;
    width: 60px;
    height: 60px;
    min-width: 60px;
    min-height: 60px;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
}

.avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-info .username {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: white;
}

.profile-info .user-email {
    margin: 4px 0 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 12px;
}

.profile-menu {
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
}

.menu-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: none;
    border: none;
    color: #333;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.menu-item:hover {
    background-color: #f5f5f5;
}

.menu-item i {
    font-size: 16px;
    color: #165DFF;
}

.profile-actions {
    padding: 12px;
    background-color: #f8f9fa;
}

.logout-button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px;
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 14px;
    font-weight: 500;
}

.logout-button:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
}

.layout-topbar-action {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #333;
}

.layout-topbar-action:hover {
    background-color: rgba(22, 93, 255, 0.1);
    color: #165DFF;
}

.layout-topbar-action-highlight {
    color: #165DFF;
}

.layout-topbar-menu-button {
    display: none;
}

.layout-topbar-menu-mobile {
    position: absolute;
    top: 100%;
    right: 0;
    width: 250px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    z-index: 9998;
    margin-top: 0.5rem;
    animation: slideIn 0.3s ease;
}

.layout-topbar-menu-content {
    display: flex;
    flex-direction: column;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@media (max-width: 1024px) {
    .layout-topbar-core-menu {
        display: none;
    }

    .layout-topbar-menu-button {
        display: flex;
    }
}
</style>
