import { createApp } from 'vue';
import App from './App.vue';
import './styles/app.css';
import VSkeleton from '@/components/base/VSkeleton.vue';
const app = createApp(App);
app.component('v-skeleton', VSkeleton);
app.mount('#app');
