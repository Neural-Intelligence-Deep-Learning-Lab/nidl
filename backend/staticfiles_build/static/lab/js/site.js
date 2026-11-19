(() => {
  const root = document.documentElement;
  const theme = document.querySelector(".theme-button");
  const menu = document.querySelector(".menu-button");
  const links = document.querySelector(".nav-links");
  theme?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    localStorage.setItem("nidl-theme", next);
  });
  menu?.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
  });
  const search = document.querySelector("#publication-search");
  const year = document.querySelector("#publication-year");
  const sort = document.querySelector("#publication-sort");
  const list = document.querySelector("#publication-list");
  const noResults = document.querySelector("#no-results");
  const publications = list ? [...list.querySelectorAll(".searchable")] : [];

  const sortPublications = () => {
    if (!list || !sort) return;
    const direction = sort.value === "oldest" ? 1 : -1;
    const sorted = [...publications].sort((a, b) => {
      if (sort.value === "title-asc" || sort.value === "title-desc") {
        const titleOrder = a.dataset.title.localeCompare(b.dataset.title);
        return sort.value === "title-asc" ? titleOrder : -titleOrder;
      }
      return direction * (Number(a.dataset.year) - Number(b.dataset.year));
    });
    sorted.forEach((publication) => list.appendChild(publication));
  };

  const filter = () => {
    if (!search || !year || !noResults) return;
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    publications.forEach((item) => {
      const searchableText = (item.dataset.search || item.textContent).toLocaleLowerCase();
      const matches = searchableText.includes(query) &&
        (year.value === "all" || item.dataset.year === year.value);
      item.hidden = !matches;
      if (matches) visible += 1;
    });
    noResults.hidden = visible !== 0;
  };
  search?.addEventListener("input", filter);
  search?.addEventListener("search", filter);
  year?.addEventListener("change", filter);
  sort?.addEventListener("change", () => {
    sortPublications();
    filter();
  });
  sortPublications();
  filter();
})();
