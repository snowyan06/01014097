<template>
    <div class="login-page-container">
        <!-- 登录容器 -->
        <div class="login-container">
            <div class="login-card">
                <!-- Logo & Title -->
                <div class="login-header">
                    <!-- SmartFace Logo -->
                    <svg viewBox="0 0 54 40" fill="none" xmlns="http://www.w3.org/2000/svg" class="login-logo">
                        <path
                            fill-rule="evenodd"
                            clip-rule="evenodd"
                            d="M17.1637 19.2467C17.1566 19.4033 17.1529 19.561 17.1529 19.7194C17.1529 25.3503 21.7203 29.915 27.3546 29.915C32.9887 29.915 37.5561 25.3503 37.5561 19.7194C37.5561 19.5572 37.5524 19.3959 37.5449 19.2355C38.5617 19.0801 39.5759 18.9013 40.5867 18.6994L40.6926 18.6782C40.7191 19.0218 40.7326 19.369 40.7326 19.7194C40.7326 27.1036 34.743 33.0896 27.3546 33.0896C19.966 33.0896 13.9765 27.1036 13.9765 19.7194C13.9765 19.374 13.9896 19.0316 14.0154 18.6927L14.0486 18.6994C15.0837 18.9062 16.1223 19.0886 17.1637 19.2467ZM33.3284 11.4538C31.6493 10.2396 29.5855 9.52381 27.3546 9.52381C25.1195 9.52381 23.0524 10.2421 21.3717 11.4603C20.0078 11.3232 18.6475 11.1387 17.2933 10.907C19.7453 8.11308 23.3438 6.34921 27.3546 6.34921C31.36 6.34921 34.9543 8.10844 37.4061 10.896C36.0521 11.1292 34.692 11.3152 33.3284 11.4538ZM43.826 18.0518C43.881 18.6003 43.9091 19.1566 43.9091 19.7194C43.9091 28.8568 36.4973 36.2642 27.3546 36.2642C18.2117 36.2642 10.8 28.8568 10.8 19.7194C10.8 19.1615 10.8276 18.61 10.8816 18.0663L7.75383 17.4411C7.66775 18.1886 7.62354 18.9488 7.62354 19.7194C7.62354 30.6102 16.4574 39.4388 27.3546 39.4388C38.2517 39.4388 47.0855 30.6102 47.0855 19.7194C47.0855 18.9439 47.0407 18.1789 46.9536 17.4267L43.826 18.0518ZM44.2613 9.54743L40.9084 10.2176C37.9134 5.95821 32.9593 3.1746 27.3546 3.1746C21.7442 3.1746 16.7856 5.96385 13.7915 10.2305L10.4399 9.56057C13.892 3.83178 20.1756 0 27.3546 0C34.5281 0 40.8075 3.82591 44.2613 9.54743Z"
                            fill="currentColor"
                        />
                    </svg>

                    <h1 class="login-title">SmartFace</h1>
                    <p class="login-subtitle">智面未来 · AI 面试教练平台</p>
                </div>

                <!-- 登录表单 -->
                <form @submit.prevent="handleLogin" class="login-form">
                    <!-- 错误提示 -->
                    <div v-if="errorMessage" class="error-message">
                        {{ errorMessage }}
                    </div>

                    <!-- 用户名 -->
                    <div class="form-group">
                        <label for="username" class="form-label">用户名</label>
                        <InputText
                            id="username"
                            type="text"
                            placeholder="请输入您的用户名"
                            v-model="username"
                            class="form-input"
                        />
                    </div>

                    <!-- 密码 -->
                    <div class="form-group">
                        <label for="password" class="form-label">密码</label>
                        <Password
                            id="password"
                            v-model="password"
                            placeholder="请输入密码"
                            :toggleMask="true"
                            class="form-input"
                            :feedback="false"
                        />
                    </div>

                    <!-- 记住我 & 忘记密码 -->
                    <div class="form-options">
                        <div class="remember-me">
                            <Checkbox v-model="rememberMe" id="rememberme" binary class="checkbox" />
                            <label for="rememberme" class="checkbox-label">记住我</label>
                        </div>
                        <a href="#" class="forgot-password">忘记密码？</a>
                    </div>

                    <!-- 登录按钮 -->
                    <button
                        type="submit"
                        class="login-button"
                        :disabled="isLoading"
                    >
                        <span v-if="!isLoading">登录</span>
                        <span v-else class="loading-spinner">
                            <svg class="animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            登录中...
                        </span>
                    </button>

                    <!-- 注册链接 -->
                    <div class="register-link">
                        <span>还没有账号？</span>
                        <a
                            href="#"
                            @click.prevent="router.push({ name: 'register' })"
                            class="register-btn"
                        >
                            立即注册
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { InputText, Password, Checkbox } from 'primevue';
import axios from 'axios';

