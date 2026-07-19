
<template>
    <teleport to="body">
        <!-- 划词气泡 -->
        <div
            v-if="showSelectionBubble && selectionBubblePosition"
            class="selection-bubble"
            :style="{
                left: selectionBubblePosition.x + 'px',
                top: selectionBubblePosition.y + 'px'
            }"
            @mousedown.stop
            @click="handleBubbleClick"
        >
            <span class="bubble-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="2" width="16" height="16" rx="5" stroke="currentColor" stroke-width="1.8"/><circle cx="9.5" cy="10" r="1.5" fill="currentColor"/><circle cx="14.5" cy="10" r="1.5" fill="currentColor"/><path d="M9 14c.8.8 2.2.8 3 0" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="18" x2="8" y2="21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="16" y1="18" x2="16" y2="21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></span>
            <span class="bubble-text">AI 分析</span>
        </div>

        <!-- 悬浮球（最小化状态） -->
        <div
            v-if="isActive && isMinimized"
            class="floating-ball"
            @click="handleBallClick"
            :class="{ 'speaking': isDigitalHumanSpeaking }"
        >
            <div class="ball-avatar"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="2" width="16" height="16" rx="5" stroke="currentColor" stroke-width="1.6"/><circle cx="9.5" cy="10" r="1.5" fill="currentColor"/><circle cx="14.5" cy="10" r="1.5" fill="currentColor"/><path d="M9 14c.8.8 2.2.8 3 0" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="18" x2="8" y2="21" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><line x1="16" y1="18" x2="16" y2="21" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
            <div v-if="isDigitalHumanSpeaking" class="ball-pulse"></div>
            <div v-if="isDigitalHumanSpeaking" class="ball-pulse delay"></div>
        </div>

        <!-- 悬浮卡片（展开状态） - 用v-show避免video元素销毁导致WebRTC断开 -->
        <div
            v-show="isActive && isVisible && !isMinimized"
            ref="cardRef"
            class="floating-card"
            :style="cardStyle"
            @mousedown.stop="startCardDrag"
        >
            <!-- 卡片头部 -->
            <div class="card-header">
                <div class="header-left">
                    <span class="header-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="2" width="16" height="16" rx="5" stroke="currentColor" stroke-width="1.8"/><circle cx="9.5" cy="10" r="1.5" fill="currentColor"/><circle cx="14.5" cy="10" r="1.5" fill="currentColor"/><path d="M9 14c.8.8 2.2.8 3 0" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="18" x2="8" y2="21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="16" y1="18" x2="16" y2="21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></span>
                    <span class="header-title">AI 助手</span>
                    <span v-if="isDigitalHumanConnected" class="status-dot connected"></span>
                    <span v-else class="status-dot disconnected"></span>
                </div>
                <div class="header-actions">
                    <button class="action-btn minimize-btn" @click.stop="handleMinimize" title="最小化">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/>
                        </svg>
                    </button>
                    <button class="action-btn close-btn" @click.stop="handleClose" title="关闭">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
            </div>

            <!-- 卡片内容 -->
            <div class="card-body">
                <!-- 数字人视频区 -->
                <div class="video-area">
                    <video
                        ref="videoElement"
                        autoplay
                        playsinline
                        class="video-player"
                        :class="{ 'connected': isDigitalHumanConnected }"
                    ></video>
                    <canvas
                        v-if="chromaEnabled"
                        ref="chromaCanvas"
                        class="chroma-canvas"
                        :class="{ 'connected': isDigitalHumanConnected }"
                    ></canvas>
                    <div v-if="!isDigitalHumanConnected" class="video-placeholder">
                        <div class="placeholder-icon"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="2" width="16" height="16" rx="5" stroke="currentColor" stroke-width="1.2"/><circle cx="9.5" cy="10" r="1.5" fill="currentColor"/><circle cx="14.5" cy="10" r="1.5" fill="currentColor"/><path d="M9 14c.8.8 2.2.8 3 0" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><line x1="8" y1="18" x2="8" y2="21" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><line x1="16" y1="18" x2="16" y2="21" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg></div>
                        <div class="placeholder-text">{{ digitalHumanStatus }}</div>
                    </div>
                    <div v-if="isDigitalHumanSpeaking" class="speaking-indicator">
                        <span class="speaking-dot"></span>
                        说话中...
                    </div>
                </div>

                <!-- 聊天区 -->
                <div class="chat-area">
                    <div class="chat-history" ref="chatHistoryRef">
                        <div v-if="chatHistory.length === 0" class="empty-chat">
                            <div class="empty-icon">💬</div>
                            <div class="empty-text">向 AI 助手提问</div>
                        </div>
                        <div
                            v-for="(msg, index) in chatHistory"
                            :key="index"
                            :class="['chat-message', msg.role]"
                        >
                            <div class="message-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
                            <div class="message-bubble">{{ msg.text }}</div>
                        </div>
                    </div>

                    <!-- 输入区 -->
                    <div class="chat-input-area" v-if="isDigitalHumanConnected">
                        <div class="input-row">
                            <button
                                @click.stop="toggleMic"
                                class="mic-btn"
                                :class="{ 'listening': isListening }"
                                title="语音输入"
                            >
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 1C10.3431 1 9 2.34315 9 4V12C9 13.6569 10.3431 15 12 15C13.6569 15 15 13.6569 15 12V4C15 2.34315 13.6569 1 12 1Z" fill="currentColor"/>
                                    <path d="M19 10V12C19 15.866 15.866 19 12 19C8.13401 19 5 15.866 5 12V10H3V12C3 16.4183 6.58172 20 11 20V23H13V20C17.4183 20 21 16.4183 21 12V10H19Z" fill="currentColor"/>
                                </svg>
                                <div v-if="isListening" class="mic-ripple">
                                    <span></span><span></span><span></span>
                                </div>
                            </button>
                            <input
                                v-model="inputText"
                                @keyup.enter="sendMessage"
                                @mousedown.stop
                                type="text"
                                placeholder="输入问题..."
                                class="text-input"
                            />
                            <button @click.stop="sendMessage" class="send-btn" :disabled="!inputText.trim()">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Toast 提示 -->
        <div class="sa-toast-container">
            <div v-for="toast in toasts" :key="toast.id" class="sa-toast" :class="toast.type">
                <span class="toast-icon">{{ toast.type === 'success' ? '✅' : toast.type === 'error' ? '❌' : 'ℹ️' }}</span>
                <span class="toast-msg">{{ toast.message }}</span>
            </div>
        </div>
    </teleport>
