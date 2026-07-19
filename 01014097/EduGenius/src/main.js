import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

import 'primeflex/primeflex.css';
import { createGtm } from '@gtm-support/vue-gtm';

import Aura from '@primevue/themes/aura';
import PrimeVue from 'primevue/config';

import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';

import uploader from 'vue-simple-uploader';
import '@/assets/styles.scss';
import '@/assets/tailwind.css';
import Textarea from 'primevue/textarea';


const app = createApp(App);
const pinia = createPinia();

app.component('Textarea', Textarea);
app.use(pinia);
app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
});

app.use(ToastService);
app.use(ConfirmationService);
app.use(uploader);

app.mount('#app');
