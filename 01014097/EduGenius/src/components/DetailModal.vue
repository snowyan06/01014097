<template>
    <div class="modal-overlay" @click.self="handleClose">
        <div class="modal-container">
            <div class="modal-header">
                <h3>{{ title }}</h3>
                <button class="close-btn" @click="handleClose">&times;</button>
            </div>
            <div class="modal-content">
                <div v-if="items.length === 0" class="empty">暂无数据</div>
                <div v-else class="detail-list">
                    <div v-for="(item, index) in items" :key="getItemKey(item, index)" class="detail-item">
                        <span class="name">{{ getItemName(item) }}</span>
                        <span class="value">{{ getItemValue(item) }}</span>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                共 {{ items.length }} 条记录
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DetailModal',
    props: {
        title: String,
        items: {
            type: Array,
            default: () => []
        },
        type: {
            type: String,
            default: 'teacher' // 'teacher' or 'student'
        }
    },
    methods: {
        handleClose() {
            this.$emit('close');
        },
        getItemKey(item, index) {
            return item.teacherId || item.userId || index;
        },
        getItemName(item) {
            if (this.type === 'teacher') {
                return item.nickname || '未知教师';
            }
            return item.nickname || '匿名用户';
        },
        getItemValue(item) {
            if (this.type === 'teacher') {
                return `${item.questionCount}题`;
            }
            return `${item.count}次`;
        }
    }
}
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-container {
    background: white;
    border-radius: 8px;
    width: 80%;
    max-width: 600px;
    max-height: 80vh;
    display: flex;
    flex-direction: column;
}

.modal-header {
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h3 {
    margin: 0;
}

.close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
}

.modal-content {
    padding: 20px;
    overflow-y: auto;
    flex: 1;
}

.empty {
    text-align: center;
    color: #999;
}

.detail-list {
    display: grid;
    gap: 10px;
}

.detail-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #f5f5f5;
}

.detail-item .name {
    font-weight: 500;
}

.detail-item .value {
    color: #3498db;
}

.modal-footer {
    padding: 10px 20px;
    border-top: 1px solid #eee;
    text-align: right;
    font-size: 14px;
    color: #666;
}
</style>
