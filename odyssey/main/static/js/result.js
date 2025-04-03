document.addEventListener('DOMContentLoaded', function() {
    // Displays the weather widget for the correct city
    document.querySelector(`.weather-${document.body.dataset.city.toLowerCase().replaceAll(" ", "")}`).style.display = 'flex';

    document.addEventListener("click", function(event) {
        // If the button to add the activity to the itinerary is clicked
        if (event.target.id.startsWith("add-btn")) {
            const activity = event.target.className.substring(4);
            var clickedSlide = document.querySelector(`.${activity}`);
            clickedSlide.style.display = 'none'

            // Stores all the activities details
            const imagePath = document.querySelector(`.img${activity}`).getAttribute('src');
            let title = document.querySelector(`.title${activity}`).textContent;
            const type = document.querySelector(`.type${activity}`).textContent;
            const age = document.querySelector(`.age${activity}`).textContent;
            const price = title.slice(title.indexOf('£'))
            const detail = price + ", " + type.slice(type.indexOf(':') + 2) + ", " + age.slice(age.indexOf(':') + 2);
            title = document.querySelector(`.title${activity}`).textContent.slice(0, (title.indexOf('£')-3));
            const desc = document.querySelector(`.short-desc${activity}`).textContent;

            // Uses the saved details to create a summary that is added to the right section of the page
            document.querySelector('.chosen-activities').innerHTML += `
            <div class="chosen right-sld${activity}">
                <div class="chosen-img">
                    <img id="chosen-img" src="${imagePath}">
                </div>
                <div class="chosen-info">
                    <div class="chosen-header">
                        <h1 id="chosen-title">${title}</h1>
                        <i class="fa fa-minus" id="right-btn${activity}"></i>
                    </div>
                    <h1 id="chosen-detail">${detail}</h1>
                    <p id="chosen-desc">${desc}</p>
                </div>
            </div>`;

            // Decrements the budget by the cost of the activity
            let currentBudget = document.getElementById('current-budget').textContent;
            currentBudget = Number(currentBudget.slice(10))
            const newBudget = currentBudget - Number(price.slice(1))
            if (newBudget < 0) {
                document.getElementById('current-budget').style.color = 'red';
            }
            document.getElementById('current-budget').innerHTML = `Budget - £${newBudget}`
            
        // If the delete button of the chosen activity is clicked
        } else if (event.target.id.startsWith("right-btn")) {
            const activity = event.target.id.substring(9);
            var clickedSlide = document.querySelector(`.right-sld${activity}`);
            price = clickedSlide.querySelector('#chosen-detail').textContent;
            endIndex = price.indexOf(',');
            price = price.slice(1, endIndex);
            // Removes the slide that activity that was clicked
            clickedSlide.remove();

            // Displays the activity back in the results section
            leftSlide = document.querySelector(`.${activity}`);
            leftSlide.style.display = 'flex';

            // Increments the budget by the cost of the deleted activity
            let currentBudget = document.getElementById('current-budget').textContent;
            currentBudget = Number(currentBudget.slice(10))
            const newBudget = currentBudget + Number(price);
            if (newBudget >= 0) {
                document.getElementById('current-budget').style.color = 'black';
            }
            document.getElementById('current-budget').innerHTML = `Budget - £${newBudget}`;
        // If the itinerary save button is clicked
        } else if (event.target.id.startsWith("btn-save")) {
            const userId = document.body.dataset.userId;
            // If the user is not logged in it cannot be saved
            if (!userId) {
                pass
            // If the user is logged in
            } else {
                // Stores all the information about the itinerary (cost, dates, activities)
                const city = document.body.dataset.city;
                const country = document.body.dataset.country;
                const currentBudget = document.getElementById('current-budget').textContent.split(' - £')[1];
                const originalBudget = document.body.dataset.budget;
                const cost = originalBudget - currentBudget;
                const departure = document.body.dataset.arrive
                const arrival = document.body.dataset.depart
                let activities = [];
                document.querySelectorAll('.chosen').forEach((activity) => {
                    console.log(activity)
                    const current_activity = activity.classList[1].substring(9)
                    activities.push(current_activity)
                })

                const data = {
                    user_id: userId,
                    activity_ids: activities,
                    city: city,
                    country: country,
                    cost: cost,
                    departure: departure,
                    arrival: arrival
                };

                // Adds the itinerary to the database for that user
                fetch("/add-row/", {
                    method: "POST",
                    headers: {
                        // "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Success:", data);
                    alert("Itinerary added");
                    location.reload()
                })
                .catch(error => {
                    console.error("Error:", error);
                })
            }
            
        }
    })

    const fitlerForm = document.getElementById('filter-form');

    // When the filter form is changed it reloads the activities based on the filter
    fitlerForm.addEventListener('change', function() {
        // Stores the values in the filter form
        const minPrice = Number(document.querySelector('#price-dropdown-left').value);
        const maxPrice = Number(document.querySelector('#price-dropdown-right').value);
        const activityType = document.querySelector('#dropdown:nth-of-type(1)').value;
        const minAccessibility = Number(document.querySelector('#dropdown:nth-of-type(2)').value);
        const minPopularity = Number(document.querySelector('#dropdown:nth-of-type(3)').value);
        // Loops through all the activities
        document.querySelectorAll('.activity').forEach((activity) => {
            const current_activity = activity.classList[1]
            if (!document.querySelector(`.right-sld${current_activity}`)) {
                activity.style.display = 'flex'
            }

            // Stores the data from the activity
            let title = activity.querySelector(`.title${current_activity}`).textContent;
            let price = Number(title.slice(title.indexOf('£') + 1));
            let type = activity.querySelector(`.type${current_activity}`).textContent;
            type = type.slice(type.indexOf(':') + 2);
            let accessibility = activity.querySelector(`.access${current_activity}`).textContent;
            accessibility = accessibility.split(' ')[1].replace(/[\r\n]+/gm, "");
            let accessList = ['Limited', 'Partially', 'Fully'];
            accessibility = accessList.indexOf(accessibility);
            let popularity = activity.querySelector(`.popular${current_activity}`).textContent;
            popularity = popularity.split('⭐').length - 1

            // If the activity falls outside the filter it is hidden
            if (price < minPrice || price > maxPrice || popularity < minPopularity || (type != activityType && activityType != 'None') || accessibility < minAccessibility) {
                console.log(2)
                activity.style.display = 'none'
            }
        })
    })

    // Function that checks for a key press
    document.addEventListener('keydown', (event) => {
        const keyPressed = event.key;
        // If the key pressed is the enter key
        if (keyPressed == 'Enter') {
            // The value of the Search is stored and the search bar is cleared
            const searchInput = document.getElementById('search-bar').value;
            document.getElementById('search-bar').value = "";

            // Loops through the activities, hides any that do not include the searched term
            document.querySelectorAll('.activity').forEach((activity) => {
                const currentActivity = activity.classList[1];
                if (document.querySelector(`.${currentActivity}`).style.display === "none") {
                    activity.style.display = 'flex';
                }

                let title = activity.querySelector(`.title${currentActivity}`).textContent.toLowerCase();
                if (!title.includes(searchInput.toLowerCase())) {
                    activity.style.display = 'none';
                }
            })
        }
    })
});

// Function to sort the activities
function sortSubmit(sel) {
    const activitiesContainer = document.querySelector('.activities');
    const activities = Array.from(document.querySelectorAll('.activity'));
    const sortBy = sel;

    // Sorts all the activities based on the chosen sort
    activities.sort((a, b) => {
        if (sortBy == 'low-high') {
            const titleA = a.querySelector('#activity-title').textContent;
            const priceA = Number(titleA.slice(titleA.indexOf('£') + 1));
            const titleB = b.querySelector('#activity-title').textContent;
            const priceB = Number(titleB.slice(titleB.indexOf('£') + 1));
            return priceA - priceB;
        } else if (sortBy == 'high-low') {
            const titleA = a.querySelector('#activity-title').textContent;
            const priceA = Number(titleA.slice(titleA.indexOf('£') + 1));
            const titleB = b.querySelector('#activity-title').textContent;
            const priceB = Number(titleB.slice(titleB.indexOf('£') + 1));
            return priceB - priceA;
        } else {
            let popularityA = a.querySelector('#popularity').textContent;
            popularityA = popularityA.split('⭐').length - 1;
            let popularityB = b.querySelector('#popularity').textContent;
            popularityB = popularityB.split('⭐').length - 1;
            return popularityB - popularityA
        }
    });

    activitiesContainer.innerHTML = '';
    activities.forEach(activity => activitiesContainer.appendChild(activity));
}

// function getCSRFToken() {
//     return document.querySelector("[name=csrfmiddlewaretoken]").value;
// }