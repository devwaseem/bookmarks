import { $byId } from '@frontend/js/utils';
import './toast.scss';

export enum ToastType {
    INFO = 'INFO',
    WARNING = 'WARNING',
    ERROR = 'ERROR',
    SUCCESS = 'SUCCESS',
}

const toastContainer = $byId('waak-toast-container');

const toastTypeClasses = {
    infoSimple: 'waak-toast-info-simple',
    warningSimple: 'waak-toast-warning-simple',
    successSimple: 'waak-toast-success-simple',
    errorSimple: 'waak-toast-error-simple',
};

const toastIds = {
    simple: 'waak-toast-simple',
};

class Toast {
    private message: string;
    private type: ToastType;
    private template: HTMLElement | null = null;

    constructor(message: string, type: ToastType = ToastType.INFO) {
        this.message = message;
        this.type = type;
    }

    public show(duration: number = 0) {
        //@ts-ignore
        const template = $byId(toastIds.simple)!.content.firstElementChild.cloneNode(true);
        this.template = template;
        toastContainer?.appendChild(template);

        const messageNode = template.querySelector('.waak-toast-message');
        messageNode.textContent = this.message;

        switch (this.type) {
            case ToastType.INFO: {
                template.classList.add(toastTypeClasses.infoSimple);
                break;
            }
            case ToastType.ERROR: {
                template.classList.add(toastTypeClasses.errorSimple);
                break;
            }
            case ToastType.WARNING: {
                template.classList.add(toastTypeClasses.warningSimple);
                break;
            }
            case ToastType.SUCCESS: {
                template.classList.add(toastTypeClasses.successSimple);
                break;
            }
        }

        setTimeout(() => {
            template.classList.add('waak-toast-show');
        }, 0);

        template.querySelector('.waak-toast-close-button').addEventListener('click', () => {
            this.closeToast();
        });

        if (duration > 0) {
            setTimeout(() => {
                this.closeToast();
            }, duration);
            const progressBar = document.createElement('div');
            template.appendChild(progressBar);
            progressBar.classList.add('waak-toast-progress-bar');
            progressBar.animate([{ width: '100%' }, { width: '0%' }], {
                duration: duration,
            });
        }
    }

    public closeToast() {
        this.template!.classList.remove('waak-toast-show');
        setTimeout(() => {
            this.template!.remove();
        }, 600);
    }
}

export default Toast;
