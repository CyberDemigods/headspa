/* ===================================
   SLOW HEAD SPA - MAIN JS
   =================================== */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all modules
    initNavigation();
    initScrollEffects();
    initVoucherForm();
    initCookieBanner();
});

/* ===================================
   NAVIGATION
   =================================== */
function initNavigation() {
    const nav = document.getElementById('nav');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav__link');

    // Mobile menu toggle
    navToggle.addEventListener('click', () => {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Close menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Navbar scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            nav.classList.add('nav--scrolled');
        } else {
            nav.classList.remove('nav--scrolled');
        }

        lastScroll = currentScroll;
    });
}

/* ===================================
   SCROLL EFFECTS
   =================================== */
function initScrollEffects() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Fade in elements on scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Add fade-in class and observe elements
    const fadeElements = document.querySelectorAll(
        '.about__content, .about__image, .service-card, .pricing__category, .voucher__content, .voucher__form-container, .contact__info, .contact__map'
    );

    fadeElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });

    // Add CSS for fade-in animation
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);
}

/* ===================================
   VOUCHER FORM
   =================================== */
function initVoucherForm() {
    const form = document.getElementById('voucherForm');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Validate
        if (!data.voucherType) {
            showNotification('Wybierz rodzaj vouchera', 'error');
            return;
        }

        const gdprCheckbox = document.getElementById('gdprConsent');
        if (gdprCheckbox && !gdprCheckbox.checked) {
            showNotification('Zaakceptuj politykę prywatności i regulamin', 'error');
            return;
        }

        // Get price from selected option
        const select = document.getElementById('voucherType');
        const selectedOption = select.options[select.selectedIndex];
        const optionText = selectedOption.text;

        // Store data for payment processing
        const voucherData = {
            type: data.voucherType,
            typeName: optionText,
            buyerName: data.buyerName,
            buyerEmail: data.buyerEmail,
            recipientName: data.recipientName,
            message: data.message || ''
        };

        console.log('Voucher data:', voucherData);

        // Show confirmation and redirect to payment
        // In production, this would integrate with Przelewy24/PayU/Stripe
        showPaymentModal(voucherData);
    });
}

/* ===================================
   PAYMENT MODAL
   =================================== */
function showPaymentModal(voucherData) {
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
        <div class="modal">
            <button class="modal__close" aria-label="Zamknij">&times;</button>
            <h3 class="modal__title">Podsumowanie zamówienia</h3>
            <div class="modal__content">
                <div class="modal__row">
                    <span>Voucher:</span>
                    <strong>${voucherData.typeName}</strong>
                </div>
                <div class="modal__row">
                    <span>Dla:</span>
                    <strong>${voucherData.recipientName}</strong>
                </div>
                <div class="modal__row">
                    <span>Od:</span>
                    <strong>${voucherData.buyerName}</strong>
                </div>
                ${voucherData.message ? `
                <div class="modal__row modal__row--full">
                    <span>Dedykacja:</span>
                    <p>"${voucherData.message}"</p>
                </div>
                ` : ''}
            </div>
            <p class="modal__note">Wybierz metodę płatności:</p>
            <div class="modal__payments">
                <button class="modal__payment-btn" data-provider="przelewy24">
                    Przelewy24
                </button>
                <button class="modal__payment-btn" data-provider="payu">
                    PayU
                </button>
                <button class="modal__payment-btn" data-provider="stripe">
                    Karta płatnicza
                </button>
            </div>
            <p class="modal__disclaimer">
                Po opłaceniu voucher zostanie wysłany na adres: ${voucherData.buyerEmail}
            </p>
        </div>
    `;

    // Add modal styles
    const style = document.createElement('style');
    style.textContent = `
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(61, 52, 51, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
            padding: 1rem;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .modal {
            background: #FDF8F3;
            max-width: 500px;
            width: 100%;
            padding: 2rem;
            position: relative;
            animation: slideUp 0.3s ease;
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .modal__close {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            font-size: 2rem;
            cursor: pointer;
            color: #6B5E5A;
            line-height: 1;
        }
        .modal__close:hover { color: #3D3433; }
        .modal__title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: #3D3433;
        }
        .modal__content {
            background: #fff;
            padding: 1rem;
            margin-bottom: 1.5rem;
        }
        .modal__row {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #E8D5D0;
        }
        .modal__row:last-child { border-bottom: none; }
        .modal__row span { color: #6B5E5A; }
        .modal__row strong { color: #3D3433; }
        .modal__row--full {
            flex-direction: column;
            gap: 0.5rem;
        }
        .modal__row--full p {
            font-style: italic;
            color: #6B5E5A;
        }
        .modal__note {
            font-size: 0.875rem;
            color: #6B5E5A;
            margin-bottom: 1rem;
            text-align: center;
        }
        .modal__payments {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .modal__payment-btn {
            flex: 1;
            min-width: 120px;
            padding: 1rem;
            background: #8B4D5C;
            color: #fff;
            border: none;
            cursor: pointer;
            font-family: inherit;
            font-size: 0.875rem;
            font-weight: 500;
            transition: background 0.3s ease;
        }
        .modal__payment-btn:hover { background: #6B3A47; }
        .modal__disclaimer {
            margin-top: 1.5rem;
            font-size: 0.75rem;
            color: #6B5E5A;
            text-align: center;
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';

    // Close modal
    const closeModal = () => {
        overlay.remove();
        document.body.style.overflow = '';
    };

    overlay.querySelector('.modal__close').addEventListener('click', closeModal);
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal();
    });

    // Payment buttons
    overlay.querySelectorAll('.modal__payment-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const provider = btn.dataset.provider;
            processPayment(provider, voucherData);
        });
    });
}

/* ===================================
   PAYMENT PROCESSING
   =================================== */
function processPayment(provider, voucherData) {
    // In production, this would:
    // 1. Send data to your backend
    // 2. Create payment session with chosen provider
    // 3. Redirect to payment gateway

    console.log(`Processing payment with ${provider}:`, voucherData);

    // For demo purposes, show a message
    showNotification(
        `Przekierowanie do ${provider}... (demo)`,
        'success'
    );

    // Simulate redirect
    setTimeout(() => {
        alert(`W wersji produkcyjnej nastąpi przekierowanie do ${provider}.\n\nDane zamówienia:\n${JSON.stringify(voucherData, null, 2)}`);
    }, 1000);
}

/* ===================================
   NOTIFICATIONS
   =================================== */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;

    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 1rem 2rem;
            background: #3D3433;
            color: #FDF8F3;
            font-size: 0.875rem;
            z-index: 3000;
            animation: slideIn 0.3s ease, slideOut 0.3s ease 2.7s forwards;
        }
        .notification--success { background: #4A7C59; }
        .notification--error { background: #8B4D5C; }
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(notification);

    setTimeout(() => notification.remove(), 3000);
}

/* ===================================
   COOKIE BANNER
   =================================== */
function initCookieBanner() {
    const banner = document.getElementById('cookieBanner');
    if (!banner) return;

    const consent = localStorage.getItem('cookieConsent');
    if (consent) return;

    // Show banner after a short delay
    setTimeout(() => {
        banner.classList.add('visible');
    }, 1000);

    const acceptBtn = document.getElementById('cookieAccept');
    const rejectBtn = document.getElementById('cookieReject');

    if (acceptBtn) {
        acceptBtn.addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'accepted');
            banner.classList.remove('visible');
        });
    }

    if (rejectBtn) {
        rejectBtn.addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'essential');
            banner.classList.remove('visible');
        });
    }
}
