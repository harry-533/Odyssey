document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".selected").addEventListener("click", function() {
        document.querySelector(".options").style.display = 
            document.querySelector(".options").style.display === "block" ? "none" : "block";
    });
    
    document.querySelectorAll(".option").forEach(option => {
        option.addEventListener("click", function() {
            document.querySelector(".selected").textContent = this.textContent;
            document.querySelector(".options").style.display = "none";
            document.querySelector("#selected_option").value = this.textContent.split(' - ')[1];
            document.querySelector("#selected_option1").value = this.textContent.split(' - ')[0];
        });
    });
});