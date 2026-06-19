loadSales();

async function loadSales() {

const response = await fetch(
    `${API_URL}/sales/history`
);

const sales = await response.json();

let html = "";

sales.forEach(sale => {

    html += `
    <tr>
        <td>${sale.id}</td>
        <td>${sale.total_price}</td>
    </tr>
    `;
});

document.getElementById(
    "salesTable"
).innerHTML = html;

}
