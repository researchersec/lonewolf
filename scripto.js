async function fetchJSONData(repoUrl) {
    try {
        const response = await fetch(repoUrl);
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('data').innerHTML = "<p>Error loading data.</p>";
    }
}

function displayData(data) {
    const container = document.getElementById('data');
    container.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
}

// Replace 'yourusername' and 'repo' with your GitHub username and repo name
const repoUrl = 'https://raw.githubusercontent.com/researchersec/lomewolf/prices/latest.json';
fetchJSONData(repoUrl);
