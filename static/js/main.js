document.addEventListener('DOMContentLoaded', function() {
    const setupForm = document.getElementById('setupForm');
    const searchSection = document.getElementById('searchSection');
    const statsSection = document.getElementById('statsSection');
    const resultsSection = document.getElementById('resultsSection');
    const searchHashBtn = document.getElementById('searchHash');
    const searchTableBtn = document.getElementById('searchTable');
    const searchKeyInput = document.getElementById('searchKey');

    // Setup do sistema
    setupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const keys_pages = document.getElementById('keys_pages').value;
        const keys_buckets = document.getElementById('keys_buckets').value;

        try {
            const response = await fetch('/setup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    keys_pages: parseInt(keys_pages),
                    keys_buckets: parseInt(keys_buckets)
                })
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                document.getElementById('collisions').textContent = data.collisions;
                document.getElementById('overflow').textContent = data.overflow;
                
                // Mostrar primeira e última página
                document.getElementById('firstPage').innerHTML = data.first_page.join('<br>');
                document.getElementById('lastPage').innerHTML = data.last_page.join('<br>');
                
                // Mostrar seções
                statsSection.style.display = 'block';
                searchSection.style.display = 'block';
                resultsSection.style.display = 'block';
                
                alert('Sistema inicializado com sucesso!');
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao inicializar o sistema');
        }
    });

    // Busca por hash
    searchHashBtn.addEventListener('click', async function() {
        const key = searchKeyInput.value;
        if (!key) {
            alert('Por favor, insira uma chave de busca');
            return;
        }

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ key })
            });

            const data = await response.json();
            
            document.getElementById('hashPage').textContent = data.hash_result !== null ? data.hash_result : 'Não encontrado';
            document.getElementById('hashTime').textContent = data.hash_time + ' segundos';
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao realizar busca por hash');
        }
    });

    // Table scan
    searchTableBtn.addEventListener('click', async function() {
        const key = searchKeyInput.value;
        if (!key) {
            alert('Por favor, insira uma chave de busca');
            return;
        }

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ key })
            });

            const data = await response.json();
            
            document.getElementById('tablePage').textContent = data.table_result !== null ? data.table_result : 'Não encontrado';
            document.getElementById('tableTime').textContent = data.table_time + ' segundos';
            document.getElementById('pagesRead').textContent = data.pages_read;
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao realizar table scan');
        }
    });
}); 