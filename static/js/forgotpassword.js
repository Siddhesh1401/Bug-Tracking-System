async function sendVerificationCode() {
    const email = document.getElementById("email").value;
    
    if (!email) {
        alert("Please enter your email address.");
        return;
    }

    try {
        const response = await fetch("/forgot-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email })
        });

        const data = await response.json();
        alert(data.message);

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to send verification code.");
    }
}

async function verifyCode() {
    const code = document.getElementById("verification-code").value;

    if (code.length !== 6) {
        alert("Please enter a valid 6-digit code.");
        return;
    }

    try {
        const response = await fetch("/verify-code", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ verification_code: code })
        });

        const data = await response.json();
        alert(data.message);

        if (response.ok) {
            window.location.href = "/reset-password";
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to verify code.");
    }
}

// Password Reset Function
document.querySelector(".reset-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const newPassword = document.getElementById("new-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    if (newPassword !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    try {
        const response = await fetch("/reset-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                new_password: newPassword,
                confirm_password: confirmPassword
            })
        });

        const data = await response.json();
        alert(data.message);

        if (response.ok) {
            window.location.href = "/login";
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to reset password.");
    }
});
