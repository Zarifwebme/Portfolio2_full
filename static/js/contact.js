console.log("contact.js loaded ✅");

/* ======================
   TERMINAL ANIMATION
====================== */

function sleep(ms){
  return new Promise(r => setTimeout(r, ms));
}

async function typeLine(el, text){
  for (let i = 0; i < text.length; i++){
    el.textContent += text[i];
    await sleep(18 + Math.random() * 35);
  }
  el.textContent += "\n";
}

async function runTerminal(){
  const out = document.getElementById("termOut");
  if (!out) return;

  const lines = [
    "$ system init",
    "portfolio contact module loaded ✓",
    "",
    "$ checking security",
    "csrf protection ✓",
    "input validation ✓",
    "",
    "$ server status",
    "django backend online",
    "telegram api connected",
    "",
    "$ awaiting user message..."
  ];

  while(true){
    out.textContent = "";

    for(const l of lines){
      await typeLine(out, l);
      await sleep(250);
    }

    await sleep(1200);

    // ozgina o‘chirish effekt
    const keep = out.textContent.slice(0, 90);
    out.textContent = keep;

    await sleep(400);
  }
}


/* ======================
   OPTIONAL: submit vaqtida loading
   (backendni blok qilmaydi)
====================== */

function setupSubmitStatus(){
  const form = document.getElementById("contactForm");
  const status = document.getElementById("formStatus");

  if (!form || !status) return;

  form.addEventListener("submit", () => {
    status.textContent = "Sending...";
  });
}


/* ======================
   START
====================== */

document.addEventListener("DOMContentLoaded", () => {
  runTerminal();
  setupSubmitStatus();
});