(function () {
  function fullscreenElement() {
    return document.fullscreenElement || document.webkitFullscreenElement;
  }

  function openFullscreen(element) {
    element.classList.add("mermaid-fullscreen");

    if (element.requestFullscreen) {
      element.requestFullscreen();
      return;
    }

    if (element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen();
      return;
    }

    element.classList.toggle("mermaid-fullscreen-fallback");
  }

  function closeFallback() {
    document.querySelectorAll(".mermaid-fullscreen-fallback").forEach(function (diagram) {
      diagram.classList.remove("mermaid-fullscreen");
      diagram.classList.remove("mermaid-fullscreen-fallback");
    });
  }

  function bindMermaidZoom() {
    document.querySelectorAll(".mermaid").forEach(function (diagram) {
      if (diagram.dataset.zoomReady === "true") {
        return;
      }

      diagram.dataset.zoomReady = "true";
      diagram.setAttribute("title", "Cliquer pour agrandir");
      diagram.addEventListener("click", function () {
        if (fullscreenElement() || diagram.classList.contains("mermaid-fullscreen-fallback")) {
          return;
        }

        openFullscreen(diagram);
      });
    });
  }

  document.addEventListener("fullscreenchange", function () {
    if (!fullscreenElement()) {
      document.querySelectorAll(".mermaid-fullscreen").forEach(function (diagram) {
        diagram.classList.remove("mermaid-fullscreen");
      });
    }
  });

  document.addEventListener("webkitfullscreenchange", function () {
    if (!fullscreenElement()) {
      document.querySelectorAll(".mermaid-fullscreen").forEach(function (diagram) {
        diagram.classList.remove("mermaid-fullscreen");
      });
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeFallback();
    }
  });

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      window.setTimeout(bindMermaidZoom, 500);
    });
  } else {
    document.addEventListener("DOMContentLoaded", function () {
      window.setTimeout(bindMermaidZoom, 500);
    });
  }
})();
