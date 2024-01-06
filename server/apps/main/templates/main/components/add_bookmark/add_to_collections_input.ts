import { $byId } from '@frontend/js/utils';
import Alpine from 'alpinejs';

Alpine.data('AddToCollectionsInput', () => ({
    collectionSearchInput: '',
    isTagSearchFocused: false,
    existingCollections: Array<string>(),
    init() {
        this.$watch('existingCollections', () => {
            const collections_input = $byId('id_collections');
            if (collections_input) {
                collections_input.value = this.existingCollections.join(',');
            }
        });
    },
    addTag(tag: string) {
        if (!tag) {
            return;
        }
        if (this.existingCollections.includes(tag)) {
            // this.removeTag(tag);
            return;
        }
        this.existingCollections.push(tag);
        this.collectionSearchInput = '';
    },
    removeTag(tag: string) {
        if (!tag) {
            return;
        }
        this.existingCollections = this.existingCollections.filter((value) => value != tag);
    },
    onCollectionSearchInputFocused() {
        this.isTagSearchFocused = true;
    },
    onCollectionSearchInputBlurred() {
        this.isTagSearchFocused = false;
    },
    get shouldShowResults() {
        return this.isTagSearchFocused && this.collectionSearchInput.length > 1;
    },
    doesTagExist(tag: string) {
        return this.existingCollections.includes(tag);
    },
}));
