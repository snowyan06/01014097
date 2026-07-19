<template>
    <div class="settings-container">
        <div class="settings-header">
            <h1 class="text-2xl font-bold">设置</h1>
            <p class="text-gray-500">管理您的账号设置</p>
        </div>

        <div class="settings-card">
            <div class="settings-section">
                <h2 class="section-title">账号设置</h2>
                <div class="setting-item">
                    <label class="setting-label">通知偏好</label>
                    <div class="setting-control">
                        <input type="checkbox" id="notifications" v-model="settings.notifications">
                        <label for="notifications">接收系统通知</label>
                    </div>
                </div>
                <div class="setting-item">
                    <label class="setting-label">深色模式</label>
                    <div class="setting-control">
                        <input type="checkbox" id="darkMode" v-model="settings.darkMode">
                        <label for="darkMode">启用深色模式</label>
                    </div>
                </div>
            </div>

            <div class="settings-section">
                <h2 class="section-title">安全设置</h2>
                <div class="setting-item">
                    <label class="setting-label">修改密码</label>
                    <div class="setting-control">
                        <button class="btn-primary" @click="openPasswordDialog">修改密码</button>
                    </div>
                </div>
                <div class="setting-item">
                    <label class="setting-label">登录设备</label>
                    <div class="setting-control">
                        <button class="btn-primary" @click="openDeviceDialog">查看登录设备</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 修改密码弹窗 -->
        <Dialog v-model:visible="showPasswordDialog" modal header="修改密码" :style="{ width: '400px' }">
            <div class="password-form">
                <div class="p-field">
                    <label for="oldPassword">旧密码</label>
                    <InputText id="oldPassword" v-model="oldPassword" type="password" placeholder="请输入旧密码" />
                </div>
                <div class="p-field">
                    <label for="newPassword">新密码</label>
                    <InputText id="newPassword" v-model="newPassword" type="password" placeholder="请输入新密码" />
                </div>
                <div class="p-field">
                    <label for="confirmPassword">确认新密码</label>
                    <InputText id="confirmPassword" v-model="confirmPassword" type="password" placeholder="请确认新密码" />
                </div>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" @click="showPasswordDialog = false" outlined />
                <Button label="确定" icon="pi pi-check" @click="handleChangePassword" autofocus />
            </template>
        </Dialog>

        <!-- 登录设备弹窗 -->
        <Dialog v-model:visible="showDeviceDialog" modal header="登录设备" :style="{ width: '500px' }">
            <div class="device-info">
                <div class="info-item">
                    <label>浏览器：</label>
                    <span>{{ deviceInfo.browser }}</span>
                </div>
                <div class="info-item">
                    <label>操作系统：</label>
                    <span>{{ deviceInfo.os }}</span>
                </div>
                <div class="info-item">
                    <label>IP 地址：</label>
                    <span>{{ deviceInfo.ip || '获取中...' }}</span>
                </div>
                <div class="info-item">
                    <label>登录时间：</label>
                    <span>{{ deviceInfo.lastLoginTime }}</span>
                </div>
            </div>
            <template #footer>
                <Button label="关闭" icon="pi pi-times" @click="showDeviceDialog = false" autofocus />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

const settings = ref({
    notifications: true,
    darkMode: false
});

// 密码相关变量
const showPasswordDialog = ref(false);
const oldPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

// 设备信息变量
const showDeviceDialog = ref(false);
const deviceInfo = ref({
    browser: '',
    os: '',
    ip: '',
    lastLoginTime: ''
});

const loadSettings = () => {
    const savedSettings = localStorage.getItem('userSettings');
    if (savedSettings) {
        settings.value = { ...settings.value, ...JSON.parse(savedSettings) };
    }
};

const saveSettings = () => {
    localStorage.setItem('userSettings', JSON.stringify(settings.value));
};

// 打开密码弹窗
const openPasswordDialog = () => {
    oldPassword.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
    showPasswordDialog.value = true;
};

