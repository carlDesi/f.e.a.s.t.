var header = document.getElementById("questions");
var button = header.getElementsByClassName("btn");
for (var i = 0; i < button.length; i++) {
  button[i].addEventListener("click", function() {
  var current = document.getElementsByClassName("active");
  current[0].className = current[0].className.replace(" active", "");
  this.className += " active";
  });
}

function checkSelection() {
  var classSelect = document.getElementById("class");
  var classValue = classSelect.options[classSelect.selectedIndex].value;
  if (classValue === "") {
      alert("Please select a class.");
      return false;
  }

  var teammatesSelect = document.getElementById("teammates");
  var teammatesValue = teammatesSelect.options[teammatesSelect.selectedIndex].value;
  if (teammatesValue === "") {
      alert("Please select a groupmate to rate.");
      return false;
  }

  // If both dropdowns have a selected value, submit the form
  return true;
}