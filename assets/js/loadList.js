// Dynamically set the document title if AUTO_TITLE is enabled
if (typeof AUTO_TITLE !== 'undefined' && AUTO_TITLE === true) {
  document.title = location.hostname;
}

// Default variables
var BUCKET_URL = typeof BUCKET_URL !== 'undefined' ? BUCKET_URL : location.origin;
var GCSB_ROOT_DIR = typeof GCSB_ROOT_DIR !== 'undefined' ? GCSB_ROOT_DIR : '';
var GCSB_SORT = typeof GCSB_SORT !== 'undefined' ? GCSB_SORT : 'DEFAULT';
var EXCLUDE_FILE = Array.isArray(EXCLUDE_FILE) ? EXCLUDE_FILE : [];
var GCSBL_IGNORE_PATH = typeof GCSBL_IGNORE_PATH !== 'undefined' ? GCSBL_IGNORE_PATH : false;

// Fetch bucket data using GCS JSON API
function getBucketData() {
  const gcsApiUrl = `${BUCKET_URL}?prefix=${GCSB_ROOT_DIR}&delimiter=/`;

  // Display a loading message
  const listingElement = document.getElementById('listing');
  listingElement.innerHTML = '<p>Loading files...</p>';

  fetch(gcsApiUrl)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      // Process and display files
      const files = data.items || [];
      const directories = data.prefixes || [];
      renderListing(files, directories);
    })
    .catch((error) => {
      console.error('Error fetching bucket data:', error);
      listingElement.innerHTML = `<p>Error loading bucket contents: ${error.message}</p>`;
    });
}

// Render file and directory listing
function renderListing(files, directories) {
  const listingElement = document.getElementById('listing');
  let content = '<ul>';

  // Add directories
  directories.forEach((dir) => {
    const dirName = dir.replace(GCSB_ROOT_DIR, '');
    content += `<li class="directory"><a href="${BUCKET_URL}/${dir}" target="_blank">${dirName}/</a></li>`;
  });

  // Sort files if a sort option is selected
  if (GCSB_SORT !== 'DEFAULT') {
    files.sort((a, b) => sortFiles(a, b, GCSB_SORT));
  }

  // Add files
  files.forEach((file) => {
    if (!EXCLUDE_FILE.includes(file.name)) {
      content += `<li class="file"><a href="${BUCKET_URL}/${file.name}" target="_blank">${file.name}</a> (${bytesToHumanReadable(file.size)})</li>`;
    }
  });

  content += '</ul>';
  listingElement.innerHTML = content;
}

// Sorting logic for files
function sortFiles(a, b, sortOption) {
  switch (sortOption) {
    case 'OLD2NEW':
      return new Date(a.updated) - new Date(b.updated);
    case 'NEW2OLD':
      return new Date(b.updated) - new Date(a.updated);
    case 'A2Z':
      return a.name.localeCompare(b.name);
    case 'Z2A':
      return b.name.localeCompare(a.name);
    case 'BIG2SMALL':
      return b.size - a.size;
    case 'SMALL2BIG':
      return a.size - b.size;
    default:
      return 0;
  }
}

// Convert bytes to a human-readable format
function bytesToHumanReadable(sizeInBytes) {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let index = 0;
  while (sizeInBytes >= 1024 && index < units.length - 1) {
    sizeInBytes /= 1024;
    index++;
  }
  return `${sizeInBytes.toFixed(1)} ${units[index]}`;
}

// Initialize listing on page load
document.addEventListener('DOMContentLoaded', getBucketData);
