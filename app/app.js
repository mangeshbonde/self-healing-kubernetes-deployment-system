const express = require('express');

const app = express();
const PORT = 3000;

// Simulate crash after 10 seconds
setTimeout(() => {
    console.log("Simulating crash...");
    process.exit(1);
}, 10000);

app.get('/', (req, res) => {
    res.send("App is running but will crash soon...");
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});