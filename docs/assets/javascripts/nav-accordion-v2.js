(function () {
  function textOf(link) {
    return link ? link.textContent.replace(/\s+/g, " ").trim() : "";
  }

  function makeToggle(label, count, expanded) {
    var button = document.createElement("button");

    button.type = "button";
    button.className = "toc-collapse-toggle";
    button.setAttribute("aria-expanded", expanded ? "true" : "false");
    button.innerHTML = '<span>' + label + '</span><span class="toc-collapse-count">' + count + "</span>";

    return button;
  }

  function groupStepItems(toc) {
    var list = toc.querySelector(".md-nav__list[data-md-component='toc']");

    if (!list || list.dataset.stepsGrouped === "true") {
      return;
    }

    var items = Array.from(list.children).filter(function (item) {
      return item.matches(".md-nav__item");
    });
    var stepItems = items.filter(function (item) {
      return /^Étape\s+\d+\b/i.test(textOf(item.querySelector(":scope > .md-nav__link")));
    });

    if (stepItems.length < 4) {
      return;
    }

    var groupItem = document.createElement("li");
    var nestedList = document.createElement("ul");
    var toggle = makeToggle("Étapes de la page", stepItems.length, true);

    groupItem.className = "md-nav__item toc-collapse-group";
    nestedList.className = "md-nav__list toc-collapse-list";

    stepItems[0].before(groupItem);
    groupItem.appendChild(toggle);
    groupItem.appendChild(nestedList);

    stepItems.forEach(function (item) {
      item.classList.add("toc-collapse-child");
      nestedList.appendChild(item);
    });

    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", expanded ? "false" : "true");
      groupItem.classList.toggle("is-collapsed", expanded);
    });

    list.dataset.stepsGrouped = "true";
  }

  function markLargeToc(toc) {
    var links = toc.querySelectorAll(".md-nav__list[data-md-component='toc'] > .md-nav__item > .md-nav__link");

    if (links.length >= 10) {
      toc.classList.add("md-nav--compact-toc");
    }
  }

  function isIterationLink(link) {
    return /^Itération\s+\d+\b/i.test(textOf(link));
  }

  function setModuleOpen(item, open) {
    var toggle = item.querySelector(":scope > .md-nav__toggle");
    var link = item.querySelector(":scope > .md-nav__link");
    var nav = item.querySelector(":scope > .md-nav");

    if (toggle) {
      toggle.checked = open;
    }

    if (nav) {
      nav.style.display = open ? "block" : "none";
      nav.setAttribute("aria-expanded", open ? "true" : "false");
    }

    if (link) {
      link.setAttribute("aria-expanded", open ? "true" : "false");
    }

    item.classList.toggle("is-open", open);
  }

  function enhanceModuleNav() {
    document.querySelectorAll(".md-nav--primary .md-nav__item--nested").forEach(function (item) {
      var link = item.querySelector(":scope > .md-nav__link");
      var nav = item.querySelector(":scope > .md-nav");

      if (!link || !nav || !isIterationLink(link)) {
        return;
      }

      item.classList.add("module-accordion");
      link.removeAttribute("for");
      link.setAttribute("role", "button");
      link.setAttribute("tabindex", "0");
      link.setAttribute("title", "Ouvrir ou fermer cette itération");

      if (link.dataset.moduleAccordionReady !== "true") {
        link.dataset.moduleAccordionReady = "true";

        link.addEventListener("click", function (event) {
          event.preventDefault();
          event.stopPropagation();
          setModuleOpen(item, !item.classList.contains("is-open"));
        }, true);

        link.addEventListener("keydown", function (event) {
          if (event.key !== "Enter" && event.key !== " ") {
            return;
          }

          event.preventDefault();
          event.stopPropagation();
          setModuleOpen(item, !item.classList.contains("is-open"));
        }, true);
      }

      setModuleOpen(item, item.classList.contains("md-nav__item--active"));
    });
  }

  function enhanceNavigation() {
    document.querySelectorAll(".md-nav--secondary").forEach(function (toc) {
      groupStepItems(toc);
      markLargeToc(toc);
    });

    enhanceModuleNav();
  }

  document.addEventListener("DOMContentLoaded", enhanceNavigation);

  if (typeof document$ !== "undefined") {
    document$.subscribe(enhanceNavigation);
  }
})();
