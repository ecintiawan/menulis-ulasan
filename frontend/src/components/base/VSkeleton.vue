<script lang="ts">
	import { defineComponent, PropType } from 'vue';

	export default defineComponent({
		name: 'VSkeleton',
		props: {
			height: {
				type: String as PropType<string>,
				default: '15px',
			},
			width: {
				type: String as PropType<string>,
				default: '150px',
			},
			type: {
				type: String as PropType<'rect' | 'circle'>,
				default: 'rect',
			},
			borderRadius: {
				type: String as PropType<string>,
				default: '0px',
			},
		},
		setup() {
			return {};
		},
	});
</script>

<template>
	<div
		class="skeleton"
		:style="{
			width,
			height,
			'border-radius': type === 'rect' ? borderRadius : '9999px',
		}"
	></div>
</template>

<style lang="scss" scoped>
	.skeleton {
		@apply overflow-hidden bg-gray-300;
	}
	.skeleton::after {
		content: '';
		@apply block w-1/2 h-full bg-gradient-to-r from-gray-300 via-gray-200 to-gray-300 animate-skeleton-shimmer;
	}
</style>
