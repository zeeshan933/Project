function validateNumber(input) {
  if (input.value.length > 11) {
    alert("Please enter a number with 11 digits");
    input.value = input.value.substring(0, 11);
  }
  else if (input.value.length < 11) {
    alert("Please enter a number with 11 digits ");
    input.value = input.value.substring(0, 11);
  }
}
function changeBackgroundColor(input) {
  input.style.backgroundColor = "#252930";
  input.style.color = "#AF8C53";
}
function changeBackgroundColor2(input) {
  input.style.backgroundColor = "#AF8C53";
  input.style.color = "#252926";
}

/* time-based greeting */
function getGreeting(time) {
  if (time < 6) {
    return "Shab-e-Khair ";
  }
  if (time < 12) {
    return "Assalam-o-Alaikum ";
  } 
  else if (time < 18) {
    return "Subh-e-Khair.";
  } 
  else {
    return "Sham-o-Khair";
  }
  
}
