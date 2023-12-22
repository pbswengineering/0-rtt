<?php
$message = '';
$receiver = 'test';
if (file_exists('/tmp/balance'))
    $balance = intval(file_get_contents('/tmp/balance'));
else
    $balance = 1000;
if (!isset($_GET['refresh'])) {
    if (isset($_GET['reset'])) {
        file_put_contents('/tmp/balance', 1000);
        if (file_exists('/tmp/banklog'))
            unlink('/tmp/banklog');
        $balance = 1000;
    } else if (isset($_GET['amount']) && isset($_GET['receiver'])) {
        $amount = intval($_GET['amount']);
        if ($amount <= $balance) {
            $balance = $balance - $amount;
            file_put_contents('/tmp/balance', $balance);
            $receiver = $_GET['receiver'];
            $now = date('r');
            file_put_contents('/tmp/banklog', "$now|$amount|$receiver\n", FILE_APPEND);
            $message = '<div class="alert alert-success" role="alert">Sent ' . $amount . '$ to ' . $_GET['receiver'] . '</div>';
        } else {
            $message = '<div class="alert alert-danger" role="alert">Insufficient funds</div>';
        }
    }
}
$transfers = [];
if (file_exists('/tmp/banklog')) {
    $rawlog = file_get_contents('/tmp/banklog');
    $rows = explode("\n", $rawlog);
    foreach ($rows as $row) {
        if (strlen(trim($row)) > 0)
            $transfers[] = explode('|', $row);
    }
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Secure Bank Application - BERNARDI CORP</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
</head>

<body>
    <header>
        <nav class="navbar bg-primary" data-bs-theme="dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">
                    <img src="icon.png" alt="Logo" width="24" height="24" class="d-inline-block align-text-top">
                    Secure Bank Application
                </a>
                <?php if (isset($_SESSION['username'])) { ?>
                    <form class="d-flex" action="index.php" method="post">
                        <button name="logout" class="btn btn-outline-" type="submit">Logout</button>
                    </form>
                <?php } ?>
            </div>
        </nav>
    </header>

    <main>
        <div class="container">
            <div class="row">
                <div class="col">
                    <br>
                    <h2>Money transfer</h2>
                    <p>Current balance: <?= $balance ?>$</p>
                    <?= $message ?>
                    <form action="index.php" method="get">
                        <div class="mb-3">
                            <label for="amount" class="form-label">Receiver</label>
                            <input type="text" class="form-control" id="receiver" name="receiver" placeholder="test" value="<?= $receiver ?>">
                        </div>
                        <div class="mb-3">
                            <label for="amount" class="form-label">Amount</label>
                            <div class="input-group mb-3">
                                <span class="input-group-text">$</span>
                                <input type="number" class="form-control" id="amount" name="amount" placeholder="50" value="50">
                                <span class="input-group-text">.00</span>
                            </div>
                        </div>
                        <div class="col-auto">
                            <button type="submit" class="btn btn-primary mb-3">Send money</button>
                            <button type="submit" name="reset" class="btn btn-danger mb-3" value="reset">Reset balance</button>
                            <button name="refresh" class="btn btn-success mb-3" value="refresh">Refresh</button>
                        </div>
                    </form>
                </div> <!-- .col -->
                <div class="col">
                    <img src="logo.png" style="width: 100%">
                </div> <!-- .col -->
            </div> <!-- .row -->
            <?php if (count($transfers) > 0) { ?>
                <div class="row">
                    <div class="col">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">Timestamp</th>
                                    <th scope="col">Amount</th>
                                    <th scope="col">Receiver</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($transfers as $t) { ?>
                                    <tr>
                                        <td><?= $t[0] ?></td>
                                        <td><?= $t[1] ?>$</td>
                                        <td><?= $t[2] ?></td>
                                    </tr>
                                <?php } ?>
                            </tbody>
                        </table>
                    </div>
                </div>
            <?php } ?>
        </div>
    </main>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
</body>

</html>