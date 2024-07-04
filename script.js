const form = document.getElementById('upload-form');
const resultsContainer = document.getElementById('results');
const imageContainer = document.querySelector('.image-container');
const paletteContainer = document.getElementById('palette-container');
const errorMessage = document.getElementById('error-message');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const fileInput = document.getElementById('image-upload');
  const file = fileInput.files[0];

  if (!file) {
    errorMessage.textContent = 'Please select an image to analyze.';
    return;
  }

  const reader = new FileReader();
  reader.readAsDataURL(file);

  reader.onload = () => {
    const image = document.createElement('img');
    image.src = reader.result;
    imageContainer.innerHTML = '';
    imageContainer.appendChild(image);

    // Send the image data to the Python backend for processing
    // (explained in the next step)

    paletteContainer.textContent = 'Generating Palette...';
  };
});
