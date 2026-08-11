document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".signup-form");
    const phoneInput = document.getElementById("phone");
    const phoneError = document.getElementById("phone-error");

    // Validate Indian Phone Number Format
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        
        const phoneRegex = /^\+91\s\d{5}\s\d{5}$/; // Format: +91 XXXXX XXXXX
        
        if (!phoneRegex.test(phoneInput.value)) {
            phoneError.textContent = "Please enter a valid Indian phone number (+91 XXXXX XXXXX)";
            return;
        } else {
            phoneError.textContent = "";
        }

        alert("Form submitted successfully!");
    });
});
