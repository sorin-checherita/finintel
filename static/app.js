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
                    <strong>${item.ticker}</strong>: ${item.name || "N/A"}<br>
                    Price: ${item.price}<br>
                    P/E Ratio: ${item.pe_ratio}<br>
                    Revenue: ${item.revenue}<br>
                    EBITDA: ${item.ebitda}<br>
                    <hr>
                </div>
            `;
        });
    } catch (error) {
        output.innerHTML = `Error fetching data: ${error.message}`;
    }
});