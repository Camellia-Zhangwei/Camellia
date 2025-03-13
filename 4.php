<?php
// Connect to MySQL database
$conn = new mysqli('sql207.infinityfree.comt', 'if0_37804247', 'zw20050311', 'if0_37804247_db_timetable');


// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch timetable data from the database
$sql = "SELECT subject, day, time, teacher FROM timetable";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table border='1'><tr><th>Subject</th><th>Day</th><th>Time</th><th>Teacher</th></tr>";
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>".$row["subject"]."</td><td>".$row["day"]."</td><td>".$row["time"]."</td><td>".$row["teacher"]."</td></tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}
$conn->close();
?>