</template>

<script>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { storeToRefs } from 'pinia';
import { useDigitalHumanStore } from '@/store/digitalHumanStore';
import { voiceNavigationService } from '@/service/voiceNavigationService';

export default {
    name: 'SelectionAssistant',
    emits: ['stt-result'],
    setup(props, { emit }) {
        const store = useDigitalHumanStore();
        const { isActive, isVisible, isMinimized, selectedText, textToSpeak } = storeToRefs(store);

        // === 引用 ===
        const cardRef = ref(null);
        const videoElement = ref(null);
        const chromaCanvas = ref(null);
        const chatHistoryRef = ref(null);

        // === 数字人连接状态 ===
        const pc = ref(null);
        const sessionId = ref(null);
        const isDigitalHumanConnected = ref(false);
        const isDigitalHumanSpeaking = ref(false);
        const digitalHumanStatus = ref('未连接');
        const isConnecting = ref(false);
        const speakingCheckInterval = ref(null);
        const serverUrl = ref(import.meta.env.VITE_DIGITAL_HUMAN_SERVER_URL || 'http://localhost:7860');

        // === 绿幕抠除相关 ===
        const chromaGL = ref(null);
        const chromaProgram = ref(null);
        const chromaTexture = ref(null);
        const chromaAnimId = ref(null);
        const chromaKeyColor = ref([0.0, 1.0, 0.0]);
        const chromaThreshold = ref(0.65);
        const chromaEnabled = ref(false);

        // ===== 📊 性能埋点：唇形渲染全链路 =====
        const _lipSyncPerf = reactive({
            ttsFetchStart: null,     // TTS fetch发起时刻
            ttsResponseTime: null,   // TTS fetch返回时刻
            firstFrameTime: null,    // WebRTC首帧到达时刻
            firstRenderTime: null    // 首帧渲染完成时刻
        });
        // ===== 📊 性能埋点 END =====

        // === 聊天 ===
        const inputText = ref('');
        const chatHistory = ref([]);

        // === 语音识别 ===
        const isListening = ref(false);
        const isSpeechSupported = ref(false);
        const currentMediaRecorder = ref(null);
        const currentLanguage = ref('zh-CN');

        // === 划词 ===
        const showSelectionBubble = ref(false);
        const selectionBubblePosition = ref(null);
        let selectionTimeout = null;

        // === 拖拽 ===
        const isDragging = ref(false);
        const dragOffset = reactive({ x: 0, y: 0 });
        const cardPosition = reactive({ x: 0, y: 0 });
        const hasDragged = ref(false);

        // === Toast ===
        const toasts = ref([]);

        // === 卡片位置计算 ===
        const cardStyle = computed(() => {
            if (hasDragged.value) {
                return {
                    left: cardPosition.x + 'px',
                    top: cardPosition.y + 'px',
                };
            }
            // 默认位置：右下角
            return {
                right: '24px',
                bottom: '24px',
            };
        });

        // ==================== 划词检测 ====================
        function handleMouseUp(event) {
            // 清除之前的定时器
            if (selectionTimeout) {
                clearTimeout(selectionTimeout);
                selectionTimeout = null;
            }

            // 延迟检测，确保选区已更新
            selectionTimeout = setTimeout(() => {
                const selection = window.getSelection();
                const text = selection ? selection.toString().trim() : '';

                if (text.length >= 2 && text.length <= 500) {
                    // 检查选区是否在卡片内（如果是则不触发）
                    const cardEl = cardRef.value;
                    if (cardEl && cardEl.contains(selection.anchorNode)) {
                        showSelectionBubble.value = false;
                        return;
                    }

                    const range = selection.getRangeAt(0);
                    const rect = range.getBoundingClientRect();

                    selectionBubblePosition.value = {
                        x: rect.left + rect.width / 2 - 50,
                        y: rect.top - 40
                    };
                    showSelectionBubble.value = true;
                } else {
                    showSelectionBubble.value = false;
                }
            }, 150);
        }

        function handleMouseDown(event) {
            // 点击其他区域时隐藏气泡
            if (!event.target.closest('.selection-bubble')) {
                showSelectionBubble.value = false;
            }
        }

        function handleBubbleClick() {
            const selection = window.getSelection();
            const text = selection ? selection.toString().trim() : '';
            if (text) {
                store.triggerFromSelection(text);
                showSelectionBubble.value = false;
                // 清除选区
                selection.removeAllRanges();
            }
        }

        // ==================== 悬浮球点击 ====================
        function handleBallClick() {
            store.expand();
        }

        // ==================== 卡片拖拽 ====================
        function startCardDrag(e) {
            // 不拖拽输入框和按钮
            if (e.target.closest('.chat-input-area') ||
                e.target.closest('.header-actions') ||
                e.target.closest('.video-area')) {
                return;
            }
            if (e.button !== 0) return;
            e.preventDefault();

            const card = cardRef.value;
            if (!card) return;

            const rect = card.getBoundingClientRect();
            if (!hasDragged.value) {
                // 第一次拖拽，从计算位置切换到绝对位置
                cardPosition.x = rect.left;
                cardPosition.y = rect.top;
                hasDragged.value = true;
            }

            isDragging.value = true;
            dragOffset.x = e.clientX - rect.left;
            dragOffset.y = e.clientY - rect.top;

            document.addEventListener('mousemove', onCardDrag);
            document.addEventListener('mouseup', stopCardDrag);
        }

        function onCardDrag(e) {
            if (!isDragging.value) return;

            const x = e.clientX - dragOffset.x;
            const y = e.clientY - dragOffset.y;

            // 限制在视口内
            const maxX = window.innerWidth - 620;
            const maxY = window.innerHeight - 80;
            cardPosition.x = Math.max(0, Math.min(maxX, x));
            cardPosition.y = Math.max(0, Math.min(maxY, y));
        }

        function stopCardDrag() {
            isDragging.value = false;
            document.removeEventListener('mousemove', onCardDrag);
            document.removeEventListener('mouseup', stopCardDrag);
        }

        // ==================== 卡片操作 ====================
        function handleMinimize() {
            store.minimize();
        }

        function handleClose() {
            store.close();
            disconnectDigitalHuman();
        }

        // ==================== 数字人连接 ====================
        async function connectDigitalHuman() {
            if (isConnecting.value || isDigitalHumanConnected.value) return;

            if (!videoElement.value) {
                console.warn('video 元素不存在，延迟连接');
                await nextTick();
                if (!videoElement.value) return;
            }

            try {
                isConnecting.value = true;
                digitalHumanStatus.value = '连接中...';

                const configuration = {
                    iceServers: [
                        { urls: 'stun:stun.miwifi.com:3478' },
                        { urls: 'stun:stun.l.google.com:19302' }
                    ]
                };
                pc.value = new RTCPeerConnection(configuration);

                pc.value.onconnectionstatechange = () => {
                    if (!pc.value) return;
                    console.log('Connection state:', pc.value.connectionState);
                    if (pc.value.connectionState === 'connected') {
                        isDigitalHumanConnected.value = true;
                        digitalHumanStatus.value = '已连接';
                        isConnecting.value = false;
                        startSpeakingCheck();
                    } else if (pc.value.connectionState === 'failed' || pc.value.connectionState === 'disconnected') {
                        isDigitalHumanConnected.value = false;
                        digitalHumanStatus.value = '连接失败';
                        isConnecting.value = false;
                    }
                };

                pc.value.ontrack = (event) => {
                    if (!videoElement.value) return;
                    if (!videoElement.value.srcObject) {
                        videoElement.value.srcObject = new MediaStream();
                    }
                    event.streams[0].getTracks().forEach(track => {
                        videoElement.value.srcObject.addTrack(track);
                        if (track.kind === 'audio') {
                            track.enabled = true;
                        }
                        if (track.kind === 'video') {
                            // ===== 📊 性能埋点：唇形渲染链路 - 首帧到达标记 =====
                            if (!_lipSyncPerf.firstFrameTime) {
                                _lipSyncPerf.firstFrameTime = performance.now();
                                if (_lipSyncPerf.ttsResponseTime) {
                                    const latency = _lipSyncPerf.firstFrameTime - _lipSyncPerf.ttsResponseTime;
                                    console.log(
                                        `%c[Perf] 音频接收→首帧到达: ${latency.toFixed(2)}ms`,
                                        'color: #000; font-weight: bold; font-size: 13px; background: #fff; padding: 2px 6px; border-radius: 3px;'
                                    );
                                }
                            }
                            // ===== 📊 性能埋点 END =====
                            setupVideoTrack(track);
                        }
                    });
                    nextTick(() => {
                        if (videoElement.value && videoElement.value.paused) {
                            videoElement.value.play().catch(() => {});
                        }
                    });
                };

                const offer = await pc.value.createOffer({
                    offerToReceiveAudio: true,
                    offerToReceiveVideo: true
                });
                await pc.value.setLocalDescription(offer);

                const response = await fetch(`${serverUrl.value}/offer`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sdp: pc.value.localDescription.sdp,
                        type: pc.value.localDescription.type
                    })
                });

                if (!response.ok) {
                    let errorDetail = '';
                    try {
                        const errorData = await response.json();
                        errorDetail = errorData.msg || errorData.message || '';
                    } catch (e) {
                        errorDetail = `HTTP ${response.status}`;
                    }
                    throw new Error(errorDetail || `服务器错误 (${response.status})`);
                }

                const answer = await response.json();
                if (answer.code === -1) throw new Error(answer.msg);

                sessionId.value = answer.sessionid;
                await pc.value.setRemoteDescription(new RTCSessionDescription({
                    sdp: answer.sdp,
                    type: answer.type
                }));
                isConnecting.value = false;

            } catch (error) {
                console.error('数字人连接失败:', error);
                digitalHumanStatus.value = '连接失败';
                isConnecting.value = false;
            }
        }

        // ==================== 绿幕抠除 ====================
        function setupVideoTrack(track) {
            const video = videoElement.value;
            const canvas = chromaCanvas.value;

            // ===== 📊 性能埋点：唇形渲染链路 - 视频帧渲染完成检测 =====
            const perfFirstRender = () => {
                if (!_lipSyncPerf.firstRenderTime && _lipSyncPerf.ttsResponseTime) {
                    _lipSyncPerf.firstRenderTime = performance.now();
                    const totalLatency = _lipSyncPerf.firstRenderTime - _lipSyncPerf.ttsResponseTime;
                    console.log(
                        `%c[Perf] 唇形同步全链路耗时(TTS返回→渲染完成): ${totalLatency.toFixed(2)}ms`,
                        'color: #000; font-weight: bold; font-size: 14px; background: #fff; padding: 2px 6px; border-radius: 3px;'
                    );
                    if (_lipSyncPerf.ttsFetchStart) {
                        const e2eLatency = _lipSyncPerf.firstRenderTime - _lipSyncPerf.ttsFetchStart;
                        console.log(
                            `%c[Perf] 端到端全链路耗时(Fetch发起→渲染完成): ${e2eLatency.toFixed(2)}ms`,
                            'color: #333; font-weight: bold; font-size: 14px; background: #fff; padding: 2px 6px; border-radius: 3px;'
                        );
                    }
                    // 重置，为下一次TTS周期准备
                    _lipSyncPerf.ttsFetchStart = null;
                    _lipSyncPerf.ttsResponseTime = null;
                    _lipSyncPerf.firstFrameTime = null;
                    _lipSyncPerf.firstRenderTime = null;
                    video.removeEventListener('timeupdate', perfFirstRender);
                }
            };
            video.addEventListener('timeupdate', perfFirstRender);
            // ===== 📊 性能埋点 END =====

            if (chromaEnabled.value && canvas) {
                initChromaKey(video, canvas);
            }
        }

        function initChromaKey(video, canvas) {
            const gl = canvas.getContext('webgl', {
                alpha: true,
                premultipliedAlpha: false,
                preserveDrawingBuffer: false,
                antialias: false
            });

            if (!gl) {
                console.warn('[SA] WebGL 不可用，跳过绿幕抠除');
                chromaEnabled.value = false;
                return;
            }

            chromaGL.value = gl;

            const vsSource = `
                attribute vec2 a_position;
                attribute vec2 a_texCoord;
                varying vec2 v_texCoord;
                void main() {
                    gl_Position = vec4(a_position, 0.0, 1.0);
                    v_texCoord = a_texCoord;
                }
            `;

            const fsSource = `
                precision highp float;
                varying vec2 v_texCoord;
                uniform sampler2D u_image;
                uniform vec3 u_keyColor;
                uniform float u_threshold;

                vec3 rgb2ycbcr(vec3 c) {
                    return vec3(
                        0.299*c.r + 0.587*c.g + 0.114*c.b,
                        0.5 + (-0.168736*c.r - 0.331264*c.g + 0.5*c.b),
                        0.5 + (0.5*c.r - 0.418688*c.g - 0.081312*c.b)
                    );
                }
                void main() {
                    vec4 color = texture2D(u_image, v_texCoord);

                    // === YCbCr色彩空间检测（最准确） ===
                    vec3 ycbcr = rgb2ycbcr(color.rgb);
                    vec3 keyYcbcr = rgb2ycbcr(u_keyColor);
                    float cbDiff = ycbcr.g - keyYcbcr.g;
                    float crDiff = ycbcr.b - keyYcbcr.b;
                    float chromaDist = sqrt(cbDiff * cbDiff + crDiff * crDiff);
                    float ycbcrAlpha = smoothstep(u_threshold * 0.5, u_threshold * 1.1, chromaDist);

                    // === RGB空间绿色主导检测 ===
                    float greenDominance = color.g - max(color.r, color.b);
                    float greenRatio = color.g / (color.r + color.b + 0.001);
                    float greenAlpha = smoothstep(0.02, 0.18, 1.0 - greenDominance);
                    float highGreenAlpha = smoothstep(1.5, 2.5, greenRatio);
                    greenAlpha = min(greenAlpha, 1.0 - highGreenAlpha);

                    // === 综合两种方法，取更激进的抠除 ===
                    float alpha = min(ycbcrAlpha, greenAlpha);

                    // === 边缘区域额外处理 ===
                    if (alpha > 0.0 && alpha < 1.0) {
                        float edgeGreen = color.g - (color.r + color.b) * 0.5;
                        float edgeBoost = smoothstep(0.0, 0.12, edgeGreen);
                        alpha = min(alpha, 1.0 - edgeBoost * (1.0 - alpha));
                    }

                    // === 溢色修正（Spill Removal）===
                    float spillStrength = max(0.0, greenDominance) * (1.0 - alpha * 0.5);
                    color.r = min(1.0, color.r + spillStrength * 0.6);
                    color.b = min(1.0, color.b + spillStrength * 0.4);
                    color.g = max(color.r * 0.95, max(color.b * 0.95, color.g - spillStrength * 0.8));

                    gl_FragColor = vec4(color.rgb, alpha);
                }
            `;

            const vs = gl.createShader(gl.VERTEX_SHADER);
            gl.shaderSource(vs, vsSource);
            gl.compileShader(vs);
            if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
                console.error('[SA] 顶点着色器编译失败:', gl.getShaderInfoLog(vs));
                chromaEnabled.value = false;
                return;
            }

            const fs = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(fs, fsSource);
            gl.compileShader(fs);
            if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
                console.error('[SA] 片段着色器编译失败:', gl.getShaderInfoLog(fs));
                chromaEnabled.value = false;
                return;
            }

            const program = gl.createProgram();
            gl.attachShader(program, vs);
            gl.attachShader(program, fs);
            gl.linkProgram(program);
            if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
                console.error('[SA] 着色器程序链接失败:', gl.getProgramInfoLog(program));
                chromaEnabled.value = false;
                return;
            }

            chromaProgram.value = program;
            gl.useProgram(program);

            const positions = new Float32Array([
                -1, -1,   1, -1,   -1, 1,
                -1,  1,   1, -1,    1, 1
            ]);
            const posBuf = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
            gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
            const aPos = gl.getAttribLocation(program, 'a_position');
            gl.enableVertexAttribArray(aPos);
            gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

            const texCoords = new Float32Array([
                0, 1,   1, 1,   0, 0,
                0, 0,   1, 1,   1, 0
            ]);
            const texBuf = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, texBuf);
            gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);
            const aTex = gl.getAttribLocation(program, 'a_texCoord');
            gl.enableVertexAttribArray(aTex);
            gl.vertexAttribPointer(aTex, 2, gl.FLOAT, false, 0, 0);

            chromaTexture.value = gl.createTexture();
            gl.bindTexture(gl.TEXTURE_2D, chromaTexture.value);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

            gl.uniform3fv(gl.getUniformLocation(program, 'u_keyColor'), chromaKeyColor.value);
            gl.uniform1f(gl.getUniformLocation(program, 'u_threshold'), chromaThreshold.value);

            gl.enable(gl.BLEND);
            gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

            // 清除颜色设为完全透明
            gl.clearColor(0.0, 0.0, 0.0, 0.0);

            console.log('[SA] WebGL 绿幕抠除已初始化');
            video.classList.add('chroma-source');

            const startRendering = () => {
                if (video.videoWidth > 0 && video.videoHeight > 0) {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    gl.viewport(0, 0, canvas.width, canvas.height);
                    renderChromaFrame();
                } else {
                    requestAnimationFrame(startRendering);
                }
            };

            video.addEventListener('loadedmetadata', () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                gl.viewport(0, 0, canvas.width, canvas.height);
            });

            video.addEventListener('play', startRendering);
            video.addEventListener('pause', stopChromaRender);
        }

        function renderChromaFrame() {
            const gl = chromaGL.value;
            const video = videoElement.value;

            if (!gl || !video || video.paused || video.ended) return;

            // ===== 📊 性能埋点：唇形渲染链路 - 首帧渲染完成 =====
            if (!_lipSyncPerf.firstRenderTime && _lipSyncPerf.ttsResponseTime) {
                _lipSyncPerf.firstRenderTime = performance.now();
                const totalLatency = _lipSyncPerf.firstRenderTime - _lipSyncPerf.ttsResponseTime;
                console.log(
                    `%c[Perf] 唇形同步全链路耗时(TTS返回→渲染完成): ${totalLatency.toFixed(2)}ms`,
                    'color: #000; font-weight: bold; font-size: 14px; background: #fff; padding: 2px 6px; border-radius: 3px;'
                );
                if (_lipSyncPerf.ttsFetchStart) {
                    const e2eLatency = _lipSyncPerf.firstRenderTime - _lipSyncPerf.ttsFetchStart;
                    console.log(
                        `%c[Perf] 端到端全链路耗时(Fetch发起→渲染完成): ${e2eLatency.toFixed(2)}ms`,
                        'color: #333; font-weight: bold; font-size: 14px; background: #fff; padding: 2px 6px; border-radius: 3px;'
                    );
                }
                // 重置，为下一次TTS周期准备
                _lipSyncPerf.ttsFetchStart = null;
                _lipSyncPerf.ttsResponseTime = null;
                _lipSyncPerf.firstFrameTime = null;
                _lipSyncPerf.firstRenderTime = null;
            }
            // ===== 📊 性能埋点 END =====

            gl.bindTexture(gl.TEXTURE_2D, chromaTexture.value);
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, video);
            gl.clear(gl.COLOR_BUFFER_BIT);
            gl.drawArrays(gl.TRIANGLES, 0, 6);

            chromaAnimId.value = requestAnimationFrame(() => renderChromaFrame());
        }

        function stopChromaRender() {
            if (chromaAnimId.value) {
                cancelAnimationFrame(chromaAnimId.value);
                chromaAnimId.value = null;
            }
        }

        function cleanupChromaKey() {
            stopChromaRender();
            const gl = chromaGL.value;
            if (gl) {
                if (chromaTexture.value) gl.deleteTexture(chromaTexture.value);
                if (chromaProgram.value) gl.deleteProgram(chromaProgram.value);
                chromaTexture.value = null;
                chromaProgram.value = null;
            }
            chromaGL.value = null;
            if (videoElement.value) {
                videoElement.value.classList.remove('chroma-source');
            }
        }

        function disconnectDigitalHuman() {
            cleanupChromaKey();
            stopSpeakingCheck();
            if (pc.value) {
                pc.value.close();
                pc.value = null;
            }
            isDigitalHumanConnected.value = false;
            digitalHumanStatus.value = '未连接';
            sessionId.value = null;
            isDigitalHumanSpeaking.value = false;
            if (videoElement.value) {
                videoElement.value.srcObject = null;
            }
        }

        // ==================== 说话状态检测 ====================
        function startSpeakingCheck() {
            stopSpeakingCheck();
            speakingCheckInterval.value = setInterval(async () => {
                if (!isDigitalHumanConnected.value || !sessionId.value) {
                    stopSpeakingCheck();
                    return;
                }
                try {
                    const response = await fetch(`${serverUrl.value}/is_speaking`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ sessionid: sessionId.value })
                    });
                    const result = await response.json();
                    if (result.code === 0) {
                        isDigitalHumanSpeaking.value = result.data === true;
                    }
                } catch (error) {
                    console.error('检查说话状态失败:', error);
                }
            }, 1500);
        }

        function stopSpeakingCheck() {
            if (speakingCheckInterval.value) {
                clearInterval(speakingCheckInterval.value);
                speakingCheckInterval.value = null;
            }
        }

        // ==================== 发送消息 ====================
        async function sendMessage() {
            const text = inputText.value.trim();
            if (!text) return;

            inputText.value = '';

            // ★ 新增：先检查是否为导航指令
            try {
                const result = await voiceNavigationService.handleVoiceCommand(text, 0);
                if (result.type === 'navigation') {
                    console.log('🧭 路由跳转:', result.path);
                    addChatMessage('user', text);
                    addChatMessage('assistant', '好的，正在为您跳转...');
                    return;
                }
            } catch (e) {
                console.log('导航匹配未命中，走AI对话流程');
            }

            // 非导航指令，走原有 AI 对话流程
            addChatMessage('user', text);
            await sendToAI(text);
        }

        async function sendToAI(message) {
            if (!sessionId.value) {
                addChatMessage('assistant', '数字人未连接，请稍候...');
                return;
            }

            try {
                const response = await fetch(`${serverUrl.value}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionid: sessionId.value,
                        message: message
                    })
                });

                const result = await response.json();
                if (result.code === 0) {
                    addChatMessage('assistant', result.reply);
                    // ===== 📊 触发TTS语音合成，使性能埋点生效 =====
                    if (result.reply && result.reply.trim()) {
                        speakText(result.reply.trim());
                    }
                    // ===== 📊 END =====
                } else {
                    addChatMessage('assistant', '抱歉，出了点问题，请重试~');
                }
            } catch (error) {
                console.error('AI 对话异常:', error);
                addChatMessage('assistant', '网络错误，请稍后再试~');
            }
        }

        function addChatMessage(role, text) {
            chatHistory.value.push({
                role,
                text,
                time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
            });
            // 聊天历史已在本地 chatHistory ref 中管理

            nextTick(() => {
                if (chatHistoryRef.value) {
                    chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight;
                }
            });
        }

        // ==================== 语音识别 ====================
        function toggleMic() {
            if (isListening.value) {
                stopListening();
            } else {
                startListening();
            }
        }

        async function startListening() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: {
                        sampleRate: 16000,
                        channelCount: 1,
                        echoCancellation: true,
                        noiseSuppression: true
                    }
                });

                isListening.value = true;
                const mediaRecorder = new MediaRecorder(stream, {
                    mimeType: 'audio/webm;codecs=opus'
                });
                currentMediaRecorder.value = mediaRecorder;
                const audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = async () => {
                    stream.getTracks().forEach(track => track.stop());
                    isListening.value = false;

                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    if (audioBlob.size < 100) return;

                    try {
                        // 转换为 WAV
                        const wavBlob = await convertWebMToWAV(audioBlob);
                        const formData = new FormData();
                        formData.append('audio', wavBlob, 'recording.wav');
                        formData.append('language', currentLanguage.value === 'en-US' ? 'en' : 'zh');

                        const response = await fetch(`${serverUrl.value}/speech_to_text`, {
                            method: 'POST',
                            body: formData
                        });

                        const result = await response.json();
                        if (result.code === 0 && result.text) {
                            inputText.value = result.text;
                            emit('stt-result', result.text);
                            setTimeout(() => sendMessage(), 300);
                            showToast('识别成功', 'success');
                        } else {
                            showToast('识别失败', 'error');
                        }
                    } catch (error) {
                        console.error('语音识别失败:', error);
                        showToast('识别失败', 'error');
                    }
                };

                mediaRecorder.start();
                // 最长录音 30 秒
                setTimeout(() => {
                    if (mediaRecorder.state === 'recording') {
                        mediaRecorder.stop();
                    }
                }, 30000);

            } catch (error) {
                console.error('麦克风权限获取失败:', error);
                showToast('麦克风权限被拒绝', 'error');
            }
        }

        function stopListening() {
            if (currentMediaRecorder.value && currentMediaRecorder.value.state === 'recording') {
                currentMediaRecorder.value.stop();
            }
        }

        // WebM 转 WAV
        async function convertWebMToWAV(webmBlob) {
            return new Promise((resolve, reject) => {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
                const reader = new FileReader();
                reader.onload = async () => {
                    try {
                        const arrayBuffer = reader.result;
                        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

                        let monoBuffer;
                        if (audioBuffer.numberOfChannels > 1) {
                            monoBuffer = audioContext.createBuffer(1, audioBuffer.length, audioBuffer.sampleRate);
                            const left = audioBuffer.getChannelData(0);
                            const right = audioBuffer.getChannelData(1);
                            const mono = monoBuffer.getChannelData(0);
                            for (let i = 0; i < audioBuffer.length; i++) {
                                mono[i] = (left[i] + right[i]) / 2;
                            }
                        } else {
                            monoBuffer = audioBuffer;
                        }

                        const wavBlob = audioBufferToWav(monoBuffer);
                        resolve(wavBlob);
                    } catch (error) {
                        reject(error);
                    } finally {
                        audioContext.close();
                    }
                };
                reader.onerror = reject;
                reader.readAsArrayBuffer(webmBlob);
            });
        }

        function audioBufferToWav(buffer) {
            const numChannels = buffer.numberOfChannels;
            const sampleRate = buffer.sampleRate;
            const bitDepth = 16;
            const bytesPerSample = bitDepth / 8;
            const blockAlign = numChannels * bytesPerSample;
            const data = [];

            for (let i = 0; i < buffer.length; i++) {
                const sample = Math.max(-1, Math.min(1, buffer.getChannelData(0)[i]));
                data.push(sample < 0 ? sample * 0x8000 : sample * 0x7FFF);
            }

            const dataLength = data.length * bytesPerSample;
            const arrayBuffer = new ArrayBuffer(44 + dataLength);
            const view = new DataView(arrayBuffer);

            const writeStr = (offset, str) => {
                for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
            };

            writeStr(0, 'RIFF');
            view.setUint32(4, 36 + dataLength, true);
            writeStr(8, 'WAVE');
            writeStr(12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, 1, true);
            view.setUint16(22, numChannels, true);
            view.setUint32(24, sampleRate, true);
            view.setUint32(28, sampleRate * blockAlign, true);
            view.setUint16(32, blockAlign, true);
            view.setUint16(34, bitDepth, true);
            writeStr(36, 'data');
            view.setUint32(40, dataLength, true);

            let offset = 44;
            for (let i = 0; i < data.length; i++) {
                view.setInt16(offset, data[i], true);
                offset += 2;
            }

            return new Blob([arrayBuffer], { type: 'audio/wav' });
        }

        // ==================== TTS 说话 ====================
        async function speakText(text) {
            if (!text || !sessionId.value) {
                console.warn('[SA] speakText 跳过: text为空或sessionId不存在', { text: !!text, sessionId: !!sessionId.value });
                return;
            }
            try {
                console.log('[SA] 发送TTS请求, sessionId:', sessionId.value, 'text长度:', text.trim().length);

                // ===== 📊 性能埋点：TTS请求耗时 - 起点 =====
                const perfMarkStart = `tts-fetch-start-${Date.now()}`;
                const perfMarkEnd   = `tts-fetch-end-${Date.now()}`;
                performance.mark(perfMarkStart);
                _lipSyncPerf.ttsFetchStart = performance.now();
                // ===== 📊 性能埋点 END =====

                const response = await fetch(`${serverUrl.value}/human`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionid: sessionId.value,
                        type: 'echo',
                        interrupt: true,
                        text: text.trim()
                    })
                });
                const result = await response.json();

                // ===== 📊 性能埋点：TTS请求耗时 - 终点 =====
                performance.mark(perfMarkEnd);
                performance.measure('⏱️ [Perf] SA-TTS-Fetch-Request', perfMarkStart, perfMarkEnd);
                const measureEntries = performance.getEntriesByName('⏱️ [Perf] SA-TTS-Fetch-Request');
                const lastMeasure = measureEntries[measureEntries.length - 1];
                console.log(
                    `%c[Perf] TTS语音合成请求耗时: ${lastMeasure.duration.toFixed(2)}ms`,
                    'color: #000; font-weight: bold; font-size: 13px; background: #fff; padding: 2px 6px; border-radius: 3px;'
                );
                performance.clearMarks(perfMarkStart);
                performance.clearMarks(perfMarkEnd);
                // ===== 📊 性能埋点 END =====

                // ===== 📊 性能埋点：唇形渲染链路 - TTS返回标记 =====
                _lipSyncPerf.ttsResponseTime = performance.now();
                // ===== 📊 性能埋点 END =====

                if (result.code !== 0) {
                    console.error('[SA] TTS返回错误:', result.msg || result);
                } else {
                    console.log('[SA] TTS请求成功');
                }
            } catch (error) {
                console.error('[SA] TTS请求失败:', error);
            }
        }

        // ==================== Toast ====================
        function showToast(message, type = 'info') {
            const id = Date.now();
            toasts.value.push({ id, message, type });
            setTimeout(() => {
                const idx = toasts.value.findIndex(t => t.id === id);
                if (idx > -1) toasts.value.splice(idx, 1);
            }, 3000);
        }

        // ==================== 监听状态变化 ====================

        // 监听激活状态 - 连接/断开
        watch(() => isActive.value, async (newVal) => {
            if (newVal) {
                await nextTick();
                connectDigitalHuman();
            } else {
                disconnectDigitalHuman();
            }
        });

        // 监听可见状态 - 最小化时暂停视频节省资源，展开时恢复
        watch(() => isVisible.value, async (newVal) => {
            if (newVal && isActive.value && !isDigitalHumanConnected.value && !isConnecting.value) {
                await nextTick();
                connectDigitalHuman();
            }
            // 展开/恢复时重新播放视频并恢复渲染
            if (newVal) {
                await nextTick();
                if (videoElement.value && videoElement.value.srcObject) {
                    if (videoElement.value.paused) {
                        videoElement.value.play().catch(() => {});
                    }
                    // 恢复绿幕渲染循环
                    if (chromaGL.value && chromaAnimId.value === null) {
                        renderChromaFrame();
                    }
                }
            }
        });

        // 监听划词选中文本变化
        watch(() => selectedText.value, async (newVal) => {
            if (newVal) {
                await nextTick();
                addChatMessage('user', newVal);
                // 等连接就绪后发送
                const sendWithRetry = async (retries = 0) => {
                    if (isDigitalHumanConnected.value && sessionId.value) {
                        await sendToAI(newVal);
                    } else if (retries < 10) {
                        setTimeout(() => sendWithRetry(retries + 1), 1000);
                    } else {
                        addChatMessage('assistant', '连接超时，请重试~');
                    }
                };
                sendWithRetry();
                store.clearSelection();
            }
        });

        // 监听外部 textToSpeak - 一次性发送整段文本，保持唇形连续
        watch(() => textToSpeak.value, async (newVal) => {
            if (newVal && newVal.trim()) {
                await speakText(newVal.trim());
                textToSpeak.value = '';
            }
        });

        // 聊天历史由本地 chatHistory ref 管理，无需从 store 恢复

        // ==================== 生命周期 ====================
        onMounted(() => {
            document.addEventListener('mouseup', handleMouseUp);
            document.addEventListener('mousedown', handleMouseDown);
            isSpeechSupported.value = true; // 使用 Whisper STT
        });

        onBeforeUnmount(() => {
            document.removeEventListener('mouseup', handleMouseUp);
            document.removeEventListener('mousedown', handleMouseDown);
            disconnectDigitalHuman();
            if (selectionTimeout) clearTimeout(selectionTimeout);
        });

        return {
            // store 响应式状态 - 模板中 v-if/v-show 依赖
            isActive,
            isVisible,
            isMinimized,
            cardRef,
            videoElement,
            chromaCanvas,
            chatHistoryRef,
            isDigitalHumanConnected,
            isDigitalHumanSpeaking,
            digitalHumanStatus,
            chatHistory,
            inputText,
            isListening,
            showSelectionBubble,
            selectionBubblePosition,
            toasts,
            cardStyle,
            handleBallClick,
            handleMinimize,
            handleClose,
            handleBubbleClick,
            startCardDrag,
            sendMessage,
            toggleMic,
            chromaEnabled,
        };
    }
};
</script>

<style scoped>
/* ==================== 划词气泡 ==================== */
.selection-bubble {
    position: fixed;
    z-index: 10001;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 14px;
    background: linear-gradient(135deg, #00BFFF 0%, #1E90FF 100%);
    color: white;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(0, 191, 255, 0.4);
    transition: all 0.2s;
    user-select: none;
    animation: bubble-fade-in 0.2s ease-out;
}

.selection-bubble:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0, 191, 255, 0.5);
}

.bubble-icon {
    display: flex;
    align-items: center;
    justify-content: center;
}

.bubble-text {
    white-space: nowrap;
}

@keyframes bubble-fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ==================== 悬浮球 ==================== */
.floating-ball {
    position: fixed;
    right: 24px;
    bottom: 24px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00BFFF 0%, #1E90FF 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 10000;
    box-shadow: 0 4px 20px rgba(0, 191, 255, 0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
}

.floating-ball:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 28px rgba(0, 191, 255, 0.5);
}

.floating-ball:active {
    transform: scale(0.95);
}

.floating-ball.speaking {
    animation: ball-pulse-glow 2s ease-in-out infinite;
}

.ball-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    z-index: 1;
}

.ball-pulse {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: rgba(0, 191, 255, 0.3);
    animation: ball-ripple 2s ease-out infinite;
}

.ball-pulse.delay {
    animation-delay: 0.6s;
}

@keyframes ball-ripple {
    0% { transform: scale(1); opacity: 0.6; }
    100% { transform: scale(2); opacity: 0; }
}

@keyframes ball-pulse-glow {
    0%, 100% { box-shadow: 0 4px 20px rgba(0, 191, 255, 0.4); }
    50% { box-shadow: 0 4px 30px rgba(0, 191, 255, 0.7); }
}

/* ==================== 悬浮卡片 ==================== */
.floating-card {
    position: fixed;
    width: 600px;
    height: 420px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15), 0 2px 8px rgba(0, 0, 0, 0.08);
    z-index: 10000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: card-slide-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    user-select: none;
}

@keyframes card-slide-in {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(20px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

/* ==================== 卡片头部 ==================== */
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    background: #1a5c3a;
    color: white;
    cursor: grab;
    flex-shrink: 0;
}

.card-header:active {
    cursor: grabbing;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

.header-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.header-title {
    font-size: 14px;
    font-weight: 600;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.status-dot.connected {
    background: #86efac;
    box-shadow: 0 0 6px rgba(134, 239, 172, 0.6);
}

.status-dot.disconnected {
    background: #fca5a5;
}

.header-actions {
    display: flex;
    gap: 4px;
}

.action-btn {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    border: none;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    padding: 0;
}

.action-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

.close-btn:hover {
    background: rgba(239, 68, 68, 0.8);
}

/* ==================== 卡片内容 ==================== */
.card-body {
    display: flex;
    flex: 1;
    overflow: hidden;
    min-height: 0;
}

/* ==================== 视频区 ==================== */
.video-area {
    width: 240px;
    flex-shrink: 0;
    background: #000;
    position: relative;
    overflow: hidden;
}

.video-player {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: none;
}

.video-player.connected {
    display: block;
}

.video-player.chroma-source {
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
}

.chroma-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: none;
    will-change: transform;
    transform: translateZ(0);
    pointer-events: none;
    z-index: 1;
}

.chroma-canvas.connected {
    display: block;
}

.video-placeholder {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #666;
    gap: 8px;
}

.placeholder-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    opacity: 0.5;
}

.placeholder-text {
    font-size: 13px;
    color: #999;
}

.speaking-indicator {
    position: absolute;
    bottom: 8px;
    left: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background: rgba(0, 0, 0, 0.7);
    color: #10b981;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

.speaking-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10b981;
    animation: speaking-blink 1s ease-in-out infinite;
}

@keyframes speaking-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ==================== 聊天区 ==================== */
.chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-width: 0;
}

.chat-history {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
    min-height: 0;
}

.chat-history::-webkit-scrollbar {
    width: 4px;
}

.chat-history::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 2px;
}

.empty-chat {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #9ca3af;
    gap: 8px;
}

.empty-icon {
    font-size: 32px;
    opacity: 0.5;
}

.empty-text {
    font-size: 13px;
}

.chat-message {
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
    animation: msg-slide-in 0.2s ease-out;
}

.chat-message.user {
    flex-direction: row-reverse;
}

.message-avatar {
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 2px;
}

.message-bubble {
    max-width: 80%;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 13px;
    line-height: 1.5;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

.chat-message.user .message-bubble {
    background: #f3f4f6;
    color: #1f2937;
    border: 2px dashed #10b981;
    border-bottom-right-radius: 4px;
}

.chat-message.assistant .message-bubble {
    background: #f3f4f6;
    color: #1f2937;
    border: 1px solid #e5e7eb;
    border-bottom-left-radius: 4px;
}

@keyframes msg-slide-in {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ==================== 输入区 ==================== */
.chat-input-area {
    padding: 10px 12px;
    border-top: 1px solid #e5e7eb;
    flex-shrink: 0;
    background: #fafafa;
}

.input-row {
    display: flex;
    gap: 6px;
    align-items: center;
}

.mic-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #f3f4f6;
    color: #666;
    border: 1px solid #e5e7eb;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s;
    position: relative;
    padding: 0;
}

.mic-btn:hover {
    background: #e5e7eb;
}

.mic-btn.listening {
    background: #10b981;
    border-color: #10b981;
    color: white;
}

.mic-ripple {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.mic-ripple span {
    position: absolute;
    inset: 0;
    border-radius: 8px;
    background: rgba(16, 185, 129, 0.3);
    animation: mic-ripple-effect 1.5s ease-out infinite;
}

.mic-ripple span:nth-child(2) { animation-delay: 0.5s; }
.mic-ripple span:nth-child(3) { animation-delay: 1s; }

@keyframes mic-ripple-effect {
    0% { transform: scale(1); opacity: 0.6; }
    100% { transform: scale(2); opacity: 0; }
}

.text-input {
    flex: 1;
    min-width: 0;
    padding: 6px 10px;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 13px;
    outline: none;
    transition: border-color 0.2s;
    background: white;
}

.text-input:focus {
    border-color: #10b981;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

.send-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #10b981;
    color: white;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s;
    padding: 0;
}

.send-btn:hover:not(:disabled) {
    background: #059669;
}

.send-btn:disabled {
    background: #d1d5db;
    cursor: not-allowed;
}

/* ==================== Toast ==================== */
.sa-toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10002;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.sa-toast {
    padding: 10px 16px;
    border-radius: 8px;
    background: white;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    animation: toast-in 0.3s ease-out;
}

.sa-toast.success { border-left: 3px solid #10b981; }
.sa-toast.error { border-left: 3px solid #ef4444; }
.sa-toast.info { border-left: 3px solid #3b82f6; }

.toast-icon { flex-shrink: 0; }
.toast-msg { color: #1f2937; }

@keyframes toast-in {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}
</style>

