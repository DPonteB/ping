function startPing() {
    const ip1 = document.getElementById('ip1').value;
    const ip2 = document.getElementById('ip2').value;

    if (ip1 && ip2) {
        fetch('/start_ping', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `ip1=${ip1}&ip2=${ip2}`
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('ip1-label').innerText = data.ip1;
                document.getElementById('ip2-label').innerText = data.ip2;
                setInterval(fetchStats, 1000); // Atualiza a cada segundo
            })
            .catch(error => console.error('Erro ao iniciar o ping:', error));
    }
}

function fetchStats() {
    fetch('/get_stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total1').innerText = data[document.getElementById('ip1').value].total;
            document.getElementById('perdidos1').innerText = data[document.getElementById('ip1').value].perdidos;
            document.getElementById('taxa1').innerText = data[document.getElementById('ip1').value].taxa_perda.toFixed(2) + '%';

            document.getElementById('total2').innerText = data[document.getElementById('ip2').value].total;
            document.getElementById('perdidos2').innerText = data[document.getElementById('ip2').value].perdidos;
            document.getElementById('taxa2').innerText = data[document.getElementById('ip2').value].taxa_perda.toFixed(2) + '%';
        })
        .catch(error => console.error('Erro ao obter estatísticas:', error));
}
