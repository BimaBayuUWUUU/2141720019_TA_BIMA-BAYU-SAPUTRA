document.addEventListener("DOMContentLoaded", function () {
    // =============== TOGGLE INPUT MODE (RGB / CSV) ===============
    const inputModeBtn = document.getElementById('input-mode-btn');
    const rgbInput = document.getElementById('rgb-input');
    const fileUploadContainer = document.getElementById('file-upload-container');
    const fileUpload = document.getElementById('file-upload');
    const fileNameSpan = document.getElementById('file-name');

    const redInput = document.getElementById('r');
    const greenInput = document.getElementById('g');
    const blueInput = document.getElementById('b');

    const modelButtons = document.querySelectorAll('.model-btn');
    const selectedModelInput = document.getElementById('selected-model-input');
    const classificationForm = document.getElementById('classification-form');

    let selectedModels = [];

    // Saat halaman dimuat, mode CSV aktif (default)
    if (rgbInput) {
        rgbInput.style.display = 'none';
        inputModeBtn.textContent = 'Input Manual';
    }

    // Toggle antara manual dan CSV
    if (inputModeBtn && rgbInput && fileUploadContainer) {
        inputModeBtn.addEventListener('click', function () {
            if (rgbInput.style.display === 'none') {
                rgbInput.style.display = 'block';
                fileUploadContainer.style.display = 'none';
                if (fileUpload) fileUpload.value = '';
                inputModeBtn.textContent = 'Masukan Kanal RGB';
            } else {
                rgbInput.style.display = 'none';
                fileUploadContainer.style.display = 'block';
                if (redInput) redInput.value = '';
                if (greenInput) greenInput.value = '';
                if (blueInput) blueInput.value = '';
                inputModeBtn.textContent = 'Input Manual';
            }
        });
    }

    // Tampilkan nama file dan reset input manual saat file diupload
    if (fileUpload && fileNameSpan) {
        fileUpload.addEventListener('change', function () {
            if (this.files.length > 0) {
                fileNameSpan.textContent = this.files[0].name;
                if (redInput) redInput.value = '';
                if (greenInput) greenInput.value = '';
                if (blueInput) blueInput.value = '';
            } else {
                fileNameSpan.textContent = '';
            }
        });
    }

    // =============== PEMILIHAN MODEL ===============
    if (modelButtons.length > 0) {
        modelButtons.forEach(button => {
            button.addEventListener('click', function () {
                const modelName = this.getAttribute('data-model');

                if (selectedModels.includes(modelName)) {
                    selectedModels = selectedModels.filter(m => m !== modelName);
                    this.classList.remove('btn-success', 'active');
                    this.classList.add('btn-outline-secondary');
                } else {
                    selectedModels.push(modelName);
                    this.classList.remove('btn-outline-secondary');
                    this.classList.add('btn-success', 'active');
                }

                if (selectedModelInput) {
                    selectedModelInput.value = selectedModels.join(',');
                }
            });
        });
    }

    // =============== VALIDASI SEBELUM SUBMIT ===============
    if (classificationForm) {
        classificationForm.addEventListener('submit', function (e) {
            const isBaggingPage = window.location.pathname.includes("classification_bagging");

            if (!isBaggingPage) {
                if (selectedModels.length === 0) {
                    e.preventDefault();
                    alert("Silakan pilih setidaknya satu model.");
                    return;
                }
            }

            const r = redInput?.value.trim() || '';
            const g = greenInput?.value.trim() || '';
            const b = blueInput?.value.trim() || '';
            const csvFile = fileUpload?.files[0];

            const hasManualInput = r !== '' && g !== '' && b !== '';
            const hasCsvFile = !!csvFile;

            if (!hasManualInput && !hasCsvFile) {
                e.preventDefault();
                alert("Silakan masukkan nilai RGB atau unggah file CSV.");
            }
        });
    }

    // =============== MODEL INFO BOX (Optional) ===============
    const modelLinks = document.querySelectorAll("#model-list a");
    const modelInfoBox = document.getElementById("model-info-box");

    if (modelLinks.length > 0 && modelInfoBox) {
        modelLinks.forEach(link => {
            link.addEventListener("click", function (event) {
                event.preventDefault();

                const modelName = this.getAttribute("data-model");

                fetch(`/get_model_info/${modelName}`)
                    .then(response => {
                        if (!response.ok) throw new Error("Network response was not ok");
                        return response.json();
                    })
                    .then(data => {
                        modelInfoBox.textContent = data.info;
                    })
                    .catch(error => {
                        console.error("Error fetching model info:", error);
                        modelInfoBox.textContent = "Gagal memuat informasi model.";
                    });
            });
        });
    }

    // =============== NAVBAR ACTIVE LINK ===============
    const currentPath = window.location.pathname.replace(/\/+$/, "");

    document.querySelectorAll('.nav-links a').forEach(link => {
        let href = link.getAttribute('href') || "";

        if (!href) return;

        try {
            href = new URL(href, window.location.href).pathname;
        } catch (e) {
            console.warn("Invalid href:", href);
            return;
        }

        const normalizedHref = href.replace(/\/+$/, "");

        if (normalizedHref === currentPath) {
            link.classList.add('active');
        }
    });
});

let modelSlidesGlobal = {};
let currentModel = null;
let currentSlideIndex = 0;

function initSlideshow(models) {
    modelSlidesGlobal = models;
    showSlides("ann"); // Model default
}

function showSlides(model) {
    if (!modelSlidesGlobal[model]) return;

    currentModel = model;
    currentSlideIndex = 0;
    updateTitle();
    renderCurrentSlide();
}

function nextSlide() {
    const slides = modelSlidesGlobal[currentModel]?.slides;
    if (slides && currentSlideIndex < slides.length - 1) {
        currentSlideIndex++;
        renderCurrentSlide();
    }
}

function prevSlide() {
    if (currentSlideIndex > 0) {
        currentSlideIndex--;
        renderCurrentSlide();
    }
}

function renderCurrentSlide() {
    const slides = modelSlidesGlobal[currentModel]?.slides;
    const slideContainer = document.getElementById("slideshow");

    if (!slides || !slideContainer) return;

    const slide = slides[currentSlideIndex];
    const imageUrl = slide.image;

    slideContainer.innerHTML = `
        <div class="slide">
            <img src="${imageUrl}" alt="${slide.caption}">
            <p>${slide.caption}</p>
        </div>
    `;
}

function updateTitle() {
    const titleElement = document.getElementById("slideTitle");
    const modelName = modelSlidesGlobal[currentModel]?.name || "Tentang Model";
    titleElement.innerText = modelName;
}

// Tunggu DOM selesai dimuat sebelum menambahkan event listener
document.addEventListener("DOMContentLoaded", function () {
    const modelList = document.getElementById("modelList");
    if (modelList) {
        modelList.addEventListener("click", function (e) {
            if (e.target && e.target.matches(".model-choice")) {
                e.preventDefault();

                // Hapus kelas 'active' dari semua model
                document.querySelectorAll(".model-choice").forEach(item => {
                    item.classList.remove("active");
                });

                // Tambahkan kelas 'active' ke model yang diklik
                e.target.classList.add("active");

                // Ambil data-model dan tampilkan slideshow
                const selectedModel = e.target.getAttribute("data-model");
                showSlides(selectedModel);
            }
        });
    }
});