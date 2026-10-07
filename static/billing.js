const rows = document.getElementById("productRows");
const addButton = document.getElementById("addProduct");
const totalElement = document.getElementById("estimatedTotal");

function updateRow(row) {
    const select = row.querySelector(".product-select");
    const quantity = row.querySelector(".quantity");
    const price = row.querySelector(".price");
    const option = select.options[select.selectedIndex];
    const unitPrice = Number(option?.dataset.price || 0);

    price.value = unitPrice ? `₹${unitPrice.toFixed(2)}` : "";
    quantity.min = "1";
    updateTotal();
}

function updateTotal() {
    let total = 0;

    rows.querySelectorAll(".product-row").forEach((row) => {
        const select = row.querySelector(".product-select");
        const quantity = Number(row.querySelector(".quantity").value || 0);
        const option = select.options[select.selectedIndex];
        const unitPrice = Number(option?.dataset.price || 0);
        total += unitPrice * quantity;
    });

    totalElement.textContent = `₹${total.toFixed(2)}`;
}

function attachRowEvents(row) {
    row.querySelector(".product-select").addEventListener("change", () => updateRow(row));
    row.querySelector(".quantity").addEventListener("input", updateTotal);
    row.querySelector(".remove-row").addEventListener("click", () => {
        if (rows.querySelectorAll(".product-row").length > 1) {
            row.remove();
            updateTotal();
        }
    });
}

attachRowEvents(rows.querySelector(".product-row"));

addButton.addEventListener("click", () => {
    const first = rows.querySelector(".product-row");
    const clone = first.cloneNode(true);

    clone.querySelector(".product-select").value = "";
    clone.querySelector(".quantity").value = "1";
    clone.querySelector(".price").value = "";

    rows.appendChild(clone);
    attachRowEvents(clone);
    updateTotal();
});
