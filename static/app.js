document.getElementById("fetch-data").addEventListener("click", async () => {
    const output = document.getElementById("data-output");
    output.innerHTML = "Fetching data...";

    try {
        const response = await fetch("/financial-data");
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        output.innerHTML = "<h2>Financial Data</h2>";
        data.data.forEach((item) => {
            output.innerHTML += `
                <div>
                    <strong>${item.ticker}</strong>: ${item.name}<br>
                    Price: $${item.price.toFixed(2)}<br>
                    P/E Ratio: ${item.pe_ratio ? item.pe_ratio.toFixed(2) : "N/A"}<br>
                    Revenue: $${formatNumber(item.revenue)}<br>
                    EBITDA: ${formatPercentage(item.ebitda, item.revenue)}<br>
                    <hr>
                </div>
            `;
        });
    } catch (error) {
        output.innerHTML = `Error fetching data: ${error.message}`;
    }
});

// Helper function to format large numbers with commas
function formatNumber(num) {
    if (!num) return "N/A";
    return num.toLocaleString("en-US");
}

// Helper function to calculate and format EBITDA as a percentage of revenue
function formatPercentage(ebitda, revenue) {
    if (!ebitda || !revenue) return "N/A";
    const percentage = (ebitda / revenue) * 100;
    return `${percentage.toFixed(2)}%`;
}