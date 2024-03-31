let timeoutId = null;
let oldText = "";

function sendMessage() {
    console.log("Beagle sending message to background");
    message = {
        url: window.location.href,
        title: document.title,
        text: document.body.innerText
    };
    chrome.runtime.sendMessage(message, (response) => {
        if (chrome.runtime.lastError) {
            console.log("Background ran into an issue" + chrome.runtime.lastError.message);
        }
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

observer.observe(document.body, { childList: true, subtree: true, characterData: true });