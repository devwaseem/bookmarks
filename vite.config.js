// const { resolve } = require('path');
// const fg = require('fast-glob');
// import { defineConfig } from 'vite';

import { resolve } from 'path';
import { defineConfig } from 'vite';

const STATIC_SOURCE_DIR = 'frontend/';
const MAIN_TEMPLATES_DIR = 'server/apps/main/templates/main/';

// @ts-ignore
const DIRNAME = __dirname;

export default defineConfig({
    root: resolve(STATIC_SOURCE_DIR),
    base: '/static/', //same as `STATIC_URL` Django setting
    resolve: {
        alias: {
            // Use '@' in urls as a shortcut for './static_source'.
            '@': resolve(STATIC_SOURCE_DIR),
            '@frontend': resolve(STATIC_SOURCE_DIR),
            '@templates': resolve('server/apps/main/templates/main/templates/'),
            '@widgets': resolve('server/apps/main/templates/main/templates/widgets/'),
            '@components': resolve('server/apps/main/templates/main/components/'),
        },
    },
    server: {
        hmr: false,
    },
    build: {
        outDir: './static', // puts the manifest.json in PROJECT_ROOT/static_source/ for Django to collect
        assetsDir: '',
        manifest: true, // adds a manifest.json
        emptyOutDir: true,
        rollupOptions: {
            output: {
                entryFileNames: '[name].[hash].js',
                chunkFileNames: '[name].[hash].js',
                assetFileNames: 'assets/[name].[hash][extname]',
            },
            input: {
                /* The bundle's entry point(s).  If you provide an array of entry points or an object mapping names to entry points, they will be bundled to separate output chunks. */
                styles: resolve(__dirname, STATIC_SOURCE_DIR + 'css/styles.js'),
                // JS
                main: resolve(__dirname, STATIC_SOURCE_DIR + 'js/main.ts'),
                // Bunlde by Pages
                error_page: resolve(DIRNAME, STATIC_SOURCE_DIR + 'js/error_page.ts'),

                explore: resolve(DIRNAME, STATIC_SOURCE_DIR + 'js/pages/explore.ts'),
                add_bookmark: resolve(DIRNAME, STATIC_SOURCE_DIR + 'js/pages/add_bookmark.ts'),
            },
        },
    },
    plugins: [],
});
