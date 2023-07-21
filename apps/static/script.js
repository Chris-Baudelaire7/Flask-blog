"use strict";

const alert = document.querySelector(".alert");

(function vanishAlert() {
  if (!alert.classList.contains("alert-danger")) {
    setTimeout(() => {
      alert.style.display = "none";
    }, 7000);
  }
})();
