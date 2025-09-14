const socket = new WebSocket("ws://localhost:8765");

const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");


console.log("js started");
socket.onmessage = function(event) {
  const state = JSON.parse(event.data);
  console.log("json state reached.");
  drawBlocks(state.blocks); // your canvas rendering function
};

function drawBlocks(blocks) {
  // clear the canvas each frame
  
  //ctx.clearRect(0, 0, canvas.width, canvas.height);

  // draw each block
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (const b of blocks) {
    console.log("Drawing")
    ctx.fillStyle = "blue"; // block color
    ctx.fillRect(b.x, b.y, 50, 50); // (x, y, width, height)
  }
}