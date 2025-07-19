// Simply display an alert if no input is provided
function validateForm() {
    const url = document.getElementById('url').value.trim();

    // Check if the input is empty
    if (!url) {
        alert('Please enter a URL');
        return false;
    }

    // Basic URL validation using Regex
    const pattern = /^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}.*$/;
    if (!pattern.test(url)) {
        alert('Please enter a valid URL');
        return false;
    }

    return true; // If everything is fine, allow form submission
}

// This function is going to copy the URL and temporarily change the icon to a check
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        const icon = document.getElementById('copy-icon');
        // Change the icons
        icon.classList.remove('fa-copy');
        icon.classList.add('fa-check');
        // Now change the icons back after 2 seconds
        setTimeout(() => {
            icon.classList.remove('fa-check');
            icon.classList.add('fa-copy');
        }, 2000);
    }).catch((err) => {
        console.error('Failed to copy text: ', err);
    });
}