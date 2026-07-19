<template>
    <div class="documentation-container">
        <!-- 文档头部 -->
        <header class="document-header">
            <div class="header-content">
                <div class="branding">
                    <svg class="logo" width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 0C7.163 0 0 7.163 0 16C0 24.837 7.163 32 16 32C24.837 32 32 24.837 32 16C32 7.163 24.837 0 16 0ZM16 28C9.373 28 4 22.627 4 16C4 9.373 9.373 4 16 4C22.627 4 28 9.373 28 16C28 22.627 22.627 28 16 28Z" fill="#10B981"/>
                        <path d="M16 8C11.582 8 8 11.582 8 16C8 20.418 11.582 24 16 24C20.418 24 24 20.418 24 16C24 11.582 20.418 8 16 8Z" fill="#10B981"/>
                        <path d="M16 12C13.791 12 12 13.791 12 16C12 18.209 13.791 20 16 20C18.209 20 20 18.209 20 16C20 13.791 18.209 12 16 12Z" fill="#10B981"/>
                    </svg>
                    <h1>教学实训智能体系统</h1>
                </div>
                <div class="document-meta">
                    <span class="version">版本 1.1.0</span>
                    <span class="date">{{ currentDate }}</span>
                </div>
            </div>
            <div class="header-decoration">
                <svg width="100%" height="2" viewBox="0 0 1200 2" preserveAspectRatio="none">
                    <path d="M0,1 L1200,1" stroke="#D1FAE5" stroke-width="1" stroke-dasharray="4,2"/>
                </svg>
            </div>
        </header>

        <!-- 文档主要内容 -->
        <main class="document-content">
            <!-- 系统架构部分 -->
            <section class="document-section">
                <h2 class="section-title">
                    <span class="section-number">1.</span>
                    系统架构设计
                </h2>

                <div class="subsection">
                    <h3 class="subsection-title">
                        <span class="section-number">1.1</span>
                        总体架构
                    </h3>
                    <p class="subsection-description">
                        本系统采用微服务架构，前端使用Vue 3构建响应式用户界面，后端采用Spring Cloud微服务框架，AI服务基于Qwen-Turbo大模型构建，通过API网关统一接入。
                    </p>

                    <div class="architecture-diagram">
                        <div class="architecture-layer">
                            <div class="layer-header">前端层</div>
                            <ul class="layer-components">
                                <li>Vue 3 + TypeScript</li>
                                <li>Pinia状态管理</li>
                                <li>PrimeVue组件库</li>
                                <li>响应式设计</li>
                            </ul>
                        </div>

                        <div class="architecture-connector">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M8 12H16M12 8V16" stroke="#10B981" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>

                        <div class="architecture-layer">
                            <div class="layer-header">API网关</div>
                            <ul class="layer-components">
                                <li>Spring Cloud Gateway</li>
                                <li>JWT认证</li>
                                <li>请求路由</li>
                                <li>负载均衡</li>
                            </ul>
                        </div>

                        <div class="architecture-connector">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M8 12H16M12 8V16" stroke="#10B981" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>

                        <div class="architecture-layer">
                            <div class="layer-header">微服务层</div>
                            <ul class="layer-components">
                                <li>用户服务</li>
                                <li>课程服务</li>
                                <li>评估服务</li>
                                <li>AI集成服务</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 核心功能部分 -->
            <section class="document-section">
                <h2 class="section-title">
                    <span class="section-number">2.</span>
                    核心功能模块
                </h2>

                <div class="subsection">
                    <h3 class="subsection-title">
                        <span class="section-number">2.1</span>
                        智能备课系统
                    </h3>
                    <ul class="feature-list">
                        <li>基于课程大纲自动生成教学计划</li>
                        <li>智能推荐教学资源和案例</li>
                        <li>多维度教学效果预测</li>
                        <li>实时协作备课功能</li>
                    </ul>
                </div>

                <div class="subsection">
                    <h3 class="subsection-title">
                        <span class="section-number">2.2</span>
                        代码示例
                    </h3>
                    <div class="code-block">
            <pre><code>// 智能备课组件
@Component({
  components: { CurriculumEditor, ResourceRecommender }
})
export default class SmartPreparation extends Vue {
  @Prop({ default: () => [] }) readonly materials!: TeachingMaterial[];

  private loading = false;
  private generatedPlan: LessonPlan | null = null;

  async generatePlan() {
    this.loading = true;
    try {
      const response = await AIService.generateLessonPlan(this.materials);
      this.generatedPlan = response.data;
    } finally {
      this.loading = false;
    }
  }
}</code></pre>
                    </div>
                </div>
            </section>

            <!-- 数据模型部分 -->
            <section class="document-section">
                <h2 class="section-title">
                    <span class="section-number">3.</span>
                    数据模型设计
                </h2>

                <div class="subsection">
                    <h3 class="subsection-title">
                        <span class="section-number">3.1</span>
                        课程实体
                    </h3>
                    <div class="table-container">
                        <table class="design-table">
                            <thead>
                            <tr>
                                <th>字段</th>
                                <th>类型</th>
                                <th>描述</th>
                                <th>约束</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td><code>id</code></td>
                                <td>UUID</td>
                                <td>唯一标识符</td>
                                <td>主键</td>
                            </tr>
                            <tr>
                                <td><code>title</code></td>
                                <td>String</td>
                                <td>课程标题</td>
                                <td>非空</td>
                            </tr>
                            <tr>
                                <td><code>description</code></td>
                                <td>Text</td>
                                <td>课程描述</td>
                                <td>-</td>
                            </tr>
                            <tr>
                                <td><code>createdAt</code></td>
                                <td>DateTime</td>
                                <td>创建时间</td>
                                <td>自动</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
        </main>

        <!-- 文档页脚 -->
        <footer class="document-footer">
            <div class="footer-actions">
                <button class="action-button">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 15V3M12 15L8 11M12 15L16 11M21 15V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    导出文档
                </button>
            </div>
            <div class="footer-copyright">
                &copy; {{ currentYear }} 教学实训智能体系统. 保留所有权利.
            </div>
        </footer>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'SystemDocumentation',
    computed: {
        currentDate(): string {
            return new Date().toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        },
        currentYear(): number {
            return new Date().getFullYear();
        }
    }
});
</script>

