// Configuration for GCS bucket listing
var API_ENDPOINT = 'https://www.googleapis.com/storage/v1/b/nmfs_odp_pifsc/o';
var GCSB_SORT = 'DEFAULT'; // Sorting options
var EXCLUDE_FILE = []; // Files to exclude
var GCSB_ROOT_DIR = ''; // Root directory, if needed
var AUTO_TITLE = true;

// Set the document title automatically
if (AUTO_TITLE) {
  document.title = location.hostname;
}

// Fetch and display bucket data using JSON API
function getBucketData(pageToken = '') {
  let url = `${API_ENDPOINT}?prefix=${GCSB_ROOT_DIR}&delimiter=/`;
  if (pageToken) {
    url += `&pageToken=${pageToken}`;
  }

  // Display a loading message
  const listingElement = document.getElementById('listing');
  if (!pageToken) {
    listingElement.innerHTML = '<p>Loading files...</p>';
  }

  fetch(url)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      const files = data.items || [];
      const directories = data.prefixes || [];

      renderListing(files, directories);

      // If there's a nextPageToken, fetch more results
      if (data.nextPageToken) {
        getBucketData(data.nextPageToken);
      }
    })
    .catch((error) => {
      console.error('Error fetching bucket data:', error);
      listingElement.innerHTML = `<p>Error loading bucket contents: ${error.message}</p>`;
    });
}

// Render file and directory listing
function renderListing(files, directories) {
  const listingElement = document.getElementById('listing');
  let content = listingElement.innerHTML === '<p>Loading files...</p>' ? '' : listingElement.innerHTML;

  // Add directories
  directories.forEach((dir) => {
    content += `<li class="directory"><a href="${dir.mediaLink}" target="_blank">${dir.name}/</a></li>`;
  });

  // Sort files if a sort option is selected
  if (GCSB_SORT !== 'DEFAULT') {
    files.sort((a, b) => sortFiles(a, b, GCSB_SORT));
  }

  // Add files
  files.forEach((file) => {
    if (!EXCLUDE_FILE.includes(file.name)) {
      const size = bytesToHumanReadable(file.size);
      content += `<li class="file"><a href="${file.mediaLink}" target="_blank">${file.name}</a> (${size})</li>`;
    }
  });

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
      return parseInt(b.size, 10) - parseInt(a.size, 10);
    case 'SMALL2BIG':
      return parseInt(a.size, 10) - parseInt(b.size, 10);
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
document.addEventListener('DOMContentLoaded', () => getBucketData());
