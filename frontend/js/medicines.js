loadMedicines();

async function loadMedicines() {

const response = await fetch(
    `${API_URL}/medicines`
);

const medicines = await response.json();

let html = "";

medicines.forEach(medicine => {

    html += `
    <tr>
        <td>${medicine.id}</td>
        <td>${medicine.name}</td>
        <td>${medicine.category}</td>
        <td>${medicine.quantity}</td>
        <td>${medicine.price}</td>
    </tr>
    `;
});

document.getElementById(
    "medicineTable"
).innerHTML = html;
```

}

async function addMedicine() {

```
const medicine = {
    name: document.getElementById("name").value,
    category: document.getElementById("category").value,
    quantity: parseInt(document.getElementById("quantity").value),
    price: parseFloat(document.getElementById("price").value),
    expiry_date: document.getElementById("expiry_date").value
};

await fetch(
    `${API_URL}/medicines/`,
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(medicine)
    }
);

location.reload();

}
