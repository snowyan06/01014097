<template>
    <div class="account-container">
        <div class="account-header">
            <h1 class="text-2xl font-bold">账号信息</h1>
            <p class="text-gray-500">查看和管理您的账号信息</p>
        </div>

        <div class="account-card">
            <div class="account-info">
                <!-- 头像部分 -->
                <div class="info-item avatar-item">
                    <label class="info-label">头像</label>
                    <div class="avatar-section">
                        <div class="avatar-preview">
                            <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" class="avatar-image" />
                            <div v-else class="avatar-placeholder">
                                <i class="pi pi-user"></i>
                            </div>
                        </div>
                        <div class="avatar-actions">
                            <input
                                type="file"
                                ref="avatarInput"
                                accept="image/*"
                                @change="handleAvatarChange"
                                class="hidden"
                            />
                            <Button
                                label="选择头像"
                                icon="pi pi-upload"
                                @click="$refs.avatarInput.click()"
                                class="p-button-outlined p-button-sm"
                            />
                            <Button
                                v-if="userInfo.avatar"
                                label="移除头像"
                                icon="pi pi-trash"
                                @click="removeAvatar"
                                class="p-button-text p-button-sm p-button-danger"
                            />
                        </div>
                    </div>
                </div>

                <!-- 用户名 -->
                <div class="info-item">
                    <label class="info-label">用户名</label>
                    <span class="info-value">{{ userInfo.username }}</span>
                </div>

                <!-- 昵称 -->
                <div class="info-item">
                    <label class="info-label">昵称</label>
                    <div class="editable-field">
                        <span v-if="!editMode.nickname" class="info-value">{{ userInfo.nickname || '未设置' }}</span>
                        <InputText
                            v-else
                            v-model="editFormData.nickname"
                            class="w-full"
                            placeholder="请输入昵称"
                        />
                        <div class="action-buttons">
                            <Button
                                v-if="!editMode.nickname"
                                icon="pi pi-pencil"
                                @click="startEdit('nickname')"
                                class="p-button-text p-button-sm"
                            />
                            <template v-else>
                                <Button
                                    icon="pi pi-check"
                                    @click="saveEdit('nickname')"
                                    class="p-button-text p-button-sm p-button-success"
                                    :loading="saving"
                                />
                                <Button
                                    icon="pi pi-times"
                                    @click="cancelEdit('nickname')"
                                    class="p-button-text p-button-sm"
                                />
                            </template>
                        </div>
                    </div>
                </div>

                <!-- 邮箱 -->
                <div class="info-item">
                    <label class="info-label">邮箱</label>
                    <div class="editable-field">
                        <span v-if="!editMode.email" class="info-value">{{ userInfo.email || '未设置' }}</span>
                        <InputText
                            v-else
                            v-model="editFormData.email"
                            type="email"
                            class="w-full"
                            placeholder="请输入邮箱地址"
                        />
                        <div class="action-buttons">
                            <Button
                                v-if="!editMode.email"
                                icon="pi pi-pencil"
                                @click="startEdit('email')"
                                class="p-button-text p-button-sm"
                            />
                            <template v-else>
                                <Button
                                    icon="pi pi-check"
                                    @click="saveEdit('email')"
                                    class="p-button-text p-button-sm p-button-success"
                                    :loading="saving"
                                />
                                <Button
                                    icon="pi pi-times"
                                    @click="cancelEdit('email')"
                                    class="p-button-text p-button-sm"
                                />
                            </template>
                        </div>
                    </div>
                </div>

                <!-- 角色 -->
                <div class="info-item">
                    <label class="info-label">角色</label>
                    <span class="info-value">{{ getRoleLabel(userInfo.role) }}</span>
                </div>
            </div>
        </div>

        <!-- 消息提示 -->
        <Toast />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import axios from 'axios';

const toast = useToast();

const userInfo = ref({
    id: null,
    username: '',
    nickname: '',
    email: '',
    avatar: '',
    role: ''
});

const editMode = ref({
    username: false,
    nickname: false,
    email: false
});

const editFormData = ref({
    username: '',
    nickname: '',
    email: ''
});

const saving = ref(false);

const getRoleLabel = (role) => {
    const roleMap = {
        'user': '用户',
        'student': '学生', // 保留兼容旧数据
        'teacher': '教师', // 保留兼容旧数据
        'admin': '管理员' // 保留兼容旧数据
    };
    return roleMap[role] || role;
};

const fetchUserInfo = async () => {
    const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');

    if (authData?.id) {
        try {
            const response = await axios.get(`http://localhost:8081/api/user/profile/${authData.id}`);
            const data = response.data;

            userInfo.value = {
                id: data.id,
                username: data.username || '',
                nickname: data.nickname || '',
                email: data.email || '',
                avatar: data.avatar || '',
                role: data.role || ''
            };
        } catch (error) {
            console.error('获取用户信息出错:', error);
            toast.add({
                severity: 'error',
                summary: '错误',
                detail: '获取用户信息失败',
                life: 3000
            });

            userInfo.value = {
                id: authData.id,
                username: authData.username || '',
                nickname: authData.nickname || '',
                email: authData.email || '',
                avatar: authData.avatar || '',
                role: authData.role || ''
            };
        }
    }
};

const startEdit = (field) => {
    editFormData.value[field] = userInfo.value[field] || '';
    editMode.value[field] = true;
};

