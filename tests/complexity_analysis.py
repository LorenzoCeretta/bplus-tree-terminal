import time
import matplotlib.pyplot as plt
import numpy as np
from bplus_tree import BPlusTree
import math

class BPlusTreeComplexityAnalysis:
    """
    Classe para analisar e visualizar a complexidade de tempo das operações da árvore B+.
    """
    
    def __init__(self):
        self.results = {}
        
    def measure_operation_time(self, operation_func, data_sizes, tree_order=4):
        """
        Medir o tempo de execução para diferentes tamanhos de dados.
        """
        times = []
        
        for size in data_sizes:
            tree = BPlusTree(tree_order)
            
            if operation_func.__name__ == 'test_search':
                # Inserir dados primeiro para operações de busca
                for i in range(size):
                    tree.insert(i, f"value_{i}")
            
            # Medir tempo de operação
            start_time = time.time()
            operation_func(tree, size)
            end_time = time.time()
            
            times.append(end_time - start_time)
            
        return times
    
    def test_insert(self, tree, size):
        """Testar operação de inserção"""
        for i in range(size):
            tree.insert(i, f"value_{i}")
    
    def test_search(self, tree, size):
        """Testar operação de busca"""
        for i in range(size):
            tree.search_value(i)
    
    def test_search_missing(self, tree, size):
        """Testar busca por chaves inexistentes"""
        for i in range(size):
            tree.search_value(size + i)  # Buscar por chaves que não existem
    
    def test_range_query(self, tree, size):
        """Testar operação de consulta de intervalo"""
        # Inserir dados primeiro
        for i in range(size):
            tree.insert(i, f"value_{i}")
        
        # Realizar consultas de intervalo
        for i in range(0, size, max(1, size // 10)):
            end = min(i + size // 10, size)
            tree.range_query(i, end)
    
    def test_delete(self, tree, size):
        """Testar operação de exclusão"""
        # Inserir dados primeiro
        for i in range(size):
            tree.insert(i, f"value_{i}")
        
        # Excluir metade das chaves
        for i in range(0, size, 2):
            tree.delete(i)
    
    def analyze_complexities(self):
        """
        Analisar e plotar a complexidade de tempo de todas as operações da árvore B+.
        """
        # Tamanhos de dados a serem testados (escala logarítmica para melhor visualização)
        data_sizes = [10, 50, 100, 500, 1000, 2000, 5000]
        
        # Definir operações a serem testadas
        operations = {
            'Insert': self.test_insert,
            'Search (existing)': self.test_search,
            'Search (missing)': self.test_search_missing,
            'Range Query': self.test_range_query,
            'Delete': self.test_delete
        }
        
        # Medir tempos para cada operação
        for op_name, op_func in operations.items():
            times = self.measure_operation_time(op_func, data_sizes)
            self.results[op_name] = {'sizes': data_sizes, 'times': times}
        
        # Criar o gráfico de análise de complexidade
        self.plot_complexity_analysis()
        
        # Criar comparação teórica vs. real
        self.plot_theoretical_vs_actual()
    
    def plot_complexity_analysis(self):
        """
        Plotar a análise de complexidade de tempo para todas as operações.
        """
        plt.figure(figsize=(15, 10))
        
        # Criar subplots para diferentes operações
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        # Esquema de cores para operações
        colors = ['blue', 'green', 'red', 'orange', 'purple']
        
        for i, (op_name, data) in enumerate(self.results.items()):
            ax = axes[i]
            
            # Plotar medições reais
            ax.plot(data['sizes'], data['times'], 'o-', color=colors[i], 
            label=f'{op_name} (Actual)', linewidth=2, markersize=6)
            
            # Adicionar curvas de complexidade teórica
            sizes = np.array(data['sizes'])
            
            if op_name == 'Insert':
                # O(log n) para inserção
                theoretical = np.log(sizes) * (data['times'][-1] / np.log(sizes[-1]))
                ax.plot(sizes, theoretical, '--', color='gray', 
                label='O(log n)', alpha=0.7)
                
            elif op_name in ['Search (existing)', 'Search (missing)']:
                # O(log n) para busca
                theoretical = np.log(sizes) * (data['times'][-1] / np.log(sizes[-1]))
                ax.plot(sizes, theoretical, '--', color='gray', 
                label='O(log n)', alpha=0.7)
                
            elif op_name == 'Range Query':
                # O(log n + k) onde k é o tamanho do intervalo
                # Para este teste, k é proporcional a n, então O(n)
                theoretical = sizes * (data['times'][-1] / sizes[-1])
                ax.plot(sizes, theoretical, '--', color='gray', 
                label='O(n)', alpha=0.7)
                
            elif op_name == 'Delete':
                # O(log n) para exclusão
                theoretical = np.log(sizes) * (data['times'][-1] / np.log(sizes[-1]))
                ax.plot(sizes, theoretical, '--', color='gray', 
                label='O(log n)', alpha=0.7)
            
            ax.set_xlabel('Tamanho de Dados (n)')
            ax.set_ylabel('Tempo (segundos)')
            ax.set_title(f'{op_name} - Complexidade de Tempo')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xscale('log')
            ax.set_yscale('log')
        
        # Remover o último subplot não utilizado
        axes[-1].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('bplus_tree_complexity_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_theoretical_vs_actual(self):
        """
        Criar uma comparação abrangente de complexidades teóricas vs. reais.
        """
        plt.figure(figsize=(16, 12))
        
        # Definir complexidades teóricas
        theoretical_complexities = {
            'Insert': 'O(log n)',
            'Search (existing)': 'O(log n)',
            'Search (missing)': 'O(log n)',
            'Range Query': 'O(log n + k)',
            'Delete': 'O(log n)'
        }
        
        # Criar uma tabela de resumo
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # Plot 1: Todas as operações no mesmo gráfico
        colors = ['blue', 'green', 'red', 'orange', 'purple']
        
        for i, (op_name, data) in enumerate(self.results.items()):
            ax1.plot(data['sizes'], data['times'], 'o-', color=colors[i], 
                    label=f'{op_name} ({theoretical_complexities[op_name]})', 
                    linewidth=2, markersize=6)
        
        ax1.set_xlabel('Tamanho de Dados (n)')
        ax1.set_ylabel('Tempo (segundos)')
        ax1.set_title('Operações da Árvore B+ - Comparação de Complexidade de Tempo')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        
        # Plot 2: Tabela de resumo de complexidades
        table_data = []
        for op_name in self.results.keys():
            table_data.append([
                op_name,
                theoretical_complexities[op_name],
                'O(1)' if op_name == 'Busca (existente)' else 'O(log n)',
                'O(n)' if op_name == 'Consulta de intervalo' else 'O(log n)',
                'O(log n)' if op_name != 'Consulta de intervalo' else 'O(n)'
            ])
        
        # Criar tabela
        table = ax2.table(cellText=table_data,
        colLabels=['Operação', 'Caso Médio', 'Melhor Caso', 'Pior Caso', 'Espaço'],
        cellLoc='center',
        loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 2)
        
        # Estilizar a tabela
        for i in range(len(table_data) + 1):
            for j in range(5):
                if i == 0:  # Header row
                    table[(i, j)].set_facecolor('#4CAF50')
                    table[(i, j)].set_text_props(weight='bold', color='white')
                else:
                    table[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax2.set_title('Resumo de Complexidade da Árvore B+', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig('bplus_tree_complexity_summary.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def print_complexity_summary(self):
        """
        Imprimir um resumo detalhado de complexidades.
        """
        print("\n" + "="*80)
        print("RESUMO DA ANÁLISE DE COMPLEXIDADE DA ÁRVORE B+")
        print("="*80)
        
        print("\nCOMPLEXIDADES DAS OPERAÇÕES:")
        print("-" * 50)
        
        complexities = {
            'Insert': {
                'Caso médio': 'O(log n)',
                'Melhor Caso': 'O(1)',
                'Pior Caso': 'O(log n)',
                'Espaço': 'O(log n)',
                'Descrição': 'Inserção requer encontrar a folha correta e potencialmente dividir nós'
            },
            'Search': {
                'Caso médio': 'O(log n)',
                'Melhor Caso': 'O(1)',
                'Pior Caso': 'O(log n)',
                'Espaço': 'O(1)',
                'Descrição': 'Busca navega desde a raiz até a folha usando chaves de nós internos'
            },
            'Delete': {
                'Caso médio': 'O(log n)',
                'Melhor Caso': 'O(1)',
                'Pior Caso': 'O(log n)',
                'Espaço': 'O(log n)',
                'Descrição': 'Exclusão pode exigir emprestar de irmãos ou mesclar nós'
            },
            'Range Query': {
                'Caso médio': 'O(log n + k)',
                'Melhor Caso': 'O(log n)',
                'Pior Caso': 'O(n)',
                'Espaço': 'O(k)',
                'Descrição': 'Usa estrutura de folha duplamente ligada para travessia eficiente de intervalo'
            }
        }
        
        for op, details in complexities.items():
            print(f"\n{op.upper()}:")
            print(f"  Caso médio: {details['Caso médio']}")
            print(f"  Melhor Caso:    {details['Melhor Caso']}")
            print(f"  Pior Caso:   {details['Pior Caso']}")
            print(f"  Espaço:        {details['Espaço']}")
            print(f"  Descrição:  {details['Descrição']}")


def run_complexity_analysis():
    """
    Função principal para executar a análise de complexidade.
    """
    analyzer = BPlusTreeComplexityAnalysis()
    analyzer.analyze_complexities()
    analyzer.print_complexity_summary()


if __name__ == "__main__":
    run_complexity_analysis() 