let timeoutId = null;
let oldText = "";

function sendMessage() {
    console.log("Beagle sending message to server")
    message = { url: window.location.href, title: document.title, text: document.body.innerText };

    fetch('http://localhost:4242/add_document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(message)
    }).then(response => {
        console.log("Data received by the server");
    }).catch(error => {
        console.log("Error sending data to the server");
    });
}

let observer = new MutationObserver((mutationsList, observer) => {
    let newText = document.body.innerText;
    if (newText !== oldText) {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            sendMessage();
        }, 1500);
        oldText = newText;
    }
});

sendMessage();
observer.observe(document.body, { childList: true, subtree: true, characterData: true });
