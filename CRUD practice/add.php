<?php
require_once "pdo.php";
session_start();

if ( ! isset($_SESSION['name']) ) {
    die('ACCESS DENIED');
    return;
}
if ( isset($_POST['cancel']) ) {
    header('Location: index.php');
    return;
}

$fail = false;
$added = false;

if ( isset($_POST['make']) && isset($_POST['model']) && isset($_POST['year']) && isset($_POST['mileage'])) {
  if (strlen($_POST['make']) < 1) {
    $_SESSION['fail'] = "All fields are required";
    header('Location: add.php');
    return;
  } else if (strlen($_POST['model']) < 1) {
    $_SESSION['fail'] = "All fields are required";
    header("Location: add.php");
  } else {
    if (is_numeric($_POST['year']) && is_numeric($_POST['mileage'])) {
      $_SESSION['make'] = htmlentities($_POST['make']);
      $_SESSION['model'] = htmlentities($_POST['model']);
      $_SESSION['year'] = htmlentities($_POST['year']);
      $_SESSION['mileage'] = htmlentities($_POST['mileage']);

      $sql = "INSERT INTO autos (make, model, year, mileage) VALUES (:mk, :mo, :yr, :mi)";
      $stmt = $pdo->prepare($sql);
      $stmt->execute(array(
        ':mk' => $_SESSION['make'],
        ':mo' => $_SESSION['model'],
        ':yr' => $_SESSION['year'],
        ':mi' => $_SESSION['mileage']));
      $_SESSION['added'] = "Record added";
      header('Location: index.php');
      return;
      } else {
        $_SESSION['fail'] = "Year must be numeric";
        header('Location: add.php');
        return;
      }
    }
  }

?>

<html>
<head><title>Jun Ha Park's Automobile Tracker</title></head>
<body>
<p><h1>Tracking Autos for <?php echo $_SESSION['name']?></h1></p>
<?php
$fail = isset($_SESSION['fail']) ? $_SESSION['fail']: false;
$added = isset($_SESSION['added']) ? $_SESSION['added']: false;

if ($fail !== false){
  echo("<p style='color: red;'>$fail</p>");
  unset($_SESSION['fail']);
} else if ($added !== false) {
  echo("<p style = 'color: green;'>$added</p>");
  unset($_SESSION['added']);
}
?>

</p>
<form method="post">
<p>Make:
<input type="text" name="make" size="40"></p>
<p>Model:
  <input type="text" name="model" size="40"></p>
<p>Year:
<input type="text" name="year" size="10"></p>
<p>Mileage:
<input type="text" name="mileage" size="10"></p>
<input type="submit" name ="add" value="Add"/>
<input type="submit" name="cancel" value="Cancel"></p>
</form>
</body>
