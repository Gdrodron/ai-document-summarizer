/* =========================
   APP.JS - Global Scripts
========================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

    // =========================
    // AUTO HIDE ALERTS
    // =========================

    document
    .querySelectorAll(".alert")
    .forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition =
                "opacity .5s";
            alert.style.opacity = "0";
            setTimeout(function(){
                alert.remove();
            },500);
        },4000);
    });

    // =========================
    // DELETE CONFIRMATION
    // =========================
    // NOTE: history.html already handles this via an inline
    // onsubmit="return confirm(...)" on the delete <form>, so this
    // selector currently matches nothing (no .btn-delete class in the
    // markup). Left here in case a future template uses that class,
    // but it's inert right now -- not a bug, just unused.

    document
    .querySelectorAll(".btn-delete")
    .forEach(function(button){
        button.addEventListener(
            "click",
            function(event){

                if(
                    !confirm(
                        "Are you sure you want to delete this analysis?"
                    )
                ){
                    event.preventDefault();
                }
            }
        );
    });

    // =========================
    // FILE DRAG & DROP
    // =========================

    const dropArea =
        document.getElementById(
            "dropArea"
        );
    const fileInput =
        document.getElementById(
            "document"
        );
    const browseBtn =
        document.getElementById(
            "browseBtn"
        );
    const fileName =
        document.getElementById(
            "fileName"
        );
    if(
        dropArea &&
        fileInput
    ){
        browseBtn.addEventListener(
            "click",
            function(){
                fileInput.click();
            }
        );
        fileInput.addEventListener(
            "change",
            function(){
                showFile(
                    this.files[0]
                );
            }
        );
        dropArea.addEventListener(
            "dragover",
            function(e){
                e.preventDefault();
                dropArea.classList.add(
                    "drag-active"
                );

            }
        );

        dropArea.addEventListener(
            "dragleave",
            function(){
                dropArea.classList.remove(
                    "drag-active"
                );
            }
        );

        dropArea.addEventListener(
            "drop",
            function(e){
                e.preventDefault();
                dropArea.classList.remove(
                    "drag-active"
                );

                const files =
                    e.dataTransfer.files;
                if(files.length){
                    fileInput.files =
                        files;
                    showFile(
                        files[0]
                    );
                }
            }
        );
    }

    function showFile(file){
        if(!file){
            return;
        }
        const allowed = [
            "pdf",
            "docx",
            "txt"
        ];
        const extension =
            file.name
            .split(".")
            .pop()
            .toLowerCase();
        if(
            !allowed.includes(extension)
        ){
            fileName.innerHTML =
                "❌ Unsupported file type";
            return;
        }
        fileName.innerHTML =
            "📄 " + file.name;
    }

    // =========================
    // LOADING OVERLAY
    // =========================

    const uploadForm =
        document.getElementById(
            "uploadForm"
        );
    const loadingOverlay =
        document.getElementById(
            "loadingOverlay"
        );

    if(uploadForm){
        uploadForm.addEventListener(
            "submit",
            function(){
                if(loadingOverlay){
                    loadingOverlay.classList.remove(
                        "d-none"
                    );
                }

                const button =
                    uploadForm.querySelector(
                        "button[type='submit']"
                    );
                if(button){
                    button.disabled = true;
                    button.innerHTML =
                    `
                    <span 
                    class="spinner-border spinner-border-sm">
                    </span>
                    Analyzing...
                    `;
                }
            }
        );
    }

    // =========================
    // DARK MODE TOGGLE
    // =========================
    // REMOVED: this used to attach a SECOND click handler to
    // #themeToggle that toggled a body.dark-mode class and wrote
    // 'dark-mode' / '' into localStorage['theme']. base.html already
    // owns theming via the data-bs-theme="light"/"dark" attribute and
    // the SAME localStorage['theme'] key, but with 'light'/'dark'
    // values. Having both meant every click fired two conflicting
    // handlers that stomped on each other's localStorage value, and
    // on reload data-bs-theme could end up set to the literal string
    // "dark-mode", which Bootstrap doesn't recognize -- breaking the
    // theme and desyncing the moon/sun icon. base.html's own inline
    // script at the bottom of that file is the single source of truth
    // for theming now.

    // =========================
    // SMOOTH SCROLL
    // =========================

    document
    .querySelectorAll(
        "a[href^='#']"
    )
    .forEach(function(link){

        link.addEventListener(
            "click",
            function(e){

                const target =
                    document.querySelector(
                        this.getAttribute("href")
                    );
                if(target){
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior:"smooth"
                    });

                }

            }
        );

    });

});