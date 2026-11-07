/* ==========================================================================
   ACTRACE | main.js
   Skrip global (vanilla JS). Setiap fitur aktif lewat atribut data-* sehingga
   aman dimuat di halaman mana pun dan bisa dipakai ulang di fase berikutnya.

   - [data-toggle-password]  : tombol tampil/sembunyi kata sandi
   - form[data-loading-form] : status loading saat submit + cegah kirim ganda
   - [data-autofocus]        : fokus awal ke input kosong pertama (perangkat mouse)
   - [data-year]             : tahun berjalan untuk hak cipta
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Tahun hak cipta ---------- */
  function initYear() {
    var year = String(new Date().getFullYear());
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = year;
    });
  }

  /* ---------- Tampil/sembunyi kata sandi ---------- */
  function initPasswordToggle() {
    document.querySelectorAll('[data-toggle-password]').forEach(function (button) {
      var input = document.getElementById(button.getAttribute('aria-controls'));
      if (!input) { return; }

      button.addEventListener('click', function () {
        var reveal = input.type === 'password';
        input.type = reveal ? 'text' : 'password';
        button.setAttribute('aria-pressed', String(reveal));
        button.setAttribute('aria-label', reveal ? 'Hide password' : 'Show password');
      });
    });
  }

  /* ---------- Status loading saat submit ---------- */
  function setLoading(form, isLoading) {
    var button = form.querySelector('button[type="submit"]');
    if (!button) { return; }

    var label = button.querySelector('.btn__label');
    if (label && !label.dataset.defaultText) {
      label.dataset.defaultText = label.textContent;
    }

    form.dataset.submitting = String(isLoading);
    form.setAttribute('aria-busy', String(isLoading));
    button.classList.toggle('is-loading', isLoading);
    button.setAttribute('aria-disabled', String(isLoading));

    if (label) {
      label.textContent = isLoading
        ? (button.dataset.loadingLabel || label.dataset.defaultText)
        : label.dataset.defaultText;
    }
  }

  function initLoadingForms() {
    document.querySelectorAll('form[data-loading-form]').forEach(function (form) {
      form.addEventListener('submit', function (event) {
        // Cegah kirim ganda; tombol tidak di-disable agar data form tetap utuh.
        if (form.dataset.submitting === 'true') {
          event.preventDefault();
          return;
        }
        setLoading(form, true);
      });
    });

    // Tombol Back (bfcache) bisa menampilkan halaman dalam keadaan loading.
    window.addEventListener('pageshow', function (event) {
      if (!event.persisted) { return; }
      document.querySelectorAll('form[data-loading-form]').forEach(function (form) {
        setLoading(form, false);
      });
    });
  }

  /* ---------- Fokus awal ---------- */
  function initAutofocus() {
    // Di layar sentuh, fokus otomatis memunculkan keyboard dan menutupi form.
    if (!window.matchMedia || !window.matchMedia('(pointer: fine)').matches) { return; }

    var fields = document.querySelectorAll('[data-autofocus]');
    for (var i = 0; i < fields.length; i += 1) {
      if (!fields[i].value) {
        fields[i].focus();
        return;
      }
    }
  }

  function init() {
    initYear();
    initPasswordToggle();
    initLoadingForms();
    initAutofocus();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
