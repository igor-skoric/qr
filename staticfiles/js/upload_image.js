

// Inicijalizuj Dropzone sa željenim opcijama
Dropzone.options.imageDropzone = {
    paramName: "file", // Parametar koji šaljemo serveru
    maxFilesize: 10, // Maksimalna veličina fajla (u MB)
    acceptedFiles: 'image/*', // Samo slike
    dictDefaultMessage: "Povucite i spustite slike ovde ili kliknite za odabir", // Poruka kada nema fajlova
    init: function() {
        this.on("success", function(file, response) {
            // Kada je slika uspešno uploadovana, prikaži je u preview-u
            const imagePreview = document.getElementById('imagePreview');
            const imgElement = document.createElement('img');
            imgElement.src = response.file_url; // Pretpostavljamo da server vraća URL slike
            imgElement.classList.add('w-full', 'h-auto', 'rounded-lg');
            imagePreview.appendChild(imgElement);
        });

        this.on("error", function(file, response) {
            alert("Došlo je do greške prilikom upload-a." + response );
        });
    }
};