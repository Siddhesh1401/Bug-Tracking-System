document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signup-form");

    function validateField(input) {
        const errorDiv = document.getElementById(`${input.id}-error`);
        errorDiv.textContent = "";
        input.classList.remove("error");

        if (!input.validity.valid) {
            let message = input.validationMessage;
            if (input.validity.valueMissing) {
                message = `Please enter your ${input.name}`;
            }
            errorDiv.textContent = message;
            input.classList.add("error");
            return false;
        }
        return true;
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        let isValid = true;

        // Validate all required inputs
        form.querySelectorAll("input[required]").forEach(input => {
            if (!validateField(input)) isValid = false;
        });

        // Validate gender
        const genderInputs = document.querySelectorAll('input[name="gender"]');
        const genderError = document.getElementById("gender-error");
        if (![...genderInputs].some(input => input.checked)) {
            genderError.textContent = "Please select a gender";
            isValid = false;
        } else {
            genderError.textContent = "";
        }

        if (isValid) {
            console.log("Form submitted successfully!");
        }
    });
});
