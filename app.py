"""RSI Methods Web Demo: Run and visualize 3 Recursive Self-Improvement methods."""
import json
import sys
import os
import time
import tracemalloc
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "method1_aide"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "method2_scientist"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "method3_dream_rsi"))

app = FastAPI(title="RSI Methods Demo")


def run_aide():
    from problems import ALL_PROBLEMS
    from aide import run_aide_loop
    results = []
    for problem in ALL_PROBLEMS:
        log = run_aide_loop(problem, verbose=False)
        if log:
            results.append({
                "problem": problem["name"],
                "description": problem["description"],
                "iterations": log,
                "speedup": round(log[0]["mean_s"] / log[-1]["mean_s"], 2) if log[-1]["mean_s"] > 0 else 999,
            })
    return results


def run_scientist():
    from datasets import DATASETS
    from scientist import run_scientist_loop
    results = []
    for ds in DATASETS:
        log = run_scientist_loop(ds, verbose=False)
        if log:
            results.append({
                "dataset": ds["name"],
                "description": ds["description"],
                "iterations": log,
                "best_accuracy": max(e.get("accuracy", 0) for e in log),
            })
    return results


def run_dream_rsi():
    from base_problem import PROBLEMS
    from dream_rsi import run_dream_loop
    results = []
    for prob in PROBLEMS:
        log = run_dream_loop(prob, verbose=False)
        if log:
            results.append({
                "problem": prob["name"],
                "description": prob["description"],
                "iterations": log,
                "best_score": max(e.get("score", 0) for e in log),
            })
    return results


@app.post("/api/run/{method}")
async def api_run(method: str):
    t0 = time.perf_counter()
    try:
        if method == "aide":
            data = run_aide()
        elif method == "scientist":
            data = run_scientist()
        elif method == "dream_rsi":
            data = run_dream_rsi()
        else:
            return {"error": f"Unknown method: {method}"}
    except Exception as e:
        return {"error": str(e)}
    elapsed = time.perf_counter() - t0
    return {"method": method, "elapsed_s": round(elapsed, 3), "results": data}


@app.get("/api/methods")
async def methods():
    return [
        {"id": "aide", "name": "AIDE", "description": "AI Development Environment: iterative code optimization through benchmarking and version selection", "paper": "WecoAI/aideml (2024)"},
        {"id": "scientist", "name": "AI Scientist", "description": "Automated ML research: hypothesis generation, experiment design, model selection", "paper": "SakanaAI/AI-Scientist (2024)"},
        {"id": "dream_rsi", "name": "Dream-RSI", "description": "Dreaming-based recursive self-improvement: generate, evaluate, and evolve solution strategies", "paper": "Inspired by FunSearch/DeepMind (2024)"},
    ]


