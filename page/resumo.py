import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards



def make_donut(value, label, color, size=150):
    fig = px.pie(
        values=[value, 100 - value], 
        names=["Produção", "Outros"],
        hole=0.6, 
        color_discrete_sequence=[color, "#EAEAEA"]
    )
    fig.update_traces(
        textinfo='none', 
        hoverinfo='label+percent'
    )
    fig.update_layout(
        width=size, height=size,  # Tamanho do gráfico ajustado
        margin=dict(l=0, r=0, t=0, b=0), 
        showlegend=False,
        annotations=[dict(
            text=f"{value}%", 
            x=0.5, y=0.5, 
            font_size=20, 
            showarrow=False
        )]
    )
    return fig

def calcular_produtividade_percentual(df, estado, ano_selecionado):
    # Filtra os dados para o estado e ano selecionados
    df_selecionado = df[(df['Estado'] == estado) & (df['Ano'] == ano_selecionado)]
    
    # Calcula a produtividade média no ano selecionado
    produtividade_ano = df_selecionado['Produtividade'].mean()
    
    # Calcula a produtividade média global (de todos os anos)
    produtividade_media_global = df['Produtividade'].mean()
    
    # Calcula o percentual de produtividade
    produtividade_percentual = round((produtividade_ano / produtividade_media_global) * 100, 2)

    # Garante que o resultado não ultrapasse 100%
    if produtividade_percentual > 100:
        produtividade_percentual = 100
    
    return produtividade_percentual


def show():

    @st.cache_data
    def load_data():
        data = pd.read_excel("data/Dados_Conab.xlsx")
        return data

    df = load_data()

    st.subheader("📋Resumo Estatístico", divider='green')

    # Aplicar o estilo CSS para diminuir o tamanho da fonte
    st.markdown("""
    <style>
        .stMetric > div {
            font-size: 18px;  /* Ajuste o tamanho da fonte conforme necessário */
        }
    </style>
    """, unsafe_allow_html=True)  

    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 4.5, 2])
   
        with col1:
            with st.container(border=True):
                col0, col1 = st.columns(2)
                with col0:
                    estado = st.radio("Selecione o estado:", df['Estado'].unique(), index=1, horizontal=True)
                with col1:    
                    ano_selecionado = st.slider("Selecione o ano:", 2001, 2024, step=1)

            if estado in df['Estado'].unique() and ano_selecionado in df['Ano'].unique():
                df_selecionado = df[(df['Estado'] == estado) & (df['Ano'] == ano_selecionado)]
                producao_total = df_selecionado['Producao'].sum()
                produtividade = df_selecionado['Produtividade'].mean()
                area_producao = df_selecionado['Area em Producao'].sum()
                media_producao = (df_selecionado['Producao'].sum())/24
                media_area = (df_selecionado['Area em Producao'].sum())/24
                
            # Usando a função para calcular o percentual de produtividade
            produtividade_percent = calcular_produtividade_percentual(df, estado, ano_selecionado)
            
            # Usando o contêiner para agrupar as métricas
    
            st.write(f"Resumo dos dados para {estado} no ano de {ano_selecionado}")
            # Exibir métricas
            col0, col1 = st.columns(2)
            with col0:
                st.metric("Ano de Produção", f"{ano_selecionado}")
                st.metric("Produção Total", f"{producao_total:.0f} mil sacas") 
            with col1:    
                st.metric("Produtividade Média", f"{produtividade:.2f} sacas/ha") 
                st.metric("Área de Produção", f"{area_producao:.0f} ha") 
        
                                   
            col0, col1= st.columns(2)
            with col0:
                st.metric("Média da Produção", f"{media_producao:.2f} mil sacas")
                
            with col1:    
                 
                st.metric("Área média de Produção", f"{media_area:.2f} ha") 
                                
        style_metric_cards(background_color="##D2691E", border_left_color="#8B4513", border_color="#F4A460", box_shadow="#F71938")
                       
        with col2:    
             
            st.markdown("<h4 style='text-align: center;'>Produção por Métrica</h4>", unsafe_allow_html=True)
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")

            # Exemplo de Cálculo de Percentuais
            producao_percent = round((producao_total / df['Producao'].sum()) * 100, 2)
            area_percent = round((area_producao / df['Area em Producao'].sum()) * 100, 2)
           
            # Gráficos Donut Centralizados
            donut_col = st.columns(3)

            #Estilo CSS para centralizar e definir o tamanho dos títulos
            st.markdown("""
            <style>
            .centered-title {
                text-align: center;
                font-size: 16px;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)

            # Gráficos Donut com Títulos Centralizados
            with donut_col[0]:
                st.plotly_chart(make_donut(producao_percent, "Produção Total", "green"), use_container_width=True)
                st.markdown("<div class='centered-title'>Produção Total</div>", unsafe_allow_html=True)

            with donut_col[1]:    
                st.plotly_chart(make_donut(area_percent, "Área de Produção", "blue"), use_container_width=True)
                st.markdown("<div class='centered-title'>Área de Produção</div>", unsafe_allow_html=True)

            with donut_col[2]:
                st.plotly_chart(make_donut(produtividade_percent, "Produtividade", "orange"), use_container_width=True)
                st.markdown("<div class='centered-title'>Produtividade Média</div>", unsafe_allow_html=True)
            
            st.divider()
            # Adicionando a informação sobre os percentuais no gráfico Donut
            st.success(f"""
                - **Produção Total**: {producao_percent}% da produção total do estado.
                - **Área de Produção**: {area_percent}% da área de produção total.
                - **Produtividade Média**: {produtividade_percent}% da produtividade média do estado em comparação com todos os anos.
            """)
        
        # Função para aplicar o estilo
        def estilo_personalizado(df):
            return df.style.background_gradient(
                subset=['Producao'], cmap='Greens'
            ).format(
                {'Producao': '{:,.2f}', 'Produtividade': '{:,.2f}', 'Area em Producao': '{:,.2f}'}
            ).set_properties(
                **{'text-align': 'center'}
            ).set_table_styles(
                [{'selector': 'th', 'props': [('text-align', 'center')]}]
            )

        with col3:
            st.markdown("###### Top 10 Anos de Maior Produção")

            # Filtrando os dados pelo estado selecionado
            df_estado = df[df['Estado'] == estado]

            # Filtrando e ordenando as maiores produções
            df_top10 = df_estado.nlargest(10, 'Producao').drop(columns=['Estado'])

                                
            # Configuração de exibição personalizada
            st.dataframe(
                df_top10,
                column_order=("Ano", "Producao"),
                hide_index=True,
                column_config={
                    "Ano": st.column_config.TextColumn("Ano"),
                    "Producao": st.column_config.ProgressColumn(
                        "Produção (mil sacas)", 
                        format="%.2f",
                        min_value=0,
                        max_value=max(df_top10["Producao"]),
                    )                         
                },
                use_container_width=True,
            )
         
            st.write("<p style='font-size:13px;'>Fonte: Conab</p>", unsafe_allow_html=True)   
    
    

                    

                

