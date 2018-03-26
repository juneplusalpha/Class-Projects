<?php
require_once "pdo.php";
session_start();

if ( ! isset($_SESSION['name']) ) {
    die('ACCESS DENIED');
}

if ( isset($_POST['make']) && isset($_POST['model'])
     && isset($_POST['year']) && isset($_POST['mileage']) ) {
     if (strlen($_POST['make']) < 1) {
       $_SESSION['fail'] = "All fields are required";

     } else if (strlen($_POST['model']) < 1) {
       $_SESSION['fail'] = "All fields are required";

     } else {
   // Data validation should go here (see add.php)
      if (is_numeric($_POST['year']) && is_numeric($_POST['mileage'])) {
        $sql = "UPDATE autos SET make = :make,
                model = :model, year = :year, mileage = :mileage
                WHERE auto_id = :auto_id";
        $stmt = $pdo->prepare($sql);
        $stmt->execute(array(
            ':make' => $_POST['make'],
            ':model' => $_POST['model'],
            ':mileage' => $_POST['mileage'],
            ':year' => $_POST['year'],
            ':auto_id' => $_GET['auto_id']));
        $_SESSION['success'] = 'Record successfully updated';
        header( 'Location: index.php' ) ;
        return;
      } else {
        $_SESSION['fail'] = "Year must be numeric";

      }
    }
  }

// Guardian
if ( ! isset($_GET['auto_id']) ) {
  $_SESSION['error'] = "Missing auto_id";
  header('Location: index.php');
  return;
}

$stmt = $pdo->prepare("SELECT make, model, year, mileage, auto_id FROM autos where auto_id = :auto_id");
$stmt->execute(array(":auto_id" => $_GET['auto_id']));
$row = $stmt->fetch(PDO::FETCH_ASSOC);
if ( $row === false ) {
    $_SESSION['error'] = 'Bad value for auto_id';
    header( 'Location: index.php' ) ;
    return;
}
$ma = htmlentities($row['make']);
$mo = htmlentities($row['model']);
$ye = htmlentities($row['year']);
$mi = htmlentities($row['mileage']);
$auto_id = htmlentities($row['auto_id']);
?>
<head>
  <title>Jun Ha Park's Automobile Tracker</title></head>
<p>Editing Automobile</p>
<?php
if(isset($_SESSION['fail'])){
  echo ('<p style="color: red;">'.$_SESSION['fail'].'</p>');
}
 ?>
<form method="post">
<p>Make
<input type="text" name="make" size="40" value="<?= $ma ?>"></p>
<p>Model
<input type="text" name="model" size="40" value="<?= $mo ?>"></p>
<p>Year
<input type="text" name="year" size="10" value="<?= $ye ?>"></p>
<p>Mileage
<input type="text" name="mileage" size="10" value="<?= $mi ?>"></p>
<p>
  <input type='hidden' name='auto_id' value='0'/>
  <input type="submit" value="Save"/>
  <input type="submit" name='cancel' value="Cancel"/>
</p>
</form>
