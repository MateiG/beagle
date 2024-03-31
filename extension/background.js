chrome.runtime.onInstalled.addListener(function () {
    chrome.tabs.query({}, function (tabs) {
        for (var i = 0; i < tabs.length; i++) {
            var url = tabs[i].url;
            if (url.startsWith('http://') || url.startsWith('https://')) {
                chrome.scripting.executeScript({
                    target: { tabId: tabs[i].id },
                    files: ['content.js']
                });
            }
        }
    });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    sendResponse({ response: "Message received" });
    fetch('http://localhost:8000/add_document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: message.url, title: message.title, text: message.text })
    }).then(response => {
        console.log("Data received by the server");
    }).catch(error => {
        console.log("Error sending data to the server");
    });
});