@app.get("/", response_class=HTMLResponse)
async def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RSI Methods Demo</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}
.container{max-width:1200px;margin:0 auto;padding:2rem}
h1{font-size:1.8rem;margin-bottom:.5rem;color:#60a5fa}
.subtitle{color:#94a3b8;margin-bottom:1.5rem;font-size:.9rem}
.badge{display:inline-block;padding:.25rem .75rem;background:#1e3a5f;color:#60a5fa;border-radius:1rem;font-size:.75rem;font-weight:600;margin-bottom:1rem}
.methods{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1rem;margin-bottom:1.5rem}
.method-card{background:#1e293b;border-radius:.75rem;padding:1.25rem;border:2px solid #334155;cursor:pointer;transition:all .2s}
.method-card:hover,.method-card.active{border-color:#3b82f6}
.method-card .name{font-size:1.1rem;font-weight:700;color:#60a5fa;margin-bottom:.3rem}
.method-card .desc{font-size:.8rem;color:#94a3b8;margin-bottom:.3rem}
.method-card .paper{font-size:.7rem;color:#64748b}
.run-btn{padding:.7rem 1.5rem;border:none;border-radius:.5rem;background:#3b82f6;color:white;font-weight:600;cursor:pointer;font-size:1rem;margin-bottom:1.5rem}
.run-btn:disabled{opacity:.5;cursor:not-allowed}
.run-btn.running{background:#f59e0b}
.elapsed{font-size:.8rem;color:#94a3b8;margin-left:1rem}
.results{display:none}
.result-panel{background:#1e293b;border-radius:.75rem;padding:1.5rem;margin-bottom:1.5rem}
.result-title{font-size:1.1rem;font-weight:600;color:#e2e8f0;margin-bottom:.3rem}
.result-desc{font-size:.8rem;color:#94a3b8;margin-bottom:1rem}
.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.75rem;margin-bottom:1rem}
.stat{background:#0f172a;padding:.75rem;border-radius:.5rem;text-align:center}
.stat-val{font-size:1.3rem;font-weight:700;color:#22c55e}
.stat-lbl{font-size:.7rem;color:#94a3b8;margin-top:.2rem}
.chart-wrap{margin-bottom:1rem}
table{width:100%;border-collapse:collapse;margin-top:.5rem}
th{text-align:left;padding:.4rem .6rem;border-bottom:1px solid #334155;color:#94a3b8;font-size:.75rem}
td{padding:.4rem .6rem;border-bottom:1px solid #0f172a;font-size:.8rem}
.correct{color:#22c55e}
.incorrect{color:#ef4444}
.spinner{display:inline-block;width:1rem;height:1rem;border:2px solid #334155;border-top-color:#3b82f6;border-radius:50%;animation:spin .6s linear infinite;margin-right:.5rem}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="container">
<span class="badge">RSI METHODS</span>
<h1>Recursive Self-Improvement Demo</h1>
<p class="subtitle">Three state-of-the-art RSI methods demonstrated on optimization problems. Select a method and run.</p>
<div class="methods" id="methods"></div>
<button class="run-btn" id="runBtn" onclick="run()">Run Selected Method</button>
<span class="elapsed" id="elapsed"></span>
<div class="results" id="results"></div>
</div>
<script>
let charts=[];
let selectedMethod='aide';

async function init(){
  const methods=await(await fetch('/api/methods')).json();
  document.getElementById('methods').innerHTML=methods.map(m=>
    `<div class="method-card${m.id===selectedMethod?' active':''}" id="mc_${m.id}" onclick="selectMethod('${m.id}')">
      <div class="name">${m.name}</div>
      <div class="desc">${m.description}</div>
      <div class="paper">${m.paper}</div>
    </div>`
  ).join('');
}

function selectMethod(id){
  selectedMethod=id;
  document.querySelectorAll('.method-card').forEach(c=>c.classList.remove('active'));
  document.getElementById('mc_'+id).classList.add('active');
}

async function run(){
  const btn=document.getElementById('runBtn');
  btn.disabled=true;btn.className='run-btn running';
  btn.innerHTML='<span class="spinner"></span>Running...';
  document.getElementById('elapsed').textContent='';
  charts.forEach(c=>c.destroy());charts=[];

  const res=await(await fetch('/api/run/'+selectedMethod,{method:'POST'})).json();
  btn.disabled=false;btn.className='run-btn';btn.textContent='Run Selected Method';

  if(res.error){
    document.getElementById('results').style.display='block';
    document.getElementById('results').innerHTML=`<div class="result-panel" style="color:#ef4444">${res.error}</div>`;
    return;
  }

  document.getElementById('elapsed').textContent=`Completed in ${res.elapsed_s}s`;
  renderResults(res);
}

function renderResults(res){
  const area=document.getElementById('results');
  area.style.display='block';
  area.innerHTML='';

  res.results.forEach((r,ri)=>{
    const panel=document.createElement('div');panel.className='result-panel';
    const name=r.problem||r.dataset;
    const desc=r.description||'';
    const iters=r.iterations||[];

    let statsHtml='';
    if(r.speedup){
      statsHtml=`<div class="stats-row">
        <div class="stat"><div class="stat-val">${r.speedup}x</div><div class="stat-lbl">Total Speedup</div></div>
        <div class="stat"><div class="stat-val">${iters.length}</div><div class="stat-lbl">Iterations</div></div>
        <div class="stat"><div class="stat-val">${(iters[0]?.mean_s*1000||0).toFixed(1)}ms</div><div class="stat-lbl">Start Time</div></div>
        <div class="stat"><div class="stat-val">${(iters[iters.length-1]?.mean_s*1000||0).toFixed(1)}ms</div><div class="stat-lbl">End Time</div></div>
      </div>`;
    }else if(r.best_accuracy!==undefined){
      statsHtml=`<div class="stats-row">
        <div class="stat"><div class="stat-val">${(r.best_accuracy*100).toFixed(1)}%</div><div class="stat-lbl">Best Accuracy</div></div>
        <div class="stat"><div class="stat-val">${iters.length}</div><div class="stat-lbl">Iterations</div></div>
      </div>`;
    }else if(r.best_score!==undefined){
      statsHtml=`<div class="stats-row">
        <div class="stat"><div class="stat-val">${r.best_score.toFixed?r.best_score.toFixed(2):r.best_score}</div><div class="stat-lbl">Best Score</div></div>
        <div class="stat"><div class="stat-val">${iters.length}</div><div class="stat-lbl">Iterations</div></div>
      </div>`;
    }

    const chartId='chart_'+ri;
    let tableHtml='';
    if(iters.length&&iters[0].mean_s!==undefined){
      tableHtml=`<table><thead><tr><th>#</th><th>Label</th><th>Mean (ms)</th><th>Memory (KB)</th><th>Correct</th><th>Change</th></tr></thead><tbody>${iters.map(e=>`<tr><td>${e.iteration}</td><td>${e.label}</td><td>${(e.mean_s*1000).toFixed(3)}</td><td>${e.peak_mem_kb?.toFixed(1)||'-'}</td><td class="${e.correct?'correct':'incorrect'}">${e.correct?'Yes':'No'}</td><td>${e.delta||'-'}</td></tr>`).join('')}</tbody></table>`;
    }else if(iters.length){
      const keys=Object.keys(iters[0]).filter(k=>k!=='__class__');
      tableHtml=`<table><thead><tr>${keys.map(k=>`<th>${k}</th>`).join('')}</tr></thead><tbody>${iters.map(e=>`<tr>${keys.map(k=>`<td>${typeof e[k]==='number'?(e[k]<1?e[k].toFixed(4):e[k].toFixed(2)):e[k]||'-'}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
    }

    panel.innerHTML=`<div class="result-title">${name}</div><div class="result-desc">${desc}</div>${statsHtml}<div class="chart-wrap"><canvas id="${chartId}"></canvas></div>${tableHtml}`;
    area.appendChild(panel);

    // draw chart
    const canvas=document.getElementById(chartId);
    if(iters.length&&iters[0].mean_s!==undefined){
      const ch=new Chart(canvas,{type:'line',data:{
        labels:iters.map(e=>e.label||'Iter '+e.iteration),
        datasets:[{label:'Time (ms)',data:iters.map(e=>e.mean_s*1000),borderColor:'#3b82f6',backgroundColor:'#3b82f622',fill:true,tension:.3}]
      },options:{responsive:true,plugins:{legend:{labels:{color:'#94a3b8'}}},scales:{x:{ticks:{color:'#64748b'},grid:{color:'#1e293b'}},y:{ticks:{color:'#64748b'},grid:{color:'#334155'}}}}});
      charts.push(ch);
    }else if(iters.length&&(iters[0].accuracy!==undefined||iters[0].score!==undefined)){
      const metric=iters[0].accuracy!==undefined?'accuracy':'score';
      const ch=new Chart(canvas,{type:'line',data:{
        labels:iters.map((_,i)=>'Iter '+i),
        datasets:[{label:metric,data:iters.map(e=>e[metric]),borderColor:'#22c55e',backgroundColor:'#22c55e22',fill:true,tension:.3}]
      },options:{responsive:true,plugins:{legend:{labels:{color:'#94a3b8'}}},scales:{x:{ticks:{color:'#64748b'},grid:{color:'#1e293b'}},y:{ticks:{color:'#64748b'},grid:{color:'#334155'}}}}});
      charts.push(ch);
    }
  });
}

init();
</script>
</body>
</html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9010)
