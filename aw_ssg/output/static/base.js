document.addEventListener("DOMContentLoaded", function() {
        const animatedSections = document.querySelectorAll(".starry-background");

        animatedSections.forEach(section => {
            for (let i = 0; i < 100; i++) {
                const star = document.createElement("div");
                star.classList.add("star");
                star.style.left = `${Math.random() * 100}vw`;
                star.style.top = `${Math.random() * 2000}px`;
                star.style.width = `${Math.random() * 3}px`;
                star.style.height = star.style.width;
                star.style.animationDuration = `${Math.random() * 200 + 50}s`;
                section.appendChild(star);
            }
        });
    document.getElementById('nav-toggle').addEventListener('click', function() {
        const navMenu = document.getElementById('nav-menu');
        navMenu.classList.toggle('hidden');
        navMenu.classList.toggle('translate-x-full');
    });

    document.querySelector('.navbar-close').addEventListener('click', function(e) {
        e.preventDefault();
        const navMenu = document.getElementById('nav-menu');
        navMenu.classList.add('hidden');
        navMenu.classList.add('translate-x-full');
    });

    window.addEventListener('scroll', function() {
        const menu = document.getElementById('menu');
        if (window.scrollY > 50) {
            menu.classList.remove('menu-bg-transparent');
            menu.classList.add('menu-bg-base');
        } else {
            menu.classList.remove('menu-bg-base');
            menu.classList.add('menu-bg-transparent');
        }
    });

    const words = ["personalised", "perfect", "allround", "attractive"];
    const buttons = document.querySelectorAll(".cta-button");

    buttons.forEach(button => {
        let currentWordIndex = 0;
        const wordElement = button.querySelector(".word");

        function changeWord() {
            const nextWordIndex = (currentWordIndex + 1) % words.length;
            const nextWordElement = document.createElement("span");
            nextWordElement.textContent = words[nextWordIndex];
            nextWordElement.classList.add("word", "next-word");

            button.appendChild(nextWordElement);

            setTimeout(() => {
                wordElement.classList.add("slide-out");
                nextWordElement.classList.add("slide-in");

                setTimeout(() => {
                    wordElement.textContent = words[nextWordIndex];
                    wordElement.classList.remove("slide-out");
                    nextWordElement.remove();
                    currentWordIndex = nextWordIndex;
                }, 1000);
            }, 50);
        }

        setInterval(changeWord, 5000);
    });

    // Counter animation
    function animateCounter(element, start, end, duration) {
        let startTime = null;

        function step(currentTime) {
            if (!startTime) startTime = currentTime;
            const progress = Math.min((currentTime - startTime) / duration, 1);
            element.textContent = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                element.textContent = end + "+";
            }
        }

        window.requestAnimationFrame(step);
    }

    // IntersectionObserver to trigger animation when in viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const endValue = parseInt(element.getAttribute('data-target'));
                animateCounter(element, 0, endValue, 2000);
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.5  // Changed from 1.0 to 0.5 for earlier triggering
    });

    // Select all counter elements and observe them
    const counterElements = document.querySelectorAll('.counter');
    counterElements.forEach(element => {
        observer.observe(element);
    });

});
