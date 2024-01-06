import Alpine from 'alpinejs';

Alpine.data('Bookmark', () => ({
    menuOpened: false,

    openMenu() {
        this.menuOpened = true;
    },

    closeMenu() {
        this.menuOpened = false;
    },
}));
