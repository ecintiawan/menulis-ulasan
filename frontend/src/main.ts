import App from '@/App.vue';
import VSkeleton from '@/components/base/VSkeleton.vue';
import '@/styles/app.css';
import { createApp } from 'vue';

const app = createApp(App);
app.component('v-skeleton', VSkeleton);
app.mount('#app');
