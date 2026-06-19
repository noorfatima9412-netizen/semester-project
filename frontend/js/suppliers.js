loadSuppliers();

async function loadSuppliers() {

const response = await fetch(
    `${API_URL}/suppliers`
);

const suppliers = await response.json();

let html = "";

suppliers.forEach(supplier => {

    html += `
    <tr>
        <td>${supplier.id}</td>
        <td>${supplier.name}</td>
        <td>${supplier.phone}</td>
    </tr>
    `;
});

document.getElementById(
    "supplierTable"
).innerHTML = html;

}
