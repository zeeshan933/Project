const fileInput = document.getElementById('fileInput');
const progressBar = document.querySelector('.progress');
const progressText = document.querySelector('.progress-text');

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  const fileSize = file.size;

  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'sheet', true);

  xhr.upload.addEventListener('progress', (e) => {
    if (e.lengthComputable) {
      const percentage = Math.min(100, (e.loaded / fileSize) * 100); // Ensure percentage doesn't go over 100
      progressBar.style.width = `${percentage}%`;
      progressText.textContent = `${Math.round(percentage)}%`;
    }
  });

  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4 && xhr.status === 200) {
      // File upload is complete, you can handle the response here if needed.
      console.log('Upload complete');
    }
  };

  const formData = new FormData();
  formData.append('file', file);
  xhr.send(formData);
});
 // Get a reference to the file input and submit button
 const fileInput2 = document.getElementById('fileInput');
 const submitButton = document.getElementById('submitButton');

 // Add an event listener to the file input
 fileInput2.addEventListener('change', function () {
   // Check if a file has been selected
   if (fileInput2.files.length > 0) {
     // Automatically click the submit button
     submitButton.click();
   }
 });