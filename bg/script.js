let canvas = document.getElementById('test'),
    ctx = canvas.getContext('2d'),
    rate = 100,
    arc = 100,
    time,
    count,
    size = 5,
    speed = 2,
    parts = new Array,
    colors = ['maroon', '#b22222', 'antiquewhite', 'maroon', 'antiquewhite'];
let mouse = { x: 0, y: 0 };

// Set canvas dimensions
function resizeCanvas() {
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = w;
    canvas.height = h;
}

// Initialize and create particles
function create() {
    time = 0;
    count = 0;

    for (let i = 0; i < arc; i++) {
        parts[i] = {
            x: Math.ceil(Math.random() * w),
            y: Math.ceil(Math.random() * h),
            toX: Math.random() * 3 - 1,
            toY: Math.random() * 2 - 1,
            c: colors[Math.floor(Math.random() * colors.length)],
            size: Math.random() * size,
        }
    }
}

// Update particles on canvas
function particles() {
    ctx.clearRect(0, 0, w, h);
    canvas.addEventListener('mousemove', MouseMove, false);
    for (let i = 0; i < arc; i++) {
        let li = parts[i];
        let distanceFactor = DistanceBetween(mouse, parts[i]);
        distanceFactor = Math.max(Math.min(20 - (distanceFactor / 5), 5), 1);
        ctx.beginPath();
        ctx.arc(li.x, li.y, li.size * distanceFactor, 0, Math.PI * 2, false);
        ctx.fillStyle = li.c;
        ctx.strokeStyle = li.c;
        if (i % 2 == 0)
            ctx.stroke();
        else
            ctx.fill();

        li.x = li.x + li.toX * (time * 0.05);
        li.y = li.y + li.toY * (time * 0.05);

        if (li.x > w) {
            li.x = 0;
        }
        if (li.y > h) {
            li.y = 0;
        }
        if (li.x < 0) {
            li.x = w;
        }
        if (li.y < 0) {
            li.y = h;
        }
    }
    if (time < speed) {
        time++;
    }
    setTimeout(particles, 1000 / rate);
}

// Mouse move event to track cursor position
function MouseMove(e) {
    mouse.x = e.layerX;
    mouse.y = e.layerY;
}

// Calculate distance between mouse and particle
function DistanceBetween(p1, p2) {
    let dx = p2.x - p1.x;
    let dy = p2.y - p1.y;
    return Math.sqrt(dx * dx + dy * dy);
}

// Call resizeCanvas on window resize
window.addEventListener('resize', function() {
    resizeCanvas();
    create();  // Recreate particles to adjust their positions
});

// Initial setup
resizeCanvas();
create();
particles();