const cancelEdit = (field) => {
    editMode.value[field] = false;
    editFormData.value[field] = '';
};

const saveEdit = async (field) => {
    const value = editFormData.value[field];

    if (field === 'email' && value && !isValidEmail(value)) {
        toast.add({
            severity: 'error',
            summary: '验证失败',
            detail: '请输入有效的邮箱地址',
            life: 3000
        });
        return;
    }

    saving.value = true;

    try {
        const updateData = {};
        updateData[field] = value;

        const response = await axios.put(
            `http://localhost:8081/api/user/profile/${userInfo.value.id}`,
            updateData
        );

        const updatedData = response.data;
        userInfo.value[field] = updatedData[field] || value;

        editMode.value[field] = false;

        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
        authData[field] = updatedData[field] || value;
        localStorage.setItem('auth', JSON.stringify(authData));

        toast.add({
            severity: 'success',
            summary: '成功',
            detail: `${getFieldLabel(field)}已更新`,
            life: 3000
        });
    } catch (error) {
        console.error('更新失败:', error);
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: error.response?.data?.message || '更新失败',
            life: 3000
        });
    } finally {
        saving.value = false;
    }
};

const handleAvatarChange = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    // 验证文件类型
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        toast.add({
            severity: 'error',
            summary: '文件类型错误',
            detail: '请上传图片文件 (JPG/PNG/GIF/WEBP)',
            life: 3000
        });
        event.target.value = '';
        return;
    }

    // 验证文件大小（限制 3MB）
    const maxSize = 3 * 1024 * 1024;
    if (file.size > maxSize) {
        toast.add({
            severity: 'error',
            summary: '文件过大',
            detail: '图片大小不能超过 3MB',
            life: 3000
        });
        event.target.value = '';
        return;
    }

    const formData = new FormData();
    formData.append('avatar', file);

    saving.value = true;

    try {
        console.log('开始上传头像...');
        const response = await axios.post(
            `http://localhost:8081/api/user/avatar/${userInfo.value.id}`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        );

        console.log('上传成功:', response.data);

        const updatedData = response.data;
        userInfo.value.avatar = updatedData.avatar;

        // 更新 localStorage
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
        authData.avatar = updatedData.avatar;
        localStorage.setItem('auth', JSON.stringify(authData));

        // 触发一个自定义事件，通知其他组件头像已更新
        window.dispatchEvent(new CustomEvent('avatar-updated', { detail: { avatar: updatedData.avatar } }));

        toast.add({
            severity: 'success',
            summary: '成功',
            detail: '头像已更新',
            life: 3000
        });
    } catch (error) {
        console.error('头像上传失败详情:', error);
        console.error('错误响应:', error.response);

        let errorMsg = '头像上传失败';
        if (error.response) {
            errorMsg = error.response.data?.message || `服务器错误：${error.response.status}`;
        } else if (error.message) {
            errorMsg = error.message;
        }

        toast.add({
            severity: 'error',
            summary: '错误',
            detail: errorMsg,
            life: 5000
        });
    } finally {
        saving.value = false;
        event.target.value = '';
    }
};

const removeAvatar = async () => {
    saving.value = true;

    try {
        const response = await axios.put(
            `http://localhost:8081/api/user/profile/${userInfo.value.id}`,
            { avatar: '' }
        );

        userInfo.value.avatar = '';

        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth') || '{}');
        authData.avatar = '';
        localStorage.setItem('auth', JSON.stringify(authData));

        // 触发头像更新事件，通知其他组件
        window.dispatchEvent(new CustomEvent('avatar-updated', { detail: { avatar: '' } }));

        toast.add({
            severity: 'success',
            summary: '成功',
            detail: '头像已移除',
            life: 3000
        });
    } catch (error) {
        console.error('移除头像失败:', error);
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: '移除头像失败',
            life: 3000
        });
    } finally {
        saving.value = false;
    }
};

const isValidEmail = (email) => {
    const emailRegex = /^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    return emailRegex.test(email);
};

const getFieldLabel = (field) => {
    const labels = {
        'username': '用户名',
        'nickname': '昵称',
        'email': '邮箱'
    };
    return labels[field] || field;
};

onMounted(() => {
    fetchUserInfo();
});
</script>

<style scoped>
.account-container {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

.account-header {
    margin-bottom: 2rem;
}

.account-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 2rem;
}

.account-info {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e0e0e0;
}

.info-item:last-child {
    border-bottom: none;
}

.info-label {
    font-weight: 500;
    color: #666;
    min-width: 80px;
}

.info-value {
    font-weight: 600;
    color: #333;
    flex: 1;
    text-align: right;
}

.avatar-item {
    align-items: flex-start;
}

.avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    width: 100%;
}

.avatar-preview {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: hidden;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
}

.avatar-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
}

.editable-field {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    justify-content: flex-end;
}

.action-buttons {
    display: flex;
    gap: 0.25rem;
}

@media (max-width: 768px) {
    .account-container {
        padding: 1rem;
    }

    .account-card {
        padding: 1.5rem;
    }

    .info-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .info-value {
        text-align: left;
        width: 100%;
    }

    .editable-field {
        flex-direction: column;
        align-items: stretch;
    }

    .action-buttons {
        justify-content: flex-start;
    }
}
</style>
