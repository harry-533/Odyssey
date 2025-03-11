document.addEventListener('DOMContentLoaded', function() {
    const urlCity = window.location.href.split('/')[4];
    document.querySelector(`.weather-${urlCity}`).style.display = 'flex';

    document.addEventListener("click", function(event) {
        if (event.target.id.startsWith("add-btn")) {
            const activity = event.target.className.substring(4);
            var clickedSlide = document.querySelector(`.${activity}`);
            clickedSlide.style.display = 'none'

            const imagePath = document.querySelector(`.img${activity}`).getAttribute('src');
            let title = document.querySelector(`.title${activity}`).textContent;
            const type = document.querySelector(`.type${activity}`).textContent;
            const age = document.querySelector(`.age${activity}`).textContent;
            const price = title.slice(title.indexOf('£'))
            const detail = price + ", " + type.slice(type.indexOf(':') + 2) + ", " + age.slice(age.indexOf(':') + 2);
            title = document.querySelector(`.title${activity}`).textContent.slice(0, (title.indexOf('£')-3));
            const desc = document.querySelector(`.short-desc${activity}`).textContent;

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

            let currentBudget = document.getElementById('current-budget').textContent;
            currentBudget = Number(currentBudget.slice(10))
            const newBudget = currentBudget - Number(price.slice(1))
            if (newBudget < 0) {
                document.getElementById('current-budget').style.color = 'red';
            }
            document.getElementById('current-budget').innerHTML = `Budget - £${newBudget}`       
        } else if (event.target.id.startsWith("right-btn")) {
            const activity = event.target.id.substring(9);
            var clickedSlide = document.querySelector(`.right-sld${activity}`);
            price = clickedSlide.querySelector('#chosen-detail').textContent;
            endIndex = price.indexOf(',');
            price = price.slice(1, endIndex);

            clickedSlide.remove();

            leftSlide = document.querySelector(`.${activity}`);
            leftSlide.style.display = 'flex';

            let currentBudget = document.getElementById('current-budget').textContent;
            currentBudget = Number(currentBudget.slice(10))
            const newBudget = currentBudget + Number(price);
            if (newBudget >= 0) {
                document.getElementById('current-budget').style.color = 'black';
            }
            document.getElementById('current-budget').innerHTML = `Budget - £${newBudget}`;
        } else if (event.target.id.startsWith("btn-save")) {
            const userId = document.body.dataset.userId;
            if (!userId) {
                pass
            } else {
                const city = document.body.dataset.city;
                const currentBudget = document.getElementById('current-budget').textContent;
                const originalBudget = document.body.dataset.budget;
                const cost = originalBudget - currentBudget;
                const depature = 'get from home'
                const arrival = 'get from home'
                const name = "user input"
                let activities = [];
                document.querySelectorAll('.chosen-activities').forEach((activity) => {
                    const current_activity = activity.querySelector('.chosen').classList[1].substring(9)
                    activities.push(current_activity)
                })

                const data = {
                    user_id: userId,
                    name: name,
                    activity_ids: activities,
                    city: city,
                    cost: cost,
                    depature: depature,
                    arrival: arrival
                };

                fetch("/add-row/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Success:", data);
                })
                .catch(error => {
                    console.error("Error:", error);
                })
            }
            
        }
    })

    const fitlerForm = document.getElementById('filter-form');

    fitlerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const minPrice = Number(document.querySelector('#price-dropdown-left').value);
        const maxPrice = Number(document.querySelector('#price-dropdown-right').value);
        const activityType = document.querySelector('#dropdown:nth-of-type(1)').value;
        const minAccessibility = Number(document.querySelector('#dropdown:nth-of-type(2)').value);
        const minPopularity = Number(document.querySelector('#dropdown:nth-of-type(3)').value);
        document.getElementById("filter-form").reset();

        document.querySelectorAll('.activity').forEach((activity) => {
            const current_activity = activity.classList[1]
            if (!document.querySelector(`.right-sld${current_activity}`)) {
                activity.style.display = 'flex'
            }

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

            if (price < minPrice || price > maxPrice || popularity < minPopularity || (type != activityType && activityType != 'None') || accessibility < minAccessibility) {
                activity.style.display = 'none'
            }
        })
    })

    document.addEventListener('keydown', (event) => {
        const keyPressed = event.key;
        if (keyPressed == 'Enter') {
            const searchInput = document.getElementById('search-bar').value;
            document.getElementById('search-bar').value = "";

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

function sortSubmit(sel) {
    const activitiesContainer = document.querySelector('.activities');
    const activities = Array.from(document.querySelectorAll('.activity'));
    const sortBy = sel;

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