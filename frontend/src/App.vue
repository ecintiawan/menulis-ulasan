<template>
    <div id="nav">
        <router-link to="/">Home</router-link>
    </div>

    <router-view />

    <!-- set progressbar -->
    <vue-progress-bar></vue-progress-bar>
</template>

<script>
import api from '@api/api-axios.js';
export default {
    mounted() {
        this.$Progress.finish();
    },
    created() {
        this.$Progress.start();
        api.interceptors.request.use(config => {
            this.$Progress.start(); // for every request start the progress
            return config;
        });
        api.interceptors.response.use(response => {
            this.$Progress.finish(); // finish when a response is received
            return response;
        });
    }
};
</script>
