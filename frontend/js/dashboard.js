fetch(`${API_URL}/dashboard/stats`)
.then(res => res.json())
.then(data => {

document.getElementById("medicines").innerText =
    data.total_medicines;

document.getElementById("suppliers").innerText =
    data.total_suppliers;

document.getElementById("sales").innerText =
    data.total_sales;

document.getElementById("revenue").innerText =
    data.total_revenue;

});
