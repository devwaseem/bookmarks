import { $byId } from "@frontend/js/utils";
import AlpineInstance from "alpinejs";

AlpineInstance.data("ModalContainer", () => ({
  closeModal(id: string) {
    $byId(id)?.remove();
  },
}));