const router = useRouter();

// 表单数据
const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const selectedRole = ref('user'); // 默认选择用户
const isLoading = ref(false);
const errorMessage = ref('');

const handleLogin = async () => {
    // 验证输入
    if (!username.value || !password.value) {
        errorMessage.value = '请输入用户名和密码';
        return;
    }

    isLoading.value = true;
    errorMessage.value = '';

    try {
        // 调用登录 API
        const response = await axios.post('/api/auth/login', {
            username: username.value,
            password: password.value,
            role: 'user' // 固定使用 user 角色
        });

        // 登录成功处理
        const {
            id,
            token,
            username: responseUsername, // 重命名避免冲突
            role,
            nickname = responseUsername // 默认值
        } = response.data;

        const authData = {
            id,
            username: responseUsername,
            nickname,
            role,
            token,
            timestamp: Date.now()
        };


        if (rememberMe.value) {
            localStorage.setItem('auth', JSON.stringify(authData));
            localStorage.setItem('isLoggedIn', 'true');
        } else {
            sessionStorage.setItem('auth', JSON.stringify(authData));
            sessionStorage.setItem('isLoggedIn', 'true');
        }
        const storage = rememberMe.value ? localStorage : sessionStorage;
        storage.setItem('auth', JSON.stringify(authData));
        storage.setItem('isLoggedIn', 'true');

        // 登录后统一跳转到首页
        try {
            console.log('准备跳转到首页');
            await router.push({ name: 'dashboard' });
        } catch (routerError) {
            console.error('路由跳转失败:', routerError);
            await router.push('/');
        }

    } catch (error) {
        // 错误处理
        console.error('登录错误:', error);
        if (error.response) {
            // 处理 API 返回的错误
            console.error('错误响应:', error.response);
            errorMessage.value = error.response.data.message || '登录失败，请检查用户名和密码';
        } else if (error.request) {
            // 请求已发出但没有响应
            console.error('错误请求:', error.request);
            errorMessage.value = '服务器无响应，请检查网络连接';
        } else {
            // 其他错误
            errorMessage.value = '登录过程中发生错误';
        }
    } finally {
        isLoading.value = false;
    }
};

</script>

<style scoped>
/* 页面容器 - 山水画背景 */
.login-page-container {
    min-height: 100vh;
    /* 上绿下白渐变 + 山水画背景 */
    background:
        linear-gradient(to bottom,
            rgba(6, 78, 59, 0.85) 0%,
            rgba(6, 78, 59, 0.8) 35%,
            rgba(255, 255, 255, 0.85) 35%,
            rgba(255, 255, 255, 0.9) 100%),
        url('/src/assets/backgrounds/landscape-1.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    position: relative;
}

/* 添加装饰性光晕效果（和主页面一致） */
.login-page-container::before,
.login-page-container::after {
    content: '';
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.15;
    animation: float 20s ease-in-out infinite;
    pointer-events: none;
}

.login-page-container::before {
    width: 400px;
    height: 400px;
    background-color: #064e3b;
    top: -100px;
    left: -100px;
    animation-delay: 0s;
}

.login-page-container::after {
    width: 350px;
    height: 350px;
    background-color: #10b981;
    bottom: -100px;
    right: 10%;
    animation-delay: -7s;
}

/* 登录容器 */
.login-container {
    width: 100%;
    max-width: 500px;
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    z-index: 10;
}

/* 登录卡片 */
.login-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(6, 78, 59, 0.15),
                0 0 0 1px rgba(255, 255, 255, 0.3);
    overflow: hidden;
    border: 1px solid rgba(6, 78, 59, 0.1);
}

