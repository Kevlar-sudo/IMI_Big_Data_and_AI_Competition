function createAlertCard(alert) {
    const card = document.createElement('div');
    card.classList.add('alert-card');

    // Determine risk level based on anomaly score
    if (alert.anomaly_score < -0.1) {
        card.classList.add('high');
    } else if (alert.anomaly_score < -0.05) {
        card.classList.add('medium');
    } else {
        card.classList.add('low');
    }

    // Add content to card
    card.innerHTML = `
        <h3>Alert ID: ${alert.abm_id || 'N/A'}</h3>
        <p>Customer ID: ${alert.customer_id}</p>
        <p>Transaction Amount: ${alert.amount_cad}</p>
        <p>Date/Time: ${alert.transaction_date} ${alert.transaction_time}</p>
        <p>Location: ${alert.city || 'N/A'}</p>
        <p>Industry Code: ${alert.industry_code || 'N/A'}</p>
        <p>Employee Count: ${alert.employee_count || 'N/A'}</p>
        <p>Sales: ${alert.sales || 'N/A'}</p>
        <p>Risk Score: ${alert.anomaly_score.toFixed(2)}</p>
        <p>Rule Based Flag: ${alert.rule_based_flag}</p>
        <button class="view-details-btn">View Details</button>
    `;

    // Add event listener for "View Details" button
    const viewDetailsBtn = card.querySelector('.view-details-btn');
    viewDetailsBtn.addEventListener('click', () => {
        console.log("View Details clicked for alert:", alert);
        // Implement logic to show more details about the alert
    });

    return card;
}

function displayAlerts(alerts) {
    const alertList = document.getElementById('alert-list');
    alertList.innerHTML = ''; // Clear existing content

    if (alerts.length === 0) {
        alertList.innerHTML = '<p>No alerts found.</p>';
        return;
    }

    alerts.forEach(alert => {
        const card = createAlertCard(alert);
        alertList.appendChild(card);
    });
}

function getFilters() {
    // Get values from all filter elements
    const customerId = document.getElementById('customer-id-filter').value;
    const transactionType = document.getElementById('transaction-type-filter').value;
    const amountMin = parseFloat(document.getElementById('amount-min-filter').value);
    const amountMax = parseFloat(document.getElementById('amount-max-filter').value);
    const riskScoreMin = parseFloat(document.getElementById('risk-score-min-filter').value);
    const riskScoreMax = parseFloat(document.getElementById('risk-score-max-filter').value);
    const ruleBasedFlag = document.getElementById('rule-based-flag-filter').value;
    const cashIndicator = document.getElementById('cash-indicator-filter').value;
    const country = document.getElementById('country-filter').value;
    const province = document.getElementById('province-filter').value;
    const city = document.getElementById('city-filter').value;
    const industryCode = document.getElementById('industry-code-filter').value;
    const employeeCountMin = parseInt(document.getElementById('employee-count-min-filter').value);
    const employeeCountMax = parseInt(document.getElementById('employee-count-max-filter').value);
    const salesMin = parseFloat(document.getElementById('sales-min-filter').value);
    const salesMax = parseFloat(document.getElementById('sales-max-filter').value);

    return {
        customerId,
        transactionType,
        amountMin,
        amountMax,
        riskScoreMin,
        riskScoreMax,
        ruleBasedFlag,
        cashIndicator,
        country,
        province,
        city,
        industryCode,
        employeeCountMin,
        employeeCountMax,
        salesMin,
        salesMax
    };
}

function filterAlerts(alerts, filters) {
    return alerts.filter(alert => {
        // Check each filter condition, return false if any condition fails
        if (filters.customerId && !alert.customer_id.includes(filters.customerId)) return false;
        if (filters.transactionType && alert.transaction_type !== filters.transactionType) return false;
        if (!isNaN(filters.amountMin) && alert.amount_cad < filters.amountMin) return false;
        if (!isNaN(filters.amountMax) && alert.amount_cad > filters.amountMax) return false;
        if (!isNaN(filters.riskScoreMin) && alert.anomaly_score < filters.riskScoreMin) return false;
        if (!isNaN(filters.riskScoreMax) && alert.anomaly_score > filters.riskScoreMax) return false;
        if (filters.ruleBasedFlag && alert.rule_based_flag.toString() !== filters.ruleBasedFlag) return false;
        if (filters.cashIndicator && alert.cash_indicator.toString() !== filters.cashIndicator) return false;
        if (filters.country && !alert.country.includes(filters.country)) return false;
        if (filters.province && !alert.province.includes(filters.province)) return false;
        if (filters.city && !alert.city.includes(filters.city)) return false;
        if (filters.industryCode && !alert.industry_code.includes(filters.industryCode)) return false;
        if (!isNaN(filters.employeeCountMin) && alert.employee_count < filters.employeeCountMin) return false;
        if (!isNaN(filters.employeeCountMax) && alert.employee_count > filters.employeeCountMax) return false;
        if (!isNaN(filters.salesMin) && alert.sales < filters.salesMin) return false;
        if (!isNaN(filters.salesMax) && alert.sales > filters.salesMax) return false;

        return true; // Alert passes all filter conditions
    });
}

// Fetch alerts from the backend and apply filters
function fetchAndDisplayAlerts() {
    fetch('/get_alerts')
        .then(response => response.json())
        .then(alerts => {
            const filters = getFilters();
            const filteredAlerts = filterAlerts(alerts, filters);
            displayAlerts(filteredAlerts);
        })
        .catch(error => {
            console.error('Error fetching alerts:', error);
            const alertList = document.getElementById('alert-list');
            alertList.innerHTML = '<p>Error loading alerts.</p>';
        });
}

// Add event listener to "Apply Filters" button
const applyFiltersBtn = document.getElementById('apply-filters-btn');
applyFiltersBtn.addEventListener('click', fetchAndDisplayAlerts);

// Initial fetch and display of alerts
fetchAndDisplayAlerts();