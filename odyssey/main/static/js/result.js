document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener("click", function(event) {
        if (event.target.id.startsWith("add-btn")) {
            const num = event.target.className[event.target.className.length - 1];
            var clickedSlide = document.querySelector(`.sld${num}`);
            clickedSlide.style.display = 'none';

            const imagePath = document.querySelector(`.img${num}`).getAttribute('src');
            let title = document.querySelector(`.title${num}`).textContent;
            const type = document.querySelector(`.type${num}`).textContent;
            const age = document.querySelector(`.age${num}`).textContent;
            const detail = title.slice(title.indexOf('£')) + ", " + type.slice(type.indexOf(':') + 2) + ", " + age.slice(age.indexOf(':') + 2);
            title = document.querySelector(`.title${num}`).textContent.slice(0, -6);
            const desc = document.querySelector(`.desc${num}`).textContent;
     
            document.querySelector('.chosen-activities').innerHTML += `
            <div class="chosen right-sld${num}">
                <div class="chosen-img">
                    <img id="chosen-img" src="${imagePath}">
                </div>
                <div class="chosen-info">
                    <div class="chosen-header">
                        <h1 id="chosen-title">${title}</h1>
                        <i class="fa fa-minus" id="right-btn${num}"></i>
                    </div>
                    <h1 id="chosen-detail">${detail}</h1>
                    <p id="chosen-desc">${desc}</p>
                </div>
            </div>`;
        }

        if (event.target.id.startsWith("right-btn")) {
            const num = event.target.id[event.target.id.length - 1];
            var clickedSlide = document.querySelector(`.right-sld${num}`)
            clickedSlide.remove();

            leftSlide = document.querySelector(`.sld${num}`);
            leftSlide.style.display = 'flex';
        }
    });

    const fitlerForm = document.getElementById('filter-form');

    fitlerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const minPrice = Number(document.querySelector('#price-dropdown-left').value);
        const maxPrice = Number(document.querySelector('#price-dropdown-right').value);
        const activityType = document.querySelector('#dropdown:nth-of-type(1)').value;
        const minAccessibility = Number(document.querySelector('#dropdown:nth-of-type(2)').value);
        const minPopularity = Number(document.querySelector('#dropdown:nth-of-type(3)').value);
        document.getElementById("filter-form").reset();

        document.querySelectorAll('.activity').forEach((activity, index) => {
            const num = activity.classList[1].slice(-1)
            if (!document.querySelector(`.right-sld${num}`)) {
                activity.style.display = 'flex'
            }

            let title = activity.querySelector(`.title${index + 1}`).textContent;
            let price = Number(title.slice(title.indexOf('£') + 1));
            let type = activity.querySelector(`.type${index + 1}`).textContent;
            type = type.slice(type.indexOf(':') + 2)
            let accessibility = activity.querySelector(`.access${index + 1}`).textContent;
            accessibility = accessibility.split(' ')[1]
            let accessList = ['Limited', 'Partially', 'Fully']
            accessibility = accessList.indexOf(accessibility) 
            let popularity = activity.querySelector(`.popular${index + 1}`).textContent;
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

            document.querySelectorAll('.activity').forEach((activity, index) => {
                const num = activity.classList[1].slice(-1)
                if (!document.querySelector(`.right-sld${num}`)) {
                    activity.style.display = 'flex'
                }

                let title = activity.querySelector(`.title${index + 1}`).textContent.toLowerCase();
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