document.addEventListener("DOMContentLoaded", function() {
    // function for when the destination dropdown was clicked
    document.querySelector(".selected").addEventListener("click", function() {
        // sets the options to display if they are not already, and hides them if they are shown currently
        document.querySelector(".options").style.display = 
            document.querySelector(".options").style.display === "block" ? "none" : "block";
    });
    
    // function for if any of the options from the destinations are clicked
    document.querySelectorAll(".option").forEach(option => {
        option.addEventListener("click", function() {
            // The chosen city is saved to selected and the options are hidden
            document.querySelector(".selected").textContent = this.textContent;
            document.querySelector(".options").style.display = "none";
            document.querySelector("#selected_option").value = this.textContent.split(' - ')[1];
            document.querySelector("#selected_option1").value = this.textContent.split(' - ')[0];
        });
    });
});