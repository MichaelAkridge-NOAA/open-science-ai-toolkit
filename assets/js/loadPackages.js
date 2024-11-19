fetch('packages.json')
  .then(response => response.json())
  .then(data => {
    const selector = document.getElementById('packageSelector');
    data.forEach(pkg => {
      const option = document.createElement('option');
      option.value = pkg.name; // Use the package name as the value
      option.textContent = pkg.name; // Also use the name as the text content
      selector.appendChild(option);
    });
  })
  .catch(error => console.error('Failed to load packages:', error));

