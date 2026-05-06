async function update(){
  let res = await fetch('/data');
  let data = await res.json();

  data.sort((a,b)=>a.total-b.total);

  document.getElementById("count").innerText =
    "Runners: " + data.length;

  let body = document.getElementById("board");
  body.innerHTML = "";

  data.forEach((r,i)=>{
    body.innerHTML += `
      <tr>
        <td>${i+1}</td>
        <td>${r.name}</td>
        <td>${r.laps}</td>
        <td>${r.total}</td>
      </tr>
    `;
  });
}

function startRace(){
  fetch('/start');
}

function resetRace(){
  fetch('/reset');
}

setInterval(update, 1000);
update();