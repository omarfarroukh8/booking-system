console.log("SaaS Dashboard Loaded 🚀");

// ==========================
// 🌙 DARK MODE TOGGLE
// ==========================
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("darkModeBtn");

    if (btn) {
        btn.addEventListener("click", toggleDarkMode);
    }

    const theme = localStorage.getItem("theme");

    if (theme === "dark") {
        document.body.classList.add("dark-mode");
    }

});


// ==========================
// 🔔 SIMPLE NOTIFICATION
// ==========================
function showNotification(message) {
    let box = document.createElement("div");

    box.innerText = message;
    box.style.position = "fixed";
    box.style.top = "20px";
    box.style.right = "20px";
    box.style.background = "#111827";
    box.style.color = "white";
    box.style.padding = "12px 20px";
    box.style.borderRadius = "8px";
    box.style.boxShadow = "0 5px 15px rgba(0,0,0,0.2)";
    box.style.zIndex = "9999";

    document.body.appendChild(box);

    setTimeout(() => {
        box.remove();
    }, 3000);
}


// ==========================
// 📊 OPTIONAL: CHART READY HOOK
// ==========================
function initChart(users, bookings) {
    const ctx = document.getElementById('chart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Users', 'Bookings'],
            datasets: [{
                label: 'Overview',
                data: [users, bookings],
                borderWidth: 1
            }]
        }
    });
}


// ==========================
// 🚀 AUTO MESSAGE ON LOAD
// ==========================
window.addEventListener("load", () => {
    console.log("Dashboard Ready ✔️");

    // showNotification("Welcome to your SaaS Dashboard 🚀");
});