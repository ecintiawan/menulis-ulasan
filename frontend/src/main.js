import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router';
import store from '@/store';
import '@style/tailwind.css';
import VueProgressBar from '@aacassandra/vue3-progressbar';


const options = {
    color: '#bffaf3',
    failedColor: '#874b4b',
    thickness: '2px',
    transition: {
        speed: '0.5s',
        opacity: '0.6s',
        termination: 300
    },
    autoRevert: true,
    location: 'top',
    inverse: false
};

const app = createApp(App);
app.use(store)
    .use(router)
    .use(VueProgressBar, options)
    .mount('#app');
