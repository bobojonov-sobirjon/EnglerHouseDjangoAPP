function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const hamburgerIcon = document.getElementById('hamburger-icon');
    const closeIcon = document.getElementById('close-icon');

    mobileMenu.classList.toggle('hidden');
    mobileMenu.classList.toggle('flex');
    hamburgerIcon.classList.toggle('hidden');
    closeIcon.classList.toggle('hidden');
}

function openFeedbackModal() {
    document.getElementById('feedbackModal').classList.remove('hidden');
    document.getElementById('feedbackModal').classList.add('flex');
}

function closeFeedbackModal() {
    document.getElementById('feedbackModal').classList.add('hidden');
    document.getElementById('feedbackModal').classList.remove('flex');
}

document.addEventListener('click', function (event) {
    const feedbackModal = document.getElementById('feedbackModal');

    if (event.target === feedbackModal) {
        closeFeedbackModal();
    }
});

AOS.init();