import Alpine from 'alpinejs';

Alpine.data('AddBookmarkLinkAssist', () => ({
  title: null,
  link: null,
  init() {
    //@ts-ignore
    this.link = this.$refs.link.value;
    //@ts-ignore
    this.title = this.$refs.title.value;

    this.$watch('link', (value, oldValue) => {
      console.log(value, oldValue);
      if (value != oldValue && value != '') {
        this.runAssist();
      }
    });

    setTimeout(() => {
      if (this.link != '') {
        this.runAssist();
      }

    }, 100)
  },

  runAssist() {
    this.$dispatch('add_bookmark:assist');
  },
}));
