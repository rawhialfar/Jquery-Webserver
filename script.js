/* javascript to accompany jquery.html */
var refreshOption = [];
var count=0;
var atomNo = [];
var bondNo = [];
$(document).ready( 
  /* this defines a function that gets called after the document is in memory */
  function()
  {
    /* add a click handler for our button */
    $("#add-button").click(
      function()
      {
        /* ajax post */
        $.post("/add_element",
        /* pass a JavaScript dictionary */
        {
          elementNo: $("#element-number").val(),	
          elementCode: $("#element-code").val(),	
          elementName: $("#element-name").val(),	
          color1: $("#color-1").val(),	
          color2: $("#color-2").val(),	
          color3: $("#color-3").val(),	
          elementRadius: $("#element-radius").val(),	
        },
        function( data )
        {
            alert( data );
            location.reload();
              // $("#label").text(data)
        }
        );
      }
    );

    $("#remove-button").click(
      function()
      {
        /* ajax post */
        $.post("/remove_element",
        /* pass a JavaScript dictionary */
        {
          elementNo: $("#element-number").val(),	
          elementCode: $("#element-code").val(),	
          elementName: $("#element-name").val(),	
          color1: $("#color-1").val(),	
          color2: $("#color-2").val(),	
          color3: $("#color-3").val(),	
          elementRadius: $("#element-radius").val(),	
        },
        function( data )
        {
            alert( data );
            // $("#label").text(data)
        }
        );
      }
    );

    $("#upload-button").click(
      
      function()
      {
        /* ajax post */
        $.post("/sdf_upload",
        /* pass a JavaScript dictionary */
        {
          fp: $("#uploadFile").files[0],	
          name: $("#molecule-name").val(),	
        },
        function( data )
        {
            // alert( data );
            // $("#outputLabel").text(data)
        }
        );
      }
    );

    $("#select-button").click(
      
      function()
      {
        /* ajax post */
        $.post("/select_molecule",
        /* pass a JavaScript dictionary */
        {
          name: $("#molecule-select").val(),	
        },
        function( data )
        {
            alert( "SVG Displayed!" );
            $("#display-molecule").html(data)
            $("#mol-name").text($("#molecule-select").val())
        }
        );
      }
    );

    $("#rotate-button").click(
      
      function()
      {
        /* ajax post */
        $.post("/rotate_molecule",
        /* pass a JavaScript dictionary */
        {
          name: $("#molecule-select").val(),	
          x: $("#x-rotation").val(),	
          y: $("#y-rotation").val(),	
          z: $("#z-rotation").val(),	
        },
        function( data )
        {
            alert( "Molecule Rotated!" );
            $("#display-molecule").html(data)
        }
        );
      }
    );

    $.ajax({
      url: '/display_options',
      dataType: 'text',
      type: 'GET',
      success: function(data) {
        var select = document.getElementById("molecule-select");
        var option = document.createElement("option");

        const options = [];

        const lists = [data]; // Create a single list with both molecule definitions
        const molList = JSON.parse(lists);
        // alert(molList)
        // alert(molList[0])
        for (let i = 0; i < molList.length; i++) {
          
          molName = molList[i][1];
          numAtoms = molList[i][2];
          numBonds = molList[i][3];
          option.value = molName;
          // alert("Number of atoms: " + numAtoms + " Number of bonds: " + numBonds);
          option.text = molName + " (Atoms: " + numAtoms + ", Bonds: " + numBonds + ")";
          // alert(molName);
          options.push({value: option.value, text: option.text})
          // console.log(molecule1, molecule2);
          // i=i+1;
        }

        // loop through the options array and add each option to the select element
        options.forEach((optionData) => {
          // create a new <option> element
          const option = document.createElement('option');
          option.value = optionData.value;
          // alert(option.value)
          option.text = optionData.text;

          // add the new <option> element to the <select> element
          select.options.add(option);
        });
      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });

    $.ajax({
      url: '/display_elements',
      dataType: 'text',
      type: 'GET',
      success: function(data) {
        // Assuming the data returned is a list of dictionaries
        
        var table = '<table>';
        table += '<thead><tr><th>Element Number</th><th>Element Code</th><th>Element Name</th><th>Color 1</th><th>Color 2</th><th>Color 3</th><th>Radius</th><th></th></tr></thead>';
        table += '<tbody>';
        
        // var elementCode=data[5:'"']
        for (var i = 0; i < data.length; i++){
            if (data[i] == ']' && data[i+1] == ']' ) {
              break;
            }
        }
        
        // alert(data.substr(1, i), "...\n")
        var elements = data.substr(1, i);

        const lists = elements.split('], ['); // split into individual lists

        // remove square brackets from the first and last lists
        lists[0] = lists[0].replace('[', '');
        lists[lists.length - 1] = lists[lists.length - 1].replace(']', '');

        for (let i = 0; i < lists.length; i++) {
          const listValues = lists[i].split(','); // split list into individual values 

          var elementNo = parseInt(listValues[0]); // 1
          var elementCode = listValues[1].replace(/"/g, ''); // "H" (remove the double quotes using a regular expression)
          var elementName = listValues[2].replace(/"/g, ''); // "Hydrogen"
          var color1 = listValues[3].replace(/"/g, ''); // "FFFFFF"
          var color2 = listValues[4].replace(/"/g, ''); // "050505"
          var color3 = listValues[5].replace(/"/g, ''); // "020202"
          var radius = parseInt(listValues[6]); // 25

          table += '<tr>';
          table += '<td>' + elementNo + '</td>';
          table += '<td>' + elementCode + '</td>';
          table += '<td>' + elementName + '</td>';
          table += '<td>' + color1+ '</td>';
          table += '<td>' + color2+ '</td>';
          table += '<td>' + color3+ '</td>';
          table += '<td>' + radius + '</td>';
          // Add a remove button to the table row
          table += '<td ><button class="remove-button text-center" style= "margin: auto; postion: center;" id="remove-button" data-row="' + elementNo + '">X</button></td>';
          
          table += '</tr>';

        }

        table += '</tbody>';
        table += '</table>';
        $('#table-container').html(table);

        // Add event listener to remove buttons
        $('.remove-button').on('click', function() {
          const $this = $(this); // Store $(this) reference in a variable
          const elementNo = $this.data('row');

          // Send a POST request to the server to remove the element
          $.ajax({
            url: '/remove_element',
            dataType: 'text',
            type: 'POST',
            data: {
              elementNo: elementNo
            },
            success: function(data) {
              // Remove the table row if the element was successfully removed
              
              alert("Element has been removed");
              location.reload();
              if (data == 'success') {
                $this.closest('tr').remove();
              }
            },
            error: function(xhr, status, error) {
              console.error(error);
            }
          });
        });
        
        
      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });
    

  }
);

function processData(data) {
  // Process the data and save it to a variable
  var parsedData = parseInt(data);

  return parsedData;
}


function saveData(parsedData) {
  // Send an AJAX POST request to save the data to a server
  fetch('/save-data', {
    method: 'POST',
    body: JSON.stringify(parsedData),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
  
  // Alternatively, store the data in local storage
  localStorage.setItem('parsedData', JSON.stringify(parsedData));
}

function addMolecule() {
  var select = document.getElementById("molecule-select");
  var moleculeName = document.getElementById("molecule-name").value.trim(); // trim any whitespace from the input

  if (moleculeName === "") {
    console.error("Molecule name cannot be empty");
    return;
  }

  // Check if the molecule name already exists in the dropdown list
  var options = select.options;
  for (var i = 0; i < options.length; i++) {
    if (options[i].value === moleculeName) {
      console.error("Molecule name already exists in the dropdown list");
      return;
    }
  }

  var option = document.createElement("option");
  option.value = moleculeName;

  
  console.log("Added molecule: " + moleculeName);
  // Retrieve the uploaded file
  var file = document.getElementById("uploadFile").files[0];
  var reader = new FileReader();

  reader.onload = function() {
    // Do something with the file contents
    console.log(reader.result);
    // Display the file contents
    // alert(reader.result);
    var lines = reader.result.split('\n');

    var nums = lines[3].split(/\s+/);
    // alert(nums);
    // The first two numbers are stored in nums[0] and nums[1], respectively
    var num_atoms = parseInt(nums[1]);
    var num_bonds = parseInt(nums[2]);
    atomNo[count] = num_atoms;
    bondNo[count] = num_bonds;

    option.text = moleculeName + " (Atoms: " + num_atoms + ", Bonds: " + num_bonds + ")";
    
  };
  reader.readAsText(file);

  // alert(option.text);

  select.add(option);
  count=count+1;
}

function submitForm(event) {
  event.preventDefault(); // prevent the default form submission behavior
    
  var form = document.getElementById("upload");
  var formData = new FormData(form);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/sdf_upload");
  xhr.onload = function() {
    if (xhr.status === 200) {
      var optionExists = checkForDuplicateMolecule();
      if (optionExists) {
        alert("Molecule already exists!");
      } else {
        addMolecule(); // add the new molecule option to the select element
        alert("File uploaded successfully!");
      }
    } else {
      alert("Error uploading file!");
      console.error(xhr.responseText);
    }
  };
  xhr.send(formData);
}

function checkForDuplicateMolecule() {
  var select = document.getElementById("molecule-select");
  var moleculeName = document.getElementById("molecule-name").value.trim();

  for (var i = 0; i < select.options.length; i++) {
    if (select.options[i].value === moleculeName) {
      return true;
    }
  }
  return false;
}
