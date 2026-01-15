<?php
session_start();

$usersFile = 'users.json';

if (!file_exists($usersFile)) {
    file_put_contents($usersFile, json_encode([]));
}

$users = json_decode(file_get_contents($usersFile), true);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if (isset($users[$username]) && password_verify($password, $users[$username])) {
        $_SESSION['username'] = $username;
        echo "Login successful! Welcome, $username.";
    } else {
        echo "Invalid username or password.";
    }
}
?>
