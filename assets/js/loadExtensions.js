fetch('extensions.json')  // 
  .then(response => response.json())
  .then(data => {
    const selector = document.getElementById('extensionSelector');
    data.forEach(ext => {
      const option = document.createElement('option');
      option.value = ext;
      option.textContent = ext;
      selector.appendChild(option);
    });
  })
  .catch(error => console.error('Failed to load extensions:', error));