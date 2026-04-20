/* ======================
   TERMINAL ANIMATION
====================== */

function sleep(ms){
  return new Promise(r => setTimeout(r, ms));
}

async function copyText(text){
  if (navigator.clipboard && window.isSecureContext){
    await navigator.clipboard.writeText(text);
    return;
  }

  const helper = document.createElement("textarea");
  helper.value = text;
  helper.setAttribute("readonly", "");
  helper.style.position = "absolute";
  helper.style.left = "-9999px";
  document.body.appendChild(helper);
  helper.select();

  const successful = document.execCommand("copy");
  document.body.removeChild(helper);

  if (!successful){
    throw new Error("Copy command failed");
  }
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
  const phoneInput = form ? form.querySelector('input[name="phone"]') : null;
  const submitButton = form ? form.querySelector('button[type="submit"]') : null;

  if (!form || !status) return;

  function setStatus(message, kind){
    status.textContent = message;
    status.style.color = kind === "error" ? "#ff8b8b" : "#9cff9c";
  }

  function clearStatus(){
    status.textContent = "";
    status.style.color = "";
  }

  function isValidPhone(value){
    return /^(\d{9}|\d{12})$/.test(value);
  }

  if (phoneInput){
    phoneInput.addEventListener("input", () => {
      const digitsOnly = phoneInput.value.replace(/\D/g, "").slice(0, 12);
      if (phoneInput.value !== digitsOnly){
        phoneInput.value = digitsOnly;
      }

      if (digitsOnly.length === 0){
        clearStatus();
        return;
      }

      if (digitsOnly.length !== 9 && digitsOnly.length !== 12){
        setStatus("Telefon 9 yoki 12 xonali bo'lishi kerak.", "error");
        return;
      }

      clearStatus();
    });
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (phoneInput && !isValidPhone(phoneInput.value.trim())){
      setStatus("Telefon faqat 9 yoki 12 xonali raqam bo'lishi kerak.", "error");
      phoneInput.focus();
      return;
    }

    clearStatus();

    if (submitButton){
      submitButton.disabled = true;
    }

    setStatus("Sending...", "success");

    try {
      const response = await fetch(form.action || window.location.href, {
        method: "POST",
        body: new FormData(form),
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "Accept": "application/json",
        },
        credentials: "same-origin",
      });

      const data = await response.json();
      setStatus(data.message || "Xabaringiz yuborildi ✅", response.ok ? "success" : "error");

      if (response.ok){
        form.reset();
      }
    } catch (error){
      setStatus("Xabar yuborilmadi. Qayta urinib ko'ring.", "error");
    } finally {
      if (submitButton){
        submitButton.disabled = false;
      }
    }
  });
}

function setupSupportCardCopy(){
  const button = document.getElementById("copyCardButton");
  const status = document.getElementById("copyStatus");

  if (!button || !status) return;

  const successMessage = button.dataset.copySuccess || "Copied";
  const errorMessage = button.dataset.copyError || "Copy failed";

  button.addEventListener("click", async () => {
    const textToCopy = button.dataset.copyText || "";

    if (!textToCopy){
      status.textContent = errorMessage;
      status.className = "copy-status error";
      return;
    }

    try {
      await copyText(textToCopy);
      status.textContent = successMessage;
      status.className = "copy-status success";
    } catch (error){
      status.textContent = errorMessage;
      status.className = "copy-status error";
    }
  });
}


/* ======================
   START
====================== */

document.addEventListener("DOMContentLoaded", () => {
  runTerminal();
  setupSubmitStatus();
  setupSupportCardCopy();
});