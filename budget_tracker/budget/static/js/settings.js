const forms = document.querySelectorAll(".api-form");

function updateCategoryDropdown(categories) {
    var dropdown = document.getElementById("id_update_category-category_select");
    dropdown.innerHTML = "<option>-- Select Category --</option>";
    categories.forEach(function(item) {
        var option = document.createElement("option");
        option.value = item.id;
        option.innerHTML = item.name;
        dropdown.appendChild(option);
    });


    dropdown.selectedIndex = 0;
}


// Create new category
forms.forEach(function(currentForm) {
    currentForm.addEventListener("submit", function(event) {
        event.preventDefault();         // don't refresh page

        const clickedButton = event.submitter;
        console.log("event and clicked button: ");
        console.log(event);
        console.log(clickedButton);

        const targetURL = clickedButton ? clickedButton.getAttribute("data-endpoint") : null;
        console.log(targetURL);

        if (!targetURL || targetURL === null) {
            console.error("Aborted: The clicked button is missing its attribute \"data-endpoint\"!");
            return;
        }
        const formData = new FormData(currentForm);

        fetch(targetURL, {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => { throw errorData; })
            }
            return response.json();
        })
        .then(data => {
            console.log("Success package received for this form: ", data);
            currentForm.reset();

            var target = targetURL.split("/").filter(Boolean)[2];
            if (target === "category") {
                updateCategoryDropdown(data.categories);
                document.getElementById("id_update_category-name").value = "";
            }
        })
        .catch(errorPackage => {
            console.log("Validation failed or server error: ", errorPackage);
        })
    });
});


// Update textfield with selected option in dropdown
var categoryDropdown = document.getElementById("id_update_category-category_select");
var updateField = document.getElementById("id_update_category-name");

categoryDropdown.addEventListener("change", function() {
    if (this.selectedIndex == 0) {
        updateField.value = "";
        return;
    }

    const selectedName = this.options[this.selectedIndex].text;
    updateField.value = selectedName;
});


// Handle name update

