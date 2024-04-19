
  function filterBoxes() {
    // Get all checkboxes
    var checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]');

    // Loop through checkboxes
    checkboxes.forEach(function (checkbox) {
      // Get the target box corresponding to the checkbox
      var targetBoxId = checkbox.getAttribute('data-target');
      var targetBox = document.getElementById(targetBoxId);

      // // Check if the checkbox is checked
      // if (checkbox.checked) {
      //   // Display the corresponding box
      //   targetBox.style.display = 'block';
      // } else {
      //   // Hide the corresponding box
      //   targetBox.style.display = 'none';
      // }
    });
  }

  // Attach event listener to checkboxes
  var checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]');
  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener('change', filterBoxes);
  });



// // Function to extract video ID from YouTube URL
// // Function to extract video ID from YouTube URL
// function extractVideoId(url) {
//     var videoId = '';
//     var match = url.match(/(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?/\r\n]{11})/);
//     if (match) {
//         videoId = match[1];
//     } else {
//         console.log('No video ID found in URL:', url);
//     }
//     return videoId;
// }

// // Function to handle form submission
// function handleSubmit(event) {
//     event.preventDefault(); // Prevent default form submission behavior
    
//     // Get the input URL from the form
//     var inputUrl = document.getElementById('urlbox').value.trim();
    
//     // Extract video ID from the input URL
//     var videoId = extractVideoId(inputUrl);

//     // Log the extracted video ID to the console for debugging
//     console.log('Extracted Video ID:', videoId);

//     // Display an alert with the extracted video ID
//     alert('Video ID: ' + videoId);
// }

// // Attach event listener to form submission
// var form = document.querySelector('.search-container form');
// form.addEventListener('submit', handleSubmit);
