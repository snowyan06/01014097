<template>
    <div class="exam-processing-container">

        <div class="grid">
            <!-- 试卷处理模块 -->
            <div class="col-12 md:col-6">
                <Card class="module-card">
                    <template #title>
                        <div class="card-title">
                            <i class="pi pi-file-edit"></i>
                            <span>试卷处理</span>
                        </div>
                    </template>
                    <template #content>
                        <div class="upload-section">
                            <FileUpload
                                mode="basic"
                                name="examFile"
                                :auto="true"
                                :multiple="false"
                                :customUpload="true"
                                accept=".pdf,.docx,.txt"
                                :maxFileSize="10000000"
                                chooseLabel="选择试卷文件"
                                @select="onExamSelect"
                                @clear="removeExamFile"
                                :disabled="processingExam"
                            />

                            <div v-if="examFile" class="file-info">
                                <i class="pi pi-file"></i>
                                <span>{{ examFile.name }}</span>
                                <i class="pi pi-times remove-icon" @click="removeExamFile"></i>
                            </div>
                        </div>

                        <div class="action-section">
                            <Button
                                label="处理试卷"
                                icon="pi pi-cog"
                                class="process-btn"
                                :loading="processingExam"
                                :disabled="!examFile"
                                @click="processExam"
                            />
                        </div>

                        <div v-if="examResult" class="result-section">
                            <Divider align="center">
                                <span class="p-tag p-tag-success">
                                    <i class="pi pi-check-circle"></i>
                                    处理完成
                                </span>
                            </Divider>

                            <div class="result-content">
                                <p class="result-message">{{ examResult.message }}</p>
                                <div class="download-buttons">
                                    <Button
                                        v-if="examResult.answer_file"
                                        label="下载标准答案"
                                        icon="pi pi-download"
                                        severity="success"
                                        outlined
                                        @click="downloadFile(examResult.answer_file)"
                                    />
                                    <Button
                                        v-if="examResult.rubric_file"
                                        label="下载评分标准"
                                        icon="pi pi-download"
                                        severity="success"
                                        outlined
                                        @click="downloadFile(examResult.rubric_file)"
                                    />
                                </div>
                            </div>
                        </div>
                    </template>
                </Card>
            </div>

            <!-- 成绩分析模块 -->
            <div class="col-12 md:col-6">
                <Card class="module-card">
                    <template #title>
                        <div class="card-title">
                            <i class="pi pi-chart-line"></i>
                            <span>成绩分析</span>
                        </div>
                    </template>
                    <template #content>
                        <div class="upload-section">
                            <FileUpload
                                mode="basic"
                                name="analysisFile"
                                :auto="true"
                                :multiple="false"
                                :customUpload="true"
                                accept=".xlsx"
                                :maxFileSize="10000000"
                                chooseLabel="选择Excel文件"
                                @select="onAnalysisSelect"
                                @clear="removeAnalysisFile"
                                :disabled="analyzingExam"
                            />

                            <div v-if="analysisFile" class="file-info">
                                <i class="pi pi-file-excel"></i>
                                <span>{{ analysisFile.name }}</span>
                                <i class="pi pi-times remove-icon" @click="removeAnalysisFile"></i>
                            </div>
                        </div>

                        <div class="action-section">
                            <Button
                                label="分析成绩"
                                icon="pi pi-chart-bar"
                                class="analyze-btn"
                                :loading="analyzingExam"
                                :disabled="!analysisFile"
                                @click="analyzeExam"
                            />
                        </div>

                        <div v-if="analysisResult" class="result-section">
                            <Divider align="center">
                                <span class="p-tag p-tag-info">
                                    <i class="pi pi-check-circle"></i>
                                    分析完成
                                </span>
                            </Divider>

                            <div class="result-content">
                                <p class="result-message">{{ analysisResult.message }}</p>
                                <div class="download-buttons">
                                    <Button
                                        v-if="analysisResult.report_path"
                                        label="下载分析报告"
                                        icon="pi pi-download"
                                        severity="info"
                                        outlined
                                        @click="downloadFile(analysisResult.report_filename)"
                                    />
                                </div>
                            </div>
                        </div>
                    </template>
                </Card>
            </div>

            <!-- 教学建议模块 -->
            <div class="col-12">
                <Card class="module-card">
                    <template #title>
                        <div class="card-title">
                            <i class="pi pi-comment"></i>
                            <span>教学建议</span>
                        </div>
                    </template>
                    <template #content>
                        <div class="suggestion-section">
                            <Textarea
                                v-model="suggestionText"
                                rows="5"
                                cols="30"
                                placeholder="请输入教学建议..."
                                autoResize
                                class="suggestion-textarea"
                            />

                            <div class="character-count">
                                {{ suggestionText.length }}/500
                            </div>
                        </div>

                        <div class="action-section">
                            <Button
                                label="提交建议"
                                icon="pi pi-paper-plane"
                                severity="info"
                                class="submit-btn"
                                :loading="submittingSuggestion"
                                :disabled="!suggestionText.trim()"
                                @click="submitSuggestion"
                            />
                        </div>

                        <div v-if="suggestionSubmitted" class="success-message">
                            <i class="pi pi-check-circle"></i>
                            教学建议已成功提交！
                        </div>
                    </template>
                </Card>
            </div>
        </div>

        <Toast position="top-right" />
        <ConfirmDialog />
    </div>
