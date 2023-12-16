// URL to your JSON file hosted on GitHub Pages
const jsonUrl = 'https://researchersec.github.io/lomewolf/lonewolf.json';

// Function to fetch data
async function fetchData() {
    try {
        const response = await fetch(jsonUrl);
        const data = await response.json();
        return data.pricing_data; // Assuming pricing data is an array in the JSON file
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to search for item prices
async function searchItem() {
    const itemId = document.getElementById('itemInput').value;
    const prices = await fetchData();

    // Filter prices based on item ID
    const filteredPrices = prices.filter(item => item.itemId === parseInt(itemId));

    // Display filtered prices
    displayPrices(filteredPrices);
}

// Function to display prices
function displayPrices(prices) {
    const displayArea = document.getElementById('priceDisplay');
    displayArea.innerHTML = ''; // Clear previous content

    if (prices.length === 0) {
        displayArea.innerText = 'Item not found or no prices available.';
        return;
    }

    // Display prices in the display area
    prices.forEach(item => {
        const itemDetails = document.createElement('div');
        itemDetails.innerHTML = `
            <p>Item ID: ${item.itemId}</p>
            <p>Market Value: ${item.marketValue}</p>
            <!-- Add more details or create diagrams here -->
        `;
        displayArea.appendChild(itemDetails);
    });
}
