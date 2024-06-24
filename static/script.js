
let points = []; // Array to store selected points
let canvas, ctx;

jarvisTime = [];
KpsTime = [];

// Function to check orientation of three points
function orientation1(p, q, r) {

    if (p == undefined || q == undefined || r == undefined) return 0;

    let val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]);
    if (val == 0) return 0;  // colinear
    return (val > 0) ? 1 : 2; // clock or counterclock wise
}

// Function to draw points on canvas
function drawPoint(x, y, color) {
    ctx.beginPath();
    ctx.arc(x, y, 1, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
}

// Function to clear canvas
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}
// Event listener for mouse click on canvas
async function canvasClick(event) {

    if(event.type == 'change'){
        console.log('change');
    }
    if(event.type == 'click'){

        if (document.getElementById('visual').disabled == false) return;

        let rect = canvas.getBoundingClientRect();
        let mouseX = event.clientX - rect.left;
        let mouseY = event.clientY - rect.top;

        // Add clicked point to array
        points.push([mouseX, mouseY]);
        points = points.filter((point, index, self) =>
            index === self.findIndex((t) => (
                t[0] === point[0] && t[1] === point[1]
            ))
        );
        // Draw the point on canvas
        drawPoint(mouseX, mouseY, 'yellow');
    }

    // Start visualization after selecting points
    if (points.length >= 3) {
        clearCanvas();
        points.forEach(point => {
            drawPoint(point[0], point[1], 'yellow');
        });
        let hullPoints = await convexHullJarvis(points);
        //let hullPoints1 = hullPoints;
        let hullPoints1 = await convexHullKirkpatrickSeidel(points);

        animate(hullPoints, hullPoints1);
    }
}


// Function to draw line between two points on canvas
function drawLine(p1, p2, col) {
    ctx.strokeStyle = col;
    ctx.beginPath();
    ctx.moveTo(p1[0], p1[1]);
    ctx.lineTo(p2[0], p2[1]);
    ctx.stroke();
}

async function convexHullKirkpatrickSeidel(points) {
    let data = [];

    let start = new Date().getTime();
    await fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "value": points })
    })
        .then(response => response.text())
        .then(result => {
            //console.log(result);
            const temp = JSON.parse(result)
            try { const temp = JSON.parse(result) }
            catch (err) {
                console.log(result);
            }
            // console.log(temp);
            data = temp['val']
            // console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    let end = new Date().getTime();


    let hull = data;
    //console.log(hull);

    //time taken
    let time = end - start;

    console.log("Time taken by Kirkpatrick Seidel Algorithm: " + time + "ms");
    KpsTime.push(time);

    return hull;

}


// Jarvis March Algorithm
async function convexHullJarvis(points) {
    let data = [];

    let start = new Date().getTime();
    await fetch('/process2', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "value": points })
    })
        .then(response => response.text())
        .then(result => {
            const temp = JSON.parse(result)
            // console.log(temp);
            data = temp['val']
            // console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    let hull = data;
    //sort points clockwise
    hull = arrangeClockwise(hull);
    //console.log(hull);
    let end = new Date().getTime();
    let time = end - start;
    console.clear();

    console.log("Time taken by Jarvis March Algorithm: " + time + "ms");
    jarvisTime.push(time);
    return hull;
}

//function to arrange points in clockwise order

function arrangeClockwise(points) {
    let n = points.length;
    let centroidx = 0;
    let centroidy = 0;
    for (let i = 0; i < n; i++) {
        centroidx += points[i][0];
        centroidy += points[i][1];
    }
    centroidx /= n;
    centroidy /= n;

    points.sort((a, b) => {
        let angle = [Math.atan2(a[1] - centroidy, a[0] - centroidx), Math.atan2(b[1] - centroidy, b[0] - centroidx)];
        if (angle[0] < angle[1]) return -1;
        if (angle[0] > angle[1]) return 1;
        return 0;
    });

    return points;
}

// Function to animate Algorithm
function animate(hullPoints, hullPoints1) {
    // Clear canvas
    clearCanvas();

    // Draw all points
    points.forEach(point => {
        drawPoint(point[0], point[1], 'yellow');
    });

    hullPoints1 = arrangeClockwise(hullPoints1);

    let flag = document.getElementById('whichhull').value; 
    // console.log(flag);

    if(flag === 'jarvis' || flag === 'both'){ 
    // Draw Jarvis March Hull
    for (let i = 0; i < hullPoints.length; i++) {
        let nextIndex = (i + 1) % hullPoints.length;
        drawLine(hullPoints[i], hullPoints[nextIndex], 'cyan');
    }
    }

    if(flag === 'kps' || flag === 'both'){
    // Draw Kirkpatrick Seidel Hull
    for (let i = 0; i < hullPoints1.length; i++) {
        let nextIndex = (i + 1) % hullPoints1.length;
        drawLine(hullPoints1[i], hullPoints1[nextIndex], 'red');
    }
    }
}

async function randompoints() {
    points = [];
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    // Add event listener for mouse click on canvas
    canvas.addEventListener('click', canvasClick);

    // Disable button after starting visualization
    document.getElementById('visual').disabled = true;

    let n = document.getElementById('points').value;
    let width = canvas.width;
    let height = canvas.height;
    const XC = width / 2;
    const YC = height / 2;

    //points.push([0.997*width , 0.997*height]);
    //drawPoint(0.997*width, 0.997*height, 'black');
    /////////////////////
    for (let i = 0; i < n; i++) {
        let x = Math.random() * width * 0.9 + 0.05 * width;
        let y = Math.random() * height * 0.9 + 0.05 * height;
        points.push([x, y]);
        drawPoint(x, y, 'yellow');
    }


    //console.log(points)


    if (points.length >= 3) {
        let hullPoints = await convexHullJarvis(points);
        //console.log(hullPoints);
        //let hullPoints1 = hullPoints;
        let hullPoints1 = await convexHullKirkpatrickSeidel(points);

        //check if both same
        let flag = 1;
        if (hullPoints.length != hullPoints1.length) flag = 0;

        animate(hullPoints, hullPoints1);
    }

}

function reset() {
    points = [];
    clearCanvas();
    document.getElementById('visual').disabled = false;
}

// Start Visualization
function startVisualization() {
    // Get canvas element and context
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    hullopt = document.getElementById('whichhull');
    hullopt.addEventListener('change', canvasClick);

    // Add event listener for mouse click on canvas
    canvas.addEventListener('click', canvasClick);

    // Disable button after starting visualization
    document.getElementById('visual').disabled = true;
}

// Example of how to test the Jarvis March Algorithm with the selected points
