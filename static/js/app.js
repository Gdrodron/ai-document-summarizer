document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // Drag & Drop Upload
    // ==========================

    const dropArea = document.getElementById("dropArea");
    const fileInput = document.getElementById("document");
    const browseBtn = document.getElementById("browseBtn");
    const fileName = document.getElementById("fileName");

    if (dropArea && fileInput && browseBtn && fileName) {

        browseBtn.addEventListener("click", () => {
            fileInput.click();
        });

        dropArea.addEventListener("click", () => {
            fileInput.click();
        });

        fileInput.addEventListener("change", () => {

            if (fileInput.files.length > 0) {

                fileName.textContent =
                    "Selected: " + fileInput.files[0].name;

            }

        });

        ["dragenter", "dragover"].forEach(event => {

            dropArea.addEventListener(event, (e) => {

                e.preventDefault();

                dropArea.classList.add("drag-over");

            });

        });

        ["dragleave", "drop"].forEach(event => {

            dropArea.addEventListener(event, (e) => {

                e.preventDefault();

                dropArea.classList.remove("drag-over");

            });

        });

        dropArea.addEventListener("drop", (e) => {

            e.preventDefault();

            fileInput.files = e.dataTransfer.files;

            if (fileInput.files.length > 0) {

                fileName.textContent =
                    "Selected: " + fileInput.files[0].name;

            }

        });

    }

    // ==========================
    // Loading Screen
    // ==========================

    const uploadForm = document.getElementById("uploadForm");
    const loadingOverlay = document.getElementById("loadingOverlay");

    if (uploadForm && loadingOverlay) {

        uploadForm.addEventListener("submit", () => {

            loadingOverlay.classList.remove("d-none");

        });

    }

    // ==========================
    // Copy Summary
    // ==========================

    const copyButton = document.getElementById("copySummary");
    const summaryText = document.getElementById("summaryText");

    if (copyButton && summaryText) {

        copyButton.addEventListener("click", async () => {

            try {

                await navigator.clipboard.writeText(summaryText.innerText);

                copyButton.innerHTML =
                    '<i class="bi bi-check-lg"></i> Copied';

                const toastElement =
                    document.getElementById("copyToast");

                if (toastElement) {

                    const toast =
                        new bootstrap.Toast(toastElement);

                    toast.show();

                }

                setTimeout(() => {

                    copyButton.innerHTML =
                        '<i class="bi bi-clipboard"></i> Copy';

                }, 2000);

            }

            catch (error) {

                console.error(error);

            }

        });

    }

});

// ==========================
// Dark Mode
// ==========================

const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {

    if (localStorage.getItem("theme") === "dark") {

        document.body.classList.add("dark-mode");

        themeToggle.innerHTML =
            '<i class="bi bi-sun-fill"></i>';

    }

    themeToggle.addEventListener("click", () => {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {

            localStorage.setItem("theme", "dark");

            themeToggle.innerHTML =
                '<i class="bi bi-sun-fill"></i>';

        } else {

            localStorage.setItem("theme", "light");

            themeToggle.innerHTML =
                '<i class="bi bi-moon-stars-fill"></i>';

        }

    });

}