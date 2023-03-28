// anti spambot email descrambler
window.addEventListener('load', (event) => {
    var encMail = "ZGlya0BkaXJrbWVlci5jb20="
    const form = document.getElementById('contact')
    form.setAttribute("href", "mailto:".concat(atob(encMail)));
})