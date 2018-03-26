<?php
session_start();
require_once "pdo.php";
if (! $_SESSION) {
  echo('<p><h1>Welcome to Autos Database</h1></p>');
  echo('<p><a href="login.php">Please log in</a></p>');
  echo('<p>Attempt to go to <a href="add.php">add data</a> without logging in - it should fail with an error message.</P>');
}else if ( isset($_SESSION['error']) ) {
    echo '<p style="color:red">'.$_SESSION['error']."</p>\n";
    unset($_SESSION['error']);
}else {
    echo ('<p><h1>Welcome to the Automobiles Database</h1></p>');
    $stmt = $pdo->query("SELECT make, model, year, mileage, auto_id FROM autos");
    if (! isset($stmt)){
      echo ("<p style='color: red;'>No rows found</p>");
    }
    if (isset($_SESSION['added'])) {
      echo ("<p style='color: green;'>Record added</p>");
      unset($_SESSION['added']);
    }
    if (isset($_SESSION['delete'])) {
      echo ("<p style ='color:green;'>Record deleted</p>");
      unset($_SESSION['delete']);
    }
    if (isset($_SESSION['success'])) {
      echo ("<p style='color: green;'>Record updated?</p>");
      unset($_SESSION['success']);
    }
    if (isset($stmt)) {
      echo "<table border='1'"."\n";
      echo "<thead><tr><th>";
      echo "<b>Make</b>";
      echo "</th><th>";
      echo "<b>Model</b>";
      echo "</th><th>";
      echo "<b>Year</b>";
      echo "</th><th>";
      echo "<b>Mileage</b>";
      echo "</th><th>";
      echo "<b>Action</b>";
      echo "</th></thead>";
      while ( $row = $stmt->fetch(PDO::FETCH_ASSOC) ) {
          echo "<tr><td>";
          echo(htmlentities($row['make']));
          echo("</td><td>");
          echo(htmlentities($row['model']));
          echo("</td><td>");
          echo(htmlentities($row['year']));
          echo("</td><td>");
          echo(htmlentities($row['mileage']));
          echo("</td><td>");
          echo('<a href="edit.php?auto_id='.$row['auto_id'].'">Edit</a> / ');
          echo('<a href="delete.php?auto_id='.$row['auto_id'].'">Delete</a>');
          echo("</td></tr>\n");
        }
    }
}
?>
<head><head><title>Jun Ha Park's Index Page</title></head>
</table>
<?php
if ($_SESSION) {
  echo('<p><a href="add.php">Add New Entry</a><br>');
  echo ('<a href="logout.php">Logout</a></p>');
}
?>

</body>