</template>

<script setup>
import { nextTick, ref } from 'vue';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
import { defineProps } from 'vue'

// 文件上传相关状态
const examFile = ref(null);
const analysisFile = ref(null);
const processingExam = ref(false);
const analyzingExam = ref(false);
const examResult = ref(null);
const analysisResult = ref(null);

// 教学建议相关状态
const suggestionText = ref('');
const submittingSuggestion = ref(false);
const suggestionSubmitted = ref(false);
const props = defineProps({
    prepTime: {
        type: Number,
        required: true
    },
    prepRevisions: {
        type: Number,
        required: true
    }
})

// 选择试卷文件
const onExamSelect = async (event) => {
    const file = event.files?.[0] || event.originalEvent?.files?.[0];
    if (!file) {
        console.error("未获取到文件对象", event);
        return;
    }

    examFile.value = null;
    await nextTick();

    examFile.value = new File([file], file.name, {
        type: file.type,
        lastModified: file.lastModified
    });
};

// 选择分析文件（Excel）
const onAnalysisSelect = async (event) => {
    const file = event.files?.[0] || event.originalEvent?.files?.[0];
    if (!file) return;

    analysisFile.value = null;
    await nextTick();

    analysisFile.value = new File([file], file.name, {
        type: file.type,
        lastModified: file.lastModified
    });
};

// 删除文件
const removeExamFile = () => {
    examFile.value = null;
    examResult.value = null;
};

const removeAnalysisFile = () => {
    analysisFile.value = null;
    analysisResult.value = null;
};
const getBeijingTime = () => {
    const now = new Date();
    now.setHours(now.getHours() + 8); // UTC+8
    return now.toISOString(); // 格式: "2025-07-15T18:40:08.519Z"（自动调整时区）
};
// 处理试卷
const processExam = async () => {
    if (!examFile.value) return;
    processingExam.value = true;
    try {
        const formData = new FormData();
        formData.append('file', examFile.value);

        // 1. 先处理试卷
        const response = await axios.post('http://localhost:8000/process-exam', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        examResult.value = response.data;
        console.log(response.data)

        // 2. 获取当前教师ID
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth'));
        const teacherId = authData?.id;
        if (!teacherId) {
            throw new Error("未找到教师ID，请先登录");
        }

        // 3. 保存标准答案文件
        const answerFileName = examResult.value.answer_file.split('/').pop();
        const answerFileNameWithoutExt = answerFileName.replace(/\.[^/.]+$/, "");
        const createdAt = getBeijingTime();
        const answerFileInfo = {
            resourceName: answerFileNameWithoutExt,
            fileType: answerFileName.split('.').pop().toUpperCase(),
            teacherId: teacherId,
            fileSize: examResult.value.answer_size,
            filePath: answerFileName,
            createdAt: createdAt
        };
        console.log(answerFileInfo)

        await axios.post('http://localhost:8080/api/teaching-materials', answerFileInfo);

        // 4. 保存评分标准文件
        if (examResult.value.rubric_file) {
            const rubricFileName = examResult.value.rubric_file.split('/').pop();
            const rubricFileNameWithoutExt = rubricFileName.replace(/\.[^/.]+$/, "");

            const rubricFileInfo = {
                resourceName: rubricFileNameWithoutExt,
                fileType: rubricFileName.split('.').pop().toUpperCase(),
                teacherId: teacherId,
                fileSize: examResult.value.rubric_size,
                filePath: rubricFileName,
                createdAt: createdAt
            };

            await axios.post('http://localhost:8080/api/teaching-materials', rubricFileInfo);
        }

        toast.add({
            severity: 'success',
            summary: '成功',
            detail: '试卷处理成功，标准答案和评分标准已保存到教学资料库',
            life: 3000
        });
    } catch (error) {
        console.error('处理失败:', error);
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: error.response?.data?.detail || '处理过程中出错',
            life: 5000
        });
    } finally {
        processingExam.value = false;
    }
};
// 分析成绩
const analyzeExam = async () => {
    if (!analysisFile.value) return;

    analyzingExam.value = true;

    try {
        const formData = new FormData();
        formData.append('file', analysisFile.value);

        // 1. 分析成绩
        const response = await axios.post('http://localhost:8000/analyze-exam', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        analysisResult.value = response.data;

        // 2. 获取当前教师ID
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth'));
        const teacherId = authData?.id;
        if (!teacherId) {
            throw new Error("未找到教师ID，请先登录");
        }

        // 3. 使用标准的ISO格式时间
        const createdAt = getBeijingTime();

        // 4. 提取文件名
        const reportFileName = analysisResult.value.report_path.split(/[\\/]/).pop();
        const fileNameWithoutExt = reportFileName.replace(/\.[^/.]+$/, "");

        // 5. 构造请求数据（完全匹配成功案例的格式）
        const fileInfo = {
            resourceName: fileNameWithoutExt,
            fileType: reportFileName.split('.').pop().toUpperCase(),
            teacherId: teacherId,
            fileSize: analysisResult.value.report_size,
            filePath: reportFileName,
            createdAt: createdAt // 使用ISO格式
        };


        // 6. 发送请求
        const saveResponse = await axios.post(
            'http://localhost:8080/api/teaching-materials',
            fileInfo
        );

        toast.add({
            severity: 'success',
            summary: '成功',
            detail: '成绩分析成功并已保存到教学资料库',
            life: 3000
        });
    } catch (error) {
        console.error('完整错误信息:', {
            message: error.message,
            response: error.response?.data,
            config: error.config
        });
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: error.response?.data?.message || '分析过程中出错',
            life: 5000
        });
    } finally {
        analyzingExam.value = false;
    }
};

