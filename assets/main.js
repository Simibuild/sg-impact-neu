document.addEventListener("DOMContentLoaded", () => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header: Schatten beim Scrollen
  const header = document.querySelector("header.site");
  const onScroll = () => header && header.classList.toggle("scrolled", window.scrollY > 10);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobiles Menü
  const burger = document.querySelector(".burger");
  const navLinks = document.querySelector(".nav-links");
  if (burger && navLinks) {
    burger.addEventListener("click", () => {
      const open = navLinks.classList.toggle("open");
      burger.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", String(open));
    });
    navLinks.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        navLinks.classList.remove("open");
        burger.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      })
    );
  }

  // Reveal beim Scrollen
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        }),
      { threshold: 0.12 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }

  // Scroll-Showcase: Schritte folgen dem Scrollweg
  const wrap = document.querySelector(".showcase-wrap");
  if (wrap) {
    const steps = [...wrap.querySelectorAll(".sc-step")];
    const slides = [...wrap.querySelectorAll(".slide")];
    const bar = wrap.querySelector(".sc-progress span");
    const isStatic = () => reduceMotion || window.matchMedia("(max-width: 1000px)").matches;
    const update = () => {
      if (isStatic()) {
        steps.forEach((s) => s.classList.add("active"));
        return;
      }
      const rect = wrap.getBoundingClientRect();
      const total = wrap.offsetHeight - window.innerHeight;
      const p = Math.min(Math.max(-rect.top / total, 0), 0.999);
      const i = Math.floor(p * steps.length);
      steps.forEach((s, k) => s.classList.toggle("active", k === i));
      slides.forEach((s, k) => s.classList.toggle("active", k === i));
      if (bar) bar.style.width = p * 100 + "%";
    };
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // Checkliste: Sichtbarkeit
  const check = document.querySelector("[data-check]");
  if (check) {
    const boxes = [...check.querySelectorAll(".check-input")];
    const result = document.getElementById("r-check");
    const update = () => {
      const n = boxes.filter((b) => b.checked).length;
      let text;
      if (n === 0) text = "Hake an, was zutrifft.";
      else if (n <= 2) text = n + " von " + boxes.length + ": Da ist viel Luft nach oben. Im Erstgespräch zeige ich dir die wichtigsten Hebel.";
      else if (n <= 4) text = n + " von " + boxes.length + ": Eine gute Basis, einige Hebel sind noch offen.";
      else text = n + " von " + boxes.length + ": Sehr solide Grundlage. Wir schauen gemeinsam, wo du noch gewinnst.";
      result.textContent = text;
    };
    boxes.forEach((b) => b.addEventListener("change", update));
    update();
  }

  // Kontaktformular: öffnet das E-Mail-Programm mit vorausgefüllter Nachricht (kein Server nötig)
  const form = document.querySelector("form.form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const v = (name) => form.elements[name].value.trim();
      const lines = ["Name: " + v("name"), "E-Mail: " + v("email")];
      if (v("phone")) lines.push("Telefon: " + v("phone"));
      if (v("betrieb")) lines.push("Betrieb: " + v("betrieb"));
      if (v("ziel")) lines.push("Ziel: " + v("ziel"));
      lines.push("", v("message"));
      const subject = encodeURIComponent("Anfrage über sg-impact.de");
      const body = encodeURIComponent(lines.join("\n"));
      window.location.href = "mailto:" + form.dataset.mail + "?subject=" + subject + "&body=" + body;
    });
  }
});
