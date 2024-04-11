document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('searchButton');
    const queryInput = document.getElementById('query');

    queryInput.addEventListener('keypress', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            search();
        }
    });

    searchButton.addEventListener('click', search);

    function search() {
        const query = queryInput.value;
        fetch(`http://localhost:8000/search?query=${query}`)
            .then(response => response.json())
            .then(data => {
                const resultsContainer = document.getElementById('results');
                if (data.status === "success") {
                    let resultsHtml = "";
                    data.results.slice(0, 5).forEach((result, i) => {
                        if (result.score > 0) {
                            resultsHtml += `
                            <div id="result-${i}">
                                <strong>RESULT ${i + 1} (${result.score.toFixed(2)}):</strong>
                                ${result.title}<br>
                                <a href="${result.url}" target="_blank">${result.url}</a>
                                <button class="delete-button right-align" data-url="${result.url}" data-result-id="result-${i}">Delete</button>
                                <hr>
                            </div>
                        `;
                        }
                    });
                    resultsContainer.innerHTML = resultsHtml;
                    document.querySelectorAll('.delete-button').forEach(button => {
                        button.addEventListener('click', function () {
                            deleteDocument(this.getAttribute('data-url'), this.getAttribute('data-result-id'));
                        });
                    });
                } else {
                    resultsContainer.innerHTML = `<strong>Error:</strong> ${data.message}`;
                }
            });
    }

    function deleteDocument(url, resultId) {
        fetch(`http://localhost:8000/delete_document`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "url": url })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    document.getElementById(resultId).remove();
                    alert("Document deleted successfully.");
                } else {
                    alert("Error deleting document: " + data.message);
                }
            });
    }

});
