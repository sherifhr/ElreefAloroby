var table = document.getElementById('farm-list');
var selectedCells = [];

for (var i = 0; i < table.rows.length; i++) {
    var row = table.rows[i];
    var cell5 = row.cells[5];
    //selectedCells6.push(cell6.textContent);
    selectedCells.push(cell5.textContent);
  
    //selectedCells.push(cell5.textContent +'-'+ cell6.textContent);
  }
const uniqueItemsSet   = new Set(selectedCells);
const uniqueItemsArray = Array.from(uniqueItemsSet);

for (var i = 0; i <uniqueItemsArray.length; i++) {
    console.log(uniqueItemsArray);
    document.getElementById("result"+i).textContent =uniqueItemsArray[i].toString();     
}

function assignValue() {
    var dropdown = document.getElementById('myDropdown');
    var selectedOption = dropdown.options[dropdown.selectedIndex];
    var selectedValue = selectedOption.value;
    var input = document.getElementById('myInput');
    input.value= dropdown.options[dropdown.selectedIndex].text;  
}
// console.log(selectedValue);
console.log('Before pause');
setTimeout(function() {
console.log('After 3 seconds');
}, 3000);


function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}


