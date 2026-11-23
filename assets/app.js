// Komodo & Ko — Terms & Conditions signing page logic
// Handles the guest signature pad, full-form validation, and PDF export.

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", init);

  var REQUIRED_FIELD_IDS = ["resName", "resEmail", "resId", "resBoat", "resDate", "resRoom"];

  function init() {
    var canvas = document.getElementById("guestSignatureCanvas");
    if (!canvas) return;

    var wrap = canvas.closest(".sig-canvas-wrap");
    var placeholder = wrap ? wrap.querySelector(".sig-placeholder") : null;
    var pad = new window.SignaturePad(canvas, {
      backgroundColor: "rgba(255,255,255,0)",
      penColor: "#1c2a19",
    });

    function resizeCanvas() {
      var data = pad.isEmpty() ? null : pad.toData();
      var ratio = Math.max(window.devicePixelRatio || 1, 1);
      canvas.width = canvas.offsetWidth * ratio;
      canvas.height = canvas.offsetHeight * ratio;
      canvas.getContext("2d").scale(ratio, ratio);
      pad.clear();
      if (data) pad.fromData(data);
      togglePlaceholder();
    }

    function togglePlaceholder() {
      if (placeholder) placeholder.style.display = pad.isEmpty() ? "flex" : "none";
    }

    window.addEventListener("resize", debounce(resizeCanvas, 200));
    resizeCanvas();

    pad.addEventListener("endStroke", function () {
      togglePlaceholder();
      if (wrap) wrap.classList.remove("field-missing");
      validateForm();
    });

    var clearBtn = document.getElementById("clearSignature");
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        pad.clear();
        togglePlaceholder();
        validateForm();
      });
    }

    // Auto-fill today's date on both sides.
    var today = new Date();
    var dateStr = today.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
    var guestDateEl = document.getElementById("guestSignDate");
    var companyDateEl = document.getElementById("companySignDate");
    if (guestDateEl) guestDateEl.textContent = dateStr;
    if (companyDateEl) companyDateEl.textContent = dateStr;

    // Mirror the reservation-form name into the signature name field.
    var resName = document.getElementById("resName");
    var sigName = document.getElementById("guestSignName");
    if (resName && sigName) {
      resName.addEventListener("input", function () {
        if (!sigName.dataset.touched) sigName.value = resName.value;
        clearMissing(resName);
        validateForm();
      });
      sigName.addEventListener("input", function () {
        sigName.dataset.touched = "1";
        clearMissing(sigName);
        validateForm();
      });
    }

    REQUIRED_FIELD_IDS.forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      var evt = el.tagName === "SELECT" ? "change" : "input";
      el.addEventListener(evt, function () {
        clearMissing(el);
        validateForm();
      });
    });

    var agreeBox = document.getElementById("agreeCheckbox");
    var agreeWrap = document.querySelector(".agree-box");
    if (agreeBox) {
      agreeBox.addEventListener("change", function () {
        if (agreeWrap) agreeWrap.classList.remove("field-missing");
        validateForm();
      });
    }

    var downloadBtn = document.getElementById("downloadPdfBtn");
    var statusMsg = document.getElementById("statusMsg");

    function clearMissing(el) {
      el.classList.remove("field-missing");
    }

    function fieldLabel(id) {
      var labels = {
        resName: "your name",
        resEmail: "your email",
        resId: "your NIK / passport number",
        resBoat: "the boat name",
        resDate: "the date of travel",
        resRoom: "the room type",
      };
      return labels[id] || id;
    }

    function validateForm() {
      var missingFields = [];
      REQUIRED_FIELD_IDS.forEach(function (id) {
        var el = document.getElementById(id);
        if (el && !el.value.trim()) missingFields.push(id);
      });

      var nameOk = sigName && sigName.value.trim().length > 1;
      var agreeOk = agreeBox && agreeBox.checked;
      var sigOk = !pad.isEmpty();
      var ready = missingFields.length === 0 && nameOk && agreeOk && sigOk;

      if (downloadBtn) downloadBtn.disabled = !ready;
      return { ready: ready, missingFields: missingFields, nameOk: nameOk, agreeOk: agreeOk, sigOk: sigOk };
    }

    validateForm();

    if (downloadBtn) {
      downloadBtn.addEventListener("click", function () {
        var v = validateForm();
        if (!v.ready) {
          var missing = v.missingFields.map(fieldLabel);
          if (!v.nameOk) missing.push("your name on the signature line");
          if (!v.agreeOk) missing.push("the agreement checkbox");
          if (!v.sigOk) missing.push("your signature");

          v.missingFields.forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.classList.add("field-missing");
          });
          if (!v.nameOk && sigName) sigName.classList.add("field-missing");
          if (!v.agreeOk && agreeWrap) agreeWrap.classList.add("field-missing");
          if (!v.sigOk && wrap) wrap.classList.add("field-missing");

          setStatus("Please complete: " + missing.join(", ") + ".", "err");

          var firstMissingEl =
            (v.missingFields[0] && document.getElementById(v.missingFields[0])) ||
            (!v.nameOk && sigName) ||
            (!v.agreeOk && agreeWrap) ||
            (!v.sigOk && wrap);
          if (firstMissingEl && firstMissingEl.scrollIntoView) {
            firstMissingEl.scrollIntoView({ behavior: "smooth", block: "center" });
          }
          return;
        }
        exportPdf(canvas, pad);
      });
    }

    function setStatus(msg, kind) {
      if (!statusMsg) return;
      statusMsg.textContent = msg;
      statusMsg.className = "status-msg" + (kind ? " " + kind : "");
    }

    // Fields whose live <input>/<select> value should be baked into plain
    // text before capture — html2canvas renders native form controls
    // inconsistently across browsers, so this guarantees the guest's
    // answers always show up in the exported PDF.
    var SNAPSHOT_FIELD_IDS = ["resName", "resEmail", "resId", "resBoat", "resDate", "resRoom", "resDestination"];

    function fieldDisplayValue(el) {
      if (el.tagName === "SELECT") {
        return el.options[el.selectedIndex] ? el.options[el.selectedIndex].text : "";
      }
      if (el.type === "date" && el.value) {
        var d = new Date(el.value + "T00:00:00");
        if (!isNaN(d.getTime())) {
          return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
        }
      }
      return el.value;
    }

    function bakeFormForCapture() {
      var restoreOps = [];

      SNAPSHOT_FIELD_IDS.forEach(function (id) {
        var el = document.getElementById(id);
        if (!el) return;
        var span = document.createElement("div");
        span.className = "value-snapshot";
        span.textContent = fieldDisplayValue(el) || " ";
        el.insertAdjacentElement("afterend", span);
        var prevDisplay = el.style.display;
        el.style.display = "none";
        restoreOps.push(function () {
          span.remove();
          el.style.display = prevDisplay;
        });
      });

      if (sigName) {
        var nameSpan = document.createElement("div");
        nameSpan.className = "sig-name-snapshot";
        nameSpan.textContent = sigName.value || " ";
        sigName.insertAdjacentElement("afterend", nameSpan);
        var prevNameDisplay = sigName.style.display;
        sigName.style.display = "none";
        restoreOps.push(function () {
          nameSpan.remove();
          sigName.style.display = prevNameDisplay;
        });
      }

      if (agreeBox) {
        var checkSpan = document.createElement("div");
        checkSpan.className = "checkbox-snapshot";
        checkSpan.textContent = agreeBox.checked ? "✓" : "";
        agreeBox.insertAdjacentElement("afterend", checkSpan);
        var prevCheckDisplay = agreeBox.style.display;
        agreeBox.style.display = "none";
        restoreOps.push(function () {
          checkSpan.remove();
          agreeBox.style.display = prevCheckDisplay;
        });
      }

      return function restore() {
        restoreOps.forEach(function (fn) {
          fn();
        });
      };
    }

    // Slice a tall canvas into separate page-sized canvases instead of
    // re-embedding the whole image on every page (which otherwise bloats
    // the PDF file size by duplicating the full image once per page).
    function addCanvasAsPages(pdf, sourceCanvas) {
      var pageWidthMm = pdf.internal.pageSize.getWidth();
      var pageHeightMm = pdf.internal.pageSize.getHeight();
      var pxPerMm = sourceCanvas.width / pageWidthMm;
      var pageHeightPx = Math.floor(pageHeightMm * pxPerMm);
      var renderedPx = 0;
      var first = true;

      while (renderedPx < sourceCanvas.height) {
        var sliceHeightPx = Math.min(pageHeightPx, sourceCanvas.height - renderedPx);
        var pageCanvas = document.createElement("canvas");
        pageCanvas.width = sourceCanvas.width;
        pageCanvas.height = sliceHeightPx;
        var ctx = pageCanvas.getContext("2d");
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, pageCanvas.width, pageCanvas.height);
        ctx.drawImage(
          sourceCanvas,
          0, renderedPx, sourceCanvas.width, sliceHeightPx,
          0, 0, sourceCanvas.width, sliceHeightPx
        );

        var sliceImgData = pageCanvas.toDataURL("image/jpeg", 0.75);
        var sliceHeightMm = sliceHeightPx / pxPerMm;
        if (!first) pdf.addPage();
        pdf.addImage(sliceImgData, "JPEG", 0, 0, pageWidthMm, sliceHeightMm);

        renderedPx += sliceHeightPx;
        first = false;
      }
    }

    function exportPdf(sigCanvas, sigPad) {
      setStatus("Preparing your PDF…", "");
      if (downloadBtn) downloadBtn.disabled = true;

      var target = document.getElementById("contract");
      document.body.classList.add("pdf-rendering");

      // Bake the signature-pad drawing into a flat <img> so html2canvas
      // (which cannot read live canvas strokes reliably in all browsers)
      // captures exactly what the guest drew.
      var dataUrl = sigPad.isEmpty() ? null : sigCanvas.toDataURL("image/png");
      var swapImg = null;
      if (dataUrl) {
        swapImg = document.createElement("img");
        swapImg.src = dataUrl;
        swapImg.style.width = "100%";
        swapImg.style.height = "100%";
        swapImg.style.objectFit = "contain";
        sigCanvas.style.display = "none";
        sigCanvas.parentNode.appendChild(swapImg);
      }

      var restoreForm = bakeFormForCapture();

      // A moderate scale keeps the text crisp without ballooning the
      // resulting PDF's file size on a long, multi-section document.
      window
        .html2canvas(target, { scale: 1, useCORS: true, backgroundColor: "#ffffff" })
        .then(function (canvasImg) {
          var pdf = new window.jspdf.jsPDF("p", "mm", "a4");
          addCanvasAsPages(pdf, canvasImg);

          var guestName = (sigName && sigName.value.trim()) || "Guest";
          var safeName = guestName.replace(/[^a-z0-9]+/gi, "-").replace(/^-+|-+$/g, "");
          var fileLabel = document.body.getAttribute("data-file-label") || "Terms-and-Conditions";
          pdf.save("Komodo-and-Ko_" + fileLabel + "_" + safeName + ".pdf");

          setStatus("PDF downloaded. You can now send it to the operator.", "ok");
        })
        .catch(function (err) {
          console.error(err);
          setStatus("Something went wrong generating the PDF. Please try again.", "err");
        })
        .finally(function () {
          document.body.classList.remove("pdf-rendering");
          restoreForm();
          if (swapImg) {
            swapImg.remove();
            sigCanvas.style.display = "block";
          }
          if (downloadBtn) downloadBtn.disabled = !validateForm().ready;
        });
    }
  }

  function debounce(fn, wait) {
    var t;
    return function () {
      clearTimeout(t);
      var args = arguments;
      t = setTimeout(function () {
        fn.apply(null, args);
      }, wait);
    };
  }
})();
