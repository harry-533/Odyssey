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
                const activities = document.querySelector('.itinerary-activities');
                keys = Object.keys(rowData);
                let city = rowData[keys[0]]['city'];
                activities.getElementsById('activities-title').textContent += `${city}`
                for (let i = 0; i < keys.length; i++) {
                    let title = rowData[keys[i]]['title'];
                    let price = rowData[keys[i]]['price'];
                    let desc = rowData[keys[i]]['desc'];
                    let image = getImageSrc(city, rowData[keys[i]]['image']);

                    document.querySelector('.chosen-activities').innerHTML += `
                        <div class="activity${image}">
                            <img id="activity-img" src="${image}">
                            <div class="activity-details">
                                <h2 id="activity-header">${title} - £${price}</h2>
                                <h4 id="activiyt-desc">${desc}</h4>
                            </div>
                        </div>`;
                }
            });

            const activityCollection = document.querySelector('.itinerary-activities');
            activityCollection.style.display = 'block';

            const body = document.querySelector('.main');
            body.style.filter = 'blur(2px)';
        }

        if (event.target.id == "exit-btn") {
            const activityCollection = document.querySelector('.itinerary-activities');
            activityCollection.style.display = 'none'

            const body = document.querySelector('.main');
            body.style.filter = 'none'
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