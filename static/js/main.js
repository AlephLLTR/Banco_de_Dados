document.addEventListener('DOMContentLoaded', function() {
    const setupForm = document.getElementById('setupForm');
    const searchSection = document.getElementById('searchSection');
    const statsSection = document.getElementById('statsSection');
    const resultsSection = document.getElementById('resultsSection');
    const paginationSection = document.getElementById('paginationSection');
    const searchHashBtn = document.getElementById('searchHash');
    const searchTableBtn = document.getElementById('searchTable');
    const searchKeyInput = document.getElementById('searchKey');
    
    // Elementos de paginação
    const perPageSelect = document.getElementById('perPage');
    const currentPageInput = document.getElementById('currentPage');
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');
    const pagesContent = document.getElementById('pagesContent');
    
    let totalPages = 0;
    let currentPage = 1;

    // Função para carregar páginas
    async function loadPages(page = 1, perPage = 10) {
        try {
            const response = await fetch(`/pages?page=${page}&per_page=${perPage}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                totalPages = data.total_pages;
                currentPage = data.current_page;
                
                // Atualiza a interface
                currentPageInput.value = currentPage;
                pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
                
                // Atualiza os botões
                prevPageBtn.disabled = currentPage === 1;
                nextPageBtn.disabled = currentPage === totalPages;
                
                // Mostra o conteúdo das páginas
                pagesContent.innerHTML = data.pages.map(page => `
                    <div class="mb-3">
                        <h5>Página ${page.page_number}</h5>
                        <div class="border p-2 bg-light">
                            ${page.content.join('<br>')}
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Erro ao carregar páginas:', error);
            alert('Erro ao carregar páginas');
        }
    }

    // Event listeners para paginação
    perPageSelect.addEventListener('change', () => {
        loadPages(1, parseInt(perPageSelect.value));
    });

    currentPageInput.addEventListener('change', () => {
        const page = parseInt(currentPageInput.value);
        if (page >= 1 && page <= totalPages) {
            loadPages(page, parseInt(perPageSelect.value));
        }
    });

    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            loadPages(currentPage - 1, parseInt(perPageSelect.value));
        }
    });

    nextPageBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            loadPages(currentPage + 1, parseInt(perPageSelect.value));
        }
    });

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
                paginationSection.style.display = 'block';
                
                // Carregar primeira página
                loadPages(1, parseInt(perPageSelect.value));
                
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