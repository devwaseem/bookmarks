// import 'vite/modulepreload-polyfill'

import collapse from '@alpinejs/collapse';
import focus from '@alpinejs/focus';
import mask from '@alpinejs/mask';

import Tooltip from '@ryangjchandler/alpine-tooltip';
import 'tippy.js/dist/tippy.css'; // Need this for alpine Tooltip

import Alpine from 'alpinejs';
import { $byId, openLinkInNewWindow } from './utils';

// import "htmx.org"; <- HTMX doesn't support bundling properly, so include htmx via script before this file
import 'htmx.org/dist/ext/alpine-morph.js';
import 'htmx.org/dist/ext/loading-states.js';
import 'htmx.org/dist/ext/preload.js';
import 'htmx.org/dist/ext/morphdom-swap';

import Toast, { ToastType } from '@components/toast/toast';
import './components';
import './index.ts';

if (import.meta.env.MODE != 'production') {
    //@ts-ignore
    await import('htmx.org/dist/ext/debug.js');
}

// @ts-expect-error
const { htmx } = window;

// HTMX Configuration (https://htmx.org/docs/#config)
htmx.defineExtension('get-csrf', {
    onEvent(name: string, evt: any) {
        if (name === 'htmx:configRequest') {
            evt.detail.headers['X-CSRFToken'] = getCsrfToken();
        }
    },
});

function getCsrfToken(): string {
    return document.body.dataset.csrfToken!;
    // return JSON.parse($byId('csrf_token')!.textContent!);
}

document.addEventListener('htmx:historyRestore', () => {
    removeOrphanElementsGeneratedByAlpineJs();
});

function removeOrphanElementsGeneratedByAlpineJs() {
    document.querySelectorAll('[x-from-template]').forEach((e) => e.remove());
}

// document.addEventListener('htmx:afterSettle', (event: Event) => {
// @ts-ignore
// debugger;
// Alpine.initTree(event.target);
// });

document.addEventListener('htmx:sendError', () => {
    const message =
        "We're sorry, it looks like there was a problem connecting to the network or server. Please check your internet connection and try again, or wait a few minutes and try again later.";
    const toast = new Toast(message, ToastType.ERROR);
    toast.show(5000);
});

document.addEventListener('htmx:beforeOnLoad', function (event) {
    //@ts-ignore
    const xhr = event.detail.xhr;
    if (xhr.status >= 400 && xhr.status < 599) {
        event.stopPropagation(); // Tell htmx not to process these requests
        let message = 'Something went wrong! Please try again!';
        if (xhr.status == 429) {
            message = 'Too Many Requests. Please wait and try again later.';
        }

        const toast = new Toast(message, ToastType.ERROR);
        toast.show(5000);
    }
});

document.addEventListener('alert', (event: Event) => {
    // @ts-ignore
    const message = event?.detail?.message;
    if (message) {
        alert(message);
    }
});

document.addEventListener('toast', (event) => {
    // @ts-ignore
    const message = event?.detail?.message;
    // @ts-ignore
    const type = event?.detail?.type;
    // @ts-ignore
    const duration = event?.detail?.duration || 5000;
    if (message && type) {
        const toast = new Toast(message, type);
        toast.show(duration);
    }
});

window.Alpine = Alpine;
window.$byId = $byId;

//@ts-ignore
window.openLinkInNewWindow = openLinkInNewWindow;

Alpine.plugin(focus);
Alpine.plugin(collapse);
Alpine.plugin(mask);
Alpine.plugin(Tooltip);
Alpine.start();
