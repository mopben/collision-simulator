const socket = new WebSocket("ws://localhost:8765");
const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
const collisionSound = new Audio("audio/collision.mp3");

const soundPool = [];
const POOL_SIZE = 500;
for (let i = 0; i < POOL_SIZE; i ++) {
  soundPool.push(collisionSound);
}

let current = 0;
function playCollisionSound() {
    const sound = soundPool[current];
    sound.currentTime = 0;
    sound.play();
    current = (current + 1) % POOL_SIZE;
}


function drawBlocks(blocks) {

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (const b of blocks) {
    console.log("Drawing")
    ctx.fillStyle = b.color;
    ctx.fillRect(b.x, b.y, b.x2 - b.x, b.y2 - b.y); 
  }
}

console.log("js started");
socket.onmessage = function(event) {
  const state = JSON.parse(event.data);
  drawBlocks(state.blocks);
  
  if (state.collisionOccured) {
      playCollisionSound();
      
      const counterElement = document.getElementById("collision-counter");
      counterElement.textContent = "Collision counter: " + state.totalCollisions;

  }
};
