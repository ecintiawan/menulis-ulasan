<template>
	<div class="skeleton"></div>
</template>

<script lang="ts">
	import { defineComponent } from 'vue';

	export default defineComponent({
		setup() {
			return {};
		},
	});
</script>

<style lang="scss" scoped>
	.skeleton {
		@apply bg-gray-400;
	}
	.skeleton::after {
		@apply block w-1/2 h-full;
	}
</style>
