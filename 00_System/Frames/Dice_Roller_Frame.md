# Digital Dice Roller

<iframe src="data:text/html;charset=utf-8,
<html>
<head>
<style>
body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
.dice-section { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
button { background: #d20000; color: white; border: none; padding: 8px 15px; border-radius: 3px; cursor: pointer; margin: 2px; }
button:hover { background: #a10000; }
.result { font-size: 24px; font-weight: bold; color: #d20000; margin: 10px 0; }
</style>
</head>
<body>
<div class='dice-section'>
<h3>Quick Dice Rolls</h3>
<button onclick='roll(4)'>d4</button>
<button onclick='roll(6)'>d6</button>
<button onclick='roll(8)'>d8</button>
<button onclick='roll(10)'>d10</button>
<button onclick='roll(12)'>d12</button>
<button onclick='roll(20)'>d20</button>
<button onclick='roll(100)'>d100</button>
<div class='result' id='result'>Click a die to roll</div>
</div>

<script>
function roll(sides) {
  const result = Math.floor(Math.random() * sides) + 1;
  document.getElementById('result').innerHTML = 'd' + sides + ': ' + result;
}
</script>
</body>
</html>
" width="100%" height="150"></iframe>

## Usage
- Click any die button to roll
- Results appear immediately below
- Use for quick rolls during sessions
