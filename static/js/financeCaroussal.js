const container = document.querySelector('.carousel-container');

let isDragging = false;
let startX;
let scrollLeft;

container.addEventListener('mousedown', (e) => {
    isDragging = true;
    container.classList.add('dragging');
    startX = e.pageX - container.offsetLeft;
    scrollLeft = container.scrollLeft;
});

container.addEventListener('mouseleave', () => {
    isDragging = false;
    container.classList.remove('dragging');
});

container.addEventListener('mouseup', () => {
    isDragging = false;
    container.classList.remove('dragging');
});

container.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - container.offsetLeft;
    const walk = (x - startX) * 2; // Adjust scroll sensitivity
    container.scrollLeft = scrollLeft - walk;
});

// Add touch support for mobile
container.addEventListener('touchstart', (e) => {
    isDragging = true;
    startX = e.touches[0].pageX - container.offsetLeft;
    scrollLeft = container.scrollLeft;
});

container.addEventListener('touchend', () => {
    isDragging = false;
});

container.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    const x = e.touches[0].pageX - container.offsetLeft;
    const walk = (x - startX) * 2; // Adjust scroll sensitivity
    container.scrollLeft = scrollLeft - walk;
});
