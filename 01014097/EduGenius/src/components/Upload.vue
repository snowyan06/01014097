<template>
    <div class="upload-container p-4 surface-card border-round" style="max-width: 800px; margin: 0 auto">
        <!-- 文件选择区域 - 只在未上传成功时显示 -->
        <div v-if="!isUploadSuccess" class="upload-area p-4 border-1 border-300 border-round mb-4 text-center">
            <FileUpload
                mode="basic"
                name="file"
                accept=".doc,.docx,.txt,.xlsx"
                :maxFileSize="10000000"
                @select="handleFileSelect"
                chooseLabel="点击选择文件"
                :auto="false"
                class="w-full"
            />
            <small class="text-500 block mt-2">支持Word、Excel和文本文件，最大10MB</small>
        </div>

        <!-- 文件信息和操作 -->
        <div v-if="selectedFile" class="file-info p-3 mb-4 flex align-items-center surface-100 border-round gap-3">
            <i class="pi pi-file text-xl" :class="fileIconClass"></i>
            <div class="flex-grow-1 overflow-hidden">
                <div class="font-medium truncate">{{ selectedFile.name }}</div>
                <div class="text-sm text-500">{{ formatFileSize(selectedFile.size) }}</div>
            </div>
            <Button
                icon="pi pi-times"
                class="p-button-text p-button-sm"
                @click="clearSelection"
            />
        </div>

        <!-- 上传按钮 - 只在有选中文件且未上传成功时显示 -->
        <div v-if="selectedFile && !isUploadSuccess" class="text-center mb-4">
            <Button
                label="上传文件"
                icon="pi pi-upload"
                @click="handleUpload"
                class="p-button-raised w-full sm:w-auto"
                :loading="uploadStatus === 'uploading'"
            />
        </div>

        <!-- 上传状态反馈 -->
        <Message v-if="uploadMessage" :severity="uploadStatus" class="mb-4">
            <i class="pi mr-2" :class="{
                'pi-spinner pi-spin': uploadStatus === 'uploading',
                'pi-check-circle': uploadStatus === 'success',
                'pi-times-circle': uploadStatus === 'error'
            }"></i>
            <span>{{ uploadMessage }}</span>
        </Message>

        <!-- 内容展示区域 -->
        <div v-if="uploadResult" class="result-container p-4 surface-100 border-round">
            <!-- 文本内容展示 -->
            <div v-if="contentText" class="mb-5">
                <div class="flex align-items-center justify-content-between mb-3">
                    <h4 class="m-0">文本内容 <span v-if="lineCount">(共 {{ lineCount }} 行)</span></h4>
                    <Button
                        icon="pi pi-copy"
                        label="复制文本"
                        class="p-button-sm  ml-auto"
                        @click="copyTextContent"
                    />
                </div>
                <div class="text-content p-3 bg-white border-round">
                    <pre class="m-0 p-0 whitespace-pre-wrap font-sans text-sm">{{ contentText }}</pre>
                </div>
            </div>

            <!-- 表格展示 - 统一处理Word和Excel表格 -->
            <div v-if="contentTables.length > 0">
                <div v-for="(table, index) in contentTables" :key="'table-'+index" class="mb-5">
                    <h4 class="mb-3">{{ table.title }}</h4>
                    <div v-if="table.data.length === 0" class="p-3 bg-gray-100 border-round">
                        <p class="text-gray-600 m-0">此表格为空</p>
                    </div>
                    <DataTable
                        v-else
                        :value="table.data"
                        class="p-datatable-sm"
                        responsiveLayout="scroll"
                        :scrollable="true"
                        scrollHeight="flex"
                    >
                        <Column
                            v-for="col in table.columns"
                            :key="col.field"
                            :field="col.field"
                            :header="col.header"
                        >
                            <template #body="{ data }">
                                {{ data[col.field] ?? '-' }}
                            </template>
                        </Column>
                    </DataTable>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue';
