document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".choose-us-box, .choose-us-image, h2");

    function checkScroll() {
        elements.forEach((element) => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elementTop < windowHeight - 50) {
                element.classList.add("visible");
            }
        });
    }

    window.addEventListener("scroll", checkScroll);
    checkScroll(); // Run on page load
});
// Open & Close Modal