/* 头部区域 */
.login-header {
    text-align: center;
    padding: 28px 30px 22px;
    background: linear-gradient(135deg, rgba(6, 78, 59, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%);
    border-bottom: 2px solid rgba(6, 78, 59, 0.1);
}

/* Logo */
.login-logo {
    width: 56px;
    height: 56px;
    margin: 0 auto 12px;
    color: #064e3b;
    animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

/* 标题 */
.login-title {
    font-size: 28px;
    font-weight: 700;
    color: #064e3b;
    margin: 0 0 6px 0;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', serif;
    letter-spacing: 1px;
}

/* 副标题 */
.login-subtitle {
    font-size: 13px;
    color: #6b7280;
    margin: 0;
    font-weight: 400;
}

/* 表单区域 */
.login-form {
    padding: 28px 40px 24px;
}

/* 表单组 */
.form-group {
    margin-bottom: 18px;
}

/* 表单标签 */
.form-label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 6px;
}

/* 表单输入框 */
.form-input {
    width: 100%;
    padding: 12px 16px;
    font-size: 15px;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    transition: all 0.3s ease;
    outline: none;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.9);
}

.form-input:hover {
    border-color: #d1d5db;
    background: rgba(255, 255, 255, 1);
}

.form-input:focus {
    border-color: #10b981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
    background: rgba(255, 255, 255, 1);
}

/* 表单选项 */
.form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}

/* 记住我 */
.remember-me {
    display: flex;
    align-items: center;
    gap: 8px;
}

.checkbox {
    width: 18px;
    height: 18px;
    cursor: pointer;
}

.checkbox-label {
    font-size: 14px;
    color: #6b7280;
    cursor: pointer;
    user-select: none;
}

/* 忘记密码 */
.forgot-password {
    font-size: 14px;
    color: #10b981;
    text-decoration: none;
    transition: color 0.3s ease;
}

.forgot-password:hover {
    color: #059669;
    text-decoration: underline;
}

/* 登录按钮 */
.login-button {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
    color: #ffffff;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(6, 78, 59, 0.25);
}

.login-button:hover:not(:disabled) {
    background: linear-gradient(135deg, #043f2f 0%, #059669 100%);
    box-shadow: 0 6px 20px rgba(6, 78, 59, 0.35);
    transform: translateY(-2px);
}

.login-button:active:not(:disabled) {
    transform: translateY(0);
}

.login-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* 加载动画 */
.loading-spinner {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.animate-spin {
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* 注册链接 */
.register-link {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #e5e7eb;
    font-size: 14px;
    color: #6b7280;
}

.register-btn {
    color: #10b981;
    text-decoration: none;
    font-weight: 600;
    margin-left: 4px;
    transition: color 0.3s ease;
}

.register-btn:hover {
    color: #059669;
    text-decoration: underline;
}

/* 错误提示 */
.error-message {
    padding: 12px 16px;
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 8px;
    color: #dc2626;
    font-size: 14px;
    margin-bottom: 24px;
    animation: shake 0.5s ease-in-out;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-8px); }
    75% { transform: translateX(8px); }
}

/* 淡入动画 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 浮动动画 */
@keyframes float {
    0%, 100% {
        transform: translate(0, 0);
    }
    25% {
        transform: translate(20px, -20px);
    }
    50% {
        transform: translate(-10px, 15px);
    }
    75% {
        transform: translate(15px, 10px);
    }
}

/* 响应式设计 */
@media (max-width: 640px) {
    .login-container {
        max-width: 100%;
    }

    .login-header {
        padding: 30px 20px 25px;
    }

    .login-title {
        font-size: 26px;
    }

    .login-form {
        padding: 25px 24px 20px;
    }
}
</style>
