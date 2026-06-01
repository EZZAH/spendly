// Logout confirmation modal
function showLogoutModal() {
    const modal = document.getElementById('logoutModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeLogoutModal() {
    const modal = document.getElementById('logoutModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function confirmLogout() {
    const form = document.getElementById('logoutForm');
    if (form) {
        form.submit();
    }
}

// Close modal when clicking on overlay
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('logoutModal');
    const overlay = document.querySelector('.modal-overlay');

    if (overlay) {
        overlay.addEventListener('click', closeLogoutModal);
    }
});