import axios from 'axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

export default {
    components: {
        DataTable,
        Column
    },
    props: {
        // 从父组件接收的解析结果
        parsedData: {
            type: Object,
            default: null
        }
    },
    emits: ['update:parsedData'],
    setup(props, { emit }) {
        const selectedFile = ref(null);
        const uploadStatus = ref(null);
        const uploadMessage = ref('');
        const uploadResult = ref(null);

        // 计算属性，判断是否上传成功
        const isUploadSuccess = computed(() => {
            return uploadStatus.value === 'success';
        });

        // 根据文件类型获取图标类
        const fileIconClass = computed(() => {
            if (!selectedFile.value) return '';
            const ext = selectedFile.value.name.split('.').pop().toLowerCase();
            switch (ext) {
                case 'docx':
                    return 'pi pi-file-word text-blue-600';
                case 'xlsx':
                    return 'pi pi-file-excel text-green-600';
                case 'txt':
                    return 'pi pi-file text-gray-600';
                default:
                    return 'pi pi-file';
            }
        });

        // 统一文本内容
        const contentText = computed(() => {
            if (!uploadResult.value?.content) return '';

            // 处理Word文档文本
            if (uploadResult.value.content.text) {
                return uploadResult.value.content.text.join('\n');
            }
            // 处理文本文件内容
            if (uploadResult.value.content.lines) {
                return uploadResult.value.content.lines.join('\n');
            }
            // 处理Excel中没有表格的文本
            if (isExcelData(uploadResult.value.content)) {
                const sheets = Object.values(uploadResult.value.content);
                if (sheets.length === 1 && sheets[0].length === 1 && sheets[0][0].length === 1) {
                    return String(sheets[0][0][0]);
                }
            }
            return '';
        });

        // 检查是否为Excel数据
        const isExcelData = (content) => {
            return content &&
                !content.text &&
                !content.lines &&
                !content.tables &&
                Object.keys(content).some(key => Array.isArray(content[key]));
        };

        // 行数统计
        const lineCount = computed(() => {
            if (uploadResult.value?.content?.line_count) {
                return uploadResult.value.content.line_count;
            }
            if (contentText.value) {
                return contentText.value.split('\n').length;
            }
            return 0;
        });

        // 统一表格数据
        const contentTables = computed(() => {
            const tables = [];

            if (!uploadResult.value?.content) return tables;

            const content = uploadResult.value.content;

            // 处理Word表格
            if (content.tables) {
                content.tables.forEach((table, index) => {
                    tables.push({
                        title: `表格 ${index + 1}`,
                        data: formatTableData(table),
                        columns: table[0]?.map((col, colIndex) => ({
                            field: colIndex.toString(),
                            header: col || `列 ${colIndex + 1}`
                        })) || []
                    });
                });
            }

            // 处理Excel表格
            if (isExcelData(content)) {
                Object.entries(content).forEach(([sheetName, sheet]) => {
                    tables.push({
                        title: `工作表: ${sheetName}`,
                        data: formatExcelData(sheet),
                        columns: excelColumns(sheet)
                    });
                });
            }

            return tables;
        });

        // Excel列配置
        const excelColumns = (sheet) => {
            if (!sheet || sheet.length === 0) return [];

            // 处理单行单列数据
            if (sheet.length === 1 && sheet[0].length === 1) {
                return [{
                    field: 'value',
                    header: '值'
                }];
            }

            // 处理多列数据
            const maxColumns = Math.max(...sheet.map(row => row.length));
            return Array.from({ length: maxColumns }, (_, i) => ({
                field: `col${i}`,
                header: `列 ${i + 1}`
            }));
        };

        // 格式化Excel数据
        const formatExcelData = (sheet) => {
            if (!sheet || sheet.length === 0) return [];

            // 处理单行单列数据
            if (sheet.length === 1 && sheet[0].length === 1) {
                return [{ value: sheet[0][0] }];
            }

            // 处理多行多列数据
            return sheet.map((row, rowIndex) => {
                const rowData = {};
                row.forEach((cell, colIndex) => {
                    rowData[`col${colIndex}`] = cell;
                });
                return rowData;
            });
        };

        // 格式化Word表格数据
        const formatTableData = (table) => {
            if (!table || table.length === 0) return [];
            return table.slice(1).map(row => {
                const rowData = {};
                row.forEach((cell, index) => {
                    rowData[index] = cell;
                });
                return rowData;
            });
        };

        const handleFileSelect = (event) => {
            selectedFile.value = event.files[0];
            uploadStatus.value = null;
            uploadMessage.value = '';
            uploadResult.value = null;
        };

        const clearSelection = () => {
            selectedFile.value = null;
            uploadStatus.value = null;
            uploadMessage.value = '';
            uploadResult.value = null;
        };

        const handleUpload = async () => {
            if (!selectedFile.value) return;

            uploadStatus.value = 'uploading';
            uploadMessage.value = '文件上传解析中，请稍候...';

            const formData = new FormData();
            formData.append('file', selectedFile.value);

            try {
                const response = await axios.post('http://localhost:8000/upload-file', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                uploadStatus.value = 'success';
                uploadMessage.value = '文件解析成功';
                uploadResult.value = response.data;

                // 新增：将解析结果发送给父组件
                emit('update:parsedData', response.data);
            } catch (error) {
                uploadStatus.value = 'error';
                uploadMessage.value = error.response?.data?.message || '文件解析失败';
                console.error('上传错误:', error);
            }
        };

        const formatFileSize = (bytes) => {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        };

        const copyTextContent = () => {
            if (!contentText.value) return;
            navigator.clipboard.writeText(contentText.value);
            uploadMessage.value = '文本内容已复制';
            uploadStatus.value = 'success';
        };

        return {
            selectedFile,
            uploadStatus,
            uploadMessage,
            uploadResult,
            isUploadSuccess,
            fileIconClass,
            contentText,
            lineCount,
            contentTables,
            handleFileSelect,
            clearSelection,
            handleUpload,
            formatFileSize,
            copyTextContent
        };
    }
};
</script>

<style scoped>
/* 样式部分保持不变 */
.upload-container {
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.upload-area {
    transition: all 0.3s ease;
    cursor: pointer;
    border: 2px dashed var(--surface-300);
    background-color: var(--surface-50);
}

.upload-area:hover {
    border-color: var(--primary-color);
    background-color: var(--surface-100);
}

.file-info {
    transition: all 0.3s ease;
    min-height: 3.5rem;
}

.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.result-container {
    max-height: 70vh;
    overflow-y: auto;
    width: 100%;
}

.text-content {
    max-height: 40vh;
    overflow-y: auto;
    line-height: 1.6;
    background: white;
    padding: 1rem;
    border-radius: 4px;
    width: 100%;
    min-width: 0;
}

.text-content pre {
    white-space: pre-wrap;
    word-break: break-word;
    overflow-wrap: break-word;
    font-family: inherit;
    max-width: 100%;
}

.p-datatable {
    font-size: 0.9rem;
}

.p-datatable-wrapper {
    max-height: 400px;
    overflow: auto;
}

@media (min-width: 576px) {
    .upload-container {
        padding: 1.5rem;
    }

    .upload-area {
        padding: 2rem;
    }
}

@media (min-width: 768px) {
    .upload-container {
        max-width: 900px;
    }

    .text-content {
        padding: 1.5rem;
    }
}

@media (min-width: 992px) {
    .upload-container {
        max-width: 1100px;
    }

    .text-content pre {
        font-size: 0.9rem;
    }
}

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--surface-100);
}

::-webkit-scrollbar-thumb {
    background: var(--surface-300);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--surface-400);
}
</style>