// 修改密码处理函数
const handleChangePassword = async () => {
    // 验证输入
    if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: '请填写所有字段',
            life: 3000
        });
        return;
    }

    if (newPassword.value !== confirmPassword.value) {
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: '两次输入的密码不一致',
            life: 3000
        });
        return;
    }

    if (oldPassword.value === newPassword.value) {
        toast.add({
            severity: 'warn',
            summary: '警告',
            detail: '新密码不能与旧密码重复',
            life: 3000
        });
        return;
    }

    try {
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
        const userId = authData?.id;

        if (!userId) {
            toast.add({
                severity: 'error',
                summary: '错误',
                detail: '用户未登录',
                life: 3000
            });
            return;
        }

        // 调用后端 API 修改密码
        const response = await fetch(`/api/admin/users/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                password: newPassword.value
            })
        });

        if (response.ok) {
            toast.add({
                severity: 'success',
                summary: '成功',
                detail: '密码修改成功',
                life: 3000
            });

            showPasswordDialog.value = false;
            oldPassword.value = '';
            newPassword.value = '';
            confirmPassword.value = '';
        } else {
            const error = await response.json();
            toast.add({
                severity: 'error',
                summary: '错误',
                detail: error.message || '修改失败',
                life: 3000
            });
        }
    } catch (error) {
        console.error('修改密码出错:', error);
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: '网络错误，请稍后重试',
            life: 3000
        });
    }
};

// 打开设备信息弹窗
const openDeviceDialog = async () => {
    const userAgent = navigator.userAgent;

    // 检测浏览器
    if (userAgent.indexOf('Chrome') > -1) {
        deviceInfo.value.browser = 'Chrome';
    } else if (userAgent.indexOf('Firefox') > -1) {
        deviceInfo.value.browser = 'Firefox';
    } else if (userAgent.indexOf('Safari') > -1) {
        deviceInfo.value.browser = 'Safari';
    } else if (userAgent.indexOf('Edge') > -1) {
        deviceInfo.value.browser = 'Edge';
    } else {
        deviceInfo.value.browser = 'Unknown';
    }

    // 检测操作系统
    if (userAgent.indexOf('Win') > -1) {
        deviceInfo.value.os = 'Windows';
    } else if (userAgent.indexOf('Mac') > -1) {
        deviceInfo.value.os = 'macOS';
    } else if (userAgent.indexOf('Linux') > -1) {
        deviceInfo.value.os = 'Linux';
    } else if (userAgent.indexOf('Android') > -1) {
        deviceInfo.value.os = 'Android';
    } else if (userAgent.indexOf('iOS') > -1) {
        deviceInfo.value.os = 'iOS';
    }

    // 模拟 IP（实际项目中应该从后端获取）
    deviceInfo.value.ip = '192.168.1.100';

    // 获取登录时间
    const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
    if (authData?.timestamp) {
        deviceInfo.value.lastLoginTime = new Date(authData.timestamp).toLocaleString('zh-CN');
    }

    showDeviceDialog.value = true;
};

watch(settings, (newSettings) => {
    saveSettings();

    // 应用深色模式
    if (newSettings.darkMode) {
        document.documentElement.classList.add('app-dark');
    } else {
        document.documentElement.classList.remove('app-dark');
    }
}, { deep: true });

onMounted(() => {
    loadSettings();
});
</script>

<style scoped>
.settings-container {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

.settings-header {
    margin-bottom: 2rem;
}

.settings-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 2rem;
}

.settings-section {
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #e0e0e0;
}

.settings-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: #333;
}

.setting-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.setting-item:last-child {
    border-bottom: none;
}

.setting-label {
    font-weight: 500;
    color: #666;
}

.setting-control {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-primary {
    background-color: #3CC88F;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-primary:hover {
    background-color: #35b37f;
}

.password-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.p-field {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.device-info {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.info-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
    border-bottom: none;
}

.info-item label {
    font-weight: 600;
    color: #666;
}

.info-item span {
    color: #333;
}

/* 深色模式全局样式 */
.app-dark body {
    background-color: #1a1a2e !important;
    color: #e0e0e0 !important;
}

.app-dark .settings-container {
    background-color: #1a1a2e !important;
}

.app-dark .settings-card {
    background-color: #16213e !important;
    color: #e0e0e0 !important;
}

.app-dark .section-title {
    color: #e0e0e0 !important;
}

.app-dark .setting-label {
    color: #b0b0b0 !important;
}

.app-dark .info-item label {
    color: #b0b0b0 !important;
}

.app-dark .info-item span {
    color: #ffffff !important;
}

.app-dark input[type="text"],
.app-dark input[type="password"] {
    background-color: #0f3460 !important;
    color: #e0e0e0 !important;
    border-color: #1a1a2e !important;
}

@media (max-width: 768px) {
    .settings-container {
        padding: 1rem;
    }

    .settings-card {
        padding: 1.5rem;
    }

    .setting-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .setting-control {
        align-self: flex-end;
    }
}
</style>
