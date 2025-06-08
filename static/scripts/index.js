const images = document.querySelectorAll('.image-showcase img');
let currentIndex = 0;

function cycleImages() {
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].classList.add('active');
  }

  // Set initial image
images[0].classList.add('active');
  
  // Start cycling images
setInterval(cycleImages, 4000);