<style scoped>
.documentation-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #ffffff;
    color: #1F2937;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
}

/* 文档头部样式 */
.document-header {
    padding: 2.5rem 3rem 1.5rem;
    background-color: #F9FAFB;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.branding {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.branding h1 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
    margin: 0;
    letter-spacing: -0.025em;
}

.logo {
    flex-shrink: 0;
}

.document-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.875rem;
    color: #6B7280;
}

.header-decoration {
    height: 2px;
}

/* 文档内容样式 */
.document-content {
    flex: 1;
    padding: 2rem 3rem;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
}

.document-section {
    margin-bottom: 3rem;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #111827;
    margin: 0 0 1.5rem;
    display: flex;
    align-items: center;
    position: relative;
    padding-bottom: 0.75rem;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 3rem;
    height: 2px;
    background-color: #10B981;
}

.section-number {
    color: #10B981;
    margin-right: 0.5rem;
    font-weight: 600;
}

.subsection {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background-color: #F9FAFB;
    border-radius: 0.5rem;
    border-left: 4px solid #10B981;
    transition: all 0.2s ease;
}

.subsection:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transform: translateY(-1px);
}

.subsection-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
    margin: 0 0 1rem;
    display: flex;
    align-items: center;
}

.subsection-description {
    margin: 0 0 1.5rem;
    color: #4B5563;
    line-height: 1.7;
}

.feature-list {
    margin: 0 0 1.5rem;
    padding-left: 1.25rem;
    color: #4B5563;
}

.feature-list li {
    margin-bottom: 0.5rem;
    position: relative;
}

.feature-list li::before {
    content: '';
    position: absolute;
    left: -1.25rem;
    top: 0.5rem;
    width: 0.5rem;
    height: 0.5rem;
    background-color: #10B981;
    border-radius: 50%;
}

/* 架构图样式 */
.architecture-diagram {
    display: flex;
    align-items: stretch;
    gap: 1rem;
    margin: 2rem 0;
}

.architecture-layer {
    flex: 1;
    min-width: 0;
    background-color: white;
    border-radius: 0.375rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    border: 1px solid #E5E7EB;
    transition: all 0.2s ease;
}

.architecture-layer:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.layer-header {
    padding: 0.75rem 1rem;
    background-color: #10B981;
    color: white;
    font-weight: 500;
    font-size: 0.875rem;
}

.layer-components {
    margin: 0;
    padding: 1rem;
    list-style: none;
    font-size: 0.875rem;
    color: #4B5563;
}

.layer-components li {
    padding: 0.375rem 0;
    position: relative;
    padding-left: 1.25rem;
}

.layer-components li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.65rem;
    width: 0.375rem;
    height: 0.375rem;
    background-color: #10B981;
    border-radius: 50%;
}

.architecture-connector {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #10B981;
}

/* 代码块样式 */
.code-block {
    background-color: #1F2937;
    border-radius: 0.375rem;
    padding: 1.25rem;
    font-family: 'SF Mono', 'Roboto Mono', monospace;
    font-size: 0.875rem;
    overflow-x: auto;
}

.code-block pre {
    margin: 0;
    color: #E5E7EB;
    line-height: 1.5;
}

.code-block code {
    color: inherit;
}

/* 表格样式 */
.table-container {
    overflow-x: auto;
    margin: 1.5rem 0;
    border-radius: 0.375rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.design-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
}

.design-table th,
.design-table td {
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid #E5E7EB;
}

.design-table th {
    background-color: #ECFDF5;
    font-weight: 500;
    color: #065F46;
}

.design-table td {
    color: #4B5563;
    background-color: white;
}

.design-table tr:hover td {
    background-color: #F9FAFB;
}

.design-table code {
    background-color: #D1FAE5;
    padding: 0.2rem 0.4rem;
    border-radius: 0.25rem;
    font-family: 'SF Mono', 'Roboto Mono', monospace;
    font-size: 0.8125rem;
    color: #065F46;
}

/* 页脚样式 */
.document-footer {
    padding: 1.5rem 3rem;
    border-top: 1px solid #E5E7EB;
    background-color: #F9FAFB;
}

.footer-actions {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}

.action-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: white;
    border: 1px solid #E5E7EB;
    border-radius: 0.375rem;
    color: #065F46;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.action-button:hover {
    background-color: #ECFDF5;
    border-color: #A7F3D0;
}

.action-button svg {
    flex-shrink: 0;
}

.footer-copyright {
    font-size: 0.75rem;
    color: #6B7280;
    text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .document-header,
    .document-content,
    .document-footer {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }

    .architecture-diagram {
        flex-direction: column;
    }

    .architecture-connector {
        transform: rotate(90deg);
        padding: 0.5rem 0;
    }
}
</style>
