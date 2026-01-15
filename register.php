<?php
session_start();

$usersFile = 'users.json';

if (!file_exists($usersFile)) {
    file_put_contents($usersFile, json_encode([]));
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];

    if (empty($username) || empty($password)) {
        echo "Username and password are required.";
        exit;
    }

    if ($password !== $confirm_password) {
        echo "Passwords do not match.";
        exit;
    }

    $users = json_decode(file_get_contents($usersFile), true);

    if (isset($users[$username])) {
        echo "Username already exists.";
        exit;
    }

    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    $users[$username] = $hashed_password;

    file_put_contents($usersFile, json_encode($users, JSON_PRETTY_PRINT));

    echo "Registration successful! You can now <a href='login.html'>login</a>.";
}
?>
