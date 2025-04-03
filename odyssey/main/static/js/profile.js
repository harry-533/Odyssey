document.addEventListener('DOMContentLoaded', function() {
    // Function that waits for clicks on the page
    document.addEventListener("click", function(event) {
        // If the click was the delete button on the itineraires
        if (event.target.id.startsWith("right-btn")) {
            itineraryId = event.target.id.slice(9)
            // Fetches the correct itinerary to delete it
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

        // If the Itinerary is clicked open up the extra details
        if (event.target.id == "itinerary-location") {
            document.querySelector('.activities').innerHTML = '';
            itineraryId = event.target.classList[0]
            
            // Gets the activities so they can be displayed
            getActivities(itineraryId).then(rowData => {
                const activities = document.querySelector('.itinerary-activities');
                keys = Object.keys(rowData);
                let city = rowData[keys[0]]['city'];
                activities.querySelector('#activities-title').textContent = `${document.body.dataset.username} - ${city}`;
                // Loops through the activities and displays them in a new popup
                for (let i = 0; i < keys.length; i++) {
                    let title = rowData[keys[i]]['title'];
                    let price = rowData[keys[i]]['price'];
                    let desc = rowData[keys[i]]['desc'];
                    let image = rowData[keys[i]]['image'];
                    let imageSrc = `/static/images/result/activityimg/${city.toLowerCase()}/${image}.png`

                    document.querySelector('.activities').innerHTML += `
                        <div class="activity">
                            <img id="activity-img" src="${imageSrc}">
                            <div class="activity-details">
                                <h2 id="activity-header">${title} - ${price}</h2>
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

        // Hides the popup if the exit button is clicked
        if (event.target.id == "exit-btn") {
            const activityCollection = document.querySelector('.itinerary-activities');
            activityCollection.style.display = 'none'

            const body = document.querySelector('.main');
            body.style.filter = 'none'
        }

        // If the change profile image button is pressed the form to change the image is shown
        if (event.target.id == "profile-img") {
            const userDetails = document.querySelector('.user-details');
            const imageForm = document.getElementById('img-form');

            if (userDetails.style.display == 'block') {
                userDetails.style.display = 'none';
                imageForm.style.display = 'block';
            } else {
                userDetails.style.display = 'block';
                imageForm.style.display = 'none';
            }
        }
    })
})

// Returns the activities for that paticular itinerary
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