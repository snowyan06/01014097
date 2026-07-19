<template>
    <div class="stats-card">
        <h3>{{ title }}</h3>
        <div class="stats-value" :class="type">
            {{ value || 0 }}
        </div>

        <div v-if="secondaryValue !== undefined" class="stats-secondary">
            {{ secondaryLabel }}: {{ secondaryValue || 0 }}
        </div>

        <div class="stats-preview" v-if="details && details.length">
            <div v-for="(item, index) in previewItems" :key="getItemKey(item, index)" class="preview-item">
                <span>{{ getItemName(item) }}:</span>
                <span>{{ getItemValue(item) }}</span>
            </div>
        </div>

        <button v-if="details.length > 3" class="show-more" @click="$emit('show-more')">
            查看更多 ({{ details.length }})
        </button>
    </div>
</template>

<script>
export default {
    name: 'StatsCard',
    props: {
        title: String,
        value: [Number, String],
        secondaryValue: [Number, String],
        secondaryLabel: String,
        details: {
            type: Array,
            default: () => []
        },
        type: {
            type: String,
            default: 'teacher' // 'teacher' or 'student'
        }
    },
    computed: {
        previewItems() {
            return this.details.slice(0, 3);
        }
    },
    methods: {
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
.stats-card {
    flex: 1;
    min-width: 250px;
    background: #f9f9f9;
    border-radius: 6px;
    padding: 15px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stats-card h3 {
    margin-top: 0;
    color: #555;
    font-size: 16px;
}

.stats-value {
    font-size: 32px;
    font-weight: bold;
    margin: 10px 0;
}

.stats-value.teacher {
    color: #3498db;
}

.stats-value.student {
    color: #2ecc71;
}

.stats-secondary {
    font-size: 14px;
    color: #666;
    margin-bottom: 10px;
}

.stats-preview {
    margin-top: 10px;
    font-size: 14px;
    color: #666;
}

.preview-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.show-more {
    margin-top: 10px;
    background: none;
    border: none;
    color: #3498db;
    cursor: pointer;
    font-size: 12px;
    padding: 2px 5px;
}

.show-more:hover {
    text-decoration: underline;
}
</style>
