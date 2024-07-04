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

    // Send the image data to the Python backend for processing (explained next)
    fetch('/analyze', {
      method: 'POST',
      body: file
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        errorMessage.textContent = data.error;
        return;
      }
      displayPalette(data.classifications);
    })
    .catch(error => {
      errorMessage.textContent = 'An error occurred while processing the image.';
      console.error(error);
    });
  };
});

function displayPalette(classifications) {
  paletteContainer.innerHTML = '';
  for (const classification of classifications) {
    const colorDiv = document.createElement('div');
    colorDiv.classList.add('color-box');
    colorDiv.style.backgroundColor = `rgb(${classification.color.join(', ')})`;

    const colorInfo = document.createElement('p');
    colorInfo.textContent = `Season: ${classification.season_type}, Saturation: ${classification.saturation_level}, Temperature: ${classification.temperature}`;
    colorDiv.appendChild(colorInfo);

    paletteContainer.appendChild(colorDiv);
  }
}

