document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-pdf-library]").forEach((library) => {
    const frame = library.querySelector("[data-pdf-frame]");
    const title = library.querySelector("#pdf-viewer-title");
    const openLink = library.querySelector("[data-pdf-open]");
    const downloadLink = library.querySelector("[download]");
    const items = library.querySelectorAll("[data-pdf-src]");

    if (!frame || !title || !openLink || !items.length) {
      return;
    }

    items.forEach((item) => {
      item.addEventListener("click", () => {
        const src = item.dataset.pdfSrc;
        const label = item.dataset.pdfTitle || item.textContent.trim();

        if (!src) {
          return;
        }

        frame.src = src;
        title.textContent = label;
        openLink.href = src;

        if (downloadLink) {
          downloadLink.href = src;
        }

        items.forEach((entry) => entry.classList.remove("is-active"));
        item.classList.add("is-active");
      });
    });
  });
});
