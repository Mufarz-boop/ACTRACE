
"use strict";

/* ==========================================
   ACTRACE - ERROR PAGE INTERACTIONS
   Shared script: 403, 404, 500
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    // Go back to previous page
    const backButton = document.querySelector("[data-go-back]");

    if (backButton) {
        backButton.addEventListener("click", () => {

            if (window.history.length > 1) {
                window.history.back();
            } else {
                window.location.assign("/");
            }

        });
    }


    // Reload current page
    const reloadButton = document.querySelector("[data-reload]");

    if (reloadButton) {
        reloadButton.addEventListener("click", () => {
            window.location.reload();
        });
    }

});
