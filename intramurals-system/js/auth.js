function login() {
    const email = document.getElementById("email").value.trim();
    const pass = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    if (!email || !pass) {
        alert("Fill all fields");
        return;
    }

    const atIndex = email.indexOf("@");
    if (atIndex === -1) {
        alert("Enter a valid email address");
        return;
    }

    const localName = email.slice(0, atIndex);
    const domain = email.slice(atIndex + 1).toLowerCase();

    if (role === "Student") {
        if (domain !== "student.com") {
            alert("Student role requires an @student.com account");
            return;
        }
    } else if (role === "Admin") {
        if (domain !== "admin.com") {
            alert("Admin role requires an @admin.com account");
            return;
        }
    }

    localStorage.setItem("user", JSON.stringify({ name: localName, email, role }));

    if (role === "Admin") {
        window.location.href = "admin-dashboard.html";
    } else {
        window.location.href = "student-dashboard.html";
    }
}