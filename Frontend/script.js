document.addEventListener('DOMContentLoaded', function () {
    const searchBox = document.getElementById('search-box');
    const topicInput = document.getElementById('topic');
    const authorInput = document.getElementById('author');
    const locationInput = document.getElementById('location');
    const suggestionsDiv = document.getElementById('suggestions');

    searchBox.addEventListener('input', debounce(handleSearch, 300));

    function handleSearch() {
        const query = searchBox.value.trim();
        const topic = topicInput.value.trim();
        const author = authorInput.value.trim();
        const location = locationInput.value.trim();

        if (query.length >= 3) {
            const apiUrl = 'http://localhost:8000/search/';
            const requestBody = {
                query: query,
                topic: topic,
                author: author,
                specific_location: location
            };

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            })
            .then(response => response.json())
            .then(data => {
                updateSuggestions(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
        } else {
            suggestionsDiv.innerHTML = '';
            suggestionsDiv.style.display = 'none';
        }
    }

    function updateSuggestions(data) {
        console.log(data);
        suggestionsDiv.innerHTML = ''; 
    
        if (Array.isArray(data) && data.length > 0) {
            const titles = data.map(item => item.title);
    
            titles.forEach(title => {
                const suggestionItem = document.createElement('p');
                suggestionItem.textContent = title;
                suggestionItem.addEventListener('click', () => {
                    searchBox.value = title;
                    suggestionsDiv.style.display = 'none';
                });
                suggestionsDiv.appendChild(suggestionItem);
            });
    
            suggestionsDiv.style.display = 'block';
        } else {
            const noDataMessage = document.createElement('p');
            noDataMessage.textContent = 'No data found.';
            suggestionsDiv.appendChild(noDataMessage);
    
            suggestionsDiv.style.display = 'block';
        }
    }
    

    function debounce(func, wait) {
        let timeout;
        return function () {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                func.apply(context, args);
            }, wait);
        };
    }
});
