const joystick = document.getElementById("joystick");
const thumb = document.getElementById("thumb");

let dragging = false;
const center = { x: 100, y: 100 }; // Center of base
const maxDistance = 80;
let currentDirection = null; // Last sent direction
let lastMoveTime = 0;
const throttleDelay = 100; // ms

// Send fetch request only if direction has changed
function sendDirection(direction) {
  if (direction !== currentDirection) {
    currentDirection = direction;
    fetch(`/${direction}`).catch(err => console.error("Request failed:", err));
  }
}

// Calculate direction based on angle and displacement
function getDirection(dx, dy) {
  const angle = Math.atan2(dy, dx);
  const distance = Math.sqrt(dx * dx + dy * dy);

  if (distance < 20) return "release";

  const deg = angle * (180 / Math.PI);

  if (deg >= -45 && deg <= 45) return "right";
  if (deg > 45 && deg < 135) return "backward";
  if (deg >= 135 || deg <= -135) return "left";
  if (deg < -45 && deg > -135) return "forward";

  return "release";
}

// Update thumb position and send direction
function updateThumb(x, y) {
  const dx = x - center.x;
  const dy = y - center.y;

  const distance = Math.min(Math.sqrt(dx * dx + dy * dy), maxDistance);
  const angle = Math.atan2(dy, dx);

  const newX = center.x + distance * Math.cos(angle);
  const newY = center.y + distance * Math.sin(angle);

  thumb.style.left = `${newX - 40}px`;
  thumb.style.top = `${newY - 40}px`;

  const direction = getDirection(dx, dy);
  sendDirection(direction);
}

// Reset thumb to center and release control
function resetThumb() {
  thumb.style.left = "60px";
  thumb.style.top = "60px";
  currentDirection = null;
  sendDirection("release");
}

// Mouse events
joystick.addEventListener("mousedown", (e) => {
  dragging = true;
  updateThumb(e.offsetX, e.offsetY);
});

document.addEventListener("mousemove", (e) => {
  if (dragging) {
    const now = Date.now();
    if (now - lastMoveTime > throttleDelay) {
      lastMoveTime = now;
      const rect = joystick.getBoundingClientRect();
      updateThumb(e.clientX - rect.left, e.clientY - rect.top);
    }
  }
});

document.addEventListener("mouseup", () => {
  if (dragging) {
    dragging = false;
    resetThumb();
  }
});

// Touch events
joystick.addEventListener("touchstart", (e) => {
  dragging = true;
  const touch = e.touches[0];
  const rect = joystick.getBoundingClientRect();
  updateThumb(touch.clientX - rect.left, touch.clientY - rect.top);
});

joystick.addEventListener("touchmove", (e) => {
  if (dragging) {
    const now = Date.now();
    if (now - lastMoveTime > throttleDelay) {
      lastMoveTime = now;
      const touch = e.touches[0];
      const rect = joystick.getBoundingClientRect();
      updateThumb(touch.clientX - rect.left, touch.clientY - rect.top);
    }
  }
});

joystick.addEventListener("touchend", () => {
  dragging = false;
  resetThumb();
});
