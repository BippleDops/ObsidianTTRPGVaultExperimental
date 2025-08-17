# Random Generators Frame

<iframe src="data:text/html;charset=utf-8,
<html>
<head>
<style>
body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
.generator { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
button { background: #007acc; color: white; border: none; padding: 8px 15px; border-radius: 3px; cursor: pointer; }
button:hover { background: #005a9d; }
#result { margin-top: 10px; padding: 10px; background: #e8f4f8; border-radius: 3px; }
</style>
</head>
<body>
<div class='generator'>
<h3>Random NPC Name Generator</h3>
<button onclick='generateName()'>Generate Name</button>
<div id='result'></div>
</div>

<script>
const firstNames = ['Aeliana', 'Gareth', 'Lyanna', 'Theron', 'Nerida', 'Corvus', 'Seraphina', 'Magnus'];
const lastNames = ['Stormwind', 'Brightblade', 'Deepwater', 'Goldleaf', 'Ironwood', 'Shadowmere'];

function generateName() {
  const first = firstNames[Math.floor(Math.random() * firstNames.length)];
  const last = lastNames[Math.floor(Math.random() * lastNames.length)];
  document.getElementById('result').innerHTML = first + ' ' + last;
}
</script>
</body>
</html>
" width="100%" height="200"></iframe>

## Usage
- Click the button to generate random NPC names
- Copy the result to create new NPCs
- Modify the name lists in the HTML if needed
