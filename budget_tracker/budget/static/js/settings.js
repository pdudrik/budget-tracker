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


function updateSubcategoryDropdown() {
    return;
}


// Multi-purpose function which handles post requests - create, update, delete
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

            else if (target === "subcategory") {
                updateSubcategoryDropdown(data.subcategories);
                // document.getElementById()
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

//------------ SECTION SUBCATEGORY ------------//
// Filter subcategories based on selected category (parent) in updating name
document.addEventListener("DOMContentLoaded", function() {
    const allSubcategories = JSON.parse(document.getElementById("subcategories-data").textContent);
    const subCategoryDropdown = document.getElementById("id_update_subcategory-category");
    const subcategoryDropdownField = document.getElementById("id_update_subcategory-name");
    
    console.log(allSubcategories);
    console.log(subCategoryDropdown);
    console.log(subcategoryDropdownField);

    subCategoryDropdown.selectedIndex = 0;
    subcategoryDropdown = document.getElementById("id_update_subcategory-subcategory");
    
    function filterSubcategories() {
        subcategoryDropdown.innerHTML = "<option>-- Select subcategory --</option>";
        subcategoryDropdownField.value = "";      // clean field after selecting other category

        const selectedCategoryId = subCategoryDropdown.value;
        const filteredSubcategories = allSubcategories.filter(sub => sub.category_id == selectedCategoryId);
        
        console.log("Filtered subcategories: ", filteredSubcategories);

        filteredSubcategories.forEach(sub => {
            const option = document.createElement("option");
            option.value = sub.id;
            option.textContent = sub.name
            subcategoryDropdown.appendChild(option);       
        });
        
        console.log(subcategoryDropdown);
        subcategoryDropdown.selectedIndex = 0;
    }

    subCategoryDropdown.addEventListener("change", filterSubcategories);
    filterSubcategories();


});


// Update text in input based on selected subcategory to be updated
document.addEventListener("DOMContentLoaded", function() {

    var subcategoryDropdown = document.getElementById("id_update_subcategory-subcategory");
    var updateSubcategoryField = document.getElementById("id_update_subcategory-name");
    
    subcategoryDropdown.addEventListener("change", function() {
        console.log("changed subcategory dropdown option");
        if (this.selectedIndex == 0) {
            updateSubcategoryField.value = "";
            return
        }
        
        const selectedName = this.options[this.selectedIndex].text;
        updateSubcategoryField.value = selectedName;
    });
});

