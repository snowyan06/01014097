<template>
    <div>
        <!-- 嵌入模式：不使用teleport，直接渲染在父组件内 -->
        <div v-if="embedMode && show"
           ref="containerRef"
           class="digital-human-container embed-mode"
           :style="embedContainerStyle"
        >
            <div class="main-content">
                <div class="video-section full-width">
                    <div class="video-container">
                        <video
                            ref="videoElement"
                            autoplay
                            playsinline
                            muted
                            class="video-player"
                            :class="{ 'connected': isConnected }"
                        ></video>

                        <div class="connection-status" :class="{ 'connected': isConnected }">
                            {{ connectionStatus }}
                        </div>

                        <div v-if="isSpeaking && interruptEnabled" class="interrupt-indicator" title="AI 正在说话，您可以直接打断">
                            <span class="indicator-icon">🎤</span>
                            <span class="indicator-text">{{ currentLanguage === 'en-US' ? 'Tap to interrupt' : '点击麦克风可打断' }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 学习中心模式：使用teleport挂载到body -->
        <teleport v-else to="body">
        <div v-if="!isSpeechSupported || speechNetworkError" class="speech-warning-banner">
            <div class="banner-content">
                <span class="banner-icon">⚠️</span>
                <span class="banner-text">
                    语音识别服务暂时不可用，请使用文字输入
                    <button @click="retrySpeechService" class="retry-btn">重试</button>
                </span>
            </div>
        </div>

        <div v-if="showPermissionGuide" class="permission-guide-overlay">
            <div class="permission-guide-modal">
                <div class="guide-header">
                    <div class="guide-icon-wrapper">
                        <span class="guide-icon">🎤</span>
                    </div>
                    <h3 class="guide-title">使用语音输入</h3>
                </div>

                <div class="guide-body">
                    <p class="guide-text">
                        即将请求麦克风权限，用于语音识别功能
                    </p>

                    <div class="guide-steps">
                        <div class="step">
                            <span class="step-number">1</span>
                            <span class="step-text">点击"允许"授予麦克风权限</span>
                        </div>
                        <div class="step">
                            <span class="step-number">2</span>
                            <span class="step-text">对着麦克风清楚说话</span>
                        </div>
                        <div class="step">
                            <span class="step-number">3</span>
                            <span class="step-text">说完会自动发送并识别</span>
                        </div>
                    </div>

                    <div class="guide-tips">
                        <div class="tip-item">
                            <span class="tip-icon">💡</span>
                            <span class="tip-text">浏览器会在顶部弹出权限请求框</span>
                        </div>
                        <div class="tip-item">
                            <span class="tip-icon">🔒</span>
                            <span class="tip-text">权限仅请求一次，下次无需再次授权</span>
                        </div>
                        <div class="tip-item">
                            <span class="tip-icon">🌐</span>
                            <span class="tip-text">点击麦克风左侧按钮可切换中/英文</span>
                        </div>
                    </div>
                </div>

                <div class="guide-footer">
                    <button @click="cancelPermission" class="guide-btn guide-btn-secondary">
                        暂不使用
                    </button>
                    <button @click="requestPermission" class="guide-btn guide-btn-primary">
                        好的，继续
                    </button>
                </div>
            </div>
        </div>

        <div class="toast-container">
            <div v-for="toast in toasts" :key="toast.id" class="toast" :class="toast.type">
                <div class="toast-icon">{{ toast.icon }}</div>
                <div class="toast-content">
                    <div class="toast-message">{{ toast.message }}</div>
                    <div class="toast-description">{{ toast.description }}</div>
                </div>
                <div class="toast-progress"></div>
            </div>
        </div>

        <div
           ref="containerRef"
           class="digital-human-container"
           v-if="show"
           :style="containerStyle"
        >
            <button @click="closeDigitalHuman" class="close-btn" title="关闭数字人">
                ×
            </button>

            <div class="main-content" @mousedown.stop="startDrag">
                <div class="video-section">
                    <div class="video-container">
                        <video
                            ref="videoElement"
                            autoplay
                            playsinline
                            muted
                            class="video-player"
                            :class="{ 'connected': isConnected }"
                        ></video>

                        <div class="connection-status" :class="{ 'connected': isConnected }">
                            {{ connectionStatus }}
                        </div>

                        <div v-if="isSpeaking && interruptEnabled" class="interrupt-indicator" title="AI 正在说话，您可以直接打断">
                            <span class="indicator-icon">🎤</span>
                            <span class="indicator-text">{{ currentLanguage === 'en-US' ? 'Tap to interrupt' : '点击麦克风可打断' }}</span>
                        </div>
                    </div>
                </div>

                <div class="chat-section">
                    <div class="chat-history">
                        <div class="history-scroll" ref="historyScroll">
                            <div
                                v-for="(msg, index) in chatHistory"
                                :key="index"
                                :class="['message', msg.role]"
                            >
                                <div class="message-content">
                                    <span class="message-icon">{{ msg.role === 'user' ? '👤' : '🤖' }}</span>
                                    <span class="message-text">{{ msg.text }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="input-area" v-if="isConnected">
                        <div class="preset-questions">
                            <button @click.stop="ask('你好，很高兴认识你')" class="preset-btn" title="打招呼">
                                打招呼
                            </button>
                            <button @click.stop="ask('请介绍一下你自己')" class="preset-btn" title="自我介绍">
                                自我介绍
                            </button>
                            <button @click.stop="ask('今天天气怎么样')" class="preset-btn" title="天气">
                                天气
                            </button>
                            <button @click.stop="ask('你能帮我学习吗')" class="preset-btn" title="学习帮助">
                                学习帮助
                            </button>
                        </div>

                        <div class="input-row">
                            <button
                                @click.stop="toggleLanguage"
                                class="lang-btn"
                                :title="'当前语言：' + getCurrentLanguageDisplay().name"
                                v-if="isSpeechSupported"
                            >
                                <span class="lang-flag">{{ getCurrentLanguageDisplay().flag }}</span>
                                <span class="lang-text">{{ getCurrentLanguageDisplay().name }}</span>
                            </button>

                            <div v-if="isListening" class="waveform-visualizer">
                                <div class="waveform-bar listening"></div>
                                <div class="waveform-bar listening"></div>
                                <div class="waveform-bar listening"></div>
                                <div class="waveform-bar listening"></div>
                                <div class="waveform-bar listening"></div>
                            </div>

                            <button
                                @click.stop="startListening"
                                class="mic-btn"
                                :class="{ 'listening': isListening }"
                                :title="isListening ? '停止录音' : '语音输入'"
                                v-if="isSpeechSupported"
                            >
                                <svg class="mic-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 1C10.3431 1 9 2.34315 9 4V12C9 13.6569 10.3431 15 12 15C13.6569 15 15 13.6569 15 12V4C15 2.34315 13.6569 1 12 1Z" fill="currentColor"/>
                                    <path d="M19 10V12C19 15.866 15.866 19 12 19C8.13401 19 5 15.866 5 12V10H3V12C3 16.4183 6.58172 20 11 20V23H13V20C17.4183 20 21 16.4183 21 12V10H19Z" fill="currentColor"/>
                                </svg>
                                <div v-if="isListening" class="ripple-container">
                                    <div class="ripple"></div>
                                    <div class="ripple"></div>
                                    <div class="ripple"></div>
                                </div>
                            </button>

                            <input
                                v-model="inputText"
                                @keyup.enter="sendText"
                                @mousedown.stop
                                type="text"
                                placeholder="输入文字，或点击麦克风说话..."
                                class="text-input"
                            />
                            <button @click.stop="sendText" class="send-btn" :disabled="!inputText.trim()">
                                发送
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </teleport>
    </div>
</template>

<script>

export default {
    name: 'DigitalHuman',
    props: {
            show: {
                type: Boolean,
                default: false
            },
            textToSpeak: {
                type: String,
                default: ''
            },
            width: {
                type: [String, Number],
                default: 1200
            },
            aspectRatio: {
                type: Number,
                default: 3/4
            },
            maxHeight: {
                type: [String, Number],
                default: 800
            },
            initialPosition: {
                type: Object,
                default: () => ({ x: 100, y: 50 })
            },
            embedMode: {
                type: Boolean,
                default: false
            }
        },
    data() {
        return {
            pc: null,
            sessionId: null,
            isConnected: false,
            connectionStatus: '未连接',
            isSpeaking: false,
            serverUrl: 'http:' + '//localhost:7860',
            speakingCheckInterval: null,
            videoAspectRatio: 9/16,
            reconnectTimer: null,
            isConnecting: false,
            inputText: '',
            chatHistory: [],

            // 新增：语音识别相关
            isListening: false,
            recognition: null,
            isSpeechSupported: false,
            // 新增：网络错误标志
            speechNetworkError: false,

            // 新增：权限引导
            hasRequestedMicPermission: false,
            showPermissionGuide: false,

            // 新增：语言切换
            currentLanguage: 'zh-CN',  // 默认中文
            speechLanguages: [
                { code: 'zh-CN', name: '中文', flag: '🇨🇳' },
                { code: 'en-US', name: 'English', flag: '🇺🇸' }
            ],
            showLanguageSelector: false,

            // 新增：语音打断相关
            lastSpeakTime: 0,  // 记录上次说话时间
            interruptEnabled: true,  // 是否允许打断
            isProcessingInterrupt: false,  // 正在处理打断

            // 新增：Toast 提示
            toasts: [],

            // 拖拽相关
            isDragging: false,
            dragOffset: { x: 0, y: 0 },
            position: { x: 20, y: 20 },
            // 新增：录音器引用
            currentMediaRecorder: null
        }
    },
     computed: {
        embedContainerStyle() {
            return {
                width: '100%',
                height: '100%'
            };
        }
    },
    watch: {
        textToSpeak(newVal, oldVal) {
            if (newVal && newVal !== oldVal && this.isConnected) {
                this.speakText(newVal);
            }
        },
        show(newVal, oldVal) {
            console.log(`👀 show 变化：${oldVal} -> ${newVal}`);
            console.log(`🔗 isConnected: ${this.isConnected}`);
            console.log(`🔒 isConnecting: ${this.isConnecting}`);

            // 只在 show 从 false 变为 true 时才连接
            if (newVal && !oldVal && !this.isConnected && !this.isConnecting) {
                console.log(' 触发连接!');
                this.connect();
            } else if (!newVal && this.isConnected) {
                console.log('🛑 断开连接!');
                // 关闭数字人时断开连接
                this.disconnect();
            }
        }
    },
    mounted() {
        console.log('🎭 DigitalHuman 组件已挂载!');
        console.log('📏 初始宽高:', this.width, this.height);
        console.log('📐 初始位置:', this.position);

        // 新增：初始化语音识别
        this.initSpeechRecognition();

        // 新增：添加键盘快捷键监听
        document.addEventListener('keydown', this.handleKeyPress);

        if (this.show) {
            console.log('🚀 触发连接!');
            this.connect();
        }
    },

    beforeUnmount() {
        this.disconnect();

        document.removeEventListener('mousemove', this.onDrag);
        document.removeEventListener('mouseup', this.stopDrag);

        // 新增：移除键盘事件监听
        document.removeEventListener('keydown', this.handleKeyPress);
    },
    methods: {
        // 修改：关闭数字人方法 - 同时触发两个事件
        closeDigitalHuman() {
            console.log('❌ 点击关闭按钮');

            // 方法 1: 触发 close 事件（显式方式）- 父组件正在监听这个
            this.$emit('close');
            console.log('✅ 已发送 close 事件');

            // 方法 2: 触发 update:show 事件（v-model 方式）- 备用
            this.$emit('update:show', false);
            console.log('✅ 已发送 update:show 事件');
        },

        startDrag(e) {
            if (e.button !== 0) return; // 只响应左键
            e.preventDefault();

            const container = this.$refs.containerRef;
            const rect = container.getBoundingClientRect();

            this.isDragging = true;
            this.dragOffset = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            };

            // 可选：添加样式提示
            container.style.cursor = 'grabbing';
        },

        onDrag(e) {
            if (!this.isDragging) return;

            const x = e.clientX - this.dragOffset.x;
            const y = e.clientY - this.dragOffset.y;

            // 可选：限制在视口内
            const maxX = window.innerWidth - this.width - 10;
            const maxY = window.innerHeight - 100; // 留出底部空间
            const minX = 10;
            const minY = 10;

            this.position.x = Math.max(minX, Math.min(maxX, x));
            this.position.y = Math.max(minY, Math.min(maxY, y));
        },

        stopDrag() {
            if (!this.isDragging) return;

            this.isDragging = false;
            const container = this.$refs.containerRef;
            if (container) {
                container.style.cursor = 'grab';
            }
        },

        // 修改：使用本地 Whisper STT 服务
        initSpeechRecognition() {
            console.log('✅ 使用本地 Whisper STT 服务');
            this.isSpeechSupported = true;
        },

        // 新增：WebM 转 WAV 格式
        async convertWebMToWAV(webmBlob) {
            return new Promise((resolve, reject) => {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)({
                    sampleRate: 16000
                });

                const reader = new FileReader();
                reader.onload = async () => {
                    try {
                        const arrayBuffer = reader.result;
                        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

                        // 转换为单声道
                        let monoBuffer;
                        if (audioBuffer.numberOfChannels > 1) {
                            monoBuffer = audioContext.createBuffer(
                                1,
                                audioBuffer.length,
                                audioBuffer.sampleRate
                            );
                            const leftChannel = audioBuffer.getChannelData(0);
                            const rightChannel = audioBuffer.getChannelData(1);
                            const monoChannel = monoBuffer.getChannelData(0);
                            for (let i = 0; i < audioBuffer.length; i++) {
                                monoChannel[i] = (leftChannel[i] + rightChannel[i]) / 2;
                            }
                        } else {
                            monoBuffer = audioBuffer;
                        }

                        // 转换为 WAV
                        const wavBlob = this.audioBufferToWav(monoBuffer);
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
        },

        // 新增：AudioBuffer 转 WAV Blob
        audioBufferToWav(buffer) {
            const numChannels = buffer.numberOfChannels;
            const sampleRate = buffer.sampleRate;
            const format = 1; // PCM
            const bitDepth = 16;

            const bytesPerSample = bitDepth / 8;
            const blockAlign = numChannels * bytesPerSample;

            const data = [];
            for (let i = 0; i < buffer.length; i++) {
                const sample = Math.max(-1, Math.min(1, buffer.getChannelData(0)[i]));
                const intSample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
                data.push(intSample);
            }

            const dataLength = data.length * bytesPerSample;
            const bufferLength = 44 + dataLength;
            const arrayBuffer = new ArrayBuffer(bufferLength);
            const view = new DataView(arrayBuffer);

            // WAV Header
            this.writeString(view, 0, 'RIFF');
            view.setUint32(4, 36 + dataLength, true);
            this.writeString(view, 8, 'WAVE');
            this.writeString(view, 12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, format, true);
            view.setUint16(22, numChannels, true);
            view.setUint32(24, sampleRate, true);
            view.setUint32(28, sampleRate * blockAlign, true);
            view.setUint16(32, blockAlign, true);
            view.setUint16(34, bitDepth, true);
            this.writeString(view, 36, 'data');
            view.setUint32(40, dataLength, true);

            // Write PCM samples
            let offset = 44;
            for (let i = 0; i < data.length; i++) {
                view.setInt16(offset, data[i], true);
                offset += 2;
            }

            return new Blob([arrayBuffer], { type: 'audio/wav' });
        },

        writeString(view, offset, string) {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        },

        // 修改：开始录音并上传识别
        async startListening() {
            if (!this.isSpeechSupported) {
                this.showToast('语音功能不可用', 'warning');
                return;
            }

            if (this.isListening) {
                this.stopListening();
                return;
            }

            // 打断 AI
            const now = Date.now();
            if (this.isSpeaking && this.interruptEnabled) {
                console.log('⚡ 检测到语音打断！');
                await this.interruptAI();
            }

            try {
                console.log('🎤 开始录音...');

                // 请求麦克风权限
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: {
                        sampleRate: 16000,
                        channelCount: 1,
                        echoCancellation: true,
                        noiseSuppression: true
                    }
                });

                this.isListening = true;
                const mediaRecorder = new MediaRecorder(stream, {
                    mimeType: 'audio/webm;codecs=opus'
                });

                const audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = async () => {
                    console.log('⏹️ 录音停止，开始识别...');

                    stream.getTracks().forEach(track => track.stop());

                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

                    if (audioBlob.size < 1000) {
                        console.warn('⚠️ 录音数据太小，可能未录到声音');
                        this.showToast('录音时间太短', 'warning', '请至少录制 2 秒');
                        this.isListening = false;
                        return;
                    }

                    try {
                        // 新增：将 WebM 转换为 WAV 格式
                        const wavBlob = await this.convertWebMToWAV(audioBlob);

                        const formData = new FormData();
                        formData.append('audio', wavBlob, 'recording.wav');
                        formData.append('language', this.currentLanguage === 'en-US' ? 'en' : 'zh');

                        const response = await fetch(`${this.serverUrl}/speech_to_text`, {
                            method: 'POST',
                            body: formData
                        });

                        const result = await response.json();

                        if (result.code === 0 && result.text) {
                            console.log('✅ 识别成功:', result.text);
                            this.inputText = result.text;

                            const recognizedText = result.text;
                            setTimeout(() => {
                                console.log('🚀 自动发送识别文本:', recognizedText);
                                this.sendText();
                            }, 500);

                            this.showToast('识别成功', 'success', result.text);
                        } else {
                            console.error('❌ 识别失败:', result.msg);
                            this.showToast('识别失败', 'error', result.msg || '请重试');
                        }
                    } catch (error) {
                        console.error('❌ 识别请求失败:', error);
                        this.showToast('网络错误', 'error', '请检查后端服务是否启动');
                    } finally {
                        this.isListening = false;
                    }
                };

                mediaRecorder.onerror = (error) => {
                    console.error('❌ 录音错误:', error);
                    this.isListening = false;
                    stream.getTracks().forEach(track => track.stop());
                    this.showToast('录音失败', 'error');
                };

                // 开始录音
                mediaRecorder.start();
                console.log('🔴 录音中...');

                const isEnglish = this.currentLanguage === 'en-US';
                this.showToast(
                    isEnglish ? 'Recording...' : '录音中...',
                    'success',
                    isEnglish ? 'Click again to stop and recognize' : '再次点击停止并识别'
                );

                // 保存引用以便停止
                this.currentMediaRecorder = mediaRecorder;

            } catch (error) {
                console.error('❌ 启动录音失败:', error);
                this.isListening = false;

                if (error.name === 'NotAllowedError') {
                    this.showToast('麦克风权限被拒绝', 'error', '请在浏览器设置中允许麦克风访问');
                } else {
                    this.showToast('无法访问麦克风', 'error', error.message);
                }
            }
        },

        // 修改：停止录音
        stopListening() {
            if (this.currentMediaRecorder && this.currentMediaRecorder.state !== 'inactive') {
                console.log('⏹️ 停止录音');
                this.currentMediaRecorder.stop();
                this.isListening = false;
            }
        },

        // 新增：Toast 提示方法
        showToast(message, type = 'info', description = '') {
            const id = Date.now();
            const toastConfig = {
                id,
                message,
                type,
                description,
                duration: type === 'error' ? 5000 : 3000 // 错误提示显示更久
            };

            this.toasts.push(toastConfig);

            // 定时移除
            setTimeout(() => {
                this.removeToast(id);
            }, toastConfig.duration);
        },

        removeToast(id) {
            const index = this.toasts.findIndex(t => t.id === id);
            if (index > -1) {
                this.toasts.splice(index, 1);
            }
        },

        async connect() {
            // 防止重复连接
            if (this.isConnecting) {
                console.log('⚠️ 正在连接中，忽略重复请求');
                return;
            }

            // 确保 video 元素存在
            if (!this.$refs.videoElement) {
                console.error('❌ video 元素不存在，无法连接');
                return;
            }

            try {
                this.isConnecting = true;  // 设置连接锁
                this.connectionStatus = '连接中...';
                const configuration = {
                    iceServers: [
                        { urls: 'stun:stun.miwifi.com:3478' },
                        { urls: 'stun:stun.l.google.com:19302' }
                    ]
                };
                this.pc = new RTCPeerConnection(configuration);

                this.pc.onconnectionstatechange = () => {
                    console.log('Connection state:', this.pc.connectionState);
                    if (this.pc.connectionState === 'connected') {
                        this.isConnected = true;
                        this.connectionStatus = '已连接';
                        this.isConnecting = false;  // 连接成功，释放锁
                        this.startSpeakingCheck();
                    } else if (this.pc.connectionState === 'failed') {
                        this.connectionStatus = '连接失败';
                        this.isConnecting = false;  // 连接失败，释放锁
                    }
                };

                this.pc.ontrack = (event) => {
                     console.log('📥 收到 track:', event.track.kind);
                      if (!this.$refs.videoElement) {
                           console.error('❌ video 元素在 ontrack 中不存在');
                           return;
                      }
                      if (!this.$refs.videoElement.srcObject) {
                           this.$refs.videoElement.srcObject = new MediaStream();
                      }
                      event.streams[0].getTracks().forEach(track => {
                          this.$refs.videoElement.srcObject.addTrack(track);
                          if (track.kind === 'video') {
                              this.setupVideoTrack(track);
                          }
                      });
               };

                const offer = await this.pc.createOffer({
                    offerToReceiveAudio: true,
                    offerToReceiveVideo: true
                });
                await this.pc.setLocalDescription(offer);

                const response = await fetch(`${this.serverUrl}/offer`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sdp: this.pc.localDescription.sdp,
                        type: this.pc.localDescription.type
                    })
                });

                const answer = await response.json();
                if (answer.code === -1) throw new Error(answer.msg);

                this.sessionId = answer.sessionid;
                await this.pc.setRemoteDescription(answer);
                // 成功设置后释放锁
                this.isConnecting = false;

            } catch (error) {
                console.error('Connection failed:', error);
                this.connectionStatus = `连接失败：${error.message}`;
                this.isConnecting = false;  // 连接失败，释放锁
            }
        },

        setupVideoTrack(track) {
            const video = this.$refs.videoElement;

            const updateAspectRatio = () => {
                if (video.videoWidth > 0 && video.videoHeight > 0) {
                    this.videoAspectRatio = video.videoHeight / video.videoWidth;
                    console.log('Detected video aspect ratio:', this.videoAspectRatio);
                }
            };

            video.addEventListener('loadedmetadata', updateAspectRatio);

            const checkInterval = setInterval(() => {
                if (video.videoWidth > 0) {
                    updateAspectRatio();
                    clearInterval(checkInterval);
                }
            }, 500);

            track.onmute = () => clearInterval(checkInterval);
        },

        async reconnect() {
            await this.disconnect();
            // 使用定时器延迟重连，避免立即重连导致状态冲突
            this.reconnectTimer = setTimeout(() => {
                this.connect();
            }, 3000);
        },

        disconnect() {
            if (this.pc) {
                // 先关闭连接
                this.pc.close();
                this.pc = null;
            }
            this.isConnected = false;
            this.connectionStatus = '未连接';
            this.sessionId = null;
            this.stopSpeakingCheck();
            if (this.$refs.videoElement) {
                this.$refs.videoElement.srcObject = null;
            }
            // 清除可能的重连定时器
            if (this.reconnectTimer) {
                clearTimeout(this.reconnectTimer);
                this.reconnectTimer = null;
            }
            // 释放连接锁
            this.isConnecting = false;
        },

        // 修改：发送文字方法 - 改为调用 AI
        sendText() {
            if (!this.inputText.trim()) return;

            const text = this.inputText.trim();

            // 添加到对话历史
            this.addHistory('user', text);

            console.log('📝 发送文字:', text);

            // 调用 AI 对话接口
            this.sendToAI(text);

            // 清空输入框
            this.inputText = '';
        },

        // 修改：预设问题 - 调用 AI
        ask(question) {
            console.log('❓ 预设问题:', question);

            // 添加到对话历史
            this.addHistory('user', question);

            this.inputText = question;

            // 调用 AI 对话接口
            this.sendToAI(question);
        },

        // 新增：添加对话历史
        addHistory(role, text) {
            this.chatHistory.push({
                role: role,
                text: text,
                time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
            });

            // 自动滚动到底部
            this.$nextTick(() => {
                const history = this.$refs.historyScroll;
                if (history) {
                    history.scrollTop = history.scrollHeight;
                }
            });
        },

        // 新增：发送到 AI
        async sendToAI(message) {
            try {
                const response = await fetch(`${this.serverUrl}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionid: this.sessionId,
                        message: message
                    })
                });

                const result = await response.json();

                if (result.code === 0) {
                    console.log('🤖 AI 回复:', result.reply);
                    // AI 会自动播放回复，无需手动处理
                    // 添加到对话历史 (AI 的回复)
                    this.addHistory('assistant', result.reply);
                } else {
                    console.error('❌ AI 对话失败:', result.msg);
                    this.addHistory('assistant', '抱歉，我现在有点累，等会再聊吧~');
                }
            } catch (error) {
                console.error('❌ AI 对话异常:', error);
                this.addHistory('assistant', '抱歉，出了点问题，请稍后再试~');
            }
        },

        async speakText(text) {
            if (!this.isConnected || !text.trim()) return;
            try {
                const response = await fetch(`${this.serverUrl}/human`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionid: this.sessionId,
                        type: 'echo',
                        interrupt: true,
                        text: text.trim()
                    })
                });
                const result = await response.json();
                if (result.code === 0) {
                    this.isSpeaking = true;
                    console.log('✅ TTS 发送成功');
                }
            } catch (error) {
                console.error('朗读失败:', error);
            }
        },

        testTTS() {
            console.log('🎤 开始测试 TTS...');
            const testText = '你好，这是数字人语音测试';
            console.log('📝 发送文字:', testText);
            console.log('🔑 SessionID:', this.sessionId);
            this.speakText(testText);
        },

        startSpeakingCheck() {
            this.speakingCheckInterval = setInterval(async () => {
                if (!this.isConnected) return;
                try {
                    const response = await fetch(`${this.serverUrl}/is_speaking`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ sessionid: this.sessionId })
                    });
                    const result = await response.json();
                    if (result.code === 0) {
                        this.isSpeaking = result.data;
                    }
                } catch (error) {
                    console.error('检查说话状态失败:', error);
                }
            }, 1000);
        },

        stopSpeakingCheck() {
            if (this.speakingCheckInterval) {
                clearInterval(this.speakingCheckInterval);
                this.speakingCheckInterval = null;
            }
        },

        // 新增：取消权限请求
        cancelPermission() {
            this.showPermissionGuide = false;
            this.showToast('已取消语音输入', 'info', '你可以随时点击麦克风按钮重新开始');
        },

        // 新增：切换语言
        toggleLanguage() {
            // 切换到另一种语言
            const currentIndex = this.speechLanguages.findIndex(lang => lang.code === this.currentLanguage);
            const nextIndex = (currentIndex + 1) % this.speechLanguages.length;
            const newLanguage = this.speechLanguages[nextIndex];

            this.currentLanguage = newLanguage.code;

            // 保存到 localStorage
            localStorage.setItem('speech_language', newLanguage.code);

            // 重新初始化语音识别
            if (this.recognition) {
                this.recognition.lang = newLanguage.code;
            }

            // 显示提示
            const langName = newLanguage.name;
            this.showToast(
                `已切换到${langName}`,
                'success',
                `当前语音识别语言：${langName}`
            );

            console.log(`🔄 语言已切换：${newLanguage.code}`);
        },

        // 新增：获取当前语言显示名称
        getCurrentLanguageDisplay() {
            const lang = this.speechLanguages.find(l => l.code === this.currentLanguage);
            return lang ? { name: lang.name, flag: lang.flag } : { name: '中文', flag: '🇨🇳' };
        },

        // 新增：AI 打断方法
        async interruptAI() {
            if (!this.isConnected || !this.sessionId) {
                console.warn('⚠️ 未连接，无法打断');
                return;
            }

            if (this.isProcessingInterrupt) {
                console.log('⏸️ 正在处理打断，忽略重复请求');
                return;
            }

            try {
                this.isProcessingInterrupt = true;
                console.log('🔇 正在停止 AI 播放...');

                // 调用后端接口停止 TTS
                const response = await fetch(`${this.serverUrl}/interrupt`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionid: this.sessionId
                    })
                });

                const result = await response.json();

                if (result.code === 0) {
                    console.log('✅ AI 已停止说话');
                    this.isSpeaking = false;

                    // 显示打断提示
                    const isEnglish = this.currentLanguage === 'en-US';
                    this.showToast(
                        isEnglish ? 'Interrupted AI' : '已打断 AI',
                        'info',
                        isEnglish ? 'AI stopped, listening to you now' : 'AI 已停止，正在聆听您的发言'
                    );
                } else {
                    console.warn('⚠️ 打断失败:', result.msg);
                }
            } catch (error) {
                console.error('❌ 打断 AI 失败:', error);
            } finally {
                this.isProcessingInterrupt = false;
                this.lastSpeakTime = Date.now();
            }
        },

        // 新增：重试语音服务
        retrySpeechService() {
            this.speechNetworkError = false;
            this.showToast('正在重新初始化...', 'info', '请稍候');

            setTimeout(() => {
                this.initSpeechRecognition();
                if (this.isSpeechSupported) {
                    this.showToast('✅ 语音服务已恢复', 'success');
                } else {
                    this.speechNetworkError = true;
                    this.showToast('❌ 仍无法连接，请使用文字输入', 'error');
                }
            }, 1500);
        },

        // 新增：键盘快捷键处理
        handleKeyPress(event) {
            // 按 M 键快速启动/停止语音识别
            if (event.key === 'm' || event.key === 'M') {
                // 避免在输入框聚焦时触发
                if (event.target.tagName === 'INPUT') {
                    return;
                }

                event.preventDefault();
                console.log('⌨️ 快捷键 M 触发语音');
                this.startListening();
            }

            // 按 S 键强制停止 AI
            if ((event.key === 's' || event.key === 'S') && this.isSpeaking) {
                event.preventDefault();
                console.log('⌨️ 快捷键 S 停止 AI');
                this.interruptAI();
            }
        }
    }
}
</script>

<style scoped>
.digital-human-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    width: 1200px !important;
    height: 800px !important;
    max-width: 1200px !important;
    max-height: 800px !important;
    min-width: 1200px !important;
    min-height: 800px !important;
}
/* 嵌入模式样式 */
.embed-mode {
    position: relative !important;
    background: transparent !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    width: 100% !important;
    height: 100% !important;
    max-width: none !important;
    max-height: none !important;
    min-width: auto !important;
    min-height: auto !important;
}

.embed-mode .main-content {
    height: 100%;
}

.embed-mode .video-section {
    width: 100%;
    height: 100%;
}
/* 嵌入模式全宽视频 */
.video-section.full-width {
    width: 100% !important;
    height: 100% !important;
}
/* 关闭按钮 */
.close-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    font-size: 22px;
    line-height: 1;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    transition: all 0.3s;
    padding: 0;
    pointer-events: auto;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

.close-btn:hover {
    background: rgba(239, 68, 68, 0.95);
    transform: scale(1.15);
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.5);
}

.close-btn:active {
    transform: scale(0.95);
}

.main-content {
    display: flex;
    flex-direction: row;
    flex: 1;
    overflow: hidden;
}

.video-section {
    width: 33.33%;
    background: #000;
    position: relative;
    flex-shrink: 0;
}

.video-container {
    position: relative;
    width: 100%;
    height: 100%;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 0;
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

.connection-status {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 6px 12px;
    background: rgba(0, 0, 0, 0.75);
    color: white;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    backdrop-filter: blur(8px);
    z-index: 10;
    transition: all 0.3s;
}

.connection-status.connected {
    background: rgba(34, 197, 94, 0.85);
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.4);
}

/* 新增：打断状态指示器 */
.interrupt-indicator {
    position: absolute;
    bottom: 10px;
    left: 10px;
    padding: 8px 14px;
    background: rgba(239, 68, 68, 0.85);
    color: white;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    backdrop-filter: blur(8px);
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 6px;
    animation: pulse-interrupt 2s ease-in-out infinite;
    box-shadow: 0 2px 12px rgba(239, 68, 68, 0.4);
    cursor: pointer;
    transition: all 0.3s;
}

.interrupt-indicator:hover {
    background: rgba(239, 68, 68, 0.95);
    transform: scale(1.05);
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.5);
}

.indicator-icon {
    font-size: 14px;
    animation: bounce 1s ease-in-out infinite;
}

.indicator-text {
    white-space: nowrap;
}

@keyframes pulse-interrupt {
    0%, 100% {
        opacity: 0.85;
        transform: scale(1);
    }
    50% {
        opacity: 1;
        transform: scale(1.02);
    }
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-3px);
    }
}

.chat-section {
    width: 66.67%;
    display: flex;
    flex-direction: column;
    background: rgba(249, 250, 251, 0.98);
    overflow: hidden;
    flex: 1;
}

.chat-history {
    flex: 1;
    overflow: hidden;
    border-bottom: 1px solid #e5e7eb;
    min-height: 0;
}

.history-scroll {
    height: 100%;
    overflow-y: auto;
    padding: 12px;
}

.history-scroll::-webkit-scrollbar {
    width: 6px;
}

.history-scroll::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.history-scroll::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}

.history-scroll::-webkit-scrollbar-thumb:hover {
    background: #555;
}

.message {
    margin-bottom: 12px;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-content {
    display: flex;
    align-items: flex-start;
    gap: 8px;
}

.message-icon {
    font-size: 16px;
    flex-shrink: 0;
}

.message-text {
    flex: 1;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.5;
    max-width: 80%;
    word-wrap: break-word;
}

.message.user .message-content {
    flex-direction: row-reverse;
}

.message.user .message-text {
    background: linear-gradient(135deg, #95ec69 0%, #7ed321 100%);
    color: #1f2937;
    box-shadow: 0 2px 8px rgba(149, 236, 105, 0.3);
}

.message.assistant .message-text {
    background: #f5f5f5;
    color: #1f2937;
    border: 1px solid #e5e7eb;
}

.input-area {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: rgba(255, 255, 255, 0.98);
    border-top: 1px solid #e5e7eb;
    flex-shrink: 0;
}

.preset-questions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 10px;
    padding: 4px;
}

.preset-btn {
    padding: 8px 16px;
    background: white;
    color: #3b82f6;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s;
    white-space: nowrap;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.preset-btn:hover {
    background: #f9fafb;
    border-color: #3b82f6;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}

.preset-btn:active {
    transform: translateY(0);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* 输入行样式 */
.input-row {
    display: flex;
    gap: 6px;
    align-items: center;
    width: 100%;
}

/* 语言切换按钮 */
.lang-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 10px;
    background: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
    font-size: 12px;
    color: #666;
}

.lang-btn:hover {
    background: #e8e8e8;
    border-color: #d0d0d0;
}

.lang-btn .lang-flag {
    font-size: 14px;
}

.lang-btn .lang-text {
    font-weight: 500;
    white-space: nowrap;
}

.text-input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
    transition: all 0.2s ease;
    background: #fff;
}

.text-input:focus {
    border-color: #07C160;
    box-shadow: 0 0 0 2px rgba(7, 193, 96, 0.1);
}

.send-btn {
    padding: 8px 16px;
    background: #07C160;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    flex-shrink: 0;
    white-space: nowrap;
}

.send-btn:hover:not(:disabled) {
    background: #06AD56;
}

.send-btn:disabled {
    background: #e0e0e0;
    color: #999;
    cursor: not-allowed;
    opacity: 1;
}

/* 麦克风按钮 */
.mic-btn {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: #f5f5f5;
    color: #666;
    border: 1px solid #e0e0e0;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    position: relative;
    overflow: visible;
    padding: 0;
}

.mic-btn:hover {
    background: #e8e8e8;
    border-color: #d0d0d0;
}

.mic-btn:active {
    background: #d9d9d9;
    transform: scale(0.95);
}

.mic-btn .mic-icon {
    width: 18px;
    height: 18px;
    transition: all 0.2s ease;
}

.mic-btn.listening {
    background: #07C160;
    border-color: #07C160;
    color: white;
    animation: none;
}

.mic-btn.listening:hover {
    background: #06AD56;
    border-color: #06AD56;
}

/* 新增：波纹效果容器 */
.mic-btn .ripple-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    pointer-events: none;
}

/* 新增：波纹圈 */
.mic-btn.listening .ripple {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: rgba(7, 193, 96, 0.4);
    animation: ripple-effect 1.5s ease-out infinite;
}

.mic-btn.listening .ripple:nth-child(2) {
    animation-delay: 0.5s;
}

.mic-btn.listening .ripple:nth-child(3) {
    animation-delay: 1s;
}

@keyframes ripple-effect {
    0% {
        width: 100%;
        height: 100%;
        opacity: 1;
    }
    100% {
        width: 300%;
        height: 300%;
        opacity: 0;
    }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.15);
    }
}

/* 新增：语音波形动画 */
.waveform-visualizer {
    display: flex;
    align-items: flex-end;
    gap: 2px;
    height: 18px;
    margin-right: 6px;
}

.waveform-bar {
    width: 3px;
    background: #07C160;
    animation: waveform 0.6s ease-in-out infinite;
    border-radius: 1.5px;
}

.waveform-bar.listening {
    background: #07C160;
}

.waveform-bar:nth-child(1) { animation-delay: 0s; height: 40%; }
.waveform-bar:nth-child(2) { animation-delay: 0.1s; height: 70%; }
.waveform-bar:nth-child(3) { animation-delay: 0.2s; height: 100%; }
.waveform-bar:nth-child(4) { animation-delay: 0.3s; height: 60%; }
.waveform-bar:nth-child(5) { animation-delay: 0.4s; height: 80%; }

@keyframes waveform {
    0%, 100% {
        transform: scaleY(0.5);
    }
    50% {
        transform: scaleY(1);
    }
}

/* 新增：Toast 提示样式 */
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.toast {
    min-width: 280px;
    max-width: 400px;
    padding: 14px 18px;
    border-radius: 10px;
    background: white;
    color: #1f2937;
    font-size: 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    animation: slide-in 0.3s ease-out;
    backdrop-filter: blur(8px);
    display: flex;
    align-items: flex-start;
    gap: 12px;
    position: relative;
    overflow: hidden;
    border-left: 4px solid;
}

.toast.success {
    border-left-color: #10b981;
    background: linear-gradient(to right, #ecfdf5, white);
}

.toast.error {
    border-left-color: #ef4444;
    background: linear-gradient(to right, #fef2f2, white);
}

.toast.warning {
    border-left-color: #f59e0b;
    background: linear-gradient(to right, #fffbeb, white);
}

.toast.info {
    border-left-color: #3b82f6;
    background: linear-gradient(to right, #eff6ff, white);
}

.toast-icon {
    font-size: 18px;
    flex-shrink: 0;
    margin-top: 1px;
}

.toast-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.toast-message {
    font-weight: 500;
    line-height: 1.5;
}

.toast-description {
    font-size: 12px;
    opacity: 0.8;
    line-height: 1.4;
}

/* 新增：Toast 进度条 */
.toast-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    background: currentColor;
    opacity: 0.3;
    animation: progress-bar 3s linear forwards;
}

.toast.success .toast-progress {
    background: #10b981;
}

.toast.error .toast-progress {
    background: #ef4444;
}

.toast.warning .toast-progress {
    background: #f59e0b;
}

.toast.info .toast-progress {
    background: #3b82f6;
}

@keyframes progress-bar {
    from {
        width: 100%;
    }
    to {
        width: 0%;
    }
}

@keyframes slide-in {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* 新增：语音服务不可用提示横幅 */
.speech-warning-banner {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 12px 24px;
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.4);
    z-index: 9998;
    animation: slide-down 0.5s ease-out;
}

.banner-content {
    display: flex;
    align-items: center;
    gap: 12px;
}

.banner-icon {
    font-size: 20px;
}

.banner-text {
    font-size: 14px;
    font-weight: 500;
}

.retry-btn {
    margin-left: 8px;
    padding: 4px 12px;
    background: rgba(255, 255, 255, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 6px;
    color: white;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.3s;
}

.retry-btn:hover {
    background: rgba(255, 255, 255, 0.5);
}

@keyframes slide-down {
    from {
        transform: translateX(-50%) translateY(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
}

/* 新增：权限引导弹窗样式 */
.permission-guide-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10001;
    animation: fade-in 0.3s ease-out;
    backdrop-filter: blur(4px);
}

.permission-guide-modal {
    background: white;
    border-radius: 16px;
    width: 90%;
    max-width: 480px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: modal-slide-up 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden;
}

.guide-header {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    padding: 24px;
    text-align: center;
}

.guide-icon-wrapper {
    width: 64px;
    height: 64px;
    margin: 0 auto 12px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.guide-icon {
    font-size: 32px;
}

.guide-title {
    color: white;
    font-size: 20px;
    font-weight: 600;
    margin: 0;
}

.guide-body {
    padding: 24px;
}

.guide-text {
    font-size: 15px;
    color: #374151;
    margin-bottom: 20px;
    line-height: 1.6;
    text-align: center;
}

.guide-steps {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
}

.step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #f9fafb;
    border-radius: 8px;
}

.step-number {
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    flex-shrink: 0;
}

.step-text {
    font-size: 14px;
    color: #1f2937;
    font-weight: 500;
}

.guide-tips {
    background: #eff6ff;
    border-radius: 8px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.tip-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #1e40af;
}

.tip-icon {
    font-size: 16px;
}

.tip-text {
    line-height: 1.5;
}

.guide-footer {
    display: flex;
    gap: 12px;
    padding: 16px 24px;
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
}

.guide-btn {
    flex: 1;
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    border: none;
}

.guide-btn-secondary {
    background: white;
    color: #6b7280;
    border: 2px solid #e5e7eb;
}

.guide-btn-secondary:hover {
    background: #f9fafb;
    border-color: #d1d5db;
}

.guide-btn-primary {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.guide-btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

@keyframes fade-in {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes modal-slide-up {
    from {
        transform: translateY(50px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

</style>
