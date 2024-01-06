export function $byId(id: string): HTMLElement | null {
    return document.getElementById(id);
}

export function $query(select: string): HTMLElement | null {
    return document.querySelector(select);
}

export function $queryAll(select: string) {
    return document.querySelectorAll(select);
}

export function openLinkInNewWindow(link: string) {
  window.open(link, '_blank')
}