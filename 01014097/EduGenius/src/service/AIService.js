import axios from 'axios';

const aiClient = axios.create({
  baseURL: import.meta.env.VITE_AI_SERVICE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 300000
});

export const AIService = {
  generateCourse(name, content) {
    return aiClient.post('/generate-course', { name, content });
  },

  askQuestion(question, context) {
    return aiClient.post('/ask-question', { question, context });
  },

  generateQuestion(prompt) {
    return aiClient.post('/generate-question', { prompt });
  },

  generateStudentQuestion(prompt) {
    return aiClient.post('/question/generate', { prompt });
  },

  gradeAnswer(question, questionType, studentAnswer) {
    return aiClient.post('/question/grade', { question, question_type: questionType, student_answer: studentAnswer });
  },

  uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    return aiClient.post('/upload-file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },

  processExam(file) {
    const formData = new FormData();
    formData.append('file', file);
    return aiClient.post('/process-exam', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000
    });
  },

  analyzeExam(file) {
    const formData = new FormData();
    formData.append('file', file);
    return aiClient.post('/analyze-exam', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000
    });
  },

  downloadFile(filename) {
    return aiClient.get(`/download-file/${encodeURIComponent(filename)}`, {
      responseType: 'blob'
    });
  },

  getKnowledgeGraph(userId) {
    return aiClient.get('/knowledge-graph', { params: { user_id: userId } });
  },

  getUserKnowledgeMastery(userId) {
    return aiClient.get('/user-knowledge-mastery', { params: { user_id: userId } });
  },

  generateMindmap(topic, difficulty, preference) {
    return aiClient.post('/generate-mindmap', { topic, difficulty, preference });
  },

  generateCodeExamples(topic, difficulty, preference) {
    return aiClient.post('/generate-code-examples', { topic, difficulty, preference });
  },

  generatePracticeQuestions(topic, difficulty, preference) {
    return aiClient.post('/generate-practice-questions', { topic, difficulty, preference });
  },

  generateAnalysisReport(topic, difficulty, preference) {
    return aiClient.post('/generate-analysis-report', { topic, difficulty, preference });
  }
};
