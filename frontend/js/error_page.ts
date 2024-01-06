import AlpineInstance from "alpinejs";

AlpineInstance.data("ErrorPageComponent", () => ({
  goBack() {
    window.history.go(-1);
  },
  get canGoBack() {
    return window.history.length > 1;
  },
}));
