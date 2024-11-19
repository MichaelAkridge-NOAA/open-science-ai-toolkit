// Configuration for GCS bucket listing
var API_ENDPOINT = 'https://www.googleapis.com/storage/v1/b/nmfs_odp_pifsc/o';
var GCSB_ROOT_DIR = ''; // Root directory
var AUTO_TITLE = true;

// Set the document title automatically
if (AUTO_TITLE) {
  document.title = location.hostname;
}

// Fetch and display bucket data for the specified directory
function getBucketData(directory = '', isSubdirectory = false) {
  const url = `${API_ENDPOINT}?prefix=${directory}&delimiter=/`;

  // Display a loading message
  const listingElement = document.getElementById('listing');
  if (!isSubdirectory) {
    listingElement.innerHTML = '<p>Loading files...</p>';
  }

  fetch(url)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      if (isSubdirectory) {
        renderSubdirectory(data, directory);
      } else {
        renderListing(data);
      }
    })
    .catch((error) => {
      console.error('Error fetching bucket data:', error);
      listingElement.innerHTML = `<p>Error loading bucket contents: ${error.message}</p>`;
    });
}

// Render the root listing (directories and top-level files)
function renderListing(data) {
  const listingElement = document.getElementById('listing');
  let content = '<ul>';

  // Add directories
  if (data.prefixes) {
    data.prefixes.forEach((prefix) => {
      const dirName = prefix.replace(GCSB_ROOT_DIR, '').replace(/\/$/, '');
      content += `<li class="directory"><a href="#" onclick="getBucketData('${prefix}', true); return false;">${dirName}/</a></li>`;
    });
  }

  // Add files
  if (data.items) {
    data.items.forEach((item) => {
      content += `<li class="file"><a href="${item.mediaLink}" target="_blank">${item.name.replace(GCSB_ROOT_DIR, '')}</a></li>`;
    });
  }

  content += '</ul>';
  listingElement.innerHTML = content;
}

// Render the contents of a subdirectory
function renderSubdirectory(data, directory) {
  const subListingId = `sub-${directory}`;
  let content = `<ul id="${subListingId}">`;

  // Add directories
  if (data.prefixes) {
    data.prefixes.forEach((prefix) => {
      const dirName = prefix.replace(directory, '').replace(/\/$/, '');
      content += `<li class="directory"><a href="#" onclick="getBucketData('${prefix}', true); return false;">${dirName}/</a></li>`;
    });
  }

  // Add files
  if (data.items) {
    data.items.forEach((item) => {
      content += `<li class="file"><a href="${item.mediaLink}" target="_blank">${item.name.replace(directory, '')}</a></li>`;
    });
  }

  content += '</ul>';

  // Add the subdirectory content below the clicked directory
  const existingElement = document.getElementById(subListingId);
  if (existingElement) {
    existingElement.remove(); // Remove if already expanded
  } else {
    const parentElement = document.querySelector(`a[href="#"][onclick*="${directory}"]`).parentElement;
    parentElement.insertAdjacentHTML('beforeend', content);
  }
}

// Initialize listing on page load
document.addEventListener('DOMContentLoaded', () => getBucketData());
