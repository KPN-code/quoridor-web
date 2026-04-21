const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");

async function getState() {
    const res = await fetch("/state");
    return await res.json();
}

async function aiMove() {
    await fetch("/ai");
}

function draw(state) {
    ctx.clearRect(0,0,600,600);

    // pelaajat
    state.pos.forEach((p,i) => {
        ctx.fillStyle = i === 0 ? "blue" : "red";
        ctx.beginPath();
        ctx.arc(p[0]*60+30,p[1]*60+30,20,0,Math.PI*2);
        ctx.fill();
    });
}

canvas.onclick = async (e) => {
    const x = Math.floor(e.offsetX / 60);
    const y = Math.floor(e.offsetY / 60);

    await fetch("/move", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({c:x,r:y})
    });

    await aiMove();
    const state = await getState();
    draw(state);
};

async function loop() {
    const state = await getState();
    draw(state);
}

setInterval(loop, 500);