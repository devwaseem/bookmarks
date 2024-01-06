import Alpine from 'alpinejs';

Alpine.data('AddBookmarkLinkAssist', () => ({
    title: null,
    link: null,
    init() {
        this.link = this.$refs.link.value;
        this.title = this.$refs.title.value;
        console.log(this.link);

        this.$watch('link', (value, oldValue) => {
            console.log(value, oldValue);
            if (value != oldValue && value != '') {
                this.runAssist();
            }
        });

        if (this.link != '') {
            this.runAssist();
        }
    },

    runAssist() {
        this.$dispatch('add_bookmark:assist');
    },
}));