// 下载文件
const downloadFile = (filename) => {
    try {
        const fileName = filename.split('/').pop();
        const encodedName = encodeURIComponent(fileName);

        const link = document.createElement('a');
        link.href = `http://localhost:8080/api/files/download/${encodedName}`;
        console.log(`尝试下载文件: ${filename}`);
        link.target = '_blank';
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('下载失败:', error);
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: '文件下载失败，请重试',
            life: 5000
        });
    }
};

// 提交教学建议
const submitSuggestion = async () => {
    if (!suggestionText.value.trim()) return;
    submittingSuggestion.value = true;

    try {
        const authData = JSON.parse(localStorage.getItem('auth') || sessionStorage.getItem('auth'));
        const teacherId = authData?.id;
        if (!teacherId) {
            throw new Error("未找到教师ID，请先登录");
        }

        const payload = {
            date: new Date().toISOString().split('T')[0],
            prepTime: props.prepTime,
            prepRevisions: props.prepRevisions,
            optimizationNotes: suggestionText.value.trim()
        };

        await axios.post(
            `http://localhost:8080/api/teaching-efficiency/record?teacherId=${teacherId}`,
            payload
        );

        suggestionSubmitted.value = true;
        suggestionText.value = '';

        toast.add({
            severity: 'success',
            summary: '成功',
            detail: '教学建议已保存至教学效率记录',
            life: 3000
        });

        // 3秒后重置提交状态
        setTimeout(() => {
            suggestionSubmitted.value = false;
        }, 3000);
    } catch (error) {
        console.error('提交教学建议失败:', error);
        toast.add({
            severity: 'error',
            summary: '错误',
            detail: error.response?.data?.detail || '提交失败，请重试',
            life: 5000
        });
    } finally {
        submittingSuggestion.value = false;
    }
};
</script>

<style scoped>
.exam-processing-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header-section {
    text-align: center;
    margin-bottom: 2.5rem;
}

.header-section h1 {
    font-size: 2.2rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.header-section .subtitle {
    font-size: 1.1rem;
    color: #7f8c8d;
    margin-top: 0;
}

.module-card {
    height: 100%;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
}

.module-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.card-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: #2c3e50;
}

.card-title i {
    font-size: 1.5rem;
}

.upload-section {
    margin-bottom: 1.5rem;
}

.file-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 1rem;
    padding: 0.75rem;
    background-color: #f8f9fa;
    border-radius: 6px;
    border: 1px dashed #dee2e6;
}

.file-info i.pi-file {
    color: #3498db;
}

.file-info i.pi-file-excel {
    color: #27ae60;
}

.remove-icon {
    margin-left: auto;
    cursor: pointer;
    color: #e74c3c;
}

.remove-icon:hover {
    color: #c0392b;
}

.action-section {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0;
}

.process-btn, .analyze-btn {
    background: linear-gradient(135deg, #3498db, #2980b9);
    border: none;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

.submit-btn {
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

.result-section {
    margin-top: 1.5rem;
    animation: fadeIn 0.5s ease;
}

.result-content {
    padding: 0 1rem;
}

.result-message {
    color: #555;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.download-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.suggestion-section {
    margin-bottom: 1.5rem;
}

.suggestion-textarea {
    width: 100%;
    border-radius: 6px;
    padding: 1rem;
    border: 1px solid #dee2e6;
    transition: border-color 0.3s ease;
}

.suggestion-textarea:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.2);
}

.character-count {
    text-align: right;
    font-size: 0.85rem;
    color: #7f8c8d;
    margin-top: 0.25rem;
}

.success-message {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    color: #27ae60;
    font-weight: 500;
    margin-top: 1rem;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
    .exam-processing-container {
        padding: 1rem;
    }

    .header-section h1 {
        font-size: 1.8rem;
    }

    .download-buttons {
        flex-direction: column;
        align-items: center;
    }
}
</style>
