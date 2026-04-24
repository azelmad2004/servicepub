// Toggle between citizen and admin forms
document.querySelectorAll('.auth-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and forms
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));

        // Add active class to clicked tab and corresponding form
        tab.classList.add('active');
        document.getElementById(`${tab.dataset.tab}-form`).classList.add('active');
    });
});

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Password strength indicator
const passwordInput = document.getElementById('password-inscription');
if (passwordInput) {
    passwordInput.addEventListener('input', function() {
        const strengthBar = document.querySelector('.strength-bar');
        const strengthText = document.querySelector('.strength-text');
        const password = this.value;
        let strength = 0;

        if (password.length > 5) strength += 20;
        if (password.length > 7) strength += 20;
        if (/[A-Z]/.test(password)) strength += 20;
        if (/[0-9]/.test(password)) strength += 20;
        if (/[^A-Za-z0-9]/.test(password)) strength += 20;

        strengthBar.style.width = strength + '%';

        if (strength < 40) {
            strengthBar.style.backgroundColor = '#ff4d4d';
            strengthText.textContent = 'Faible';
        } else if (strength < 80) {
            strengthBar.style.backgroundColor = '#ffa64d';
            strengthText.textContent = 'Moyen';
        } else {
            strengthBar.style.backgroundColor = '#2a61c1';
            strengthText.textContent = 'Fort';
        }
    });
}

// Form submission
document.getElementById('citoyen-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Here you would normally handle the login request
    window.location.href = 'dashboard-citoyen.htm';
});

document.getElementById('administration-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Here you would normally handle the login request
    window.location.href = 'dashboard-administration.htm';
});

document.getElementById('inscription-citoyen-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Here you would normally handle the registration request
    alert('Inscription réussie! Vous allez être redirigé vers la page de connexion.');
    window.location.href = 'se_connecter.htm';
});

document.getElementById('inscription-administration-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Here you would normally handle the registration request
    alert('Demande d\'inscription envoyée! Votre compte sera activé après validation.');
});



// Contact form submission
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Simple form validation
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    if (name && email && subject && message) {
        // Simulate form submission
        alert('Votre message a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.');
        this.reset();
    } else {
        alert('Veuillez remplir tous les champs obligatoires.');
    }
});

// Password reset functionality
let countdownInterval;

function nextStep(step) {
    // Hide all steps
    document.querySelectorAll('.password-form').forEach(form => {
        form.classList.remove('active');
    });

    // Show current step
    document.getElementById(`step${step}-form`).classList.add('active');

    // Update step indicator
    document.querySelectorAll('.step').forEach(stepEl => {
        stepEl.classList.remove('active');
        if (parseInt(stepEl.dataset.step) <= step) {
            stepEl.classList.add('active');
        }
    });

    // Start countdown for step 2
    if (step === 2) {
        startCountdown();
    }
}

function startCountdown() {
    let countdown = 60;
    const countdownElement = document.getElementById('countdown');
    const resendLink = document.getElementById('resend-link');

    resendLink.style.pointerEvents = 'none';
    resendLink.style.opacity = '0.5';

    clearInterval(countdownInterval);

    countdownInterval = setInterval(() => {
        countdown--;
        countdownElement.textContent = countdown;

        if (countdown <= 0) {
            clearInterval(countdownInterval);
            resendLink.style.pointerEvents = 'auto';
            resendLink.style.opacity = '1';
            countdownElement.textContent = '';
        }
    }, 1000);
}

document.getElementById('resend-link').addEventListener('click', function(e) {
    e.preventDefault();
    startCountdown();
});

// Final password reset submission
document.getElementById('step3-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-new-password').value;

    if (newPassword !== confirmPassword) {
        alert('Les mots de passe ne correspondent pas.');
        return;
    }

    // Simulate password reset
    alert('Votre mot de passe a été réinitialisé avec succès! Vous pouvez maintenant vous connecter.');
    window.location.href = 'se_connecter.htm';
});

// Mobile menu toggle
document.getElementById('menuToggle').addEventListener('click', function() {
    const navList = document.getElementById('navList');
    navList.classList.toggle('show');
});

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const navList = document.getElementById('navList');
    const menuToggle = document.getElementById('menuToggle');

    if (!navList.contains(e.target) && !menuToggle.contains(e.target) && navList.classList.contains('show')) {
        navList.classList.remove('show');
    }
});



// Delivery options functionality
document.querySelectorAll('.delivery-option-card').forEach(card => {
    const header = card.querySelector('.option-header');
    header.addEventListener('click', () => {
        // Remove selected class from all cards
        document.querySelectorAll('.delivery-option-card').forEach(c => {
            c.classList.remove('selected');
        });

        // Add selected class to clicked card
        card.classList.add('selected');

        // Update radio button
        const radio = card.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }
    });
});

