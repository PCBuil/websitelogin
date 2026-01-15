<?php
// dashboard.php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: login.html");
    exit();
}
echo "Welcome to your dashboard, " . $_SESSION['username'];
?>
