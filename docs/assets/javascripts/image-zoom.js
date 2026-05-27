(function () {
  if (window.__imageZoomInitialized) {
    return;
  }

  window.__imageZoomInitialized = true;

  function closeZoom() {
    var overlay = document.querySelector(".image-zoom-overlay");

    if (overlay) {
      overlay.remove();
      document.body.style.overflow = "";
    }
  }

  function openZoom(sourceImage) {
    closeZoom();

    var overlay = document.createElement("div");
    var image = document.createElement("img");

    overlay.className = "image-zoom-overlay";
    image.src = sourceImage.currentSrc || sourceImage.src;
    image.alt = sourceImage.alt || "";

    overlay.appendChild(image);
    document.body.appendChild(overlay);
    document.body.style.overflow = "hidden";
  }

  document.addEventListener("click", function (event) {
    var overlay = event.target.closest(".image-zoom-overlay");

    if (overlay && event.target === overlay) {
      closeZoom();
      return;
    }

    var image = event.target.closest(".md-typeset img");

    if (!image || image.closest("a")) {
      return;
    }

    event.preventDefault();
    openZoom(image);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeZoom();
    }
  });

  if (typeof document$ !== "undefined") {
    document$.subscribe(closeZoom);
  }
})();