// Payment methods functionality
document.querySelectorAll('.payment-option-card').forEach(card => {
    card.addEventListener('click', () => {
        // Remove selected class from all cards
        document.querySelectorAll('.payment-option-card').forEach(c => {
            c.classList.remove('selected');
        });

        // Add selected class to clicked card
        card.classList.add('selected');

        // Update radio button
        const radio = card.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
            showPaymentForm(radio.id);
        }
    });
});

// Show appropriate payment form based on selection
function showPaymentForm(paymentMethodId) {
    // Hide all payment forms
    document.querySelectorAll('.payment-form').forEach(form => {
        form.style.display = 'none';
    });

    // Show selected payment form
    const formId = paymentMethodId.replace('payment-', '') + '-form';
    const selectedForm = document.getElementById(formId);
    if (selectedForm) {
        selectedForm.style.display = 'block';
    }
}

// Credit card number formatting
document.getElementById('card-number') ? addEventListener('input', function(e) {

    let value = e.target.value.replace(/\D/g, '');

    // Format as groups of 4 digits
    if (value.length > 0) {
        value = value.match(new RegExp('.{1,4}', 'g')).join(' ');
    }

    e.target.value = value;

    // Detect card type
    detectCardType(value);
});

// Card expiry date formatting
document.getElementById('card-expiry') ? addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');

    if (value.length > 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }

    e.target.value = value;
});

// Detect credit card type
function detectCardType(cardNumber) {
    const cardTypeIcon = document.querySelector('.card-type');
    if (!cardTypeIcon) return;

    const cleanNumber = cardNumber.replace(/\D/g, '');

    let cardType = 'credit-card';

    if (/^4/.test(cleanNumber)) {
        cardType = 'cc-visa';
    } else if (/^5[1-5]/.test(cleanNumber)) {
        cardType = 'cc-mastercard';
    } else if (/^3[47]/.test(cleanNumber)) {
        cardType = 'cc-amex';
    } else if (/^6(?:011|5)/.test(cleanNumber)) {
        cardType = 'cc-discover';
    }

    cardTypeIcon.className = `fas fa-${cardType}`;
}

// Agency selection change
document.getElementById('agency-select') ? addEventListener('change', function(e) {
    const agencyInfo = document.getElementById('agency-info');
    if (agencyInfo && e.target.value) {
        agencyInfo.style.display = 'block';
    } else if (agencyInfo) {
        agencyInfo.style.display = 'none';
    }
});

// Pay now button functionality
document.getElementById('pay-now') ? addEventListener('click', function() {
    const selectedPaymentMethod = document.querySelector('input[name="payment-method"]:checked');

    if (!selectedPaymentMethod) {
        alert('Veuillez sélectionner un mode de paiement');
        return;
    }

    // Validate form based on payment method
    let isValid = true;
    const paymentMethod = selectedPaymentMethod.id;

    if (paymentMethod === 'payment-card') {
        isValid = validateCardForm();
    } else if (paymentMethod === 'payment-mobile') {
        isValid = validateMobileForm();
    }

    if (isValid) {
        // Show loading state
        this.classList.add('loading');
        this.disabled = true;

        // Simulate payment processing
        setTimeout(() => {
            alert('Paiement traité avec succès! Votre document sera disponible sous peu.');
            window.location.href = 'confirmation.htm';
        }, 2000);
    }
});

// Validate credit card form
function validateCardForm() {
    const cardNumber = document.getElementById('card-number').value;
    const cardExpiry = document.getElementById('card-expiry').value;
    const cardCvv = document.getElementById('card-cvv').value;
    const cardHolder = document.getElementById('card-holder').value;

    if (!cardNumber || cardNumber.replace(/\D/g, '').length !== 16) {
        alert('Veuillez entrer un numéro de carte valide (16 chiffres)');
        return false;
    }

    if (!cardExpiry || !/^\d{2}\/\d{2}$/.test(cardExpiry)) {
        alert('Veuillez entrer une date d\'expiration valide (MM/AA)');
        return false;
    }

    if (!cardCvv || cardCvv.length !== 3) {
        alert('Veuillez entrer un code CVV valide (3 chiffres)');
        return false;
    }

    if (!cardHolder) {
        alert('Veuillez entrer le nom du titulaire de la carte');
        return false;
    }

    return true;
}

// Validate mobile payment form
function validateMobileForm() {
    const provider = document.getElementById('mobile-provider').value;
    const phoneNumber = document.getElementById('mobile-number').value;

    if (!provider) {
        alert('Veuillez sélectionner votre opérateur mobile');
        return false;
    }

    if (!phoneNumber || !/^0[6-7]\d{8}$/.test(phoneNumber)) {
        alert('Veuillez entrer un numéro de téléphone mobile valide');
        return false;
    }

    return true;
}

// Initialize payment forms
document.addEventListener('DOMContentLoaded', function() {
    // Show default payment form (credit card)
    showPaymentForm('payment-card');

    // Set up agency info
    const agencySelect = document.getElementById('agency-select');
    const agencyInfo = document.getElementById('agency-info');
    if (agencySelect && agencyInfo) {
        agencyInfo.style.display = agencySelect.value ? 'block' : 'none';
    }
});