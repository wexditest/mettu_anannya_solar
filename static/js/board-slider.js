(() => {
  const carousel = document.querySelector("[data-board-carousel]");
  if (!carousel) return;

  const track = carousel.querySelector("[data-board-track]");
  const slides = Array.from(carousel.querySelectorAll("[data-board-slide]"));
  const status = carousel.querySelector("[data-board-status]");
  const previous = carousel.querySelector("[data-board-previous]");
  const next = carousel.querySelector("[data-board-next]");
  const toggle = carousel.querySelector("[data-board-toggle]");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  if (!track || !status || !previous || !next || !toggle || slides.length < 2) {
    return;
  }

  let activeIndex = 0;
  let userPaused = reducedMotion.matches;
  let interactionPaused = false;
  let inViewport = false;
  let timer;

  const updateSlide = () => {
    track.style.transform = `translateX(-${activeIndex * 100}%)`;
    slides.forEach((slide, index) => {
      const active = index === activeIndex;
      slide.setAttribute("aria-hidden", String(!active));
      slide.inert = !active;
    });
    status.textContent = `${activeIndex + 1} / ${slides.length}`;
  };

  const updateTimer = () => {
    window.clearInterval(timer);
    toggle.disabled = reducedMotion.matches;
    toggle.textContent = reducedMotion.matches
      ? "Auto-play off"
      : userPaused
        ? "Play slideshow"
        : "Pause slideshow";
    toggle.setAttribute("aria-pressed", String(userPaused));

    if (!userPaused && !interactionPaused && inViewport && !reducedMotion.matches) {
      timer = window.setInterval(() => {
        activeIndex = (activeIndex + 1) % slides.length;
        updateSlide();
      }, 6000);
    }
  };

  const showSlide = (index) => {
    activeIndex = (index + slides.length) % slides.length;
    updateSlide();
    updateTimer();
  };

  previous.addEventListener("click", () => showSlide(activeIndex - 1));
  next.addEventListener("click", () => showSlide(activeIndex + 1));
  toggle.addEventListener("click", () => {
    userPaused = !userPaused;
    updateTimer();
  });

  carousel.addEventListener("mouseenter", () => {
    interactionPaused = true;
    updateTimer();
  });
  carousel.addEventListener("mouseleave", () => {
    interactionPaused = false;
    updateTimer();
  });
  carousel.addEventListener("focusin", () => {
    interactionPaused = true;
    updateTimer();
  });
  carousel.addEventListener("focusout", (event) => {
    if (!carousel.contains(event.relatedTarget)) {
      interactionPaused = false;
      updateTimer();
    }
  });

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      inViewport = entries.some((entry) => entry.isIntersecting);
      updateTimer();
    }, { threshold: 0.35 });
    observer.observe(carousel);
  } else {
    inViewport = true;
  }

  updateSlide();
  updateTimer();
})();
