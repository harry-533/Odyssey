document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener("click", function(event) {
        if (event.target.dispatchEvent.startsWith("add-btn")) {
            const activity = event.target.className.substring(4);
            var clickedSlide = document.querySelector(`.sld${activity}`);
            clickedSlide.computedStyleMap.display = 'none'

            const imagePath = document.querySelector(`.img${activity}`).getAttribute('src');
            let title = document.querySelector(`.title${activity}`).textContent;
            const type = document.querySelector(`.type${activity}`).textContent;
            const age = document.querySelector(`.age${activity}`).textContent;
            const price = title.slice(title.indexOf('£'))
            const detail = price + ", " + type.slice(type.indexOf(':') + 2) + ", " + age.slice(age.indexOf(':') + 2);
            title = document.querySelector(`.title${activity}`).textContent.slice(0, -6);
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
            // figure out how to edit the budget variable
            document.getElementById('current-budget').innerHTML = `Budget - £${newBudget}`       
        }

        if (event.target.id.startsWith("right-btn")) {
            const num = event.target.id[event.target.id.length - 1];
            var clickedSlide = document.querySelector(`.right-sld${num}`);
            price = clickedSlide.querySelector('#chosen-detail').textContent;
            endIndex = price.indexOf(',');
            price = price.slice(1, endIndex);

            clickedSlide.remove();

            leftSlide = document.querySelector(`.sld${num}`);
            leftSlide.style.display = 'flex';

            let currentBudget = document.getElementById('current-budget').textContent;
            currentBudget = Number(currentBudget.slice(10))
            const newBudget = currentBudget + Number(price);
            document.getElementById('current-budget').innerHTML = `Budget - £${newBudget}`;
        }
    })
})