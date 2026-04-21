const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");

const CELL = 60;

// ── HOVER STATE ───────────────────────────────
let hoverWall = null;

// ── API ───────────────────────────────────────
async function getState() {
    const res = await fetch("/state");
    return await res.json();
}

async function aiMove() {
    await fetch("/ai");
}

// ── PIIRTO ────────────────────────────────────
function draw(state) {
    ctx.clearRect(0,0,600,600);

    // grid
    ctx.strokeStyle = "#444";
    for (let i=0;i<9;i++){
        for (let j=0;j<9;j++){
            ctx.strokeRect(i*CELL, j*CELL, CELL, CELL);
        }
    }

    // seinät
    ctx.fillStyle = "orange";
    for (let r=0;r<8;r++){
        for (let c=0;c<8;c++){
            if (state.h_walls[r][c]){
                ctx.fillRect(c*CELL, r*CELL+CELL-5, CELL*2, 10);
            }
            if (state.v_walls[r][c]){
                ctx.fillRect(c*CELL+CELL-5, r*CELL, 10, CELL*2);
            }
        }
    }

    // ── HOVER PREVIEW ─────────────────────────
    if (hoverWall) {
        ctx.globalAlpha = 0.5;
        ctx.fillStyle = "yellow";

        const {horiz, wc, wr} = hoverWall;

        if (horiz) {
            ctx.fillRect(wc*CELL, wr*CELL+CELL-5, CELL*2, 10);
        } else {
            ctx.fillRect(wc*CELL+CELL-5, wr*CELL, 10, CELL*2);
        }

        ctx.globalAlpha = 1.0;
    }

    // pelaajat
    state.pos.forEach((p,i) => {
        ctx.fillStyle = i === 0 ? "blue" : "red";
        ctx.beginPath();
        ctx.arc(p[0]*CELL+30, p[1]*CELL+30, 20, 0, Math.PI*2);
        ctx.fill();
    });
}

// ── MOUSE MOVE (HOVER) ───────────────────────
canvas.addEventListener("mousemove", (e) => {
    const x = e.offsetX;
    const y = e.offsetY;

    const cellX = Math.floor(x / CELL);
    const cellY = Math.floor(y / CELL);

    const offsetX = x % CELL;
    const offsetY = y % CELL;

    let horiz;
    if (offsetY > offsetX) {
        horiz = true;
    } else {
        horiz = false;
    }

    if (cellX >= 8 || cellY >= 8) {
        hoverWall = null;
        return;
    }

    hoverWall = {
        horiz: horiz,
        wc: cellX,
        wr: cellY
    };
});

// ── VASEN KLIKKAUS = LIIKE ───────────────────
canvas.addEventListener("click", async (e) => {
    const x = Math.floor(e.offsetX / CELL);
    const y = Math.floor(e.offsetY / CELL);

    const res = await fetch("/move", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            type:"move",
            c:x,
            r:y
        })
    });

    const data = await res.json();
    if (data.error){
        console.log("Virhe:", data.error);
        return;
    }

    await aiMove();
    draw(await getState());
});

// ── OIKEA KLIKKAUS = SEINÄ ───────────────────
canvas.addEventListener("contextmenu", async (e) => {
    e.preventDefault();

    const x = e.offsetX;
    const y = e.offsetY;

    const cellX = Math.floor(x / CELL);
    const cellY = Math.floor(y / CELL);

    const offsetX = x % CELL;
    const offsetY = y % CELL;

    let horiz;
    if (offsetY > offsetX) {
        horiz = true;
    } else {
        horiz = false;
    }

    const wc = cellX;
    const wr = cellY;

    if (wc >= 8 || wr >= 8) {
        console.log("Reuna – ei voi asettaa seinää");
        return;
    }

    const res = await fetch("/move", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            type:"wall",
            horiz: horiz,
            wc: wc,
            wr: wr
        })
    });

    const data = await res.json();
    if (data.error){
        console.log("Virhe:", data.error);
        return;
    }

    await aiMove();
    draw(await getState());
});

// ── LOOP ─────────────────────────────────────
async function loop() {
    draw(await getState());
}

setInterval(loop, 500);
