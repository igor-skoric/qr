
// Povezivanje sa WebSocket serverom
const socket = new WebSocket('ws://' + window.location.host + '/ws/somepath/');

// Kada se uspostavi konekcija, pošaljite inicijalnu poruku
socket.onopen = function(e) {
    console.log("WebSocket connected");
};

// Kada stigne poruka od servera (update slike)
socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Received data:", data);

    // Ažuriraj UI sa novom slikom
    const imageContainer = document.getElementById("image-container");
    imageContainer.src = data.message;  // Pretpostavljamo da 'message' sadrži ime slike
};

// Kada dođe do greške u vezi
socket.onerror = function(error) {
    console.log("WebSocket Error:", error);
};

// Kada WebSocket konekcija bude zatvorena
socket.onclose = function(event) {
    if (event.wasClean) {
        console.log('Closed cleanly');
    } else {
        console.error('Connection died');
    }
};

// Funkcija za slanje poruke serveru (ako želiš da šalješ nešto)
function sendMessage(message) {
    socket.send(JSON.stringify({'message': message}));
}
