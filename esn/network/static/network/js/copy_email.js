document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', () => {
            const email = button.getAttribute('data-email');
            navigator.clipboard.writeText(email);
        });
    });
});