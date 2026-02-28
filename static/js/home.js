console.log("home.js loaded");

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function typeText(el, text, speedMin = 18, speedMax = 45) {
  for (let i = 0; i < text.length; i++) {
    el.textContent += text[i];
    const jitter = speedMin + Math.random() * (speedMax - speedMin);
    await sleep(jitter);
  }
}

async function runTyping() {
  const target = document.getElementById("typeTarget");
  const dataEl = document.getElementById("typeData");
  if (!target || !dataEl) return;

  let lines = [];
  try {
    lines = JSON.parse(dataEl.getAttribute("data-lines") || "[]");
  } catch {
    lines = [];
  }

  while (true) {
    target.textContent = "";
    for (const line of lines) {
      await typeText(target, "$ " + line);
      await sleep(450);
      target.textContent += "\n";
      await sleep(120);
    }
    await sleep(900);

    // Oxiridan ozgina o‘chirib, qayta yozish effekt (sodda)
    const full = target.textContent;
    for (let i = 0; i < Math.min(80, full.length); i++) {
      target.textContent = target.textContent.slice(0, -1);
      await sleep(12);
    }
    await sleep(400);
  }
}

document.addEventListener("DOMContentLoaded", runTyping);