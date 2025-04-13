// static/js/script.js
document.addEventListener("DOMContentLoaded", function () {
    const modelLinks = document.querySelectorAll("#model-list a");
    const modelInfoBox = document.getElementById("model-info-box");

    // Tambahkan event listener untuk setiap link model
    modelLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Mencegah navigasi default

            const modelName = this.getAttribute("data-model"); // Ambil nama model dari atribut data

            // Kirim permintaan ke API Flask untuk mendapatkan informasi model
            fetch(`/get_model_info/${modelName}`)
                .then(response => response.json())
                .then(data => {
                    // Tampilkan informasi model di kotak besar
                    modelInfoBox.textContent = data.info;
                })
                .catch(error => {
                    console.error("Error fetching model info:", error);
                    modelInfoBox.textContent = "Gagal memuat informasi model.";
                });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Dapatkan URL halaman saat ini
    const currentPage = window.location.pathname;

    // Dapatkan semua elemen <a> di dalam navbar
    const navLinks = document.querySelectorAll('.nav-links a');

    // Loop melalui setiap link
    navLinks.forEach(link => {
        // Jika href link cocok dengan URL halaman saat ini, tambahkan kelas 'active'
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});

const modelChoices = document.querySelectorAll('.model-choice');

modelChoices.forEach(choice => {
    choice.addEventListener('click', function() {
        // Hapus kelas 'active' dari semua pilihan
        modelChoices.forEach(c => c.classList.remove('active'));
        
        // Tambahkan kelas 'active' ke elemen yang diklik
        this.classList.add('active');
    });
});

// Toggle active state for model buttons
document.querySelectorAll('.model-btn').forEach(button => {
    button.addEventListener('click', function () {
        this.classList.toggle('active');
    });
});

// Show or hide RGB input and toggle Upload button
const toggleInput = document.getElementById('toggle-input');
const uploadButton = document.getElementById('upload-btn');
const rgbInput = document.getElementById('rgb-input');
const redInput = document.getElementById('r');
const greenInput = document.getElementById('g');
const blueInput = document.getElementById('b');
const fileUpload = document.getElementById('file-upload');

toggleInput.addEventListener('click', function () {
    if (rgbInput.style.display === 'none') {
        // Show RGB inputs and reset file upload
        rgbInput.style.display = 'inline-block';
        uploadButton.style.display = 'none';
        fileUpload.style.display = 'none';
        fileUpload.value = ''; // Clear file input but keep RGB values
    } else {
        // Show file upload and hide RGB inputs
        rgbInput.style.display = 'none';
        uploadButton.style.display = 'inline-block';
        fileUpload.style.display = 'inline-block';
    }
});

fileUpload.addEventListener('change', function () {
    if (fileUpload.files.length > 0) {
        // Clear RGB inputs only if a file is uploaded
        redInput.value = '';
        greenInput.value = '';
        blueInput.value = '';
    }
});