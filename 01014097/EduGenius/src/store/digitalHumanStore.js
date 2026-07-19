import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useDigitalHumanStore = defineStore('digitalHuman', () => {
    const isActive = ref(false);
    const isVisible = ref(false);
    const isMinimized = ref(false);
    const selectedText = ref('');
    const textToSpeak = ref('');

    function triggerFromSelection(text) {
        selectedText.value = text;
        isActive.value = true;
        isVisible.value = true;
        isMinimized.value = false;
    }

    function expand() {
        isActive.value = true;
        isVisible.value = true;
        isMinimized.value = false;
    }

    function minimize() {
        isMinimized.value = true;
    }

    function close() {
        isActive.value = false;
        isVisible.value = false;
        isMinimized.value = false;
        selectedText.value = '';
    }

    function clearSelection() {
        selectedText.value = '';
    }

    function setTextToSpeak(text) {
        textToSpeak.value = text;
    }

    return {
        isActive,
        isVisible,
        isMinimized,
        selectedText,
        textToSpeak,
        triggerFromSelection,
        expand,
        minimize,
        close,
        clearSelection,
        setTextToSpeak
    };
});
