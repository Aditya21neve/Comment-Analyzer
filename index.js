
  function filterBoxes() {
    // Get all checkboxes
    var checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]');

    // Loop through checkboxes
    checkboxes.forEach(function (checkbox) {
      // Get the target box corresponding to the checkbox
      var targetBoxId = checkbox.getAttribute('data-target');
      var targetBox = document.getElementById(targetBoxId);

      // Check if the checkbox is checked
      if (checkbox.checked) {
        // Display the corresponding box
        targetBox.style.display = 'block';
      } else {
        // Hide the corresponding box
        targetBox.style.display = 'none';
      }
    });
  }

  // Attach event listener to checkboxes
  var checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]');
  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener('change', filterBoxes);
  });

