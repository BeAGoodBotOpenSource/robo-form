document.getElementById('pdf-upload').addEventListener('change', function () {
  // Enable the "Begin Autofill" button when a file is selected
  document.getElementById('autofill-button').disabled = false;
});

document.getElementById('autofill-button').addEventListener('click', function() {
  // Get the selected PDF file
  const fileInput = document.getElementById('pdf-upload');
  const pdfFile = fileInput.files[0];

  if (!pdfFile) {
    alert('Please select a PDF file first.');
    return;
  }

  // Extract the HTML of the current webpage
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var tab = tabs[0];
    
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      func: getOuterHTML,
    }).then(result => {
      const htmlText = result[0].result;

      const isProduction = false;
      const server_url = isProduction ? 'https://robo-form.onrender.com/autofill' : 'http://localhost:4000/autofill'; 

      // Convert the PDF file to a Blob
      const reader = new FileReader();
      reader.onloadend = function() {
        const pdfBlob = new Blob([reader.result], {type: pdfFile.type});

        // Send a POST request to your Python server with the PDF file and HTML text
        const formData = new FormData();
        formData.append('pdf', pdfBlob, pdfFile.name);
        formData.append('html', htmlText);

        fetch(server_url, { // replace with your server's URL
          method: 'POST',
          body: formData
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {

          // Fill in the form using the data from the server
          const inputValues = data[0].input_values;
          console.info('info:', inputValues);
          for (let id in inputValues) {
            const value = inputValues[id];
            if (value) { // Check if the value exists to prevent unnecessary calls
              chrome.scripting.executeScript({
                target: {tabId: tab.id},
                func: setValue,
                args: [id, value]
              });
            }
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
      };

      reader.readAsArrayBuffer(pdfFile);
    });
  });
});

function getOuterHTML() {
  return document.documentElement.outerHTML;
}

function setValue(id, value) {
  const element = document.getElementById(id) || document.getElementsByName(id);
  console.info(`Element with value ${value} . id = ${id}`);
  if (element) {
    element.value = value;
    console.info(`Element.value ${element.value} . value = ${value}`);
  } else {
    console.warn(`Element with ID ${id} not found.`);
  }
}
