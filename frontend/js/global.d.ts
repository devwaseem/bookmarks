import { Alpine as AlpineType } from "alpinejs";

declare global {
    interface Window {
        Alpine: AlpineType;
        $byId: Function;
    }
    const Alpine: AlpineType;
}
