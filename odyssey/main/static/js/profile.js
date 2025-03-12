document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener("click", function(event) {
        if (event.target.id.startsWith("right-btn")) {
            itineraryId = event.target.id.slice(9)
            fetch(`/delete-row/${itineraryId}/`, {
                method: "POST",
                headers: {
                    // "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Itinerary removed');
                    location.reload()
                }
            })
        }

        if (event.target.id == "itinerary-location") {
            itineraryId = event.target.classList[0]
            
            getActivities(itineraryId).then(rowData => {
                const activities = rowData;
                
            });
        }
    })
})

async function getActivities(itineraryId) {
    return fetch(`/get-row/${itineraryId}/`)
    .then(response => response.json())
    .then(data => {
        return data;
    })
    .catch(error => console.error("Error fetching row data:", error));
}

// function getCSRFToken() {
//     return document.querySelector("[name=csrfmiddlewaretoken]").value;
// }