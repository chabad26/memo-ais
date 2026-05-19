(function () {
  if (window.__mermaidZoomInitialized) {
    return;
  }

  window.__mermaidZoomInitialized = true;

  function fullscreenElement() {
    return document.fullscreenElement || document.webkitFullscreenElement || null;
  }

  function cleanup() {
    document.querySelectorAll(".mermaid-fullscreen, .mermaid-fullscreen-fallback").forEach(function (diagram) {
      diagram.classList.remove("mermaid-fullscreen");
      diagram.classList.remove("mermaid-fullscreen-fallback");
    });
  }

  function exitFallback() {
    document.querySelectorAll(".mermaid-fullscreen-fallback").forEach(function (diagram) {
      diagram.classList.remove("mermaid-fullscreen");
      diagram.classList.remove("mermaid-fullscreen-fallback");
    });
  }

  function openFullscreen(diagram) {
    cleanup();
    diagram.classList.add("mermaid-fullscreen");

    if (diagram.requestFullscreen) {
      diagram.requestFullscreen().catch(function () {
        diagram.classList.add("mermaid-fullscreen-fallback");
      });
      return;
    }

    if (diagram.webkitRequestFullscreen) {
      diagram.webkitRequestFullscreen();
      return;
    }

    diagram.classList.add("mermaid-fullscreen-fallback");
  }

  function markDiagrams() {
    document.querySelectorAll(".mermaid").forEach(function (diagram) {
      diagram.setAttribute("title", "Cliquer pour agrandir");
    });
  }

  document.addEventListener("click", function (event) {
    var diagram = event.target.closest(".mermaid");

    if (!diagram || fullscreenElement() || diagram.classList.contains("mermaid-fullscreen-fallback")) {
      return;
    }

    event.preventDefault();
    openFullscreen(diagram);
  });

  document.addEventListener("fullscreenchange", function () {
    if (!fullscreenElement()) {
      cleanup();
    }
  });

  document.addEventListener("webkitfullscreenchange", function () {
    if (!fullscreenElement()) {
      cleanup();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      exitFallback();
    }
  });

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      cleanup();
      window.setTimeout(markDiagrams, 500);
    });
  } else {
    document.addEventListener("DOMContentLoaded", function () {
      window.setTimeout(markDiagrams, 500);
    });
  }
})();
