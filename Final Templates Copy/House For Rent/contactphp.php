<?php

// Create a connection to the database
$conn = new mysqli("localhost", "root", "", "mydb");

// Check if the connection was successful
if ($conn->connect_error) {
  die("ERROR: Could not connect. " . $conn->connect_error);
} else {
  echo "Done";
}

// Get the form data
$first_name = $_REQUEST['first_name'];
$last_name = $_REQUEST['last_name'];
$email = $_REQUEST['email'];
$phone_number = $_REQUEST['pnumber'];

// Insert the data into the database
$sql = "INSERT INTO contacts (first_name, last_name, email, pnumber) VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssss", $first_name, $last_name, $email, $phone_number);
$stmt->execute();

// Check if the query was successful
if ($stmt->affected_rows > 0) {
  echo "<h3>data stored in a database successfully. </h3>";
      header("Location: contact.php?success=true");
 /* echo nl2br("\n$first_name\n $last_name\n "
    . " $phone_number\n $email");*/
} else {
  echo "ERROR: Hush! Sorry $sql. " . $conn->error;
}

// Close the database connection
$conn->close();

?>
