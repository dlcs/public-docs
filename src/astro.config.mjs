// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'IIIF Cloud Services',
			logo: {
				src: './src/assets/cloud-services.svg',
				replacesTitle: true
			},
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/dlcs/protagonist' }],
			sidebar: [
				{
					label: 'Usage',					
					autogenerate: { directory: 'usage' }
					// items: [{ label: 'Example Guide', slug: 'guides/example' },],
				},
				{
					label: 'The Portal',
					autogenerate: { directory: 'portal' }
				},
				{
					label: 'The API',
					autogenerate: { directory: 'api-doc' },
				},
			],
		}),
	],
});
