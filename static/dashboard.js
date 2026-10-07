const dataElement = document.getElementById("dashboard-data");
const data = JSON.parse(dataElement.textContent);

const commonOptions = {
    responsive: true,
    plugins: {
        legend: { position: "top" }
    }
};

new Chart(document.getElementById("productChart"), {
    type: "bar",
    data: {
        labels: data.product_names,
        datasets: [{
            label: "Quantity Sold",
            data: data.product_quantities
        }]
    },
    options: {
        ...commonOptions,
        scales: { y: { beginAtZero: true } }
    }
});

new Chart(document.getElementById("monthlyChart"), {
    type: "line",
    data: {
        labels: data.months,
        datasets: [{
            label: "Monthly Revenue",
            data: data.month_values,
            fill: false,
            tension: 0.3
        }]
    },
    options: {
        ...commonOptions,
        scales: { y: { beginAtZero: true } }
    }
});

new Chart(document.getElementById("revenueChart"), {
    type: "doughnut",
    data: {
        labels: data.revenue_product_names,
        datasets: [{
            label: "Revenue",
            data: data.revenue_product_values
        }]
    },
    options: commonOptions
});

const profitCanvas = document.getElementById("profitChart");
if (profitCanvas && data.profit_product_names) {
    new Chart(profitCanvas, {
        type: "bar",
        data: {
            labels: data.profit_product_names,
            datasets: [{
                label: "Profit (₹)",
                data: data.profit_product_values,
                backgroundColor: "rgba(16, 185, 129, 0.75)",
                borderColor: "rgb(16, 185, 129)",
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => "₹" + Number(value).toLocaleString()
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    callbacks: {
                        label: (context) => " Profit: ₹" + Number(context.raw).toLocaleString(undefined, { minimumFractionDigits: 2 })
                    }
                }
            }
        }
    });
}
