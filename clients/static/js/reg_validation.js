function validateForm(event) {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorBox = document.getElementById("errors");
    errorBox.innerHTML = "";

    const errors = [];

    if (!/^[\w]{3,30}$/.test(username)) {
        errors.push("Имя пользователя должно быть от 3 до 30 символов и содержать только буквы, цифры и _");
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.push("Введите корректный email.");
    }

    if (password.length < 8) {
        errors.push("Пароль должен содержать минимум 8 символов.");
    }
    if (!/[A-Z]/.test(password)) {
        errors.push("Пароль должен содержать хотя бы одну заглавную букву.");
    }
    if (!/[a-z]/.test(password)) {
        errors.push("Пароль должен содержать хотя бы одну строчную букву.");
    }
    if (!/[0-9]/.test(password)) {
        errors.push("Пароль должен содержать хотя бы одну цифру.");
    }
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(password)) {
        errors.push("Пароль должен содержать хотя бы один спецсимвол.");
    }

    if (errors.length > 0) {
        event.preventDefault();
        errors.forEach(err => {
            const p = document.createElement("p");
            p.style.color = "red";
            p.innerText = err;
            errorBox.appendChild(p);
        });
    }
}

window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("regForm").addEventListener("submit", validateForm);
});
