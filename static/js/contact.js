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
  const phoneInput = form ? form.querySelector('input[name="phone"]') : null;

  if (!form || !status) return;

  function setPhoneError(message){
    status.textContent = message;
    status.style.color = "#ff8b8b";
  }

  function clearPhoneError(){
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
        clearPhoneError();
        return;
      }

      if (digitsOnly.length !== 9 && digitsOnly.length !== 12){
        setPhoneError("Telefon 9 yoki 12 xonali bo'lishi kerak.");
        return;
      }

      clearPhoneError();
    });
  }

  form.addEventListener("submit", (event) => {
    if (phoneInput && !isValidPhone(phoneInput.value.trim())){
      event.preventDefault();
      setPhoneError("Telefon faqat 9 yoki 12 xonali raqam bo'lishi kerak.");
      phoneInput.focus();
      return;
    }

    clearPhoneError();
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